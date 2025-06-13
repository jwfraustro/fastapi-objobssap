"""This module contains the API endpoints for the ObjObsSAP application."""


from typing import Annotated, Optional

from astropy.time import Time
from fastapi import APIRouter, Query
from fastapi_restful.cbv import cbv

from fastapi_objobssap import schemas
from fastapi_objobssap.services import perform_objobssap_operation

objobssap_router = APIRouter()


@cbv(objobssap_router)
class ObjObsSAPRouter:
    """Router for ObjObsSAP API endpoints."""

    @objobssap_router.get("/query", summary="Perform an ObjObsSAP query.")
    def objobssap_request(
        self,
        pos: Annotated[
            str,
            Query(
                ...,
                description="Position of object in ICRS RA and DEC coordinates",
                example="27,15.27",
                regex=r"([-+]?\d*\.?\d+),([-+]?\d*\.?\d+)",
                alias="POS",
            ),
        ],
        time: Annotated[
            Optional[str],
            Query(
                description="Time coverage of object visibility, in MJD format, in range-list form.",
                example="59522/59532",
                regex=r"(\d+)\/(\d+)",
                alias="TIME",
            ),
        ] = None,
        min_obs: Annotated[
            Optional[int],
            Query(
                description="Constraint on the minimum observability of the object in seconds.",
                example=600,
                ge=0,
                alias="MIN_OBS",
            ),
        ] = None,
        facility: Annotated[
            Optional[str],
            Query(
                description="Constrain observations to a specific facility/telescope.",
                example="HST",
                alias="FACILITY",
            ),
        ] = None,
        maxrec: Annotated[
            Optional[int],
            Query(
                description="Maximum number of records to return.",
                example=100,
                ge=0,
                alias="MAXREC",
            ),
        ] = 1000,
        responseformat: Annotated[
            Optional[schemas.ResponseFormat],
            Query(
                description="Format of the response, e.g., 'votable' or 'json'.",
                example="votable",
                alias="RESPONSEFORMAT",
            ),
        ] = "votable",
    ):
        """Perform an ObjObsSAP query."""

        position = schemas.PositionParameter(POS=pos)

        if time:
            time = schemas.TimeParameter(TIME=time)
        else:
            # If no time is provided, default to the current day, and a week after
            time = schemas.TimeParameter(start=Time.now().mjd, end=Time.now().mjd + 7)

        data = perform_objobssap_operation(
            pos=position,
            time=time,
            min_obs=min_obs,
            facility=facility,
            maxrec=maxrec,
            response_format=responseformat,
        )

        return data
