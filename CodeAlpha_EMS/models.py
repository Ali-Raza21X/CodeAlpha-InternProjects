from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
db=SQLAlchemy()

class User(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username= db.Column(db.String(100),unique=True)
    email=db.Column(db.String(100),unique=True)
    password=db.Column(db.String(200))
    role=db.Column(db.String(20),default='user')
    bookings = db.relationship('Booking', backref='user', lazy=True)
class Event(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(50),unique=True)
    date=db.Column(db.Date,nullable=False)
    description = db.Column(db.Text)
    location=db.Column(db.String(500))
    capacity=db.Column(db.Integer)
    phone = db.Column(db.String(20), nullable=False)
    bookings = db.relationship('Booking', backref='event', lazy=True)

class Booking(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))
    event_id=db.Column(db.Integer,db.ForeignKey('event.id'))
    status = db.Column(db.String(20), default='unbooked')