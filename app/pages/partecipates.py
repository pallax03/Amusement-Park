from flask import render_template, url_for, request, jsonify, make_response
from datetime import datetime
from models import Participate, Entry, Activity, Include, Category, Tariff, Visitor, Limit, Constraint, Schedule
from sqlalchemy import text

from utilities import get_visitor_with_entries, get_schedule_between_time, count_partecipates_in_schedule, check_partecipate_in_schedule, check_active_subscription, apply_constraint, count_partecipates_in_ride

def partecipates(app, db):
    # return the partecipates
    # can be specified the visitor and the date, so an entry
    # the main table can be also filtered by the activity
    # /partecipates + '?CodiceFiscale=MNNGPP99A01H501A&DataIngresso=2021-01-01'
    @app.route('/partecipates', methods=['GET'])
    def page_partecipates():
        try:
            return render_template('partecipates.j2', visitors=get_visitor_with_entries(),
                                   url_for_get_entries=url_for('get_entries'),
                                   url_for_get_partecipates=url_for('get_partecipates'),
                                   url_for_get_activities=url_for('get_activities'),
                                   url_for_add_partecipate=url_for('add_partecipate'))
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 400)

# APIs
   
    # get all the partecipations of a visitor's entry
    # can be filtered by the activity
    # /api/partecipates + '?CodiceFiscale=MNNGPP99A01H501A&DataIngresso=2021-01-01'
    @app.route('/api/partecipates', methods=['GET'])
    def get_partecipates():
        try:
            codicefiscale = request.args.get('CodiceFiscale')
            dataingresso = request.args.get('DataIngresso')
            partecipates = []
            for entry in Entry.query.filter_by(CodiceFiscale=codicefiscale, Data=dataingresso).all():
                for partecipate in Participate.query.filter_by(IdIngresso=entry.IdIngresso).all():
                    activity = Activity.query.filter_by(IdAttivita=partecipate.IdAttivita).first()
                    partecipates.append({
                        'IdIngresso': partecipate.IdIngresso,
                        'Ora': partecipate.Ora.strftime("%H:%M"),
                        'Attivita': activity,
                        'PostiOccupati': count_partecipates_in_schedule(get_schedule_between_time(activity.IdAttivita, entry.Data, partecipate.Ora)) if bool(activity.IsEvent) else count_partecipates_in_ride(activity.IdAttivita, entry.Data, partecipate.Ora)
                    })
            return make_response(jsonify(partecipates), 200)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 400)


    # add a partecipate
    # /api/partecipate + json
    # vincoli inespressi:
    #   - posti massimi non raggiunti
    #  NELLE ATTRAZIONI:
    #   - controllare bene prima la tabella vincoli 
    #   - tariffa dell’abbonamento, ha inclusa quella categoria
    @app.route('/api/partecipate', methods=['POST'])
    def add_partecipate():
        try:
            dict_partecipate = {}
            data = request.get_json()
            # # check if the visitor has an entry
            entry = Entry.query.filter_by(CodiceFiscale=data['CodiceFiscale'], Data=data['DataIngresso']).first()
            if not entry:
                return make_response(jsonify({'error': 'Ingresso non presente'}), 400)
            
            data_partecipazione = datetime.strptime(data['DataIngresso'], "%Y-%m-%d").date()
            ora_partecipazione = datetime.strptime(data['Ora'], "%H:%M").time()
            
            # check if is an event or a ride
            activity = Activity.query.filter_by(IdAttivita=int(data['IdAttivita'])).first() 
            if bool(activity.IsEvent):
                # check if the Posti are full in the schedule, Ora must be in range from the start to the end
                schedule = get_schedule_between_time(int(data['IdAttivita']), data_partecipazione, ora_partecipazione)
                if not schedule:
                    return make_response(jsonify({'error': 'Evento non progrmmato in quell\'orario'}), 400)
                else:
                    if check_partecipate_in_schedule(data['CodiceFiscale'], schedule):
                        return make_response(jsonify({'error': 'Partecipazione all\'evento già presente'}), 400)
                    if count_partecipates_in_schedule(schedule) >= activity.Posti:
                        return make_response(jsonify({'error': 'Posti esauriti'}), 400)
            else:
                # check if the Posti are full in the Ora of other partecipations at the same IdAttivita
                if count_partecipates_in_ride(activity.IdAttivita, data_partecipazione, ora_partecipazione) >= activity.Posti:
                    return make_response(jsonify({'error': 'Posti esauriti'}), 400)
            
                # check if the visitor has the right tariff subscription, include
                if not Include.query.filter_by(IdCategoria=Category.query.filter_by(IdCategoria=activity.IdCategoria).first().IdCategoria, IdTariffa=Tariff.query.filter_by(NomeTariffa=check_active_subscription(data['CodiceFiscale'], data_partecipazione).NomeTariffa).first().IdTariffa).first():
                    return make_response(jsonify({'error': 'Abbonamento non include la tariffa richiesta'}), 400)
                
                # check if the visitor has the right constraints
                visitor = Visitor.query.filter_by(CodiceFiscale=data['CodiceFiscale']).first()
                for constraint in Constraint.query.filter_by(IdAttivita=int(data['IdAttivita'])).all():
                    limit = Limit.query.filter_by(IdLimite=constraint.IdLimite).first()
                    if not db.engine.execute(text(apply_constraint(visitor, limit, data_partecipazione)), visitor_codice_fiscale=visitor.CodiceFiscale, limit_valore=limit.Valore).fetchone():
                        return make_response(jsonify({'error': f'Vincolo {limit.Attributo} {limit.Condizione} {limit.Valore} non rispettato'}), 400)
            
            partecipate = Participate(IdIngresso=entry.IdIngresso, IdAttivita=data['IdAttivita'], Ora=ora_partecipazione)
            db.session.add(partecipate)
            db.session.commit()
            return make_response(jsonify({'message': f'Partecipazione di {entry.CodiceFiscale} il {data_partecipazione},a {activity.Nome} inserita'}), 200)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 400)
        
    # delete a partecipate
    # /api/partecipate + '?IdIngresso=1&Ora=10:00'
    @app.route('/api/partecipate', methods=['DELETE'])
    def delete_partecipate():
        try:
            partecipate = Participate.query.filter_by(IdIngresso=request.args.get('IdIngresso'), Ora=request.args.get('Ora')).first()
            if partecipate:
                db.session.delete(partecipate)
                db.session.commit()
                return make_response(jsonify({'message': f'Partecipazione eliminata'}), 200)
            else:
                return make_response(jsonify({'error': 'Partecipazione non trovata'}), 404)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 400)

