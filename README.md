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

Run the database, is a MySQL server, that create a database called amusamentpark, and it will automatically  create and populate some tables. 

#### Run db
```console
docker compose up --build db
```

After the db finished to start up, run the backend. 

#### Run backend
```console
docker compose up --build backend
```

now, you will be able to connect to [`http://localhost:4000`](http://localhost:4000)