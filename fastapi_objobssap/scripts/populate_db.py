"""An example initialization script for the FastAPI ObjObsSAP service."""

import random

from fastapi_objobssap.config.database import get_db
from fastapi_objobssap.models import ObjObsSAPModel, ObsMetadata


def init_metadata():
    """Initialize the metadata table with the ObjObsSAP columns."""

    with get_db() as session:
        metadata = [
            {"column_name": "t_validity", "utype": "Char.TimeAxis.Coverage.Time", "ucd": None, "unit": "d", },
            {"column_name": "validity_accuracy"},
            {"column_name": "validity_predictor"},
            {
                "column_name": "t_start",
                "utype": "Char.TimeAxis.Coverage.Bounds.Limits.StartTime",
                "ucd": "time.start",
                "unit": "d",
            },
            {
                "column_name": "t_stop",
                "utype": "Char.TimeAxis.Coverage.Bounds.Limits.StopTime",
                "ucd": "time.end",
                "unit": "d",
            },
            {
                "column_name": "t_observability",
                "utype": "Char.TimeAxis.Coverage.Support.Extent",
                "ucd": "time.duration",
                "unit": "s",
            },
            {
                "column_name": "pos_angle",
                "utype": "Char.SpatialAxis.Coverage.Location.Coord.Position2D.Value2.C3",
                "unit": "deg",
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
            },
        ]

        for col in metadata:
            # Check if the column already exists in the database
            existing_metadata = session.query(ObsMetadata).filter(ObsMetadata.column_name == col["column_name"]).first()
            if existing_metadata:
                print(f"Column {col['column_name']} already exists, skipping.")
                continue

            metadata_entry = ObsMetadata(
                column_name=col["column_name"], utype=col.get("utype"), ucd=col.get("ucd"), unit=col.get("unit")
            )

            session.add(metadata_entry)
        session.commit()


def init_fake_data():
    """Initialize the database some fake data."""

    fake_facilities = ["HST", "VLT", "JWST", "LSST", "ALMA"]
    fake_validity_accuracy = ["HIGH", "MEDIUM", "LOW"]

    random.seed(1138)

    for _ in range(1000):
        with get_db() as session:
            t_start = random.randint(59000, 60000)
            t_stop = t_start + random.randint(1, 10)

            t_observability = (t_stop - t_start) * 86400  # Convert days to seconds
            t_validity = t_stop + random.randint(30, 365)  # Validity period in days

            validity_accuracy = random.choice(fake_validity_accuracy)
            validity_predictor = "Predictor_" + str(random.randint(1, 10))

            s_ra = round(random.uniform(0, 360), 3)  # Random RA in degrees
            s_dec = round(random.uniform(-90, 90), 3)  # Random Dec in degrees

            pos_angle = round(random.uniform(0, 360), 3)  # Random angle in degrees
            em_threshold = round(random.uniform(0.1, 100.0), 3)
            target_name = "Target_" + str(random.randint(1, 100))
            em_min = round(random.uniform(0.1, 10.0), 3)
            em_max = round(em_min + random.uniform(0.1, 10.0), 3)

            elevation_min = round(random.uniform(0, 90), 3)  # Random elevation in degrees
            elevation_max = round(elevation_min + random.uniform(0, 90 - elevation_min), 3)
            moon_sep_min = round(random.uniform(0, 180), 3)
            moon_sep_max = round(moon_sep_min + random.uniform(0, 180 - moon_sep_min), 3)
            sun_sep_min = round(random.uniform(0, 180), 3)
            sun_sep_max = round(sun_sep_min + random.uniform(0, 180 - sun_sep_min), 3)

            facility = random.choice(fake_facilities)
            objobs_sap_entry = ObjObsSAPModel(
                t_validity=t_validity,
                t_start=t_start,
                t_stop=t_stop,
                t_observability=t_observability,
                validity_accuracy=validity_accuracy,
                validity_predictor=validity_predictor,
                pos_angle=pos_angle,
                em_threshold=em_threshold,
                target_name=target_name,
                em_min=em_min,
                em_max=em_max,
                elevation_min=elevation_min,
                elevation_max=elevation_max,
                moon_sep_min=moon_sep_min,
                moon_sep_max=moon_sep_max,
                sun_sep_min=sun_sep_min,
                sun_sep_max=sun_sep_max,
                s_ra=s_ra,
                s_dec=s_dec,
                facility=facility,
            )
            session.add(objobs_sap_entry)
            session.commit()


if __name__ == "__main__":
    init_metadata()
    print("Metadata table initialized with ObjObsSAP columns.")
    init_fake_data()
    print("Database populated with fake data.")
