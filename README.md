# Amusement-Park
Progetto finale per il corso (8615) in Basi Di Dati.

L'obiettivo del progetto è quello di realizzare un sistema per la gestione di un parco divertimenti.

IMMAGINE SCHEMA RELAZIONALE!!!

### Table Of Contents
- [Prerequisites](#prerequisites)
- [Running the project](#running-the-project)
- [Pages](#pages)
- [API documentation](#api)

![image](/app/static/img/SchemaRelazionale.png)

## Prerequisites
- Make sure that you have Docker and Docker Compose installed
  - Windows or macOS:
    [Install Docker Desktop](https://www.docker.com/get-started)
  - Linux: [Install Docker](https://www.docker.com/get-started) and then
    [Docker Compose](https://github.com/docker/compose)

## Running the project

Run the database, is a MySQL server, that create a database called amusamentpark, and it will automatically  create and populate some tables. 

```console
docker compose up --build
```

now, you will be able to connect to [`http://localhost:4000`](http://localhost:4000)


## PAGES
- [/visitors](http://localhost:4000/visitors)
- [/subscriptions](http://localhost:4000/subscriptions)
- [/activities](http://localhost:4000/activities)
- [/rides](http://localhost:4000/rides)
- [/events](http://localhost:4000/events)
- [/employees](http://localhost:4000/employees)
- [/services](http://localhost:4000/services)

## API documentation
### Visitor
- /visitor [GET] + "?CodiceFiscale=`codicefiscale`" -> return [json](#visitor-json)
- /visitor [POST] -> given a [json](#visitor-json) add the visitor.

#### Visitor Json
```json
{
  "CodiceFiscale": str(16),
  "Nome": str,
  "Cognome": str,
  "DataDiNascita": str, //of a date format
  "Altezza": int,
  "Peso": float
}
```

### Subscription
- /subscription [GET] + "?CodiceFiscale=`codicefiscale`" -> return the active [json](#subscription-json)
- /subscription [POST] -> given a [json](#subscription-json) add the subscription.

#### Subscription Json
```json
{
  "CodiceFiscale": str(16),
  "DataInizio": str, //of a date format
  "Costo": float,
  "Nome": str,       // chosen Tariff  
  "Giorni": int      // chosen Duration
}
```

- /subscriptions/durations [GET] -> return a json contains all the [json](#duration-json)
- /subscriptions/durations [POST] -> given a [json](#duration-json) add the duration.

  #### Duration Json
  ```json
  {
    "Giorni": int,
    "Sconto": float,
    "Descrizione": str
  }
  ```

- /subscriptions/tariffs [GET] -> return a json contains all the [json](#tariff-json)
- /subscriptions/tariffs [POST] -> given a [json](#tariff-json) add the tariff.
  
  #### Tariff Json
  ```json
  {
    "Nome": str,
    "CostoGiornaliero": float
    "Include": [int] //IdCategoria -> categorie che si vogliono includere 
  }
  ```


### Activity

#### rides
#### categories
#### constraints
#### limits

#### events
#### schedules

#### entries
#### partecipates

### Employess

#### roles
#### requires

### Service

#### Timetables
