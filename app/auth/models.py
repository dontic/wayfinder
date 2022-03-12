from app.extensions import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    apikey = db.Column(db.String(100))
    homeLAT = db.Column(db.Float)
    homeLONG = db.Column(db.Float)
    defaultPeriodPath = db.Column(db.Integer)
    maxAccuracyPath = db.Column(db.Integer)
    defaultShowVisits = db.Column(db.Boolean)
    defaultRemoveIdle = db.Column(db.Boolean)
    defaultTripColor = db.Column(db.Boolean)
    defaultPeriodVisits = db.Column(db.Integer)
    defaultIgnoreHome = db.Column(db.Boolean)
    