# Amusament-Park
Progetto finale per il corso (8615) in Basi Di Dati.

L'obiettivo del progetto è quello di realizzare un sistema per la gestione di un parco divertimenti.

IMMAGINE SCHEMA RELAZIONALE!!!

## Prerequisites
- Make sure that you have Docker and Docker Compose installed
  - Windows or macOS:
    [Install Docker Desktop](https://www.docker.com/get-started)
  - Linux: [Install Docker](https://www.docker.com/get-started) and then
    [Docker Compose](https://github.com/docker/compose)

## Running the project

Launch the database, this is a MySQL server, that create a database called amusamentpark, and it will automatically populate and create some tables. 

```console
docker compose up db
```

After the db finished to start up, run the backend. 

```console
docker compose up backend
```

now, you will be able to connect to [`http://localhost:4000`](http://localhost:4000)