from datetime import datetime, timedelta, date
import calendar

from models import *


# DASHBOARD

# raw queries
def query_N13_highest_entries_days(DataInizio, DataFine):
    DataInizio = datetime.now().replace(day=1) if DataInizio == None else datetime.strptime(DataInizio, '%Y-%m-%d') if type(DataInizio) is not date else DataInizio
    DataFine =  DataInizio.replace(day=calendar.monthrange(DataInizio.year, DataInizio.month)[1]) if DataFine == None else datetime.strptime(DataFine, '%Y-%m-%d') if type(DataFine) is not date else DataFine
    query = text(f'SELECT Data, COUNT(*) AS NumeroIngressi FROM INGRESSI WHERE Data BETWEEN \'{DataInizio}\' AND \'{DataFine}\' GROUP BY Data ORDER BY NumeroIngressi DESC')
    dict = []
    for result in db.session.execute(query):
        dict.append({'Data': datetime.strftime(result[0], '%Y-%m-%d'), 'NumeroIngressi': result[1]})
    return dict

# WARNING: SQL INJECTION, so pass a Category.Nome as a parameter   
def query_N14_most_partecipated_rides(categoryname = None):
    categoryname = '' if categoryname==None else 'WHERE c.Nome = ' + categoryname
    query = text(f'SELECT a.Nome as NomeCategoria, COUNT(p.IdAttivita) as PartecipazioniTotali FROM ATTIVITA as a, CATEGORIE as c, PARTECIPA as p WHERE a.IsEvent=false AND a.IdCategoria = c.IdCategoria AND a.IdAttivita = p.IdAttivita { categoryname } GROUP BY a.Nome, c.Nome ORDER BY PartecipazioniTotali')
    dict = []
    for result in db.session.execute(query):
        dict.append({'NomeCategoria': result[0], 'PartecipazioniTotali': result[1]})
    return dict

# WARNING: SQL INJECTION, so pass a Tariff.NomeTariffa as a parameter
def query_N15_highest_shopped_subscriptions(tariffname = None):
    tariffname = '' if tariffname==None else 'WHERE NomeTariffa = ' + tariffname
    query = text(f'SELECT NomeTariffa, Giorni, COUNT(*) as NumeroAbbonamenti FROM ABBONAMENTI {tariffname} GROUP BY NomeTariffa, Giorni ORDER BY Giorni')
    dict = []
    for result in db.session.execute(query):
        dict.append({'NomeTariffa': result[0], 'Giorni': result[1], 'NumeroAbbonamenti': result[2]})
    return dict

# VISITORS

# check if the subscription is active
# data can be a string or a datetime object
# return the subscription if active, None otherwise
def check_active_subscription(CodiceFiscale, Data):
        for subscription in Subscription.query.filter_by(CodiceFiscale=CodiceFiscale).all():
            subscription_endDate = subscription.DataInizio + timedelta(days=float(subscription.Giorni))
            formatted_date = datetime.strptime(Data, '%Y-%m-%d').date() if type(Data) == str else Data
            if subscription.DataInizio <= formatted_date and subscription_endDate >= formatted_date:
                return subscription
        return None


# SUBSCRIPTIONS

# delete all the subscriptions that are not active anymore,
# filter by CodiceFiscale or Tariffa or Durata
def delete_non_active_subscriptions(codicefiscale=None, tariffa=None, durata=None):
    subscriptions = Subscription.query.all()
    if codicefiscale:
        subscriptions = Subscription.query.filter_by(CodiceFiscale=codicefiscale).all()
    if tariffa:
        subscriptions = Subscription.query.filter_by(NomeTariffa=tariffa.NomeTariffa).all()
    if durata:
        subscriptions = Subscription.query.filter_by(Giorni=durata.Giorni).all()
    
    for subscription in subscriptions:
        if datetime.strptime(str(subscription.DataInizio),'%Y-%m-%d') + timedelta(days=float(subscription.Giorni)) < datetime.now():
            db.session.delete(subscription)
    db.session.commit()


# PARTECIPATES

# return the schedule of an activity in a specific date and time,
# if schedule is programmed between Start<Ora<Inizio
# - IdAttivita must be an int
# - Data and Ora can be a str o a date, time
def get_schedule_between_time(IdAttivita, Data, Ora):
    Data, Ora = Data.strftime("%Y-%m-%d").date() if type(Data) == str else Data, Ora.strftime("%H:%M").time() if type(Ora) == str else Ora
    schedule = Schedule.query.filter_by(IdAttivita=IdAttivita, Data=Data).all()
    for s in schedule:
        if check_schedule(s, Ora):
            return s
    return None


# check if the Ora (time()) is between Inizio and Fine (time())
def check_schedule(schedule, Ora):
    return schedule.Inizio <= Ora and schedule.Fine >= Ora


# check if the visitor has already a participation in a schedule
def check_partecipate_in_schedule(codicefiscale, schedule):
    for entry in Entry.query.filter_by(CodiceFiscale=codicefiscale).all():
        for partecipate in Participate.query.filter_by(IdIngresso=entry.IdIngresso, IdAttivita=schedule.IdAttivita).all():
            if get_schedule_between_time(partecipate.IdAttivita, entry.Data, partecipate.Ora).IdProgrammazione == schedule.IdProgrammazione:
                return True
    return False



# return the number of partecipates in a schedule checking the range of Inizio<<Fine
def get_partecipates_in_schedule(schedule):
    count = 0
    for partecipate in Participate.query.filter_by(IdAttivita=schedule.IdAttivita).all():
        if check_schedule(schedule, partecipate.Ora):
            count+=1
    return count


# check if the visitor respect the limit
def apply_constraint(visitor, limit, data_partecipazione):
    if limit.Attributo == 'DataDiNascita':
        age = (data_partecipazione - visitor.DataDiNascita).days // 365.25
        return f'SELECT * FROM VISITATORI WHERE CodiceFiscale = :visitor_codice_fiscale AND {age} {limit.Condizione} :limit_valore'
    return f'SELECT * FROM VISITATORI WHERE CodiceFiscale = :visitor_codice_fiscale AND {limit.Attributo} {limit.Condizione} :limit_valore'
    


# return the visitors CodiceFiscale with entries
def get_visitor_with_entries():
    visitors = []
    for visitor in Visitor.query.all():
        if Entry.query.filter_by(CodiceFiscale=visitor.CodiceFiscale).first():
            visitors.append({'CodiceFiscale': visitor.CodiceFiscale})
    return visitors



# ACTIVITIES

# used to delete the orphan limits, if a limit is not constraint in any activity
def delete_orphan_limits():
    for limit in Limit.query.all():
        if not Constraint.query.filter_by(IdLimite=limit.IdLimite).first():
            db.session.delete(limit)
            db.session.commit()


# check if the category is not present in Activity table, Include and Require, then delete it 
def delete_orphan_categories():
    for category in Category.query.all():   
        if not Activity.query.filter_by(IdCategoria=category.IdCategoria).first() and not Include.query.filter_by(IdCategoria=category.IdCategoria).first() and not Require.query.filter_by(IdCategoria=category.IdCategoria).first():
            db.session.delete(category)
            db.session.commit()


def get_ride_limits(id_attivita):
    dict_limits = []
    for constraint in Constraint.query.filter_by(IdAttivita=id_attivita).all():
        dict_limits.append(Limit.query.get(constraint.IdLimite))
    return dict_limits


def get_categories_tariffs(id_categoria):
    dict_tariffs = []
    for include in Include.query.filter_by(IdCategoria=id_categoria).all():
        dict_tariffs.append(Tariff.query.get(include.IdTariffa))
    return dict_tariffs


def dict_schedules(id_attivita):
    dict_schedules = []
    for schedule in Schedule.query.filter_by(IdAttivita=id_attivita).all():
        dict_schedule = {
            'IdProgrammazione': schedule.IdProgrammazione,
            'Data': schedule.Data,
            'Inizio': str(schedule.Inizio),
            'Fine': str(schedule.Fine)
        }
        dict_schedules.append(dict_schedule)
    return dict_schedules


# delete schedules if the today's date is greater than the schedule's date
def delete_expired_schedules():
    for schedule in Schedule.query.all():
        if schedule.Data < datetime.now().date():
            db.session.delete(schedule)
            db.session.commit()
    


# SERVICES

# dictionary of a service with his timetable
def dict_service(service):
    service_dict = {
                'Nome': service.Nome,
                'Tipo': service.Tipo,
                'Orario': Timetable.query.filter_by(IdOrario=service.IdOrario).first()
            }
    return service_dict

# dictionary of all the services
def dict_services(services):
    return [dict_service(service) for service in services]


# EMPLOYEES

# return the requires of a role
def get_require(IdRuolo):
    requires = []
    for require in Require.query.filter_by(IdRuolo=IdRuolo).all():
        dict_require = {
            'NomeCategoria': Category.query.filter_by(IdCategoria=require.IdCategoria).first().Nome,
            'Quantita': require.Quantita
        }
        requires.append(dict_require)
    return requires 