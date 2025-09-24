<!-- markdownlint-disable-file MD024 -->

# CHANGELOG

## CHARMomics v0.3 - In Progress

### Features

- Consolidating the four `/annotation` endpoints in to a single endpoint
  - The new endpoint delineates different omic units using a query parameter

### Chores

- No longer returns annotations used for `cache` which are necessary to reduce third party API calls
- Fixed the pull request template to improve language and fix typo

## CHARMomics v0.2

### Features

- New annotation task type: JsonFileAnnotationTask
  - Allows annotation from a provided json file within CHARMomics
  - Contains a new version type called `manual` which allows for manual curated annotations
    - Ex. `curated-by-worthey` version
- Removed the Frontend service providing the ChatBot interface, feature handled by CHARM-GPT
  - Updated the project documentation to reflect the removal of the frontend service
- Added a `docker-compose.staging.yml` to allow docker swarm deployment on the CGDS development clusters
  - Updated the backend `Dockerfile` to include a production build stage
- Changed CHARMomics to use `local.charmomics.cgds/charmomics` instead of `localhost`
  - `setup.sh` script adds the url entry to the `etc/hosts` file on MacOS for local deployment
- Updated CHARMomics to be HTTPS deployment for both local and cluster deployments
  - `setup.sh` script now generates a self-signed SSL certificate for local deployment
- Added a `build.sh` script to build docker images for each service and pushes to the project GitHub docker registry
- Added Mongodb backup and restore scripts
  - `backup-database.sh` to dump the mongodb collections to a file
  - `restore-database.sh` to restore the mongodb collections from a file
- Provided scripts to annotate a list of genes or variants automatically
  - `annotate-gene-list.sh` automates annotating a list of genes using `POST /annotation/?type=gene&name={gene}`
  - `annotate-variant-list.sh` automates annotating a list of genes using
    `POST /annotation/?type=gene&name={hgvs_variant}`

### Bugs

- Added the `HTTPError` to the exception to the try and catch so a bad URL won't halt the annotation process
- Updated the annotation-config.json to fix Methylation annotation to fetch the whole value rather than just the results
interpretation
- Ensured `transcript_provisioned` is always initialized to `False` in the `AnnotationUnit` class

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
