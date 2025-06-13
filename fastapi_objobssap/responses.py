"""Response classes for FastAPI ObjObsSAP."""

from fastapi.responses import Response


class XMLResponse(Response):
    """VOTable response class"""

    media_type = "text/xml"
