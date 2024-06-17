from flask import render_template, url_for, request, make_response, jsonify
from datetime import datetime, timedelta
import urllib.parse
from models import Subscription, Duration, Tariff, Include, Category

from pages.activities import activity

# SUBSCRIPTION
def subscription(app, db):
    # PAGE (return the page and all the apis links necessary for ajax calls)
    @app.route('/subscriptions', methods=['GET'])
    def page_subscriptions():
        return render_template('subscriptions.j2', durations=get_durations().json, tariffs=get_tariffs().json, 
                                url_for_get_categories=url_for('get_categories'),
                                url_for_get_durations=url_for('get_durations'),
                                url_for_get_tariffs=url_for('get_tariffs'),
                                url_for_add_duration=url_for('add_duration'),
                                url_for_add_tariff=url_for('add_tariff'), 
                                url_for_cost=url_for('get_subscription_cost'))

# APIs
    # get the active subscription of the given visitor
    # /subscription + '?CodiceFiscale=MNNGPP99A01H501A'
    @app.route('/api/subscription', methods=['GET'])
    def get_active_subscription():
        try:
            return make_response(jsonify(Subscription.query.filter_by(CodiceFiscale=request.args.get('CodiceFiscale')).filter(datetime.strptime(str(Subscription.DataInizio),'%Y-%m-%d') + timedelta(days=float(Subscription.Giorni)) > datetime.now()).first()), 200)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 400)

    # delete the given subscription identified by codice fiscale and data inizio
    # /subscription + '?CodiceFiscale=MNNGPP99A01H501A&DataInizio=2021-01-01'
    @app.route('/api/subscription', methods=['DELETE'])
    def delete_subscription():
        try:
            subscription = Subscription.query.filter_by(CodiceFiscale=request.args.get('CodiceFiscale')).filter_by(DataInizio=request.args.get('DataInizio')).first()
            db.session.delete(subscription)
            db.session.commit()
            return make_response(jsonify({'message': f'Abbonamento di {subscription.CodiceFiscale} eliminato'}), 200)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 400)

    # add a subscription
    # /subscription + new json of Subscription
    @app.route('/api/subscription', methods=['POST'])
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
            return make_response(jsonify({'message': f'Abbonamento per {subscription.CodiceFiscale} creato'}), 201)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 400)

    # get all the durations
    @app.route('/api/subscription/durations', methods=['GET'])
    def get_durations():
        return make_response(jsonify(Duration.query.all()), 200)

    # add a new duration
    # /subscription/duration + new json of Duration
    @app.route('/api/subscription/duration', methods=['POST'])
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
        
    # delete a duration
    # /subscription/duration + '?Giorni=7'
    @app.route('/api/subscription/duration', methods=['DELETE'])
    def delete_duration():
        try:
            delete_non_active_subscriptions()
            duration = Duration.query.filter_by(Giorni=request.args.get('Giorni')).first()
            db.session.delete(duration)
            db.session.commit()
            return make_response(jsonify({'message': 'Durata eliminata'}), 200)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 400)
        

    # get all the tariffs
    @app.route('/api/subscription/tariffs', methods=['GET'])
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

    
    # add a new tariff
    # /subscription/tariff + new json of Tariff and included Categories
    @app.route('/api/subscription/tariff', methods=['POST'])
    def add_tariff():
        try:
            data = request.get_json()
            tariff = Tariff(
                NomeTariffa=data['NomeTariffa'],
                CostoGiornaliero=data['CostoGiornaliero']
            )
            db.session.add(tariff)
            db.session.commit()

            for category in data['Categories']:
                include = Include(
                    IdTariffa=tariff.IdTariffa,
                    IdCategoria=category['IdCategoria']
                )
                db.session.add(include)
            db.session.commit()

            return make_response(jsonify({'message': f"Tariffa {tariff.NomeTariffa} creata"}), 201)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 400)


    # delete a tariff, call a function to delete all old subscriptions, because if there is a subscription with the tariff to delete, it will not be deleted
    # /subscription/tariff + '?NomeTariffa=Standard'
    @app.route('/api/subscription/tariff', methods=['DELETE'])
    def delete_tariff():
        try:
            delete_non_active_subscriptions()
            tariff_name = urllib.parse.unquote(request.args.get('NomeTariffa'))
            tariff = Tariff.query.filter_by(NomeTariffa=tariff_name).first()
            includes = Include.query.filter_by(IdTariffa=tariff.IdTariffa).all()
            for include in includes:
                db.session.delete(include)
            db.session.delete(tariff)
            db.session.commit()
            return make_response(jsonify({'message': f'Tariffa {tariff.NomeTariffa} eliminata'}), 200)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 400)
        
    # get the cost of a subscription
    # /subscription/cost + '?NomeTariffa=Standard&Giorni=7'
    @app.route('/api/subscription/cost', methods=['GET'])
    def get_subscription_cost():
        try:
            tariff_name = urllib.parse.unquote(request.args.get('NomeTariffa'))
            tariff = Tariff.query.filter_by(NomeTariffa=tariff_name).first()
            duration = Duration.query.filter_by(Giorni=request.args.get('Giorni')).first()
            costo_totale = (tariff.CostoGiornaliero * duration.Giorni)
            sconto = (costo_totale * (duration.Sconto/100))
            return make_response(jsonify({'Costo': costo_totale - sconto }), 200)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 400)



# private db calls
    # delete all the subscriptions that are not active anymore
    def delete_non_active_subscriptions():
        subscriptions = Subscription.query.all()
        for subscription in subscriptions:
            if datetime.strptime(str(subscription.DataInizio),'%Y-%m-%d') + timedelta(days=float(subscription.Giorni)) < datetime.now():
                db.session.delete(subscription)
        db.session.commit()