"""This module contains schemas the API handles for the ObjObsSAP module."""

from enum import StrEnum

from pydantic import BaseModel, Field, model_validator


class PositionParameter(BaseModel):
    """Schema for a POS parameter."""

    ra: float = Field(..., description="Right Ascension in degrees")
    dec: float = Field(..., description="Declination in degrees")

    @model_validator(mode="before")
    @classmethod
    def validate_position(cls, values):
        """Validate the position format."""
        pos = values.get("POS")
        if pos:
            try:
                ra, dec = map(float, pos.split(","))
                values["ra"] = ra
                values["dec"] = dec
            except ValueError:
                raise ValueError("Invalid POS format. Use 'RA,DEC' format.")
        return values


class TimeParameter(BaseModel):
    """Schema for a TIME parameter.

    The minimum time is optional, and if not provided, defaults to the current day.
    """

    start: int = Field(..., description="Start time in MJD")
    end: int = Field(..., description="End time in MJD")

    @model_validator(mode="before")
    @classmethod
    def validate_time(cls, values):
        """Validate the time format."""
        time = values.get("TIME")
        if time:
            try:
                # Handle both MJD/MJD and single MJD formats
                if "/" in time:
                    start, end = map(int, time.split("/"))
                    values["start"] = start
                    values["end"] = end
                else:
                    # If only a single MJD is provided, it's treated as end time
                    end = int(time)
                    # Set start to the same as end for single MJD case
                    # Set start to current time in MJD
                    current_mjd = int(time.time() / 86400.0 + 40587)  # Convert Unix time to MJD
                    values["start"] = current_mjd
                    values["end"] = end
            except ValueError:
                raise ValueError("Invalid TIME format. Use 'START/END' or single MJD format.")
        return values


class ResponseFormat(StrEnum):
    """Supported response formats for the API."""

    VOTABLE = "votable"
