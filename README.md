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
- /api/visitor [GET] + "?CodiceFiscale=`codicefiscale`" -> return [json](#visitor-json)
- /api/visitor [DELETE] + "?CodiceFiscale=`codicefiscale`" -> delete the visitor and his subscriptions.
- /api/visitor [POST] -> given a [json](#visitor-json) add the visitor.

#### Visitor Json
```json
{
  "CodiceFiscale": str(16),
  "Nome": str,
  "Cognome": str,
  "DataDiNascita": str,
  "Altezza": int,
  "Peso": float
}
```

#### Entry
- /api/visitor/entries [GET] + "?CodiceFiscale=`codicefiscale`" -> return all the entries done by the given visitor
- /api/visitor/entry [POST] -> add a entry of the given visitor ([json](#visitor-entry-json))
- /api/visitor/entry [DELETE] + "?CodiceFiscale=`codicefiscale`&Data=`date`" -> delete the given entry 

#### Visitor Entry Json
```json
{
  "CodiceFiscale": str(16),
  "Data": date
}
```

### Subscription
- /api/subscription [GET] + "?CodiceFiscale=`codicefiscale`" -> return the active [json]
(#subscription-json)
- /api/subscription [DELETE] "?CodiceFiscale=`codicefiscale`&DataInizio=`datainizio`" -> delete the subscription.
- /api/subscription [POST] -> given a [json](#subscription-json) add the subscription.

#### Subscription Json
```json
{
  "CodiceFiscale": str(16),
  "DataInizio": str,
  "Costo": float,
  "Nome": str,
  "Giorni": int
}
```

- /api/subscription/durations [GET] -> return a json contains all the [json](#duration-json)
- /api/subscription/duration [POST] -> given a [json](#duration-json) add the duration.

  #### Duration Json
  ```json
  {
    "Giorni": int,
    "Sconto": float,
    "Descrizione": str
  }
  ```

- /api/subscription/tariffs [GET] -> return a json contains all the [json](#tariff-json)
- /api/subscription/tariff [POST] -> given a [json](#tariff-json) add the tariff.
  
  #### Tariff Json
  ```json
  {
    "Nome": str,
    "CostoGiornaliero": float
    "Categories": [Category] 
  }
  ```

- /subscription/cost [GET] + '?NomeTariffa=`nometariffa`&Giorni=`giorni`' -> return the cost of this subscription combo.
  #### cost Json
  ```json
  {
    "Costo": float,
  }
  ```

### Activity

- /activity

#### Rides
- /activity/rides

#### Categories
- /activity/ride/categories

- /activity/ride/categories

#### Limits
- /activity/ride/constraints
- /activity/ride/limits

#### Timetables
- /activity/events

- /activity/event/schedules
- /activity/event/schedule

#### Timetables
- /activity/entries
- /activity/entries

- /activity/entries/partecipates
- /activity/entries/partecipates

### Employess
- /employee
- /employee

#### Roles
- /employee/roles
- /employee/role

#### Require
- /employee/role/require

### Service
- /service
- /service

#### Timetables
- /service/timetable
- /service/timetable
