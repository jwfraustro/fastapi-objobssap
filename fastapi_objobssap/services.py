"""This module contains the services i.e. the functions that interact with the db for the example module.

This module should be replaced with the implementation of the developed service.
"""

import io

from astropy.io.votable import from_table, writeto
from astropy.io.votable.tree import Info, VOTableFile
from astropy.table import Table

from fastapi_objobssap.models import ObjObsSAPModel, ObsMetadata
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
    pos: PositionParameter, time: TimeParameter, min_obs: int, facility: str, maxrec: int, response_format: str, db
):
    """Perform the ObjObsSAP search with the given parameters."""

    overflow = False

    with db as session:
        query_obj = session.query(ObjObsSAPModel)

        # In real applications, POS filtering would most likely involve a more complex spatial query.
        if pos:
            query_obj = query_obj.filter(
                ObjObsSAPModel.s_ra.between(pos.ra - 0.5, pos.ra + 0.5)
                & ObjObsSAPModel.s_dec.between(pos.dec - 0.5, pos.dec + 0.5)
            )

        # The spec is somewhat ambiguous on how to handle the time range, so we take it here as to include the entire range.
        if time:
            query_obj = query_obj.filter(ObjObsSAPModel.t_start >= time.start, ObjObsSAPModel.t_stop <= time.end)

        if min_obs is not None:
            query_obj = query_obj.filter(ObjObsSAPModel.t_observability >= min_obs)

        if facility:
            query_obj = query_obj.filter(ObjObsSAPModel.facility == facility)

        results = query_obj.all()

        if len(results) > maxrec:
            results = results[:maxrec]
            overflow = True

        results = [result.to_dict(as_str=False) for result in results]

        metadata = session.query(ObsMetadata).all()
        metadata = [md.to_dict(as_str=False) for md in metadata]

    response = handle_response_format(results, metadata, response_format, overflow)

    return response
