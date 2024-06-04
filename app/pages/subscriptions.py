from flask import render_template, url_for, request, make_response, jsonify
import json
from datetime import datetime, timedelta
from models import Subscription, Duration, Tariff, Include, Category

from pages.activities import activity

# SUBSCRIPTION
def subscription(app, db):
    @app.route('/subscriptions', methods=['GET'])
    def page_subscriptions():
        return render_template('subscriptions.j2', durations=get_durations().json, tariffs=get_tariffs().json, 
                                url_for_get_categories=url_for('get_categories'),
                                url_for_get_durations=url_for('get_durations'),
                                url_for_get_tariffs=url_for('get_tariffs'),
                                url_for_add_duration=url_for('add_duration'),
                                url_for_add_tariff=url_for('add_tariff'), 
                                url_for_cost=url_for('get_subscription_cost'))

    @app.route('/subscription', methods=['GET'])
    def get_active_subscription():
        try:
            subscriptions = Subscription.query.filter_by(CodiceFiscale=request.args.get('CodiceFiscale')).all()
            for subscription in subscriptions:
                active = Subscription.query.filter_by(CodiceFiscale=subscription.CodiceFiscale).filter(datetime.strptime(str(subscription.DataInizio),'%Y-%m-%d') + timedelta(days=float(subscription.Giorni)) > datetime.now()).first()
            return make_response(jsonify(active), 200)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 400)

    @app.route('/subscription', methods=['DELETE'])
    def delete_subscription():
        try:
            subscription = Subscription.query.filter_by(CodiceFiscale=request.args.get('CodiceFiscale')).filter_by(DataInizio=request.args.get('DataInizio')).first()
            db.session.delete(subscription)
            db.session.commit()
            return make_response(jsonify({'message': 'Abbonamento eliminato'}), 200)
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


    @app.route('/subscription/durations', methods=['GET'])
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
        

    @app.route('/subscription/tariffs', methods=['GET'])
    def get_tariffs():
        try:
            tariffs = Tariff.query.all()
            tariff_list = []
            for tariff in tariffs:
                tariff_dict = {
                    "IdTariffa": tariff.IdTariffa,
                    "NomeTariffa": tariff.NomeTariffa,
                    "CostoGiornaliero": tariff.CostoGiornaliero,
                    "Categories": []
                }
                for include in Include.query.filter_by(IdTariffa=tariff.IdTariffa).all():
                    tariff_dict["Categories"].append(Category.query.filter_by(IdCategoria=include.IdCategoria).first())
                tariff_list.append(tariff_dict)

            return make_response(jsonify(tariff_list), 200)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 400)

    

    @app.route('/subscription/tariff', methods=['POST'])
    def add_tariff():
        try:
            if (data["NomeTariffa"] == None or data['NomeTariffa'] == ''):
                return make_response(jsonify({'error': 'NomeTariffa non specificato'}), 400)
            data = request.get_json()
            tariff = Tariff(
                NomeTariffa=data['NomeTariffa'],
                CostoGiornaliero=data['CostoGiornaliero']
            )
            for category in data['Categories']:
                include = Include(
                    IdTariffa=tariff.IdTariffa,
                    IdCategoria=category.IdCategoria
                )
                db.session.add(include)

            db.session.add(tariff)
            db.session.commit()
            return make_response(jsonify({'message': 'Tariffa creata'}), 201)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 400)

    @app.route('/subscription/tariff', methods=['DELETE'])
    def delete_tariff():
        try:
            tariff = Tariff.query.filter_by(NomeTariffa=request.args.get('NomeTariffa')).first()
            includes = Include.query.filter_by(IdTariffa=tariff.IdTariffa).all()
            for include in includes:
                db.session.delete(include)
            db.session.delete(tariff)
            db.session.commit()
            return make_response(jsonify({'message': 'Tariffa eliminata'}), 200)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 400)


    @app.route('/subscription/cost', methods=['GET'])
    def get_subscription_cost():
        try:
            tariff = Tariff.query.filter_by(NomeTariffa=request.args.get('NomeTariffa')).first()
            duration = Duration.query.filter_by(Giorni=request.args.get('Giorni')).first()
            costo_totale = (tariff.CostoGiornaliero * duration.Giorni)
            sconto = (costo_totale * (duration.Sconto/100))
            return make_response(jsonify({'Costo': costo_totale - sconto }), 200)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 400)
