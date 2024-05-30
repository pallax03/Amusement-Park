from dataclasses import dataclass
from sqlalchemy import UniqueConstraint
from app import db

# Define database models
@dataclass
class Visitor(db.Model):
    CodiceFiscale: str
    Nome: str
    Cognome: str
    DataDiNascita: str
    Altezza: int
    Peso: float

    __tablename__ = 'VISITATORI'

    CodiceFiscale = db.Column(db.String(16), primary_key=True)
    Nome = db.Column(db.String(50), nullable=False)
    Cognome = db.Column(db.String(50), nullable=False)
    DataDiNascita = db.Column(db.Date, nullable=False)
    Altezza = db.Column(db.Integer, nullable=False)
    Peso = db.Column(db.Float, nullable=False)

@dataclass
class Duration(db.Model):
    Giorni: int
    Sconto: float
    Descrizione: str

    __tablename__ = 'DURATE'

    Giorni = db.Column(db.Integer, primary_key=True)
    Sconto = db.Column(db.Float, nullable=False)
    Descrizione = db.Column(db.String(255), nullable=False)

@dataclass
class Tariff(db.Model):
    Nome: str
    CostoGiornaliero: float

    __tablename__ = 'TARIFFE'

    IdTariffa = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nome = db.Column(db.String(50), unique=True)
    CostoGiornaliero = db.Column(db.Float, nullable=False)

@dataclass
class Subscription(db.Model):
    CodiceFiscale: str
    DataInizio: str
    Costo: float
    Nome: str
    Giorni: int
    
    __tablename__ = 'ABBONAMENTI'

    CodiceFiscale = db.Column(db.String(16), db.ForeignKey('VISITATORI.CodiceFiscale'), primary_key=True)
    DataInizio = db.Column(db.Date, primary_key=True)
    Costo = db.Column(db.Float, nullable=False)
    Nome = db.Column(db.String(50), db.ForeignKey('TARIFFE.Nome') , nullable=False)
    Giorni = db.Column(db.Integer, db.ForeignKey('DURATE.Giorni'), nullable=False)

class Entry(db.Model):
    __tablename__ = 'INGRESSI'

    IdIngresso = db.Column(db.Integer, primary_key=True, autoincrement=True)
    CodiceFiscale = db.Column(db.String(16), db.ForeignKey('VISITATORI.CodiceFiscale'))
    Data = db.Column(db.Date, nullable=False)
    UniqueConstraint('CodiceFiscale', 'Data')

class Limit(db.Model):
    __tablename__ = 'LIMITI'

    IdLimite = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Attributo = db.Column(db.String(50), nullable=False)
    Condizione = db.Column(db.CHAR(2), nullable=False)
    Valore = db.Column(db.String(50), nullable=False)
    Descrizione = db.Column(db.String(255), nullable=False)

class Category(db.Model):
    __tablename__ = 'CATEGORIE'

    IdCategoria = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nome = db.Column(db.String(50), nullable=False)

class Activity(db.Model):
    __tablename__ = 'ATTIVITA'

    IdAttivita = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nome = db.Column(db.String(50), nullable=False)
    Descrizione = db.Column(db.String(255), nullable=False)
    Posti = db.Column(db.Integer, nullable=False)
    IsEvent = db.Column(db.Boolean, nullable=False)
    IdCategoria = db.Column(db.Integer, db.ForeignKey('CATEGORIE.IdCategoria'), nullable=True)

class Constraint(db.Model):
    __tablename__ = 'VINCOLI'

    IdAttivita = db.Column(db.Integer, db.ForeignKey('ATTIVITA.IdAttivita'), primary_key=True)
    IdLimite = db.Column(db.Integer, db.ForeignKey('LIMITI.IdLimite'), primary_key=True)

class Schedule(db.Model):
    __tablename__ = 'PROGRAMMAZIONI'

    IdProgrammazione = db.Column(db.Integer, primary_key=True, autoincrement=True)
    IdAttivita = db.Column(db.Integer, db.ForeignKey('ATTIVITA.IdAttivita'), nullable=False)
    Data = db.Column(db.Date, nullable=False)
    Inizio = db.Column(db.Time, nullable=False)
    Fine = db.Column(db.Time, nullable=False)
    UniqueConstraint('IdAttivita', 'Data', 'Inizio', 'Fine')

class Participate(db.Model):
    __tablename__ = 'PARTECIPA'

    IdIngresso = db.Column(db.Integer, db.ForeignKey('INGRESSI.IdIngresso'), primary_key=True)
    Ora = db.Column(db.Time, primary_key=True)
    IdAttivita = db.Column(db.Integer, db.ForeignKey('ATTIVITA.IdAttivita'), nullable=False)

class Include(db.Model):
    __tablename__ = 'INCLUDE'

    IdTariffa = db.Column(db.Integer, db.ForeignKey('TARIFFE.IdTariffa'), primary_key=True)
    IdCategoria = db.Column(db.Integer, db.ForeignKey('CATEGORIE.IdCategoria'), primary_key=True)

class Role(db.Model):
    __tablename__ = 'RUOLI'

    IdRuolo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nome = db.Column(db.String(50), nullable=False)
    Stipendio = db.Column(db.Float, nullable=False)

class Timetable(db.Model):
    __tablename__ = 'ORARI'

    IdOrario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Monday = db.Column(db.String(11), nullable=True)
    Tuesday = db.Column(db.String(11), nullable=True)
    Wednesday = db.Column(db.String(11), nullable=True)
    Thursday = db.Column(db.String(11), nullable=True)
    Friday = db.Column(db.String(11), nullable=True)
    Saturday = db.Column(db.String(11), nullable=True)
    Sunday = db.Column(db.String(11), nullable=True)

class Service(db.Model):
    __tablename__ = 'SERVIZI'

    IdServizio = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nome = db.Column(db.String(50), nullable=False)
    Tipo = db.Column(db.String(50), nullable=False)
    IdOrario = db.Column(db.Integer, db.ForeignKey('ORARI.IdOrario'), nullable=False)

class Employee(db.Model):
    __tablename__ = 'PERSONALE'

    CodiceFiscale = db.Column(db.String(16), primary_key=True)
    Nome = db.Column(db.String(50), nullable=False)
    Cognome = db.Column(db.String(50), nullable=False)
    IdRuolo = db.Column(db.Integer, db.ForeignKey('RUOLI.IdRuolo'), nullable=False)
    IdServizio = db.Column(db.Integer, db.ForeignKey('SERVIZI.IdServizio'), nullable=False)

class Require(db.Model):
    __tablename__ = 'NECESSITA'

    IdCategoria = db.Column(db.Integer, db.ForeignKey('CATEGORIE.IdCategoria'), primary_key=True)
    IdRuolo = db.Column(db.Integer, db.ForeignKey('RUOLI.IdRuolo'), primary_key=True)
    Quantita = db.Column(db.Integer, nullable=False)
