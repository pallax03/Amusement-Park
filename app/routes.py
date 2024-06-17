from flask import render_template

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
        return render_template('index.j2')
    
    # pages routes
    visitor(app, db)        # /visitors
    subscription(app, db)   # /subscriptions
    activity(app, db)       # /activities
    partecipates(app, db)   # /partecipations
    employee(app, db)       # /employees
    service(app, db)        # /services