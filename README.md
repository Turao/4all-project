# 4all-project

[![CircleCI](https://circleci.com/gh/Turao/4all-project/tree/develop.svg?style=svg&circle-token=7f214d329f95bee31c60557f08ac58fbcbe650a4)](https://circleci.com/gh/Turao/4all-project/tree/develop)

---
## Overview

_Datapoints_ is a Python module that provides functionalities for data extraction and storage.

Its submodule _Hermes_ is responsible for extracting geopoint data from a file and enriching this data by using a reverse geocoding API (OpenCage).

This project provides an _ENHANCEMENTS_ file, with things that can be improved.

It also provides a _LOG BOOK_, which is used to log decisions made throughout the development of this project. I think this might help you understand why things are the way they are.


---
## Table of contents:
- [Dependencies](#dependencies)
- [Configuring](#configuring)
  - [Python Virtual Environment](#python-virtual-environment)
  - [Docker Setup](#docker-setup)
    - [Manually](#manually)
  - [Configuring ulimit](#configuring-ulimit)
    - [Troubleshooting](#troubleshooting)
- [Running Hermes (data ingestion module)](#running-hermes-data-ingestion-module)
  - [Running only the Parser]($running-parser)
- [Running Unit Tests (manually)](#running-unit-tests-manually)
- [Code Quality](#code-quality)


---
## Dependencies:

- Python (version: 3.7.2)
  - Python dependencies can be found in `requirements.txt`
- Docker (version 18.09.3-ce)


---
## Configuring:

### Python Virtual Environment
To avoid dependency issues, you should activate the project's virtual environment.
- _cd_ to the app directory: i.e. `cd 4all-project/`
- Activate the environment:
  - if using bash/zsh: `source ./bin/activate`
  - the command for other shells (fish/csh/tcsh) can be found at https://docs.python.org/3/library/venv.html

### Docker Setup
**TLDR:** You can run things:
- Manually:
  - the hard way: creating containers by yourself
    - this allows you to call the app's main module
  - the easy way: running the composer
    - this only runs unit tests
- Automatically:
  - unit tests are executed by CircleCI on each commit
    - the badge above shows the status of the execution

#### Manually
In case you do not have Docker installed in your machine, please follow the instructions at https://docs.docker.com/install/
Check the environment variables provided in the `.env` file.
- I **strongly** suggest you to create an OpenCage account at https://opencagedata.com/ so you can use your own API key.
- **Note:** you should **NEVER** expose your .env files to repos.
  - I've provided them so you can run the easy way for yourself without having to create the file.

##### The easy way
- cd to `src/`
- run `sudo docker-compose up`

##### The hard way
- Export the Environment Variables (check the `.env` file for reference)
  - **Note:** the variable DB_HOST should be set as localhost if running the database locally
    - `export DB_HOST=localhost`
- To setup the PostgreSQL container, run the following command: `sudo docker run --name 4all-postgresql -e POSTGRES_PASSWORD=$DB_PASSWORD -e POSTGRES_DB=$DB_NAME -e POSTGRES_USER=$DB_USER -p 5432:$DB_PORT -d postgres`
  - This may take a while, since it might have to download the PostgreSQL image from the Docker Hub.

Other commands you might find useful:
- Following the logs generated by the image, run: `sudo docker logs --follow 4all-postgresql`
- Starting the container: `sudo docker start 4all-postgresql`
- Show containers and their statuses: `sudo docker ps`
- Stopping the container: `sudo docker stop 4all-postgresql`
- Removing the container: `sudo rm 4all-postgresql`


### Configuring ulimit:
If you want to send a high amount of requests, you might have to increase the limit of files that can be opened simultaneously (since each request opens a file descriptor).

To make things easier, we'll set both HARD and SOFT limits to the same value...

**Shell script:** to help you avoid doing too much work, I've provided a shell script in `setup/set-ulimit.sh`. Please be advised that this script will only append the lines described below to the files (no replacement is done).

- To execute the script, run from the project's directory: `./setup/set-ulimit.sh [system_user] [limit_you_want]`
    - If you do not know your user, run: `whoami`

- First, we'll ask for PAM to set some rules for us (use _optional_ instead of _required_, otherwise you might mistype the limit rule and be unable to log in)
  - Add the line `session optional pam_limits.so` to the following files:
    - `/etc/pam.d/common-session`
    - `/etc/pam.d/common-session-noninteractive`

- Then, add the limit rules to the config file `/etc/security/limits.conf`
  - Add the line `* soft nofile 10240`
  - Add the line `* hard nofile 10240`

- Log out
- Log in

- Finally, check your SOFT limit by running `ulimit -n` in the terminal

##### Troubleshooting:
- The limit did not change:
  - (a bit hacky) try to `su [your_user_here]` and run the command again, execute the program from this shell
  - check for typos in your limit rules
  - check if PAM is enabled and calling limits.so

More about _limits.conf_ and _pam.d_ can be found at:
- https://linux.die.net/man/5/limits.conf
- https://linux.die.net/man/5/pam.d


---
## Running Hermes (data ingestion module):
Hermes is the module responsible for calling the Parser and enriching the database with data provided by the OpenCage Geocoder.

To execute the data extractor module (aka Hermes):
- make sure you have your virtual environment activated (see above)
- cd to `src/`
- run `python -m datapoints.hermes [your_dataset_here] [optional_batch_size] [optional_timeout]`.
  - mock data is provided in `datapoints/tests/mock_coordinates/` 
  - batch size defaults to 200 rows at a time
  - timeout defaults to 5 seconds

### Running only the Parser:
Parser (or Location Parser, to be specific) is the module responsible for parsing the datasets, extracting latitude, longitude and distance data.

To execute (only) the parsing module :
- make sure you have your virtual environment activated (see above)
- cd to `src/`
- run `python -m datapoints.parser.location_parser [your_dataset_here]`
  - mock data is provided in `datapoints/tests/mock_coordinates/`


---
## Running Unit Tests (manually):
Unit tests are located in the `src/datapoints/tests` directory.

To execute **all** unit tests:
- make sure you have your virtual environment activated (see above)
- cd to `src/`
- run the unittest module in discover mode: `python -m unittest discover`

To execute unit tests from a single **module**:
- make sure you have your virtual environment activated (see above)
- cd to `src/`
- run the unittest module and pass module you want to test
    - i.e. `python -m unittest datapoints.tests.test_location`


---
## Code Quality:
To measure code complexity (i.e. cyclomatic complexity), you can use the _radon_ tool
- `radon cc -a src/`

More about radon can be found at: https://pypi.org/project/radon/
