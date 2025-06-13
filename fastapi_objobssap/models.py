"""This module contains the database sqlalchemy models for the ObjObsSAP module."""

from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import DeclarativeBase

from fastapi_objobssap.config.database import engine


class Base(DeclarativeBase):
    """The base class for all models."""

    __abstract__ = True

    def to_dict(self, as_str=True) -> dict:
        """Convert the model to a dictionary."""
        inner_func = str if as_str else lambda x: x
        return {column.name: inner_func(getattr(self, column.name)) for column in self.__table__.columns}


class ObjObsSAPModel(Base):
    """The ObjObsSAP data model."""

    __tablename__ = "objobssap"

    id = Column(Integer, primary_key=True, index=True)
    t_validity = Column(Integer, nullable=False, comment="Date when the observability calculation will change (MJD)")
    t_start = Column(Integer, nullable=False, comment="Observability window start time (MJD)")
    t_stop = Column(Integer, nullable=False, comment="Observability window end time (MJD)")
    t_observability = Column(Float, nullable=False, comment="Observability duration window (s)")

    # Optional properties
    validity_accuracy = Column(String, comment="Level of confidence in the validity range (HIGH, MEDIUM, LOW)")
    validity_predictor = Column(String, comment="Identifier of the software used to calculate the observability")

    pos_angle = Column(Float, comment="Satellite position angle (degrees)")

    em_threshold = Column(
        Float, comment="Energy threshold for this particular sky position and observability window (m)"
    )

    target_name = Column(String, comment="Name of the target object")

    em_min = Column(Float, comment="Energy minimum for this particular sky position and observability window (m)")
    em_max = Column(Float, comment="Energy maximum for this particular sky position and observability window (m)")

    elevation_min = Column(
        Float, comment="Minimum elevation for this particular sky position and observability window (degrees)"
    )
    elevation_max = Column(
        Float, comment="Maximum elevation for this particular sky position and observability window (degrees)"
    )

    moon_sep_min = Column(
        Float, comment="Minimum Moon separation for this sky position and observability time interval (degrees)"
    )
    moon_sep_max = Column(
        Float, comment="Maximum Moon separation for this sky position and observability time interval (degrees)"
    )

    sun_sep_min = Column(
        Float, comment="Minimum Sun separation for this sky position and observability time interval (degrees)"
    )
    sun_sep_max = Column(
        Float, comment="Maximum Sun separation for this sky position and observability time interval (degrees)"
    )

    facility = Column(String, comment="Facility name")

    # Not described in the output schema, but used for example position matching via ObsCore data model
    s_ra = Column(Float, nullable=False, comment="Right Ascension of the target object (degrees)")
    s_dec = Column(Float, nullable=False, comment="Declination of the target object (degrees)")


class ObsMetadata(Base):
    """Basic metadata model for the ObjObsSAP columns.

    Just used to make creating the VOTable easier.
    """

    __tablename__ = "objobssap_metadata"
    id = Column(Integer, primary_key=True, index=True)

    column_name = Column(String, nullable=False, comment="Name of the column")
    utype = Column(String, comment="Utype of the column")
    ucd = Column(String, comment="UCD of the column")
    unit = Column(String, comment="Unit of the column (if applicable)")


Base.metadata.create_all(engine)
