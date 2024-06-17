from flask import render_template, url_for, request, jsonify, make_response
from datetime import datetime
from models import Participate, Entry, Activity, Include, Category, Tariff

from utilities import get_visitor_with_entries, get_schedule_between_time, get_partecipates_in_schedule, check_active_subscription

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
                    partecipates.append({
                        'IdIngresso': partecipate.IdIngresso,
                        'Ora': str(partecipate.Ora),
                        'Attivita': Activity.query.filter_by(IdAttivita=partecipate.IdAttivita).first(),
                        'PostiOccupati': Participate.query.filter_by(IdAttivita=partecipate.IdAttivita, Ora=partecipate.Ora).count()
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
            if not Entry.query.filter_by(CodiceFiscale=data['CodiceFiscale'], Data=data['DataIngresso']).first():
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
                    if get_partecipates_in_schedule(schedule) >= activity.Posti:
                        return make_response(jsonify({'error': 'Posti esauriti'}), 400)
            else:
                # check if the Posti are full in the Ora of other partecipations at the same IdAttivita
                if Participate.query.filter_by(IdAttivita=int(data['IdAttivita']), Ora=ora_partecipazione).count() >= activity.Posti:
                    return make_response(jsonify({'error': 'Posti esauriti'}), 400)
            
                # check if the visitor has the right tariff subscription, include
                if not Include.query.filter_by(IdCategoria=Category.query.filter_by(IdCategoria=activity.IdCategoria).first().IdCategoria, IdTariffa=Tariff.query.filter_by(NomeTariffa=check_active_subscription(data['CodiceFiscale'], data_partecipazione).NomeTariffa).first().IdTariffa).first():
                    return make_response(jsonify({'error': 'Abbonamento non include la tariffa richiesta'}), 400)
                
                # check if the visitor has the right constraints
                # for constraint in Constraint.query.filter_by(IdAttivita=int(data['IdAttivita'])).all():
                #     if not constraint.check_constraint(data['CodiceFiscale']):
                #         return make_response(jsonify({'error': 'Vincolo non rispettato'}), 400)
            return make_response(jsonify({'message': 'Tutto OK!!'}), 200)

            # partecipate = Participate(IdIngresso=data['IdIngresso'], IdAttivita=data['IdAttivita'], Ora=data['Ora'])
            # db.session.add(partecipate)
            # db.session.commit()
            # return make_response(jsonify({'message': 'Partecipate added'}), 200)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 400)