from app import db
from datetime import datetime
from flask_login import UserMixin


class Property(db.Model):
    __tablename__ = "properties"
    id = db.Column(db.Integer, primary_key=True)
    landlord_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    landlord = db.relationship('User', backref='landlord_property', foreign_keys=[landlord_id], lazy=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    landlord_address = db.Column(db.String(200), nullable=False)
    property_type = db.Column(db.String(50))
    number_of_beds = db.Column(db.String(20))
    location = db.Column(db.String(200), nullable=False)
    state = db.Column(db.String(50))
    lga = db.Column(db.String(50))
    street = db.Column(db.String(100))
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(255))
    youtube_links = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    properties = db.relationship('Property', backref='owned_properties', lazy=True)

    def __init__(self, email, fullname, password):
        self.email = email
        self.fullname = fullname
        self.password = password

    def __repr__(self):
        return '<User {}>'.format(self.fullname)
