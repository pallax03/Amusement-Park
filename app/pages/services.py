from flask import render_template, url_for, request, jsonify, make_response
from datetime import datetime, timedelta
from models import Service, Timetable


def service(app, db):
    @app.route('/services', methods=['GET'])
    def get_services():
        return render_template('services.j2', services=Service.query.all(),
                                url_for_add_service=url_for('add_service'),
                                url_for_get_timetables=url_for('get_timetables'))
    
    @app.route('/service', methods=['GET'])
    def get_service():
        try:
            service = Service.query.filter_by(IdServizio=request.args.get('IdServizio')).first()
            return make_response(jsonify(service), 200)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 400)