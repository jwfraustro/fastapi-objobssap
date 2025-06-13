# FastAPI-ObjObsSAP

This project is a Python implementation of the proposed IVOA ObjObsSAP standard using [FastAPI](https://fastapi.tiangolo.com/).

## Getting Started

Running the project with docker-compose is the recommended way to get started quickly. It sets up a PostgreSQL database with simulated data and runs the FastAPI application. By default, the api will be available at `http://localhost:8000/query`.

Additionally, the VOSI Capabilities endpoint is available at `http://localhost:8000/capabilities`, which provides information about the available operations and their parameters.

Interactive Swagger documentation is available at `http://localhost:8000/docs`.

A script `/scripts/populate_db.py` is provided to populate the database with simulated data. This script can be run after starting the Docker container to fill the database with sample data.

### Requirements

- Python 3.11+
- [Docker Compose](https://docs.docker.com/compose/) (optional)
- [Conda](https://docs.conda.io/) (optional)

### Running with Docker Compose

```bash
docker-compose up
```

### Running with Conda

```bash
conda env create -f environment.yml
conda activate fastapi-objobssap
pip install - requirements.txt
pip install -e .
uvicorn fastapi_objobssap.main:app --reload
```

## License

See [LICENSE](./LICENSE) for details.