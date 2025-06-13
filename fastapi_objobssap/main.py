"""This module contains the main FastAPI application."""


from fastapi import FastAPI

from fastapi_objobssap.middleware import UppercaseQueryParamsMiddleware
from fastapi_objobssap.router.objobssap_router import objobssap_router
from fastapi_objobssap.router.vosi import vosi_router
from fastapi_objobssap.exceptions import (
    general_exception_handler,
    http_exception_handler,
    validation_exception_handler,
)
from fastapi.exceptions import HTTPException
from fastapi.exceptions import RequestValidationError

app = FastAPI(
    title="ObjObsSAP API",
)

# Middleware
app.add_middleware(UppercaseQueryParamsMiddleware)

# Routers
app.include_router(objobssap_router, tags=["Example Docs"])
app.include_router(vosi_router, tags=["VOSI"])

# Exception Handlers
app.add_exception_handler(Exception, general_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)