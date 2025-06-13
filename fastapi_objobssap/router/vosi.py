"""VOSI capabilities router for the ObjObsSAP service."""

from fastapi import APIRouter, Request, Response
from fastapi_restful.cbv import cbv

vosi_router = APIRouter()


@cbv(vosi_router)
class VOSIRouter:
    """Example router for the VOSI endpoints.

    Only /capabilities is required by the ObjObsSAP spec.
    """

    @vosi_router.get("/capabilities", summary="Get the VOSI capabilities.")
    def capabilities(self, request: Request):
        """Get the VOSI capabilities."""

        hostname = str(request.url).replace("capabilities", "")

        VOSI_RESPONSE = f"""
<vosi:capabilities
        xmlns:vosi="http://www.ivoa.net/xml/VOSICapabilities/v1.0"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:vs="http://www.ivoa.net/xml/VODataService/v1.1">
        <capability standardID="ivo://ivoa.net/std/VOSI#capabilities">
                <interface xsi:type="vs:ParamHTTP" version="1.0">
                        <accessURL use="full">
                                http://example.com/ObjObsSAP/capabilities
                                9
                        </accessURL>
                </interface>
        </capability>

        <capability standardID="ivo://ivoa.net/std/ObjObsSAP#query-1">
                <interface xsi:type="vs:ParamHTTP" role="std" version="1.0">
                        <accessURL>
                                {hostname}query
                        </accessURL>
                </interface>
        </capability>
</vosi:capabilities>
        """

        return Response(
            content=VOSI_RESPONSE,
            media_type="application/xml",
            headers={"Content-Type": "application/xml"},
        )
