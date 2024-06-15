from flask import render_template, url_for, request, jsonify, make_response
from datetime import datetime, timedelta

from models import Participate, Entry, Activity

def partecipates(app, db):
    # get partecipates by CodiceFiscale, and dataingresso
    # /partecipates + '?CodiceFiscale=MNNGPP99A01H501A&dataIngresso=2021-01-01'
    @app.route('/partecipates', methods=['GET'])
    def get_partecipates():
        try:
            codicefiscale = request.args.get('CodiceFiscale')
            dataingresso = request.args.get('DataIngresso')
            partecipates = []
            for entry in Entry.query.filter_by(CodiceFiscale=codicefiscale).filter_by(Data=dataingresso).all():
                partecipates.append(Participate.query.filter_by(IdIngresso=entry.IdIngresso).all())
            return render_template('partecipates.j2', codicefiscale=codicefiscale, dataingresso=dataingresso,
                                    partecipates=partecipates)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 400)


    def dict_activity(IdAttivita):
        activity = Activity.query.filter_by(IdAttivita=IdAttivita).first()
        
