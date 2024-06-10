# Marimo DataEntry

Use case presented in IPPON Blog Post "Marimo : L'Avenir du Notebook".  
Link to blog post ? As soon as it's published !

## SETUP
- clone the repo
- install poetry, more info [here](https://python-poetry.org/docs/#installation)
- install compatible python version (from 3.12), eg. `pyenv install 3.12.3`
- move to dataentry-app folder and install the project :
  - `cd dataentry-app`
  - `poetry env use 3.12 && poetry install`

## TEST LOCALLY
Still in `dataentry-app` folder, first enter the poetry shell with `poetry shell`command.  
Then :
- you can edit the Marimo Notebook with `marimo edit app.py`
- you can run th Notebook with `marimo run app.py`

From Marimo, you can load one of the test files located in the `sample_reports` folder.

## TEST IN DOCKER
Needed : docker installed locally, more info [here](https://docs.docker.com/engine/install/).  
From repository root folder :
- Build with `docker build --target=runtime -t dataentry:v1 .`
- Run with `docker run -p 8080:8080 -it dataentry:v1`

=> Marimo app should be available at http://0.0.0.0:8080/

## Functional Programming ?
This project uses a budding functional style library for python, more precisely the `Xeffect` class that helps dealing with unpure types.  
To learn more, take a look at samples provided on the [v1 beta branch of the repository](https://github.com/sebvey/python-fp/tree/v1.0.0-beta).
