from models import *
from datetime import datetime, timedelta

def check_subscription(visitor):
        return Subscription.query.filter_by(CodiceFiscale=visitor.CodiceFiscale).filter( datetime.strptime(Subscription.DataInizio,'%Y-%m-%d') + timedelta(days=float(Subscription.Giorni)) > datetime.now()).first()