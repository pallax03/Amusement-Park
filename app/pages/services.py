from flask import render_template, url_for, request, jsonify, make_response
from datetime import datetime, timedelta
from models import Service, Timetable


def service(app, db):
    @app.route('/services', methods=['GET'])
    def page_services():
        return render_template('services.j2', services=Service.query.all(),
                                url_for_add_service=url_for('add_service'),
                                url_for_get_timetables=url_for('get_timetable'))
    
#APIs
    # get all the services
    @app.route('/api/services', methods=['GET'])
    def get_services():
        return make_response(jsonify(Service.query.all()), 200)

    # get a service
    # /service + '?Nome=nomeservizio'
    @app.route('/api/service', methods=['GET'])
    def get_service():
        try:
            service = Service.query.filter_by(Nome=request.args.get('Nome')).first()
            return make_response(jsonify(service), 200)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 400)
        
    # add a service
    # /service + new json of Service
    @app.route('/api/service', methods=['POST'])
    def add_service():
        try:
            data = request.get_json()
            service = Service(
                Nome=data['Nome'],
                Tipo=data['Tipo'],
                IdOrario=data['IdOrario']
            )
            db.session.add(service)
            db.session.commit()
            return make_response(jsonify({'message': 'Servizio creato'}), 201)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 400)
        
    # delete a service
    # /service + '?Nome=nomeservizio'
    @app.route('/api/service', methods=['DELETE'])
    def delete_service():
        try:
            service = Service.query.filter_by(Nome=request.args.get('Nome')).first()
            db.session.delete(service)
            db.session.commit()
            return make_response(jsonify({'message': 'Servizio eliminato'}), 200)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 400)
    
    # get all services types
    @app.route('/api/services/types', methods=['GET'])
    def get_services_types():
        types = []
        for type in Service.query.with_entities(Service.Tipo).distinct().all():
            types.append(type)
        return make_response(types, 200)

    # get timetable of the service
    # /service/timetable + '?Nome=nomeservizio'
    @app.route('/api/service/timetable', methods=['GET'])
    def get_timetable():
        try:
            service = Service.query.filter_by(Nome=request.args.get('Nome')).first()
            timetable = Timetable.query.filter_by(IdOrario=service.IdOrario).first()
            return make_response(jsonify(timetable), 200)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 400)

