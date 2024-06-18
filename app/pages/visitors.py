from flask import render_template, url_for, request, jsonify, make_response
from datetime import datetime, timedelta
from models import Visitor, Subscription, Entry, Participate
from sqlalchemy import func

from utilities import check_active_subscription, delete_non_active_subscriptions

def visitor(app, db):
    @app.route('/visitors', methods=['GET'])
    def get_visitors():
        visitors = Visitor.query.all()
        # memorize the active subscription for each visitor, None otherwise
        for visitor in visitors:
            visitor.subscription = check_active_subscription(visitor.CodiceFiscale, datetime.now().date())
            
        return render_template('visitors.j2', visitors=visitors,
                                url_for_add_visitor=url_for('add_visitor'),
                                url_add_subscription=url_for('add_subscription'),
                                url_for_get_durations=url_for('get_durations'),
                                url_for_get_tariffs=url_for('get_tariffs'),
                                url_for_get_subscription_cost=url_for('get_subscription_cost'),
                                url_for_get_entries=url_for('get_entries'),
                                url_for_partecipates=url_for('page_partecipates'))

# APIs

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
            delete_non_active_subscriptions(codicefiscale=visitor.CodiceFiscale)
            if check_active_subscription(visitor.CodiceFiscale, datetime.now().date()):
                return make_response(jsonify({'error': 'Visitatore con abbonamento attivo'}), 400)
            if visitor:
                for e in Entry.query.filter_by(CodiceFiscale=visitor.CodiceFiscale).all():
                    for p in Participate.query.filter_by(IdIngresso=e.IdIngresso).all():
                        db.session.delete(p)
                    db.session.delete(e)
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