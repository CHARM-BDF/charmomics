# CHANGELOG

## CHARMomics v0.2

### Features - In Progress

- Removed the Frontend service providing the ChatBot interface, feature handled by CHARM-GPT
  - Updated the project documentation to reflect the removal of the frontend service
- Added a docker-compose.staging.yml to allow docker swarm deployment on the CGDS development cluster
  - Updated the backend `Dockerfile` to include a production build stage
- Changed CHARMomics to use `local.charmomics.cgds/charmomics` instead of `localhost`
  - `setup.sh` script adds the url entry to the `etc/hosts` file on MacOS for local deployment
- Updated CHARMomics to be HTTPS deployment for both local and cluster deployments
  - `setup.sh` script now generates a self-signed SSL certificate for local deployment
- Added a `build.sh` script to build docker images for each service and pushes to the project GitHub docker registry

### Chores

- Changed the FastAPI root endpoint to be `/heart-beat` and returns 'thump-thump'
- Implements GitHub Actions for beginning of CICD pipeline
  - Added integration tests to CHARMomics for each endpoint to be tested thoroughly

## CHARMomics v0.1

### Features

- Updated the documentation by renaming Franklin to CHARMomics, fixed documentation all around
- Fixed an issue with the annotation manifest collection not keeping track of the genomic unit versions
- Added new annotations to the annotation configuration to pull the ditto score
- Added a new annotation task to allow for calling subprocesses and returning annotation data
- Updated the annotation configuration fixture to reflect the 0.8.3 version of Rosalution
- Updated the Python backend to run Uvicorn to as a command rather than entrypoint to allow for faster docker stopping
- Added MongoDB in docker compose and updated the backend to use the instance
- ChatBot interface communicating with the OpenStack Ollama instance

---
