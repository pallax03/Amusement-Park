from flask import render_template, url_for, request, make_response, jsonify
import json
from datetime import datetime, timedelta
from models import Activity, Category

def activity(app, db):
    @app.route('/activities', methods=['GET'])
    def page_activities():
        return render_template('activities.j2', categories=get_categories().json, 
                                url_for_get_categories=url_for('get_categories'),
                                url_for_get_activities=url_for('get_activities'),
                                url_for_get_events=url_for('get_events'),
                                url_for_add_activity=url_for('add_activity'))

    @app.route('/activity', methods=['POST'])
    def add_activity():
        try:
            data = request.get_json()
            activity = Activity(
                Nome=data['Nome'],
                Descrizione=data['Descrizione'],
                Categoria=data['Categoria'],
                IsEvent=data['IsEvent']
            )
            db.session.add(activity)
            db.session.commit()
            return make_response(jsonify({'message': 'Attività creata'}), 201)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 400)

    @app.route('/activity/rides', methods=['GET'])
    def get_activities():
        return make_response(jsonify(Activity.query.filter_by(IsEvent=False).all()), 200)

    @app.route('/activity/rides/categories', methods=['GET'])
    def get_categories():
        return make_response(jsonify(Category.query.all()), 200)
    
    @app.route('/activity/rides/categories', methods=['POST'])
    def add_category():
        try:
            data = request.get_json()
            category = Category(
                Nome=data['Nome'],
                Descrizione=data['Descrizione']
            )
            db.session.add(category)
            db.session.commit()
            return make_response(jsonify({'message': 'Categoria creata'}), 201)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 400)

    @app.route('/activity/events', methods=['GET'])
    def get_events():
        return make_response(jsonify(Activity.query.filter_by(IsEvent=True).all()), 200)