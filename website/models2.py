
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

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    users = db.relationship('User', back_populates='role')

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    first_name = db.Column(db.String(50))
    last_name =db.Column(db.String(50))
    password = db.Column(db.String(100))
    status = db.Column(db.Enum(UserStatus), default=UserStatus.ENABLED)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    role_id = db.Column(db.Integer, db.ForeignKey('role.id', ondelete="CASCADE"), nullable=False)
    role = db.relationship('Role', back_populates='users', uselist=False)
    agent = db.relationship('Agent', back_populates='user', uselist=False)
    listing = db.relationship('Listing', back_populates='user')
    shortlists = db.relationship('Shortlist', back_populates='user')
    views = db.relationship('View', back_populates='user')
    reviews = db.relationship('Review', back_populates='user')

class Agent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cea_registration_no = db.Column(db.String(50), unique=True, nullable=False)
    agency_license_no = db.Column(db.String(50), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    user = db.relationship('User', back_populates='agent', uselist=False)
    listings = db.relationship('Listing', back_populates='agent')
    reviews = db.relationship('Review', back_populates='agent')

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
    photo = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    user = db.relationship('User', back_populates='listing', uselist=False)
    agent_id = db.Column(db.Integer, db.ForeignKey('agent.id', ondelete="CASCADE"), nullable=False)
    agent = db.relationship('Agent', back_populates='listings', uselist=False)
    shortlists = db.relationship('Shortlist', back_populates='listing', cascade="all, delete-orphan")
    views = db.relationship('View', back_populates='listing', cascade="all, delete-orphan")

class Shortlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    user = db.relationship('User', back_populates='shortlists', uselist=False)
    listing_id = db.Column(db.Integer, db.ForeignKey('listing.id', ondelete="CASCADE"), nullable=False)
    listing = db.relationship('Listing', back_populates='shortlists', uselist=False)

class View(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    user = db.relationship('User', back_populates='views', uselist=False)
    listing_id = db.Column(db.Integer, db.ForeignKey('listing.id', ondelete="CASCADE"), nullable=False)
    listing = db.relationship('Listing', back_populates='views', uselist=False)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    ratings = db.relationship('Rating', back_populates='review')
    comments = db.relationship('Comment', back_populates='review')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    user = db.relationship('User', back_populates='reviews', uselist=False)
    agent_id = db.Column(db.Integer, db.ForeignKey('agent.id', ondelete="CASCADE"), nullable=False)
    agent = db.relationship('Agent', back_populates='reviews', uselist=False)

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Float, nullable=False)
    review_id = db.Column(db.Integer, db.ForeignKey('review.id'), nullable=False)
    review = db.relationship('Review', back_populates='ratings', uselist=False)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text, nullable=False)
    review_id = db.Column(db.Integer, db.ForeignKey('review.id'), nullable=False)
    review = db.relationship('Review', back_populates='comments', uselist=False)