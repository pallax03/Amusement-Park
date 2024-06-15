from flask import render_template, url_for, request, jsonify, make_response
from datetime import datetime, timedelta

from models import Participate, Entry, Activity

def partecipates(app, db):
    # return the partecipates
    # can be specified the visitor and the date, so an entry
    # the main table can be also filtered by the activity
    # /partecipates + '?CodiceFiscale=MNNGPP99A01H501A&dataIngresso=2021-01-01'
    @app.route('/partecipates', methods=['GET'])
    def get_partecipates():
        try:

            codicefiscale = request.args.get('CodiceFiscale')
            dataingresso = request.args.get('DataIngresso')
            return render_template('partecipates.j2', codicefiscale=codicefiscale, dataingresso=dataingresso,
                                    partecipates=dict_partecipates(Entry.query.
                                                                   filter_by(CodiceFiscale=codicefiscale, 
                                                                             Data=dataingresso)
                                                                    .first().IdIngresso))
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 400)


    def dict_partecipates(idingresso):
        partecipates = []
        for partecipate in Participate.query.filter_by(IdIngresso=idingresso).all():
            partecipates.append({
                'IdIngresso': partecipate.IdIngresso,
                'Ora': str(partecipate.Ora),
                'Activity': dict_activity(partecipate.IdAttivita)
            })
        return partecipates

    # todo (aggiungere i vincoli inespressi)
    #   - posti massimi non raggiunti
    #  NELLE ATTRAZIONI:
    #   - controllare bene prima la tabella vincoli 
    #   - tariffa dell’abbonamento, ha inclusa quella categoria
    def dict_activity(IdAttivita):
        activity = Activity.query.filter_by(IdAttivita=IdAttivita).first()
        return {
            'IdAttivita': activity.IdAttivita,
            'Nome': activity.Nome,
            'Descrizione': activity.Descrizione,
            'Posti': activity.Posti,
            'IsEvent': activity.IsEvent,
            'IdCategoria': activity.IdCategoria
        }
        
