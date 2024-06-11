from flask import render_template, url_for, request, make_response, jsonify
import json
from datetime import datetime, timedelta
from models import Activity, Category, Limit, Constraint, Include, Tariff

def activity(app, db):
    @app.route('/activities', methods=['GET'])
    def page_activities():
        return render_template('activities.j2',
                                url_for_get_events=url_for('get_events'),
                                url_for_get_rides=url_for('get_rides'),
                                url_for_get_categories=url_for('get_categories'),
                                url_for_get_tariffs=url_for('get_tariffs'),
                                url_for_get_limits=url_for('get_limits'))

#APIs

    # get all the events
    # /api/activity/events
    @app.route('/api/activity/events', methods=['GET'])
    def get_events():
        try:
            return make_response(jsonify(Activity.query.filter_by(IsEvent=True).all()), 200)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 400)
        
    # add a new event
    # /api/activity/events + json
    @app.route('/api/activity/events', methods=['POST'])
    def add_event():
        try:
            data = request.get_json()
            new_event = Activity(Nome=data['Nome'], Descrizione=data['Descrizione'], Posti=data['Posti'], IsEvent=True)
            db.session.add(new_event)
            db.session.commit()
            return make_response(jsonify({'message': f"evento {new_event.Nome} aggiunto"}), 200)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 400)

    # # delete a event
    # # /api/activity/events/<int:id> + json
    # @app.route('/api/activity/events/<int:id>', methods=['DELETE'])
    # def delete_event(id):
    #     try:
    #         event = Activity.query.get(id)
    #         db.session.delete(event)
    #         db.session.commit()
    #         return make_response(jsonify({'message': 'Event deleted'}), 200)
    #     except Exception as e:
    #         return make_response(jsonify({'error': str(e)}), 400)

    # delete a event
    # /api/activity/events + '?IdEvento=1'
    @app.route('/api/activity/events', methods=['DELETE'])
    def delete_event():
        try:
            event = Activity.query.filter_by(IdAttivita=int(request.args.get('IdEvento'))).first()
            db.session.delete(event)
            db.session.commit()
            return make_response(jsonify({'message': f'evento {event.Nome} eliminato'}), 200)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 400)

    # get all the rides, can be filter by category and included tariff
    # /api/activity/rides + '?category=Acqua&limit=1&tariff=Bronze'
    @app.route('/api/activity/rides', methods=['GET'])
    def get_rides():
        try:
            activities = []
            for activity in Activity.query.filter_by(IsEvent=False).all():
                
                dict_activity = {
                    'Nome': activity.Nome,
                    'Descrizione': activity.Descrizione,
                    'Posti': activity.Posti,
                    'NomeCategoria': Category.query.get(activity.IdCategoria).Nome,
                    'Limiti': get_ride_limits(activity.IdAttivita),
                    'Tariffe': get_categories_tariffs(activity.IdCategoria)
                }
                activities.append(dict_activity)

            # filter by selected filters
            if request.args.get('category'):
                activities = [activity for activity in activities if activity['NomeCategoria'] == request.args.get('category')]

            if request.args.get('limit')!='':
                if request.args.get('limit')=='0':
                    # filter activities by Limiti==[]
                    activities = [activity for activity in activities if not activity['Limiti']]
                else:
                    # filter activities by limit IdLimite
                    activities = [activity for activity in activities if int(request.args.get('limit')) in [limit.IdLimite for limit in activity['Limiti']]]    

    
            if request.args.get('tariff'):
                activities = [activity for activity in activities if request.args.get('tariff') in [tariff.NomeTariffa for tariff in activity['Tariffe']]]

            return make_response(jsonify(activities), 200)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 400)

    # TODO
    # add a new ride
    # /api/activity/rides + json
    @app.route('/api/activity/rides', methods=['POST'])
    def add_ride():
        try:
            data = request.get_json()
            new_ride = Activity(Nome=data['Nome'], Descrizione=data['Descrizione'], Posti=data['Posti'], IsEvent=False, IdCategoria=data['IdCategoria'])
            db.session.add(new_ride)
            db.session.commit()
            return make_response(jsonify({'message': f"attrazione {new_ride.Nome} aggiunta"}), 200)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 400)

    # get all the categories
    # /api/activity/rides/categories
    @app.route('/api/activity/rides/categories', methods=['GET']) 
    def get_categories():
        try:
            return make_response(jsonify(Category.query.all()), 200)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 400)
        

    # get all the limits
    # /api/activity/rides/limits
    @app.route('/api/activity/rides/limits', methods=['GET'])
    def get_limits():
        try:
            return make_response(jsonify(Limit.query.all()), 200)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 400)
        

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