from flask import render_template, url_for, request, make_response, jsonify
import json
import urllib.parse
from datetime import datetime, timedelta
from models import Activity, Schedule, Category, Limit, Constraint, Include, Tariff, Require

def activity(app, db):
    @app.route('/activities', methods=['GET'])
    def page_activities():
        return render_template('activities.j2',
                                url_for_get_events=url_for('get_events'),
                                url_for_get_schedules=url_for('get_schedules'),
                                url_for_get_rides=url_for('get_rides'),
                                url_for_get_categories=url_for('get_categories'),
                                url_for_get_tariffs=url_for('get_tariffs'),
                                url_for_get_limits=url_for('get_limits'))

#APIs
    # get all the activities (events and rides).
    # /api/activities 
    @app.route('/api/activities', methods=['GET'])
    def get_activities():
        try:
            activities = Activity.query.all()
            for activity in activities:
                activity.IsEvent = bool(activity.IsEvent)
            return make_response(jsonify(activities), 200)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 400)


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

    # delete a event
    # (if haven't any schedules or if the schedules are expired)
    # /api/activity/events + '?IdEvento=1'
    @app.route('/api/activity/events', methods=['DELETE'])
    def delete_event():
        try:
            delete_expired_schedules()
            event = Activity.query.filter_by(IdAttivita=int(request.args.get('IdAttivita'))).first()
            db.session.delete(event)
            db.session.commit()
            return make_response(jsonify({'message': f'evento {event.Nome} eliminato'}), 200)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 400)


    # get all the schedules for an event
    # /api/activity/events/schedules + '?IdAttivita=1'
    @app.route('/api/activity/events/schedules', methods=['GET'])
    def get_schedules():
        try:
            return make_response(jsonify(dict_schedules(int(request.args.get('IdAttivita')))), 200)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 400)


    # add a schedule for an event
    # /api/activity/events/schedules + json
    @app.route('/api/activity/events/schedules', methods=['POST'])
    def add_schedule():
        try:
            data = request.get_json()
            data['Inizio'] = datetime.strptime(data['Inizio'], '%H:%M').time()
            data['Fine'] = datetime.strptime(data['Fine'], '%H:%M').time() 
            # if start time is less than end time, swap them
            if data['Fine'] <= data['Inizio']:
                data['Inizio'], data['Fine'] = data['Fine'], data['Inizio']  
            
            new_schedule = Schedule(IdAttivita=data['IdAttivita'], Data=datetime.strptime(data['Data'], '%Y-%m-%d').date(), Inizio=data['Inizio'], Fine=data['Fine'])
            db.session.add(new_schedule)
            db.session.commit()
            return make_response(jsonify({'message': f"Agginuta programmazione {new_schedule.Nome}, il {new_schedule.Data} {new_schedule.Inizio}-{new_schedule.Fine}"}), 200)
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
                    'IdAttivita': activity.IdAttivita,
                    'Nome': activity.Nome,
                    'Descrizione': activity.Descrizione,
                    'Posti': activity.Posti,
                    'NomeCategoria': Category.query.get(activity.IdCategoria).Nome,
                    'Limiti': get_ride_limits(activity.IdAttivita),
                    'Tariffe': get_categories_tariffs(activity.IdCategoria)
                }
                activities.append(dict_activity)

            # filter by selected filters
            category = urllib.parse.unquote(request.args.get('category'))
            if category:
                activities = [activity for activity in activities if activity['NomeCategoria'] == category]

            if request.args.get('limit')!='':
                if request.args.get('limit')=='0':
                    # filter activities by Limiti==[]
                    activities = [activity for activity in activities if not activity['Limiti']]
                else:
                    # filter activities by limit IdLimite
                    activities = [activity for activity in activities if int(request.args.get('limit')) in [limit.IdLimite for limit in activity['Limiti']]]    

            tariff_name = urllib.parse.unquote(request.args.get('tariff'))
            if tariff_name:
                activities = [activity for activity in activities if tariff_name in [tariff.NomeTariffa for tariff in activity['Tariffe']]]

            return make_response(jsonify(activities), 200)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 400)

    # add a new ride 
    # /api/activity/rides + json:
    # {
    #     "Nome": "ride1",
    #     "Descrizione": "ride1",
    #     "Posti": 10,
    #     "Categoria": "nuovacategoria",
    #     "Limiti": [1,2]
    # }
    @app.route('/api/activity/rides', methods=['POST'])
    def add_ride():
        try:
            data = request.get_json()
            new_ride = Activity(Nome=data['Nome'], Descrizione=data['Descrizione'], Posti=data['Posti'], IsEvent=False)
            # if the data['Categoria'] is not in the Category table, add it
            if not Category.query.filter_by(Nome=data['Categoria']).first():
                new_category = Category(Nome=data['Categoria'])
                db.session.add(new_category)
                db.session.commit()
            new_ride.IdCategoria = Category.query.filter_by(Nome=data['Categoria']).first().IdCategoria
            db.session.add(new_ride)
            db.session.commit()
            
            # add the constraints
            for limit in data['Limiti']:
                new_constraint = Constraint(IdAttivita=new_ride.IdAttivita, IdLimite=limit)
                db.session.add(new_constraint)
                db.session.commit()

            return make_response(jsonify({'message': f"attrazione {new_ride.Nome} aggiunta"}), 200)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 400)

    # delete a ride
    # /api/activity/rides + '?IdAttivita=1'
    @app.route('/api/activity/rides', methods=['DELETE'])
    def delete_ride():
        try:
            ride = Activity.query.filter_by(IdAttivita=int(request.args.get('IdAttivita'))).first()
            # delete the constraints
            for constraint in Constraint.query.filter_by(IdAttivita=ride.IdAttivita).all():
                db.session.delete(constraint)
                db.session.commit()

            db.session.delete(ride)
            db.session.commit()

            delete_orphan_limits()
            delete_orphan_categories()

            return make_response(jsonify({'message': f'attrazione {ride.Nome} eliminata'}), 200)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 400)

    # get all the categories
    # /api/activity/rides/categories
    @app.route('/api/activity/rides/categories', methods=['GET']) 
    def get_categories():
        try:
            delete_orphan_categories()
            return make_response(jsonify(Category.query.all()), 200)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 400)
        

    # get all the limits
    # /api/activity/rides/limits
    @app.route('/api/activity/rides/limits', methods=['GET'])
    def get_limits():
        try:
            delete_orphan_limits()
            return make_response(jsonify(Limit.query.all()), 200)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 400)
        
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
    