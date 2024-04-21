from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from enum import Enum

class UserStatus(Enum):
    ENABLED = 'enabled'
    DISABLED = 'disabled'

class Availability(Enum):
    AVAILABLE = 'available'
    UNAVAILABLE = 'unavailable'

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    first_name = db.Column(db.String(50))
    last_name =db.Column(db.String(50))
    password = db.Column(db.String(100))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    role = db.Column(db.String(20))
    status = db.Column(db.Enum(UserStatus), default=UserStatus.ENABLED)
    listings = db.relationship('Listing', backref='user', passive_deletes=True)
    shortlists = db.relationship('Shortlist', backref='user', passive_deletes=True)

class Agent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    cea_registration_no = db.Column(db.String(50), unique=True, nullable=False)
    agency_license_no = db.Column(db.String(50), unique=True, nullable=False)
    reviews = db.relationship('Review', backref='agent', lazy=True)

class Listing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    bedrooms = db.Column(db.Integer, nullable=False)
    bathrooms = db.Column(db.Integer, nullable=False)
    size_sqft = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(150), nullable=False)
    availability = db.Column(db.Enum(Availability), default=Availability.AVAILABLE)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    photo = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    shortlists = db.relationship('Shortlist', backref='post', passive_deletes=True)

class Shortlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    listing_id = db.Column(db.Integer, db.ForeignKey('listing.id', ondelete="CASCADE"), nullable=False)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    agent_id = db.Column(db.Integer, db.ForeignKey('agent.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
