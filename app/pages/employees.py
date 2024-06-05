from flask import render_template, url_for, request, jsonify, make_response
from datetime import datetime, timedelta
from models import Employee, Role, Category, Require


def employee(app, db):
    @app.route('/employees', methods=['GET'])
    def get_employees():
        employees = Employee.query.all()
        for employee in employees:
            employee.role = Role.query.filter_by(IdRuolo=employee.IdRuolo).first()
        return render_template('employees.j2', employees=employees,
                                url_for_add_employee=url_for('add_employee'),
                                url_for_get_roles=url_for('get_roles'),
                                url_for_get_services=url_for('get_services'),
                                url_for_get_activities=url_for('get_activities'))
    
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
            employee = Employee(
                CodiceFiscale=data['CodiceFiscale'],
                Nome=data['Nome'],
                Cognome=data['Cognome'],
                DataDiNascita=data['DataDiNascita'],
                IdRuolo=data['IdRuolo']
            )
            db.session.add(employee)
            db.session.commit()
            return make_response(jsonify({'message': 'Dipendente creato'}), 201)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 400)
        
    @app.route('/employee', methods=['DELETE'])
    def delete_employee():
        try:
            employee = Employee.query.filter_by(CodiceFiscale=request.args.get('CodiceFiscale')).first()
            if employee:
                db.session.delete(employee)
                db.session.commit()
                return make_response(jsonify({'message': 'Dipendente eliminato'}), 200)
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
                IdRuolo=data['IdRuolo'],
                NomeRuolo=data['NomeRuolo']
            )
            db.session.add(role)
            db.session.commit()
            return make_response(jsonify({'message': 'Ruolo creato'}), 201)
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