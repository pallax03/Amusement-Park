from flask import render_template, url_for, request, jsonify, make_response
from datetime import datetime, timedelta

from models import Participate, Entry, Activity, Visitor


def partecipates(app, db):
    # return the partecipates
    # can be specified the visitor and the date, so an entry
    # the main table can be also filtered by the activity
    # /partecipates + '?CodiceFiscale=MNNGPP99A01H501A&DataIngresso=2021-01-01'
    @app.route('/partecipates', methods=['GET'])
    def page_partecipates():
        try:
            return render_template('partecipates.j2', visitors=get_visitor_with_entries(),
                                   url_for_get_entries=url_for('get_entries'),
                                   url_for_get_partecipates=url_for('get_partecipates'),
                                   url_for_add_partecipate=url_for('add_partecipate'))
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 400)

    
    # get all the partecipations of a visitor's entry
    # can be filtered by the activity
    # /api/partecipates + '?CodiceFiscale=MNNGPP99A01H501A&DataIngresso=2021-01-01'
    @app.route('/api/partecipates', methods=['GET'])
    def get_partecipates():
        try:
            codicefiscale = request.args.get('CodiceFiscale')
            dataingresso = request.args.get('DataIngresso')
            partecipates = []
            for entry in Entry.query.filter_by(CodiceFiscale=codicefiscale, Data=dataingresso).all():
                for partecipate in Participate.query.filter_by(IdIngresso=entry.IdIngresso).all():
                    partecipates.append({
                        'IdIngresso': partecipate.IdIngresso,
                        'Ora': str(partecipate.Ora),
                        'Attivita': dict_activity(partecipate.IdAttivita),
                        'PostiOccupati': Participate.query.filter_by(IdAttivita=partecipate.IdAttivita, Ora=partecipate.Ora).count()
                    })
            return make_response(jsonify(partecipates), 200)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 400)


    # add a partecipate
    # /api/partecipate + json
    # vincoli inespressi:
    #   - posti massimi non raggiunti
    #  NELLE ATTRAZIONI:
    #   - controllare bene prima la tabella vincoli 
    #   - tariffa dell’abbonamento, ha inclusa quella categoria
    @app.route('/api/partecipate', methods=['POST'])
    def add_partecipate():
        return make_response(jsonify({'message': 'Not implemented'}), 501)


    def get_visitor_with_entries():
        visitors = []
        for visitor in Visitor.query.all():
            if Entry.query.filter_by(CodiceFiscale=visitor.CodiceFiscale).first():
                visitors.append({'CodiceFiscale': visitor.CodiceFiscale})
        return visitors


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
        
