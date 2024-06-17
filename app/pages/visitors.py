from flask import render_template, url_for, request, jsonify, make_response
from datetime import datetime, timedelta
from models import Visitor, Subscription, Duration, Tariff, Entry
from sqlalchemy import func

from pages.subscriptions import subscription
from pages.partecipates import partecipates

def visitor(app, db):
    @app.route('/visitors', methods=['GET'])
    def get_visitors():
        visitors = Visitor.query.all()
        for visitor in visitors: #take all the active subscription per visitor
            subscriptions = Subscription.query.filter_by(CodiceFiscale=visitor.CodiceFiscale).all()
            active = Subscription()
            for subscription in subscriptions:
                active = Subscription.query.filter_by(CodiceFiscale=subscription.CodiceFiscale).filter(datetime.strptime(str(subscription.DataInizio),'%Y-%m-%d') + timedelta(days=float(subscription.Giorni)) > datetime.now()).first()
            
            visitor.subscription = active if active is not None else Subscription()
        return render_template('visitors.j2', visitors=visitors,
                                url_for_add_visitor=url_for('add_visitor'),
                                url_add_subscription=url_for('add_subscription'),
                                url_for_get_durations=url_for('get_durations'),
                                url_for_get_tariffs=url_for('get_tariffs'),
                                url_for_get_subscription_cost=url_for('get_subscription_cost'),
                                url_for_get_entries=url_for('get_entries'),
                                url_for_partecipates=url_for('page_partecipates'))

    # get visitor by CodiceFiscale
    # /api/visitor + '?CodiceFiscale=MNNGPP99A01H501A'
    @app.route('/api/visitor', methods=['GET'])
    def get_visitor():
        try:
            visitor = Visitor.query.filter_by(CodiceFiscale=request.args.get('CodiceFiscale')).first()
            return make_response(jsonify(visitor), 200)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 400)

    # add visitor
    # /api/visitor + json
    @app.route('/api/visitor', methods=['POST'])
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
            return make_response(jsonify({'message': f'Visitatore {visitor.CodiceFiscale} registrato'}), 201)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 400)
        
    # delete a visitor, and all the non active subscriptions
    # /api/visitor + '?CodiceFiscale=MNNGPP99A01H501A'
    @app.route('/api/visitor', methods=['DELETE'])
    def delete_visitor():
        try:
            visitor = Visitor.query.filter_by(CodiceFiscale=request.args.get('CodiceFiscale')).first()
            if visitor:
                db.session.delete(visitor)
                db.session.commit()
                return make_response(jsonify({'message': f'Visitatore {visitor.CodiceFiscale} eliminato'}), 200)
            else:
                return make_response(jsonify({'error': 'Visitatore non trovato'}), 404)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 400)
        
    ### ads Entry look README.md

    # get entries for a visitor
    # /api/visitor/entries + '?CodiceFiscale=MNNGPP99A01H501A'
    @app.route('/api/visitor/entries', methods=['GET'])
    def get_entries():
        try:
            entries = Entry.query.filter_by(CodiceFiscale=request.args.get('CodiceFiscale')).all() 
            return make_response(jsonify(entries), 200)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 400)
    
    # add entry for a visitor checking if the visitor exists, 
    # and if the subscription is active in the date of the entry
    # /api/visitor/entries + json
    @app.route('/api/visitor/entries', methods=['POST'])
    def add_entry():
        try:
            data = request.get_json()
            visitor = Visitor.query.filter_by(CodiceFiscale=data['CodiceFiscale']).first()
            if visitor is None:
                return make_response(jsonify({'error': 'Visitatore non trovato'}), 404)

            if check_active_subscription(visitor.CodiceFiscale, data['Data']) is None:
                return make_response(jsonify({'error': 'Abbonamento non attivo'}), 404)
            entry = Entry(
                CodiceFiscale=data['CodiceFiscale'],
                Data=data['Data']
            )
            db.session.add(entry)
            db.session.commit()
            return make_response(jsonify({'message': f'Entrata per {visitor.CodiceFiscale} registrata'}), 201)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 400)
        
    # check if the subscription is active
    def check_active_subscription(CodiceFiscale, Data):
        for subscription in Subscription.query.filter_by(CodiceFiscale=CodiceFiscale).all():
            subscription_endDate = subscription.DataInizio + timedelta(days=float(subscription.Giorni))
            formatted_date = datetime.strptime(Data, '%Y-%m-%d').date()
            if subscription.DataInizio <= formatted_date and subscription_endDate >= formatted_date:
                return subscription