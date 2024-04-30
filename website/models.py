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
    status = db.Column(db.Enum(UserStatus), default=UserStatus.ENABLED)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    role = db.relationship('Role', backref='user_role', passive_deletes=True)
    agent = db.relationship('Agent', back_populates='user', uselist=False)
    listings = db.relationship('Listing', backref='user_listing', passive_deletes=True)
    shortlists = db.relationship('Shortlist', backref='user_shortlist', passive_deletes=True)
    reviews = db.relationship('Review', backref='user_review', passive_deletes=True)

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

class Agent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    user = db.relationship('User', back_populates='agent', uselist=False)
    cea_registration_no = db.Column(db.String(50), unique=True, nullable=False)
    agency_license_no = db.Column(db.String(50), unique=True, nullable=False)
    reviews = db.relationship('Review', backref='agent_review', lazy=True)

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
    user = db.relationship('User', backref='listing_user', passive_deletes=True)
    agent_id = db.Column(db.Integer, db.ForeignKey('agent.id', ondelete="CASCADE"), nullable=False)
    agent = db.relationship('Agent', backref='listing_agent', passive_deletes=True)
    shortlists = db.relationship('Shortlist', backref='listing_shortlist', passive_deletes=True)
    views = db.relationship('View', backref='listing_view', passive_deletes=True)

class Shortlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    listing_id = db.Column(db.Integer, db.ForeignKey('listing.id', ondelete="CASCADE"), nullable=False)
    listing = db.relationship('Listing', backref='shortlist_listing', passive_deletes=True)

class View(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    listing_id = db.Column(db.Integer, db.ForeignKey('listing.id', ondelete="CASCADE"), nullable=False)
    listing = db.relationship('Listing', backref='view_listing', passive_deletes=True)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ratings = db.relationship('Rating', backref='review_rating', lazy=True)
    comments = db.relationship('Comment', backref='review_comment', lazy=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    user = db.relationship('User', backref='review_user', passive_deletes=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    agent_id = db.Column(db.Integer, db.ForeignKey('agent.id', ondelete="CASCADE"), nullable=False)

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Float, nullable=False)
    review_id = db.Column(db.Integer, db.ForeignKey('review.id'), nullable=False)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text)
    review_id = db.Column(db.Integer, db.ForeignKey('review.id'), nullable=False)
