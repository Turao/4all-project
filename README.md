# 4all-project

---
## Overview

Python Version: 3.7.2
Docker version 18.06.1-ce, build e68fc7a

---
## How-to's:
### Python Virtual Environment
To avoid versioning issues, you should activate the project's virtual environment.
- _cd_ to the app directory: i.e. `cd 4all-project/`
- Activate the environment:
  - if using bash/zsh `source ./bin/activate`
  - the command for other shells (fish/csh/tcsh) can be found at https://docs.python.org/3/library/venv.html

### Docker PostgreSQL
To speed things up, I've decided to run the PostgreSQL database into a docker container.
In case you do not have Docker installed in your machine, please follow the instructions at https://docs.docker.com/install/ 

To setup the container, run the following command: `sudo docker run --name 4all-postgresql -e POSTGRES_PASSWORD=14all41 -e POSTGRES_DB=4all-db-dev -e POSTGRES_USER=4all-user -p 5432:5432 -d postgres`

This may take a while, since it might have to download the PostgreSQL image from the Docker Hub.

Other commands you might find useful:
- Following the logs generated by the image, run: `sudo docker logs --follow 4all-postgresql`
- Starting the container: `sudo docker start 4all-postgresql`
- Show containers and their statuses: `sudo docker ps`
- Stopping the container: `sudo docker stop 4all-postgresql`
- Removing the container: `sudo rm 4all-postgresql`

### Environment Variables
#### Postgres

- `export DB_NAME=4all-db-dev`

- `export DB_HOST=localhost`
- `export DB_PORT=5432`

- `export DB_USER=4all-user`
- `export DB_PASSWORD=14all41`

- `export DB_POOL_MAX_CONNECTIONS=32`
- `export DB_POOL_TIMEOUT=300`

#### OpenCageAPI
- `export OPENCAGE_KEY=[your_app_key_here]`
