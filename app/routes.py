from flask import render_template, make_response, jsonify, url_for, request

from utilities import query_N13_highest_entries_days, query_N14_most_partecipated_rides, query_N15_highest_shopped_subscriptions

from pages.visitors import visitor
from pages.subscriptions import subscription
from pages.activities import activity
from pages.employees import employee
from pages.services import service
from pages.partecipates import partecipates

# define the routes
def routes(app, db):
    
    # home route
    @app.route('/')
    def index():
        # dashboard
        return render_template('index.j2',
                                url_for_get_categories=url_for('get_categories'),
                                url_for_get_tariffs=url_for('get_tariffs'),
                                url_for_stats_entries = url_for('get_entries_stats'),
                                url_for_stats_partecipates = url_for('get_partecipates_stats'),
                                url_for_stats_subscriptions = url_for('get_subscriptions_stats'))

    # stats of the highest entries days
    # /api/stats/entries + '?DataInizio=2021-01-01&DataFine=2021-12-31'
    @app.route('/api/stats/entries', methods=['GET'])
    def get_entries_stats():
        return make_response(jsonify(query_N13_highest_entries_days(request.args.get('DataInizio'), request.args.get('DataFine'))), 200)

    # stats of the most partecipated rides
    # /api/stats/partecipates + '?NomeCategoria=Acqua'
    @app.route('/api/stats/partecipates', methods=['GET'])
    def get_partecipates_stats():
        return make_response(jsonify(query_N14_most_partecipated_rides(request.args.get('NomeCategoria'))), 200)
        
    # stats of the highest shopped subscriptions
    # /api/stats/subscriptions + '?NomeTariffa=VIP'
    @app.route('/api/stats/subscriptions', methods=['GET'])
    def get_subscriptions_stats():
        return make_response(jsonify(query_N15_highest_shopped_subscriptions(request.args.get('NomeTariffa'))), 200)
    
    # pages routes
    visitor(app, db)        # /visitors
    subscription(app, db)   # /subscriptions
    activity(app, db)       # /activities
    partecipates(app, db)   # /partecipations
    employee(app, db)       # /employees
    service(app, db)        # /services