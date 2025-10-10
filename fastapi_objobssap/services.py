"""This module contains the services i.e. the functions that interact with the db for the example module.

This module should be replaced with the implementation of the developed service.
"""

import io

from astropy.io.votable import from_table, writeto
from astropy.io.votable.tree import Info, VOTableFile
from astropy.table import Table

from fastapi_objobssap.responses import XMLResponse
from fastapi_objobssap.schemas import PositionParameter, TimeParameter


def handle_response_format(results, metadata, response_format, overflow):
    """Handle the response format based on the requested format."""

    # only 'votable' supported in this example implementation
    if response_format == "votable":
        table = Table(results)
        votable: VOTableFile = from_table(table)

        if overflow:
            votable.infos.append(Info(name="QUERY_STATUS", value="OVERFLOW"))

        for meta in metadata:
            for field in votable.get_first_table().fields:
                if field.name == meta["column_name"]:
                    field.utype = meta.get("utype")
                    field.ucd = meta.get("ucd")
                    field.unit = meta.get("unit")
                    break

        buffer = io.BytesIO()
        writeto(votable, buffer)
        buffer.seek(0)

        return XMLResponse(content=buffer.read())


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

    # # Here we'll simulate our telescope as being in Baltimore, MD, USA
    # LAT = 39.33286
    # LON = -76.62338

    # location = EarthLocation(lat=LAT, lon=LON, height=0)
    # observer = Observer(location=location, name="Example Observatory", timezone="US/Eastern")

    # coords = SkyCoord(ra=pos.ra * u.deg, dec=pos.dec * u.deg)
    # target = FixedTarget(coords)

    # time_range = Time(time.start, time.end, format="mjd")

    # constraints = [AtNightConstraint.twilight_civil()]

    # obs_table = observability_table(constraints, observer, [target], times=time_range)

    # response = obs_table

    return response
