from flask import render_template, url_for, request, jsonify, make_response
from datetime import datetime, timedelta
from models import Employee, Role, Category, Require, Service

from pages.services import service

def employee(app, db):
    @app.route('/employees', methods=['GET'])
    def page_employees():
        employees = []
        for employee in Employee.query.all():
            role = Role.query.filter_by(IdRuolo=employee.IdRuolo).first()
            employees.append({  'CodiceFiscale': employee.CodiceFiscale,
                                    'Nome': employee.Nome,
                                    'Cognome': employee.Cognome,
                                    'DataDiNascita': employee.DataDiNascita,
                                    'Ruolo': role.Nome,
                                    'Servizio': Service.query.filter_by(IdServizio=employee.IdServizio).first().Nome if employee.IdServizio != None else None })
        return render_template('employees.j2', employees=employees,
                                url_for_add_employee=url_for('add_employee'),
                                url_for_get_roles=url_for('get_roles'),
                                url_for_check_require=url_for('get_requires'),
                                url_for_get_services=url_for('get_services'))

    @app.route('/employee', methods=['GET'])
    def get_employee():
        try:
            employee = Employee.query.filter_by(CodiceFiscale=request.args.get('CodiceFiscale')).first()
            return make_response(jsonify(employee), 200)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 400)

    @app.route('/employee', methods=['POST'])
    def add_employee():
        try:
            data = request.get_json()

            role = Role.query.filter_by(Nome=data['Ruolo']['Nome']).first()
            if(role == None):
                role = Role(Nome=data['Ruolo']['Nome'], Stipendio=data['Ruolo']['Stipendio'])
                db.session.add(role)
                db.session.commit()
                role = Role.query.filter_by(Nome=data['Ruolo']['Nome']).first()
            
            employee = Employee(CodiceFiscale=data['CodiceFiscale'],
                                    Nome=data['Nome'],
                                    Cognome=data['Cognome'],
                                    DataDiNascita=data['DataNascita'],
                                    IdRuolo=role.IdRuolo)

            db.session.add(employee)
            db.session.commit()
            return make_response(jsonify({'message': "Dipendente assunto"}), 201)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 400)

    @app.route('/employee', methods=['DELETE'])
    def delete_employee():
        try:
            employee = Employee.query.filter_by(CodiceFiscale=request.args.get('CodiceFiscale')).first()
            if employee:
                db.session.delete(employee)
                db.session.commit()
                return make_response(jsonify({'message': 'Dipendente licenziato'}), 200)
            else:
                return make_response(jsonify({'error': 'Dipendente non trovato'}), 404)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 400)

    @app.route('/employee/roles', methods=['GET'])
    def get_roles():
        return make_response(jsonify(Role.query.all()), 200)

    @app.route('/employee/role', methods=['POST'])
    def add_role():
        try:
            data = request.get_json()
            role = Role(
                Nome=data['Nome'],
                Stipendio=data['Stipendio']
            )
            db.session.add(role)
            db.session.commit()
            return make_response(jsonify({'message': 'Ruolo creato'}), 201)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 400)

    # given a role, return if it can be assigned to a service
    @app.route('/employee/role/require', methods=['GET'])
    def get_requires():
        try:
            return make_response(Require.query.filter_by(IdRuolo=request.args.get('IdRuolo')).all() == [], 200)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 400)

    @app.route('/employee/role/require', methods=['POST'])
    def add_require():
        try:
            data = request.get_json()
            require = Require(
                IdRuolo=data['IdRuolo'],
                IdCategoria=data['IdCategoria']
            )
            db.session.add(require)
            db.session.commit()
            return make_response(jsonify({'message': 'Requisito creato'}), 201)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 400)
