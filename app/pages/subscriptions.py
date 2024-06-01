from flask import render_template, url_for, request, make_response, jsonify
from datetime import datetime, timedelta
from models import Subscription, Duration, Tariff

# SUBSCRIPTION
def subscription(app, db):
    @app.route('/subscriptions', methods=['GET'])
    def get_avaible_subscriptions():
        return render_template('subscriptions.html', durations=Duration.query.all(), tariffs=Tariff.query.all(), 
                               url_for_add_duration=url_for('add_duration'), url_for_add_tariff=url_for('add_tariff'), url_for_cost=url_for('get_subscription_cost'))


    @app.route('/subscription', methods=['GET'])
    def get_active_subscription():
        try:
            subscriptions = Subscription.query.filter_by(CodiceFiscale=request.args.get('CodiceFiscale')).all()
            for subscription in subscriptions:
                active = Subscription.query.filter_by(CodiceFiscale=subscription.CodiceFiscale).filter(datetime.strptime(str(subscription.DataInizio),'%Y-%m-%d') + timedelta(days=float(subscription.Giorni)) > datetime.now()).first()
            return make_response(jsonify(active), 200)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 400)


    @app.route('/subscription', methods=['POST'])
    def add_subscription():
        try:
            data = request.get_json()
            subscription = Subscription(
                CodiceFiscale=data['CodiceFiscale'],
                DataInizio=data['DataInizio'],
                Costo=data['Costo'],
                NomeTariffa=data['NomeTariffa'],
                Giorni=data['Giorni']
            )
            db.session.add(subscription)
            db.session.commit()
            return make_response(jsonify({'message': 'Abbonamento creato'}), 201)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 400)


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
                NomeTariffa=data['NomeTariffa'],
                CostoGiornaliero=data['CostoGiornaliero']
            )
            db.session.add(tariff)
            db.session.commit()
            return make_response(jsonify({'message': 'Tariffa creata'}), 201)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 400)


    @app.route('/subscription/cost', methods=['GET'])
    def get_subscription_cost():
        try:
            tariff = Tariff.query.filter_by(NomeTariffa=request.args.get('NomeTariffa')).first()
            duration = Duration.query.filter_by(Giorni=request.args.get('Giorni')).first()
            return make_response(jsonify({'Costo': tariff.CostoGiornaliero * duration.Giorni * duration.Sconto}), 200)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 400)
