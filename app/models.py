from dataclasses import dataclass
from sqlalchemy import UniqueConstraint
from sqlalchemy.dialects.mysql import BIT
from sqlalchemy import text
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
    IdTariffa: int
    NomeTariffa: str
    CostoGiornaliero: float

    __tablename__ = 'TARIFFE'

    IdTariffa = db.Column(db.Integer, primary_key=True, autoincrement=True)
    NomeTariffa = db.Column(db.String(50), unique=True)
    CostoGiornaliero = db.Column(db.Float, nullable=False)

@dataclass
class Subscription(db.Model):
    CodiceFiscale: str
    DataInizio: str
    Costo: float
    NomeTariffa: str
    Giorni: int
    
    __tablename__ = 'ABBONAMENTI'

    CodiceFiscale = db.Column(db.String(16), db.ForeignKey('VISITATORI.CodiceFiscale'), primary_key=True)
    DataInizio = db.Column(db.Date, primary_key=True)
    Costo = db.Column(db.Float, nullable=False)
    NomeTariffa = db.Column(db.String(50), db.ForeignKey('TARIFFE.NomeTariffa') , nullable=False)
    Giorni = db.Column(db.Integer, db.ForeignKey('DURATE.Giorni'), nullable=False)

@dataclass
class Entry(db.Model):
    IdIngresso: int
    CodiceFiscale: str
    Data: str

    __tablename__ = 'INGRESSI'

    IdIngresso = db.Column(db.Integer, primary_key=True, autoincrement=True)
    CodiceFiscale = db.Column(db.String(16), db.ForeignKey('VISITATORI.CodiceFiscale'))
    Data = db.Column(db.Date, nullable=False)
    UniqueConstraint('CodiceFiscale', 'Data')

@dataclass
class Limit(db.Model):
    IdLimite: int
    Attributo: str
    Condizione: str
    Valore: str
    Descrizione: str

    __tablename__ = 'LIMITI'

    IdLimite = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Attributo = db.Column(db.String(50), nullable=False)
    Condizione = db.Column(db.CHAR(2), nullable=False)
    Valore = db.Column(db.String(50), nullable=False)
    Descrizione = db.Column(db.String(255), nullable=False)

@dataclass
class Category(db.Model):
    IdCategoria: int
    Nome: str

    __tablename__ = 'CATEGORIE'

    IdCategoria = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nome = db.Column(db.String(50), nullable=False, unique=True)

@dataclass
class Activity(db.Model):
    IdAttivita: int
    Nome: str
    Descrizione: str
    Posti: int
    IsEvent: bool
    IdCategoria: int

    __tablename__ = 'ATTIVITA'

    IdAttivita = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nome = db.Column(db.String(50), nullable=False)
    Descrizione = db.Column(db.String(255), nullable=False)
    Posti = db.Column(db.Integer, nullable=False)
    IsEvent = db.Column(BIT(1), nullable=False)
    IdCategoria = db.Column(db.Integer, db.ForeignKey('CATEGORIE.IdCategoria'), nullable=True)

@dataclass
class Constraint(db.Model):
    IdAttivita: int
    IdLimite: int

    __tablename__ = 'VINCOLA'

    IdAttivita = db.Column(db.Integer, db.ForeignKey('ATTIVITA.IdAttivita'), primary_key=True)
    IdLimite = db.Column(db.Integer, db.ForeignKey('LIMITI.IdLimite'), primary_key=True)

@dataclass
class Schedule(db.Model):
    IdProgrammazione: int
    IdAttivita: int
    Data: str
    Inizio: str
    Fine: str

    __tablename__ = 'PROGRAMMAZIONI'

    IdProgrammazione = db.Column(db.Integer, primary_key=True, autoincrement=True)
    IdAttivita = db.Column(db.Integer, db.ForeignKey('ATTIVITA.IdAttivita'), nullable=False)
    Data = db.Column(db.Date, nullable=False)
    Inizio = db.Column(db.Time, nullable=False)
    Fine = db.Column(db.Time, nullable=False)
    UniqueConstraint('IdAttivita', 'Data', 'Inizio', 'Fine')

@dataclass
class Participate(db.Model):
    IdIngresso: int
    Ora: str
    IdAttivita: int

    __tablename__ = 'PARTECIPA'

    IdIngresso = db.Column(db.Integer, db.ForeignKey('INGRESSI.IdIngresso'), primary_key=True)
    Ora = db.Column(db.Time, primary_key=True)
    IdAttivita = db.Column(db.Integer, db.ForeignKey('ATTIVITA.IdAttivita'), nullable=False)

@dataclass
class Include(db.Model):
    IdTariffa = int
    IdCategoria = int

    __tablename__ = 'INCLUDE'

    IdTariffa = db.Column(db.Integer, db.ForeignKey('TARIFFE.IdTariffa'), primary_key=True)
    IdCategoria = db.Column(db.Integer, db.ForeignKey('CATEGORIE.IdCategoria'), primary_key=True)

@dataclass
class Role(db.Model):
    IdRuolo: int
    Nome: str
    Stipendio: float

    __tablename__ = 'RUOLI'

    IdRuolo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nome = db.Column(db.String(50), nullable=False, unique=True)
    Stipendio = db.Column(db.Float, nullable=False)

@dataclass
class Timetable(db.Model):
    IdOrario: int
    Lunedi: str
    Martedi: str
    Mercoledi: str
    Giovedi: str
    Venerdi: str
    Sabato: str
    Domenica: str

    __tablename__ = 'ORARI'

    IdOrario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Lunedi = db.Column(db.String(11), nullable=True)
    Martedi = db.Column(db.String(11), nullable=True)
    Mercoledi = db.Column(db.String(11), nullable=True)
    Giovedi = db.Column(db.String(11), nullable=True)
    Venerdi = db.Column(db.String(11), nullable=True)
    Sabato = db.Column(db.String(11), nullable=True)
    Domenica = db.Column(db.String(11), nullable=True)

@dataclass
class Service(db.Model):
    IdServizio: int
    Nome: str
    Tipo: str
    IdOrario: int

    __tablename__ = 'SERVIZI'

    IdServizio = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nome = db.Column(db.String(50), nullable=False, unique=True)
    Tipo = db.Column(db.String(50), nullable=False)
    IdOrario = db.Column(db.Integer, db.ForeignKey('ORARI.IdOrario'), nullable=False)

@dataclass
class Employee(db.Model):
    CodiceFiscale: str
    Nome: str
    Cognome: str
    DataDiNascita: str
    IdRuolo: int
    IdServizio: int

    __tablename__ = 'PERSONALE'

    CodiceFiscale = db.Column(db.String(16), primary_key=True)
    Nome = db.Column(db.String(50), nullable=False)
    Cognome = db.Column(db.String(50), nullable=False)
    DataDiNascita = db.Column(db.Date, nullable=False)
    IdRuolo = db.Column(db.Integer, db.ForeignKey('RUOLI.IdRuolo'), nullable=False)
    IdServizio = db.Column(db.Integer, db.ForeignKey('SERVIZI.IdServizio'), nullable=True)

@dataclass
class Require(db.Model):
    IdCategoria = int
    IdRuolo = int
    Quantita = int

    __tablename__ = 'NECESSITA'

    IdCategoria = db.Column(db.Integer, db.ForeignKey('CATEGORIE.IdCategoria'), primary_key=True)
    IdRuolo = db.Column(db.Integer, db.ForeignKey('RUOLI.IdRuolo'), primary_key=True)
    Quantita = db.Column(db.Integer, nullable=False)
