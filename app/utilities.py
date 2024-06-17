# queries for index (stats)
from datetime import datetime, timedelta
from models import *


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

# delete all the subscriptions that are not active anymore
def delete_non_active_subscriptions():
    subscriptions = Subscription.query.all()
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


# return the number of partecipates in a schedule checking the range of Inizio<<Fine
def get_partecipates_in_schedule(schedule):
    count = 0
    for partecipate in Participate.query.filter_by(IdAttivita=schedule.IdAttivita).all():
        if check_schedule(schedule, partecipate.Ora):
            count+=1
    return count


# apply contraints to a visitor
# def apply_constraints(visitor, limit):
#     return db.session.execute('SELECT * FROM Constraint WHERE CodiceFiscale = :CodiceFiscale AND :limit', {'CodiceFiscale': visitor.CodiceFiscale, 'limit': limit}).fetchall()


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