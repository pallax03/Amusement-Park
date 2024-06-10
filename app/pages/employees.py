from flask import render_template, url_for, request, jsonify, make_response
from datetime import datetime, timedelta
from models import Employee, Role, Require, Service, Category

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
                dict_employee['Servizio'] = True if get_require(employee.IdRuolo) == [] else False
            else:
                service = Service.query.filter_by(IdServizio=employee.IdServizio).first()
                dict_employee['Servizio'] = service.Nome
            employees.append(dict_employee)

        return render_template('employees.j2', employees=employees, services=Service.query.all(),
                                url_for_add_employee=url_for('add_employee'),
                                url_for_get_roles=url_for('get_roles'),
                                url_for_delete_role=url_for('delete_role'),
                                url_for_get_categories=url_for('get_categories'),
                                url_for_add_employee_service=url_for('add_employee_service'))

# APIs

    # add a employee and if the role is not present, add it
    # /employee + new json of Employee
    @app.route('/api/employee', methods=['POST'])
    def add_employee():
        try:
            data = request.get_json()

            if Role.query.filter_by(Nome=data['Ruolo']['Nome']).first() == None:
                role = Role(Nome=data['Ruolo']['Nome'], Stipendio=data['Ruolo']['Stipendio'])
                db.session.add(role)
                db.session.commit()

                for require in data['Ruolo']['Requires']:
                    require = Require(IdRuolo=role.IdRuolo, IdCategoria=Category.query.filter_by(Nome=require['NomeCategoria']).first().IdCategoria, Quantita=require['Quantita'])
                    db.session.add(require)
                    db.session.commit()

            role = Role.query.filter_by(Nome=data['Ruolo']['Nome']).first()
            employee = Employee(
                CodiceFiscale=data['CodiceFiscale'],
                Nome=data['Nome'],
                Cognome=data['Cognome'],
                DataDiNascita=data['DataNascita'],
                IdRuolo=role.IdRuolo
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
        dict_roles = []
        for role in Role.query.all():
            dict_roles.append({'IdRuolo': role.IdRuolo, 
                               'Nome': role.Nome, 
                               'Stipendio': role.Stipendio,
                               'Requires': get_require(role.IdRuolo)})
        return make_response(jsonify(dict_roles), 200)

    # delete a role
    # /employee/role + '?IdRuolo=1'
    @app.route('/api/employee/role', methods=['DELETE'])
    def delete_role():
        try:
            role = Role.query.filter_by(IdRuolo=request.args.get('IdRuolo')).first()
            if role:
                # before deleting the role, delete all the requires
                for require in Require.query.filter_by(IdRuolo=role.IdRuolo).all():
                    db.session.delete(require)
                db.session.delete(role)
                db.session.commit()
                return make_response(jsonify({'message': 'Ruolo eliminato'}), 200)
            else:
                return make_response(jsonify({'error': 'Ruolo non trovato'}), 404)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 400)

    # add a service to a employee, the service can be None
    # /employee/service + '?CodiceFiscale=RSSMRA85M01H501Z&IdServizio=1'
    @app.route('/api/employee/service', methods=['POST'])
    def add_employee_service():
        try:
            employee = Employee.query.filter_by(CodiceFiscale=request.args.get('CodiceFiscale')).first()
            service = Service.query.filter_by(IdServizio=request.args.get('IdServizio')).first()

            if employee:
                employee.IdServizio = None if request.args.get('IdServizio') == '' or request.args.get('IdServizio') == None else service.IdServizio
                db.session.commit()
                return make_response(jsonify({'message': 'Servizio assegnato'}), 200)
            else:
                return make_response(jsonify({'error': 'Dipendente o servizio non trovato'}), 404)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 400)

    def get_require(IdRuolo):
        requires = []
        for require in Require.query.filter_by(IdRuolo=IdRuolo).all():
            dict_require = {
                'NomeCategoria': Category.query.filter_by(IdCategoria=require.IdCategoria).first().Nome,
                'Quantita': require.Quantita
            }
            requires.append(dict_require)
        return requires 