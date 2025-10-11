"""This module contains schemas the API handles for the ObjObsSAP module."""

from enum import StrEnum

from astropy.time import Time
from pydantic import BaseModel, Field, model_validator

OBJOBSSAP_METADATA = [
    {
        "column_name": "t_validity",
        "utype": "Char.TimeAxis.Coverage.Time",
        "ucd": None,
        "unit": "d",
        "datatype": "float",
    },
    {
        "column_name": "validity_accuracy",
        "datatype": "char",
        "arraysize": "*",
    },
    {"column_name": "validity_predictor", "datatype": "char", "arraysize": "*"},
    {
        "column_name": "t_start",
        "utype": "Char.TimeAxis.Coverage.Bounds.Limits.StartTime",
        "ucd": "time.start",
        "unit": "d",
        "datatype": "float",
    },
    {
        "column_name": "t_stop",
        "utype": "Char.TimeAxis.Coverage.Bounds.Limits.StopTime",
        "ucd": "time.end",
        "unit": "d",
        "datatype": "float",
    },
    {
        "column_name": "t_observability",
        "utype": "Char.TimeAxis.Coverage.Support.Extent",
        "ucd": "time.duration",
        "unit": "s",
        "datatype": "float",
    },
    {
        "column_name": "pos_angle",
        "utype": "Char.SpatialAxis.Coverage.Location.Coord.Position2D.Value2.C3",
        "unit": "deg",
        "datatype": "float",
    },
    {
        "column_name": "em_threshold",
        "utype": "Char.Spectral.Axis.Energy.Threshold",
        "ucd": "em.energy",
        "unit": "m",
    },
    {"column_name": "target_name", "utype": "Target.Name", "ucd": "meta.id;src"},
    {"column_name": "em_min", "utype": "Char.Spectral.Axis.Energy.Min", "ucd": "em.energy", "unit": "m"},
    {"column_name": "em_max", "utype": "Char.Spectral.Axis.Energy.Max", "ucd": "em.energy", "unit": "m"},
    {
        "column_name": "elevation_min",
        "utype": "Char.SpatialAxis.Coverage.Extent.angular_distance",
        "unit": "deg",
    },
    {
        "column_name": "elevation_max",
        "utype": "Char.SpatialAxis.Coverage.Extent.angular_distance",
        "unit": "deg",
    },
    {"column_name": "moon_sep_min", "unit": "deg"},
    {"column_name": "moon_sep_max", "unit": "deg"},
    {"column_name": "sun_sep_min", "unit": "deg"},
    {"column_name": "sun_sep_max", "unit": "deg"},
    {
        "column_name": "facility",
        "utype": "Char.SpatialAxis.Coverage.Provenance.ObsConfig.Facility.name",
        "ucd": "meta.id;instr.tel",
        "arraysize": "*",
        "datatype": "char",
    },
]


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

    start: float = Field(..., description="Start time in MJD")
    end: float = Field(..., description="End time in MJD")

    @model_validator(mode="before")
    @classmethod
    def validate_time(cls, values):
        """Validate the time format."""
        time = values.get("TIME")
        if time:
            try:
                # Handle both MJD/MJD and single MJD formats
                time_parts = time.split("/")
                if len(time_parts) == 2:
                    start, end = map(float, time_parts)
                elif len(time_parts) == 1:
                    end = float(time_parts[0])
                    start = Time.now().mjd
                else:
                    raise ValueError
                values["start"] = start
                values["end"] = end
            except ValueError:
                raise ValueError("Invalid TIME format. Use 'START/END' or single '/MJD' format.")
        return values


class ValidityAccuracy(StrEnum):
    """Allowed values for validity_accuracy."""

    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class ResponseFormat(StrEnum):
    """Supported response formats for the API."""

    VOTABLE = "votable"
