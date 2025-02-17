# CHANGELOG

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
