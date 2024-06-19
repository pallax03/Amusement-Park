# Amusement-Park
Progetto finale per il corso (8615) in Basi Di Dati.

L'obiettivo del progetto è quello di realizzare un sistema per la gestione di un parco divertimenti.

IMMAGINE SCHEMA RELAZIONALE!!!
![image](/app/static/img/SchemaRelazionale.png)

### Table Of Contents
- [Prerequisites](#prerequisites)
- [Running the project](#running-the-project)
- [Pages](#pages)
- [API documentation](#api-documentation)

## Prerequisites
- Make sure that you have Docker and Docker Compose installed
  - Windows or macOS:
    [Install Docker Desktop](https://www.docker.com/get-started)
  - Linux: [Install Docker](https://www.docker.com/get-started) and then
    [Docker Compose](https://github.com/docker/compose)

## Running the project

Compose:
- a MySQL server, that create a database called amusamentpark, and it will automatically  create and populate some tables.
- a Flask web app.

```console
docker compose up --build
```

now, you will be able to connect to [`http://localhost:4000`](http://localhost:4000)


## PAGES
- [/visitors](http://localhost:4000/visitors)
- [/subscriptions](http://localhost:4000/subscriptions)
- [/activities](http://localhost:4000/activities)
- [/partecipates](http://localhost:4000/partecipates)
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

##### Visitor Entry Json
```json
{
  "CodiceFiscale": str(16),
  "Data": date
}
```

### Subscription
- /api/subscription [GET] + "?CodiceFiscale=`MNNGPP99A01H501A`" -> return the active [json]
(#subscription-json)
- /api/subscription [DELETE] '?CodiceFiscale=`MNNGPP99A01H501A`&DataInizio=`2021-01-01`' -> delete the subscription.
- /api/subscription [POST] -> given a [json](#subscription-json) add the subscription.

#### Subscription Json
```json
{
  "CodiceFiscale": str(16),
  "DataInizio": str,
  "Costo": float,
  "NomeTariffa": str,
  "Giorni": int
}
```

#### Duration
- /api/subscription/durations [GET] -> return a json contains all the [json](#duration-json)
- /api/subscription/duration [POST] -> given a [json](#duration-json) add the duration.
- /api/subscription/duration [DELETE] + '?Giorni=`7`' -> delete the given Duration.
(if is not used by any of active subscriptions)

  ##### Duration Json
  ```json
  {
    "Giorni": int,
    "Sconto": float,
    "Descrizione": str
  }
  ```

#### Tariff
- /api/subscription/tariffs [GET] -> return a json contains all the [json](#tariff-json)
- /api/subscription/tariff [POST] -> given a [json](#tariff-json) add the tariff.
- /api/subscription/tariff [DELETE] + '?NomeTariffa=`Standard`' -> delete the given Tariff.
(if is not used by any of active subscriptions)

  ##### Tariff Json
  ```json
  {
    "Nome": str,
    "CostoGiornaliero": float
    "Categories": [Category] 
  }
  ```

- /api/subscription/cost [GET] + '?NomeTariffa=`Standard`&Giorni=`7`' -> return the cost of this subscription combo.
  #### cost Json
  ```json
  {
    "Costo": float,
  }
  ```

### Activity
- /api/activities [GET] -> get all the [activities](#activity-json) (events and rides).

#### Activity Json
```json
{
  "IdAttivita": int,
  "Nome": str,
  "Descrizione": str,
  "Posti": int,
  "IsEvent": boolean
}
```

#### Event
- /api/activity/events [GET] -> return all the [events](#events-json)
- /api/activity/events [POST] -> given a json add an event
- /api/activity/events [DELETE] + '?IdEvento=1' -> delete an event (if haven't any schedules or if the schedules are expired)


##### Event Json
```json
{
  "IdAttivita": int,
  "Nome": str,
  "Descrizione": str,
  "Posti": int
}
```
#### Schedule
- /api/activity/events/schedules [GET] + '?IdAttivita=1' -> return the schedule of the specified event.
- /api/activity/events/schedules [POST] -> add a [schedule json](#schedule-json) of an event. 

##### Schedule Json
```json
{
  "IdAttivita": int,
  "Data": date,
  "Inizio": time,
  "Fine": time
}
```


#### Ride
- /api/activity/rides [GET] + '?category=Acqua&limit=1&tariff=Bronze'  -> return all the rides, can be filter by Category, Limit and included tariffs.
- /api/activity/rides [POST] -> add a new [ride](#ride-json).
- /api/activity/rides [DELETE] + '?IdAttivita=1' -> delete a ride.

##### Ride Json
```json
{
  "Nome": str,
  "Descrizione": str,
  "Posti": int,
  "NomeCategoria": str,
  "Limiti": [[json](#limit-json)], // in add rides constrait a limit using Limiti: [IdLimite, ..., IdLimite]. 
  "Tariffe": [[json](#tariff-json)] // in add rides, that doesnt need
}
```


#### Category
- /api/activity/ride/categories [GET] -> return the all the [categories](#category-json).
- for add a category it can be specified adding a ride.

##### Category Json
```json
{
  "IdCategoria": int,
  "Nome": str
}
```


#### Limit
- /api/activity/rides/limits [GET] -> return all the [limits](#limit-json) present in any ride.

##### Limit Json
```json
{
  "IdLimite": int,
  "Attributo": str,
  "Condizione": str,
  "Descrizione": str,
  "Valore": str
}
```


### Partecipate
- /partecipates
- /partecipates


### Employee
- /api/employee [POST] -> add a employee and if the role is not present, add it [json](#employee-json).
- /api/employee + '?CodiceFiscale=RSSMRA85M01H501Z' [DELETE] -> delete an employee.

#### Employee Json
```json
{
  "CodiceFiscale": str,
  "Nome": str,
  "Cognome": str,
  "DataDiNascita": str,
  "Ruolo": {
    "Nome": str
    "Stipendio": float
    "Requires": [Require](#require-json)
  }
}
```

#### Role
- /api/employee/roles -> get all the roles [json](#role-json)
- /api/employee/role [DELETE] + '?IdRuolo=1' -> delete a role
- /api/employee/service [POST] + '?CodiceFiscale=RSSMRA85M01H501Z&IdServizio=1' -> add a service to a employee, the service can be None

##### Role Json
```json
{
  "IdRuolo": int,
  "Nome": str,
  "Stipendio": float,
  "Requires": [Require](#require-json)  
}
```

##### Require Json
```json
{
  "NomeCategoria": str,
  "Quantita": int,
}
```

### Service
- /api/services [GET] /services + '?Tipo=`Negozio`' -> given the services filtered with `Tipo`, iif not wxist give all the [json](#service-timetable-json) 
- /api/services/types [GET] -> give the Tipo of the services (distinct). 
- /api/service [GET] + '?Nome=OVS' -> give the service [json](#service-timetable-json) 
- /api/service [POST] -> add the service given the [json](#service-timetable-json)
- /api/service [DELETE] + '?Nome=OVS' -> delete the service 

#### Service Timetable Json
```json
{
  "Nome": str,
  "Tipo": str,
  "Orario": [Timetable](#timetable-json)
}
```

#### Timetable
- /api/service/timetable [GET] + '?Nome=OVS' -> give the [json](#timetable-json).
- /api/service/timetable [POST] -> add the given [json](#timetable-json)

##### Timetable Json
```json
{
  "IdOrario": int,
  "Lunedi": str, //11:00-11:00
  "Martedi": str,
  "Mercoledi": str,
  "Giovedi": str,
  "Venerdi": str,
  "Sabato": str,
  "Domenica": str
}
```
