from flask import render_template, url_for, request, jsonify, make_response
from datetime import datetime, timedelta
from models import Employee, Role, Require, Service

from pages.services import service
from pages.activities import activity

def employee(app, db):
    @app.route('/employees', methods=['GET'])
    def page_employees():
        employees = []
        for employee in Employee.query.all():
            role = Role.query.filter_by(IdRuolo=employee.IdRuolo).first()
            dict_employee = {   'CodiceFiscale': employee.CodiceFiscale,
                                'Nome': employee.Nome,
                                'Cognome': employee.Cognome,
                                'DataDiNascita': employee.DataDiNascita,
                                'Ruolo': role.Nome } 
            if employee.IdServizio == None:
                dict_employee['Servizio'] = check_require(employee.IdRuolo)
            else:
                service = Service.query.filter_by(IdServizio=employee.IdServizio).first()
                dict_employee['Servizio'] = service.Nome
            employees.append(dict_employee)
        return render_template('employees.j2', employees=employees,
                                url_for_add_employee=url_for('add_employee'),
                                url_for_get_roles=url_for('get_roles'),
                                url_for_get_categories=url_for('get_categories'),
                                url_for_check_require=url_for('get_requires'),
                                url_for_get_services=url_for('get_services'))

# APIs

    # get a employee
    # @app.route('/api/employee', methods=['GET'])
    # def get_employee():
    #     try:
    #     except Exception as e:
    #         return make_response(jsonify({'error': str(e)}), 400)

    # add a employee and if the role is not present, add it
    # /employee + new json of Employee
    @app.route('/api/employee', methods=['POST'])
    def add_employee():
        try:
            # {CodiceFiscale: "RSSMRA85M01H501Z", Cognome: "Biondo", DataNascita: "2024-06-07", Nome: "Paolo", Ruolo: {Nome: 'Responsabile alle Attrazioni', Stipendio: '3000'}}
            data = request.get_json()

            role = Role.query.filter_by(Nome=data['Ruolo']['Nome']).first()
            if role == None:
                add_role(Role(Nome=data['Ruolo']['Nome'], Stipendio=data['Ruolo']['Stipendio']))

            role = Role.query.filter_by(Nome=data['Ruolo']['Nome']).first()
            employee = Employee(
                CodiceFiscale=data['CodiceFiscale'],
                Nome=data['Nome'],
                Cognome=data['Cognome'],
                DataDiNascita=data['DataNascita'],
                IdRuolo=role.IdRuolo,
                IdServizio=None
            )
            db.session.add(employee)
            db.session.commit()

            return make_response(jsonify({'message': "Dipendente assunto"}), 201)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 400)

    # delete a employee
    # /employee + '?CodiceFiscale=RSSMRA85M01H501Z'
    @app.route('/api/employee', methods=['DELETE'])
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

    # get all the roles
    @app.route('/api/employee/roles', methods=['GET'])
    def get_roles():
        return make_response(jsonify(Role.query.all()), 200)

    # add a role
    # /employee/role + new json of Role
    @app.route('/api/employee/role', methods=['POST'])
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
    @app.route('/api/employee/role/require', methods=['GET'])
    def get_requires():
        try:
            return make_response(Require.query.filter_by(IdRuolo=request.args.get('IdRuolo')).all() == [], 200)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 400)

    # add a require
    # /employee/role/require + new json of Require
    @app.route('/api/employee/role/require', methods=['POST'])
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


    # check if the Role is present in the Requires
    def check_require(IdRuolo):
        return Require.query.filter_by(IdRuolo=IdRuolo).all() == []