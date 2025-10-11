"""This module contains the services i.e. the functions that interact with the db for the example module.

This module should be replaced with the implementation of the developed service.
"""

import io
from datetime import timedelta

import numpy as np
from astroplan import FixedTarget, Observer
from astropy import units as u
from astropy.coordinates import EarthLocation, SkyCoord
from astropy.io.votable import from_table, writeto
from astropy.io.votable.tree import Group, Info, Param, Resource, VOTableFile
from astropy.table import Table
from astropy.time import Time

from fastapi_objobssap.responses import XMLResponse
from fastapi_objobssap.schemas import OBJOBSSAP_METADATA, PositionParameter, TimeParameter, ValidityAccuracy


def handle_response_format(results, metadata, response_format, overflow):
    """Handle the response format based on the requested format."""

    # only 'votable' supported in this example implementation
    if response_format == "votable":
        table = Table(
            rows=results, names=[meta["column_name"] for meta in metadata if meta["column_name"] in results[0]]
        )
        votable: VOTableFile = from_table(table)

        if overflow:
            votable.resources[0].infos.append(Info(name="QUERY_STATUS", value="OVERFLOW"))

        for meta in metadata:
            for field in votable.get_first_table().fields:
                if field.name == meta["column_name"]:
                    field.utype = meta.get("utype")
                    field.ucd = meta.get("ucd")
                    field.unit = meta.get("unit")
                    field.datatype = meta.get("datatype")
                    field.arraysize = meta.get("arraysize")
                    break

        # DataLink service descriptor
        datalink_resource = Resource(name="this", type="meta", utype="adhoc:service")
        datalink_resource.params.append(
            Param(
                votable,
                name="standardID",
                value="ivo://ivoa.net/std/ObjObsSAP#query-0.3",
                datatype="char",
                arraysize="*",
            )
        )
        datalink_resource.params.append(
            Param(
                votable,
                name="accessURL",
                value="http://example.com/objobssap/query",
                datatype="char",
                arraysize="*",
            )
        )
        input_params = Group(datalink_resource, name="inputParams")
        input_params.entries.append(Param(votable, name="pos", datatype="char", arraysize="*"))
        input_params.entries.append(Param(votable, name="time", datatype="float", arraysize="*", unit="d"))
        input_params.entries.append(Param(votable, name="min_obs", datatype="float", arraysize="*", unit="s"))
        datalink_resource.groups.append(input_params)
        votable.resources.append(datalink_resource)

        buffer = io.BytesIO()
        writeto(votable, buffer)
        buffer.seek(0)

        return XMLResponse(content=buffer.read())


def get_observable_intervals(observer: Observer, target: FixedTarget, time_range: TimeParameter, maxrec: int):
    """Get observable intervals for a target given an observer and time range.

    Technically this will return intervals that are past the end of the time range if the target is up at the end of the range.
    """

    current_time = time_range.start

    obs_table = []
    overflow = False

    while current_time < time_range.end:
        if len(obs_table) >= maxrec:
            overflow = True
            break

        rise_time = observer.target_rise_time(Time(current_time, format="mjd"), target, which="next")
        set_time = observer.target_set_time(rise_time, target, which="next")

        # targets that are always up or down
        # TODO: replace this with TargetNeverUpWarning/TargetAlwaysUpWarning handling
        if np.ma.is_masked(rise_time.mjd) or np.ma.is_masked(set_time.mjd):
            alt = observer.altaz(Time(current_time, format="mjd"), target).alt.deg
            if alt > 0:
                obs_table.append((time_range.start, time_range.end))
            break

        if not np.isnan(rise_time.mjd) and not np.isnan(set_time.mjd):
            # if rise_time > set_time:
            #     # target is up at the start of the range
            #     obs_table.append((current_time.mjd, set_time.mjd))

            # # clip to the time range
            # start_clip = max(rise_time.mjd, time_range.start)
            # end_clip = min(set_time.mjd, time_range.end)

            # if start_clip < end_clip:
            #     obs_table.append((start_clip, end_clip))

            obs_table.append((rise_time.mjd, set_time.mjd))

            current_time = set_time + timedelta(minutes=1)
            current_time = current_time.mjd
        else:
            break

    return obs_table, overflow


def parse_results(results):
    """Parse the results into the final output format."""

    parsed_results = []
    for start, end in results:
        # result_dict = {col["column_name"]: None for col in OBJOBSSAP_METADATA}
        result_dict = {
            "t_validity": start + 10,  # say the observation is valid 10 days after it starts
            "validity_accuracy": ValidityAccuracy.HIGH,
            "validity_predictor": "Example Observatory",
            "t_start": start,
            "t_stop": end,
            "t_observability": (end - start) * 86400,  # in seconds
            "facility": "Example Observatory",
        }
        parsed_results.append(result_dict)
    return parsed_results


def perform_objobssap_operation(
    pos: PositionParameter,
    time: TimeParameter,
    min_obs: int,
    facility: str,
    maxrec: int,
    response_format: str,
):
    """Perform the ObjObsSAP search with the given parameters."""

    overflow = False
    results = []

    # Here we'll simulate our telescope as being in Baltimore, MD, USA
    LAT = 39.33286
    LON = -76.62338

    location = EarthLocation(lat=LAT, lon=LON, height=0)
    observer = Observer(location=location, name="Example Observatory", timezone="US/Eastern")

    # If the user has supplied anything other than "Example Observatory" for the facility,
    # it seems a little silly to continue, no?
    if facility and facility.lower() != "example observatory".lower():
        results = parse_results(results)
        return handle_response_format(results, OBJOBSSAP_METADATA, response_format, overflow)

    coords = SkyCoord(ra=pos.ra * u.deg, dec=pos.dec * u.deg)
    target = FixedTarget(coords)

    observable_times, overflow = get_observable_intervals(observer, target, time, maxrec)

    # check that the intervals are long enough
    if min_obs and min_obs > 0:
        observable_times = [
            (start, end) for start, end in observable_times if (end - start) * 86400 >= min_obs
        ]  # 86400 seconds in a day

    results = parse_results(observable_times)
    return handle_response_format(results, OBJOBSSAP_METADATA, response_format, overflow)
