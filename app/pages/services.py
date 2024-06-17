from flask import render_template, url_for, request, jsonify, make_response
import urllib.parse
from datetime import datetime, timedelta
from models import Service, Timetable, Employee

def service(app, db):
    @app.route('/services', methods=['GET'])
    def page_services():
        return render_template('services.j2', url_for_get_services=url_for('get_services'),
                                url_for_add_service=url_for('add_service'),
                                url_for_get_services_types=url_for('get_services_types'),
                                url_for_get_timetables=url_for('get_timetable'))
    
#APIs
    # get all the services
    # can be filtered by type
    # /services + '?Tipo=Negozio'
    @app.route('/api/services', methods=['GET'])
    def get_services():
        try:
            if(request.args.get('Tipo') is None):
                return make_response(jsonify(dict_services(Service.query.all())), 200)
            
            return make_response(jsonify(dict_services(Service.query.filter_by(Tipo=request.args.get('Tipo')).all())), 200)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 400)

    # get a service
    # /service + '?Nome=OVS'
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
            for orari in data['Orario']:
                orari = None if orari == '' else orari

            # search if the given Orario already exists
            timetable = Timetable.query.filter_by(Lunedi=data['Orario']['Lunedi'], Martedi=data['Orario']['Martedi'], Mercoledi=data['Orario']['Mercoledi'], Giovedi=data['Orario']['Giovedi'], Venerdi=data['Orario']['Venerdi'], Sabato=data['Orario']['Sabato'], Domenica=data['Orario']['Domenica']).first()
            if timetable is None:
                timetable = Timetable(
                    Lunedi=data['Orario']['Lunedi'],
                    Martedi=data['Orario']['Martedi'],
                    Mercoledi=data['Orario']['Mercoledi'],
                    Giovedi=data['Orario']['Giovedi'],
                    Venerdi=data['Orario']['Venerdi'],
                    Sabato=data['Orario']['Sabato'],
                    Domenica=data['Orario']['Domenica']
                )
                db.session.add(timetable)
                db.session.commit()
            else:
                timetable = timetable.IdOrario

            service = Service(
                Nome=data['Nome'],
                Tipo=data['Tipo'],
                IdOrario=timetable
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
            
            service = Service.query.filter_by(Nome=urllib.parse.unquote(request.args.get('Nome'))).first()
            # before deleting the service, modify the people that are assigned to it
            for employee in Employee.query.filter_by(IdServizio=service.IdServizio).all():
                employee.IdServizio = None
            db.session.commit()
            
            db.session.delete(service)
            db.session.commit()
            return make_response(jsonify({'message': 'Servizio eliminato'}), 200)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 400)
    
    # get all services types
    @app.route('/api/services/types', methods=['GET'])
    def get_services_types():
        dict = []
        for tmp in Service.query.with_entities(Service.Tipo).distinct().all():
            dict.append(tmp.Tipo)
        
        return make_response(jsonify(dict), 200)

    # get timetable of the service
    # /service/timetable + '?Nome=nomeservizio'
    @app.route('/api/service/timetable', methods=['GET'])
    def get_timetable():
        try:
            # service = Service.query.filter_by(Nome=request.args.get('Nome')).first()
            # timetable = Timetable.query.filter_by(IdOrario=service.IdOrario).first()
            timetable = Timetable.query.all()
            return make_response(jsonify(timetable), 200)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 400)

    # add a timetable
    # /service/timetable + new json of Timetable
    @app.route('/api/service/timetable', methods=['POST'])
    def add_timetable():
        try:
            data = request.get_json()
            timetable = Timetable(
                Lunedi=data['Lunedi'],
                Martedi=data['Martedi'],
                Mercoledi=data['Mercoledi'],
                Giovedi=data['Giovedi'],
                Venerdi=data['Venerdi'],
                Sabato=data['Sabato'],
                Domenica=data['Domenica']
            )
            db.session.add(timetable)
            db.session.commit()
            return make_response(jsonify({'message': 'Orario creato'}), 201)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 400)
        
def dict_service(service):
    service_dict = {
                'Nome': service.Nome,
                'Tipo': service.Tipo,
                'Orario': Timetable.query.filter_by(IdOrario=service.IdOrario).first()
            }
    return service_dict

def dict_services(services):
    return [dict_service(service) for service in services]