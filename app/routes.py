from flask import render_template, url_for, flash, redirect, request, jsonify, make_response, session, Blueprint
from models import *


def visitor(app, db):
    @app.route('/visitor', methods=['GET'])
    def get_visitor():
        try:
            visitor = Visitor.query.filter_by(CodiceFiscale=request.args.get('CodiceFiscale')).first()
            return make_response(jsonify(visitor), 200)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 400)

    @app.route('/visitor', methods=['POST'])
    def add_visitor():
        try:
            data = request.get_json()
            visitor = Visitor(
                CodiceFiscale=data['CodiceFiscale'],
                Nome=data['Nome'],
                Cognome=data['Cognome'],
                DataDiNascita=data['DataDiNascita'],
                Altezza=data['Altezza'],
                Peso=data['Peso']
            )
            db.session.add(visitor)
            db.session.commit()
            return make_response(jsonify({'message': 'visitatore creato'}), 201)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 400)
        
    @app.route('/visitors', methods=['GET'])
    def get_visitors():
        return render_template('visitors.html', visitors=Visitor.query.all())
    

def subscription(app, db):
    @app.route('/subscription', methods=['GET'])
    def get_avaible_subscriptions():
        return render_template('subscriptions.html', durations=Duration.query.all(), tariffs=Tariff.query.all())

    @app.route('/subscription/cost', methods=['GET'])
    def get_subscription_cost():
        duration = request.args.get('Duration')
        tariff = request.args.get('Tariff')
        duration = Duration.query.filter_by(Giorni=duration).first()
        tariff = Tariff.query.filter_by(Nome=tariff).first()
        return make_response(jsonify({'Costo': duration.Giorni * tariff.CostoGiornaliero * duration.Sconto}), 200)


    @app.route('/subscription/duration', methods=['GET'])
    def get_durations():
        return make_response(jsonify(Duration.query.all()), 200)

    @app.route('/subscription/duration', methods=['POST'])
    def add_duration():
        try:
            data = request.get_json()
            duration = Duration(
                Giorni=data['Giorni'],
                Sconto=data['Sconto'],
                Descrizione=data['Descrizione']
            )
            db.session.add(duration)
            db.session.commit()
            return make_response(jsonify({'message': 'Durata creata'}), 201)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 400)
        
    @app.route('/subscription/tariff', methods=['GET'])
    def get_tariffs():
        return make_response(jsonify(Tariff.query.all()), 200)
    
    @app.route('/subscription/tariff', methods=['POST'])
    def add_tariff():
        try:
            data = request.get_json()
            tariff = Tariff(
                Nome=data['Nome'],
                CostoGiornaliero=data['CostoGiornaliero']
            )
            db.session.add(tariff)
            db.session.commit()
            return make_response(jsonify({'message': 'Tariffa creata'}), 201)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 400)


# def employee(app, db):
#     @app.route('/employees', methods=['GET'])
#     def get_employees():
#         return render_template('employees.html', visitors=Employee.query.all())
    
#     @app.route('/employee', methods=['POST'])
#     def add_employee():
#         try:
#             data = request.get_json()
#             visitor = Visitor(
#                 CodiceFiscale=data['CodiceFiscale'],
#                 Nome=data['Nome'],
#                 Cognome=data['Cognome'],
#                 DataDiNascita=data['DataDiNascita'],
#                 Altezza=data['Altezza'],
#                 Peso=data['Peso']
#             )
#             db.session.add(visitor)
#             db.session.commit()
#             return make_response(jsonify({'message': 'Visitor created'}), 201)
#         except Exception as e:
#             return make_response(jsonify({'error': str(e)}), 400)
        