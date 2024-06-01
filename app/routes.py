from flask import render_template, url_for, flash, redirect, request, jsonify, make_response, session, Blueprint
# from models import *
# from datetime import datetime, timedelta

# from queries import *

from pages.visitors import visitor
from pages.subscriptions import subscription
# from pages.employees import *

def routes(app, db):
    @app.route('/')
    def index():
        return render_template('index.html')
    
    #models routes
    visitor(app, db)
    subscription(app, db)
    # employee(app, db)



# # SUBSCRIPTION
# def subscription(app, db):
#     @app.route('/subscriptions', methods=['GET'])
#     def get_avaible_subscriptions():
#         return render_template('subscriptions.html', durations=Duration.query.all(), tariffs=Tariff.query.all())


#     # @app.route('/subscription/cost', methods=['GET'])
#     # def get_subscription_cost():
#     #     duration = request.args.get('Duration')
#     #     tariff = request.args.get('Tariff')
#     #     duration = Duration.query.filter_by(Giorni=duration).first()
#     #     tariff = Tariff.query.filter_by(Nome=tariff).first()
#     #     return make_response(jsonify({'Costo': duration.Giorni * tariff.CostoGiornaliero * duration.Sconto}), 200)


#     @app.route('/subscription', methods=['GET'])
#     def get_active_subscription():
#         try:
#             subscriptions = Subscription.query.filter_by(CodiceFiscale=request.args.get('CodiceFiscale')).all()
#             for subscription in subscriptions:
#                 active = Subscription.query.filter_by(CodiceFiscale=subscription.CodiceFiscale).filter(datetime.strptime(str(subscription.DataInizio),'%Y-%m-%d') + timedelta(days=float(subscription.Giorni)) > datetime.now()).first()
#             return make_response(jsonify(active), 200)
#         except Exception as e:
#             return make_response(jsonify({'error': str(e)}), 400)

#     @app.route('/subscription', methods=['POST'])
#     def add_subscription():
#         try:
#             data = request.get_json()
#             subscription = Subscription(
#                 CodiceFiscale=data['CodiceFiscale'],
#                 DataInizio=data['DataInizio'],
#                 Costo=data['Costo'],
#                 NomeTariffa=data['NomeTariffa'],
#                 Giorni=data['Giorni']
#             )
#             db.session.add(subscription)
#             db.session.commit()
#             return make_response(jsonify({'message': 'Abbonamento creato'}), 201)
#         except Exception as e:
#             return make_response(jsonify({'error': str(e)}), 400)

#     @app.route('/subscription/duration', methods=['GET'])
#     def get_durations():
#         return make_response(jsonify(Duration.query.all()), 200)

#     @app.route('/subscription/duration', methods=['POST'])
#     def add_duration():
#         try:
#             data = request.get_json()
#             duration = Duration(
#                 Giorni=data['Giorni'],
#                 Sconto=data['Sconto'],
#                 Descrizione=data['Descrizione']
#             )
#             db.session.add(duration)
#             db.session.commit()
#             return make_response(jsonify({'message': 'Durata creata'}), 201)
#         except Exception as e:
#             return make_response(jsonify({'error': str(e)}), 400)
        
#     @app.route('/subscription/tariff', methods=['GET'])
#     def get_tariffs():
#         return make_response(jsonify(Tariff.query.all()), 200)
    
#     @app.route('/subscription/tariff', methods=['POST'])
#     def add_tariff():
#         try:
#             data = request.get_json()
#             tariff = Tariff(
#                 NomeTariffa=data['NomeTariffa'],
#                 CostoGiornaliero=data['CostoGiornaliero']
#             )
#             db.session.add(tariff)
#             db.session.commit()
#             return make_response(jsonify({'message': 'Tariffa creata'}), 201)
#         except Exception as e:
#             return make_response(jsonify({'error': str(e)}), 400)


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
        