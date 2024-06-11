from flask import render_template, url_for, request, make_response, jsonify
import json
from datetime import datetime, timedelta
from models import Activity, Category, Limit, Constraint

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
    # /api/activity/rides + '?IdCategoria=1&NomeTariffa=Giornaliero'
    @app.route('/api/activity/rides', methods=['GET'])
    def get_rides():
        try:
            activities = Activity.query.filter_by(IsEvent=False).all()

            if request.args.get('IdCategoria') != None:
                activities = [activity for activity in activities if activity.IdCategoria == int(request.args.get('IdCategoria'))]
            if request.args.get('NomeTariffa') != None:
                activities = [activity for activity in activities if request.args.get('NomeTariffa') in [include.Category.Nome for include in activity.tariffs]]
            return make_response(jsonify(activities), 200)
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