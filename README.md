# FastAPI-ObjObsSAP

This project is an example Python implementation of the proposed IVOA ObjObsSAP standard using [FastAPI](https://fastapi.tiangolo.com/).

This example service provides an API to calculate observable times for celestial objects from an example telescope location (Baltimore, MD, USA) using the [Astroplan](https://astroplan.readthedocs.io/en/latest/) library.

## Getting Started

Running the project with docker-compose is the recommended way to get started quickly. By default, the api will be available at `http://localhost:8000/query`.

Additionally, the VOSI Capabilities endpoint is available at `http://localhost:8000/capabilities`, which provides information about the available operations and their parameters.

Interactive Swagger documentation is available at `http://localhost:8000/docs`.

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
pip install -r requirements.txt
pip install -e .
uvicorn fastapi_objobssap.main:app --reload
```

## License

See [LICENSE](./LICENSE) for details.
