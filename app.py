from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.dialects.postgresql import JSON

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres@localhost/voiceinndbmodels'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# set the secret key.  keep this really secret: required to use session
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

class Organization(db.Model):
    __tablename__ = 'Organization'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    created = db.Column(db.DateTime)
    location = db.Column(db.String(100))
    phone = db.Column(db.Integer)
    email = db.Column(db.String)


class Service(db.Model):
    __tablename__ = 'Service'
    id = db.Column(db.Integer, primary_key = True)
    org_id = db.Column(db.Integer, db.ForeignKey('organization.id'))    
    service_type = db.Column(db.Integer)
    service_id = db.Column(db.Integer)
    extension = db.Column(db.Integer)
    isActive = db.Column(db.Boolean)
    created = db.Column(db.DateTime)
    allocated_channels = db.Column(db.Integer)
    channels_in_use = db.Column(db.Integer)


class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key = True)
    org_id = db.Column(db.Integer, db.ForeignKey('organization.id'))
    name = db.Column(db.String(100))
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))
    phone = db.Column(db.Integer)
    email = db.Column(db.String(100))
    created = db.Column(db.DateTime)


class ServiceType(db.Model):
    __tablename__ = 'ServicecTypei'
    id = db.Column(db.Integer, primary_key = True)
    s_type_id = db.Column(db.Integer, db.ForeignKey('service.service_type'))
    name = db.Column(db.String(100))


class GeneralizedDialplan(db.Model):
    __tablename__ = 'GeneralizedDialplan'
    id = db.Column(db.Integer, primary_key = True)
    s_id = db.Column(db.Integer, db.ForeignKey('service.service_id'))
    dialplan = db.Column(JSON)
    previous_version_id = db.Column(db.Integer)


class GeneralizedDataIncoming(db.Model):
    __tablename__ = 'GeneralizedDataIncoming'
    id = db.Column(db.Integer, primary_key = True)
    g_id = db.Column(db.Integer, db.ForeignKey('generalizeddialplan.id'))
    generalized_dialplan_id = db.Column(db.Integer)
    data = db.Column(JSON)
    incoming_number = db.Column(db.Integer)


class GeneralizedDataOutgoing(db.Model):
    __tablename__ = 'GeneralizedDataOutgoing'
    id = db.Column(db.Integer, primary_key = True)
    g_id = db.Column(db.Integer, db.ForeignKey('generalizeddialplan.id'))
    generalized_dialplan_id = db.Column(db.Integer)
    data = db.Column(JSON)
    outgoing_number = db.Column(db.Integer)


class IncomingLog(db.Model):
    __tablename__ = 'IncomingLog'
    id = db.Column(db.Integer, primary_key = True)
    org_id = db.Column(db.Integer, db.ForeignKey('organization.id'))
    service = db.Column(db.String(100))
    call_time = db.Column(db.DateTime)
    call_duration = db.Column(db.Float)
    complete = db.Column(db.Boolean)
    phone = db.Column(db.Integer)
    status = db.Column(db.String(100))


class OutgoingLog(db.Model):
    __tablename__ = 'OutgoingLog'
    id = db.Column(db.Integer, primary_key = True)
    org_id = db.Column(db.Integer, db.ForeignKey('organization.id'))
    service = db.Column(db.String(100))
    call_time = db.Column(db.DateTime)
    call_duration = db.Column(db.Float)
    complete = db.Column(db.Boolean)
    phone = db.Column(db.Integer)
    status = db.Column(db.String(100))


class Comment(db.Model):
    __tablename__ = 'Comment'
    id = db.Column(db.Integer, primary_key = True)
    il_id = db.Column(db.Integer, db.ForeignKey('incominglog.id'))
    comment = db.Column(db.String(500))
