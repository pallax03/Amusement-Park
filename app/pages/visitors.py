from flask import render_template, url_for, request, jsonify, make_response
from datetime import datetime, timedelta
from models import Visitor, Subscription, Duration, Tariff

from pages.subscriptions import subscription

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
                                url_for_get_subscription_cost=url_for('get_subscription_cost'))


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
        

    @app.route('/visitor', methods=['DELETE'])
    def delete_visitor():
        try:
            visitor = Visitor.query.filter_by(CodiceFiscale=request.args.get('CodiceFiscale')).first()
            if visitor:
                Subscription.query.filter_by(CodiceFiscale=visitor.CodiceFiscale).delete()
                db.session.delete(visitor)
                db.session.commit()
                return make_response(jsonify({'message': 'Visitor deleted'}), 200)
            else:
                return make_response(jsonify({'message': 'Visitor not found'}), 404)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 400)