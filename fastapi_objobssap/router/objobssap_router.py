"""This module contains the API endpoints for the ObjObsSAP application."""


from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Query
from fastapi_restful.cbv import cbv

from fastapi_objobssap import schemas
from fastapi_objobssap.config.database import get_db
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
                alias="MINOBS",
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
        db=Depends(get_db),
    ):
        """Perform an ObjObsSAP query."""

        position = schemas.PositionParameter(POS=pos)

        if time:
            time = schemas.TimeParameter(TIME=time)

        data = perform_objobssap_operation(
            pos=position,
            time=time,
            min_obs=min_obs,
            facility=facility,
            maxrec=maxrec,
            response_format=responseformat,
            db=db,
        )

        return data
