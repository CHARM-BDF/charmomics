<!-- markdownlint-disable-file MD024 -->

# CHANGELOG

## CHARMomics v0.2.2

- Added Monarch Initiative KG external database annotations for Genes. An annotation API call with a gene symbol may
  provide these annotations if available:
  - Pairwise gene to gene interactions with evidence from pubmed or obolibrary.
  - Gene to expression site using UBERON codes.
  - Gene to gene homology association provided by PANTHER.
  - Gene to pathway association using Reactome.

## CHARMomics v0.2.1

- A new `Diagnostic Tests` endpoint that serves up a number of diagnostic tests
  - New diagnostic tests include: Microsatellite Instability, Mismatch Repair Immunohistochemistry, and Mismatch Repair
    Germline.
  - Querying the diagnostic test endpoint will provided the comprehensive list of diagnostic test result
    interpretations, but querying a gene symbol, still provide that gene's diagnostic test result interpretation.
  - New Enum types were created for the diagnostic testing endpoint, will display the tests in the Swagger docs for drop
    down selection.
- Added a `catalog.md` for displaying what omics annotations are available along with examples of what those annotations
  look like.
  - Added an **Available Annotations for CHARMomics** section in the general `README.md` to point users to the
    `catalog.md`
- Added a new annotation method to queue a single annotation task. This allows a genomic unit to be created with a
  single annotation that matches on the genomic unit type and the dataset name.
  - Example: Allows Microsatellite Instability (MSI) to be considered a diagnostic test unit type and contain only the
    MSI annotations.
- Performed an audit on package versions used by CHARMomics.
  - Up-ticked python packages to remove deprecation warnings when running newer versions of Python
  - Up-ticked the versions for the `common-static-analysis.yml` for the Hadolint, Shellchecker, and Markdown
- Changed the language from `Omic` back to `Genomic` throughout the project.

### Features

- Consolidating the four `/annotation` endpoints in to a single endpoint
  - The new endpoint delineates different genomic units using a query parameter

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
