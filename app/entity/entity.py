# app/entity/entity.py
from app import db
from sqlalchemy.sql import func
from enum import Enum
from flask_login import UserMixin

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    users = db.relationship("User", back_populates="profile")

    @classmethod
    def create_profile(cls, name, description):
        profile = cls.query.filter_by(name=name).first()

        if profile:
            return False
        
        else:

            new_profile = cls(name=name, description=description)
            db.session.add(new_profile)
            db.session.commit()
            return True
    
    @classmethod
    def update_profile(cls, profile_id, name, description):
        profile = cls.query.get(profile_id)

        if not profile:
            return None
        
        existing_profile = cls.query.filter(cls.name == name, cls.id != profile_id).first()
        if not existing_profile:
            profile.name = name
            profile.description = description
            db.session.commit()
            return True
        
        else:
            return False
        
    @classmethod
    def search_profile(cls, search_query):
        if search_query:
            filtered_profiles = cls.query.filter(
                (cls.name.ilike(f"%{search_query}%")) |
                (cls.description.ilike(f"%{search_query}%"))
            ).all()
        
        else:
            filtered_profiles = cls.query.all()

        return filtered_profiles
            
    @classmethod
    def delete_profile(cls, id):
        profile = cls.query.get(id)

        if not profile:
            return False
        
        db.session.delete(profile)
        db.session.commit()
        return True

    @classmethod
    def get_all_profiles(cls):

        return cls.query.all()
    
    @classmethod
    def get_profile_id(cls, id):

        return cls.query.get(id)

    @classmethod
    def get_profile_name(cls, name):
        
        return cls.query.filter_by(name=name).first()

class User(db.Model, UserMixin):
    class UserStatus(Enum):
        ENABLED = "ENABLED"
        DISABLED = "DISABLED"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    first_name = db.Column(db.String(50))
    last_name =db.Column(db.String(50))
    password = db.Column(db.String(100))
    status = db.Column(db.Enum(UserStatus), default=UserStatus.ENABLED)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    profile_id = db.Column(db.Integer, db.ForeignKey("profile.id", ondelete="CASCADE"), nullable=False)
    profile = db.relationship("Profile", back_populates="users", uselist=False)
    agent = db.relationship("Agent", back_populates="user", uselist=False)
    listing = db.relationship("Listing", back_populates="user")
    shortlists = db.relationship("Shortlist", back_populates="user")
    views = db.relationship("View", back_populates="user")
    feedbacks = db.relationship("Feedback", back_populates="user")

    @classmethod
    def create_user(cls, email, first_name, last_name, password, profile_id):
        user = cls.query.filter_by(email=email).first()

        if user:
            return False
        
        else:
            new_user = cls(email=email, first_name=first_name, last_name=last_name, password=password, profile_id=profile_id)
            db.session.add(new_user)
            db.session.commit()
            return new_user
    
    @classmethod
    def update_user(cls, user_id, email, first_name, last_name):
        user = cls.query.get(user_id)

        if not user:
            return None
        
        existing_user = cls.query.filter(cls.email == email, cls.id != user_id).first()
        if not existing_user:
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            db.session.commit()
            return True
        
        else:
            return False
        
    @classmethod
    def update_password(cls, user_id, new_password):
        user = cls.query.get(user_id)

        if user:
            user.password = new_password
            db.session.commit()
            return True
        else:
            return False
        

        
    @classmethod
    def update_status(cls, id):
        user = cls.query.get(id)

        if not user:
            return None
        
        if user.status == cls.UserStatus.ENABLED:
            user.status = cls.UserStatus.DISABLED
        
        else:
            user.status = cls.UserStatus.ENABLED

        db.session.commit()
        return user.status

    @classmethod
    def get_all_users(cls):

        return cls.query.all()

    @classmethod
    def get_user_id(cls, id):

        return cls.query.get(id)

    @classmethod
    def get_user_by_email(cls, email):

        return cls.query.filter_by(email=email).first()
    
    @classmethod
    def search_user(cls, search_query):
        if search_query:
            filtered_users = cls.query.filter(
                (cls.email.ilike(f"%{search_query}%")) |
                (cls.first_name.ilike(f"%{search_query}%")) |
                (cls.last_name.ilike(f"%{search_query}%"))
            ).all()
        
        else:
            filtered_users = cls.query.all()

        return filtered_users

class Agent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cea_registration_no = db.Column(db.String(50), unique=True, nullable=False)
    agency_license_no = db.Column(db.String(50), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    user = db.relationship("User", back_populates="agent", uselist=False)
    listings = db.relationship("Listing", back_populates="agent")
    feedbacks = db.relationship("Feedback", back_populates="agent")

    @classmethod
    def create_agent(cls, cea_registration_no, agency_license_no, user_id):
        agent = cls.query.filter_by(cea_registration_no=cea_registration_no).first()

        if agent:
            return None

        else:
            new_agent = cls(cea_registration_no=cea_registration_no, agency_license_no=agency_license_no, user_id=user_id)
            db.session.add(new_agent)
            db.session.commit()
            return new_agent
    
    @classmethod
    def get_agent_id(cls, id):

        return cls.query.get(id)

    @classmethod
    def get_agent_user_id(cls, user_id):
        
        return cls.query.filter_by(user_id=user_id).first()

    @classmethod
    def get_cea_no(cls, cea_registration_no):

        return cls.query.filter_by(cea_registration_no=cea_registration_no).first()

class Listing(db.Model):
    class Availability(Enum):
        AVAILABLE = "AVAILABLE"
        UNAVAILABLE = "UNAVAILABLE"

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
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    user = db.relationship("User", back_populates="listing", uselist=False)
    agent_id = db.Column(db.Integer, db.ForeignKey("agent.id", ondelete="CASCADE"), nullable=False)
    agent = db.relationship("Agent", back_populates="listings", uselist=False)
    shortlists = db.relationship("Shortlist", back_populates="listing", cascade="all, delete-orphan")
    views = db.relationship("View", back_populates="listing", cascade="all, delete-orphan")

    @classmethod
    def create_listing(cls, title, description, type, price, 
                       bedrooms, bathrooms, size_sqft, location, file_path, 
                       user_id, agent_id):
        
        new_listing = cls(title=title, description=description, type=type, price=price, bedrooms=bedrooms, 
                          bathrooms=bathrooms, size_sqft=size_sqft, location=location, photo=file_path, user_id=user_id, 
                          agent_id=agent_id)
        db.session.add(new_listing)
        try:
            db.session.commit()
            return True
        except:
            db.session.rollback()
            return False
    
    @classmethod
    def update_listing(cls, id, title, description, type, price, 
                       bedrooms, bathrooms, size_sqft, location, file_path):
        
        listing = cls.query.get(id)

        if not listing:
            return None

        listing.title = title
        listing.description = description
        listing.type = type
        listing.price = price
        listing.bedrooms = bedrooms
        listing.bathrooms = bathrooms
        listing.size_sqft = size_sqft
        listing.location = location
        
        if file_path:
            listing.photo = file_path

        db.session.commit()
        return listing

    @classmethod
    def update_status(cls, id):
        listing = cls.query.get(id)

        if not listing:
            return None
        
        if listing.availability == cls.Availability.AVAILABLE:
            listing.availability = cls.Availability.UNAVAILABLE
        
        else:
            listing.availability = cls.Availability.AVAILABLE

        db.session.commit()
        return listing.availability

    @classmethod
    def delete_listing(cls, id):
        listing = cls.query.get(id)

        if not listing:
            return False
        
        db.session.delete(listing)
        db.session.commit()
        return True

    @classmethod
    def get_all_listings_with_agents(cls):

        query_result = db.session.query(Listing, Agent).join(Listing, Listing.agent_id == Agent.id).all()
        return query_result

    @classmethod
    def get_all_listings(cls):

        return cls.query.all()
    
    @classmethod
    def get_listing_id(cls, id):

        return cls.query.get(id)
    
    @classmethod
    def get_listing_by_user(cls, user_id):
        
        return cls.query.filter_by(user_id=user_id).all()

    @classmethod
    def get_listing_by_agent(cls, agent_id):
        
        return cls.query.filter_by(agent_id=agent_id).all()
    
    @classmethod
    def search_listing_by_location(cls, search_query):
        if search_query:
            filtered_listings = cls.query.filter(
                (cls.location.ilike(f"%{search_query}%"))
            ).all()

        else:
            filtered_listings = cls.query.all()

        return filtered_listings
    
    @classmethod
    def search_listing_by_type(cls, type):

        return cls.query.filter_by(type=type).all()
    
    @classmethod
    def search_by_price_range(cls, min_price, max_price):

        return cls.query.filter(cls.price.between(min_price, max_price)).all()
    
    @classmethod
    def search_by_min_price(cls, min_price):

        return cls.query.filter(cls.price >= min_price).all()
    
    @classmethod
    def search_by_max_price(cls, max_price):

        return cls.query.filter(cls.price <= max_price).all()
    
    @classmethod
    def search_by_bedrooms(cls, bedrooms):

        return cls.query.filter_by(bedrooms=bedrooms).all()
    
    @classmethod
    def search_by_min_bedrooms(cls, min_bedrooms):

        return cls.query.filter(cls.bedrooms >= min_bedrooms).all()

class Shortlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    user = db.relationship("User", back_populates="shortlists", uselist=False)
    listing_id = db.Column(db.Integer, db.ForeignKey("listing.id", ondelete="CASCADE"), nullable=False)
    listing = db.relationship("Listing", back_populates="shortlists", uselist=False)

    @classmethod
    def manage_shortlist(cls, user_id, listing_id):
        shortlist = cls.query.filter_by(user_id=user_id, listing_id=listing_id).first()

        if shortlist:
            db.session.delete(shortlist)
            db.session.commit()
            return True
        
        else:
            new_shortlist = cls(user_id=user_id, listing_id=listing_id)
            db.session.add(new_shortlist)
            db.session.commit()
            return new_shortlist

    @classmethod
    def get_shortlist(cls, user_id, listing_id):

        return cls.query.filter_by(user_id=user_id, listing_id=listing_id).first()
    
    @classmethod
    def get_shortlists_in_period(cls, listing_ids, start_date, end_date):

        return cls.query.filter(cls.date_created >= start_date,
                                cls.date_created <= end_date,
                                cls.listing_id.in_(listing_ids)).all()

class View(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    user = db.relationship("User", back_populates="views", uselist=False)
    listing_id = db.Column(db.Integer, db.ForeignKey("listing.id", ondelete="CASCADE"), nullable=False)
    listing = db.relationship("Listing", back_populates="views", uselist=False)

    @classmethod
    def create_view(cls, user_id, listing_id):

        new_view = cls(user_id=user_id, listing_id=listing_id)
        db.session.add(new_view)
        db.session.commit()
        return new_view

    @classmethod
    def get_views_in_period(cls, listing_ids, start_date, end_date):

        return cls.query.filter(cls.date_created >= start_date,
                                cls.date_created <= end_date,
                                cls.listing_id.in_(listing_ids)).all()

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    ratings = db.relationship("Rating", back_populates="feedback")
    reviews = db.relationship("Review", back_populates="feedback")
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    user = db.relationship("User", back_populates="feedbacks", uselist=False)
    agent_id = db.Column(db.Integer, db.ForeignKey("agent.id", ondelete="CASCADE"), nullable=False)
    agent = db.relationship("Agent", back_populates="feedbacks", uselist=False)

    @classmethod
    def get_or_create_feedback(cls, agent_id, user_id):
        feedback = cls.query.filter_by(agent_id=agent_id, user_id=user_id).first()

        if feedback:
            return feedback

        new_feedback = cls(agent_id=agent_id, user_id=user_id)
        db.session.add(new_feedback)
        db.session.commit()
        return new_feedback
    
    @classmethod
    def get_feedback_by_agent(cls, agent_id):

        return cls.query.filter_by(agent_id=agent_id).all()
    
    @classmethod
    def get_feedback_by_agent_user(cls, agent_id, user_id):

        return cls.query.filter_by(agent_id=agent_id, user_id=user_id).first()
    
    @classmethod
    def delete_feedback(cls, id):
        feedback = cls.query.filter_by(id=id).first()

        if feedback:
            db.session.delete(feedback)
            db.session.commit()
            return True
        
        else:
            return False
        
class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Float, nullable=False)
    feedback_id = db.Column(db.Integer, db.ForeignKey("feedback.id"), nullable=False)
    feedback = db.relationship("Feedback", back_populates="ratings", uselist=False)

    @classmethod
    def create_or_update_rating(cls, rating_value, feedback_id):
        rating = cls.query.filter_by(feedback_id=feedback_id).first()

        if rating:
            rating.rating = rating_value

        else:
            new_rating = cls(feedback_id=feedback_id, rating=rating_value)
            db.session.add(new_rating)
        
        db.session.commit()
        return True

    @classmethod
    def delete_rating(cls, feedback_id):
        rating = cls.query.filter_by(feedback_id=feedback_id).first()

        if rating:
            db.session.delete(rating)
            db.session.commit()
            return True
        
        else:
            return False

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    review = db.Column(db.Text, nullable=False)
    feedback_id = db.Column(db.Integer, db.ForeignKey("feedback.id"), nullable=False)
    feedback = db.relationship("Feedback", back_populates="reviews", uselist=False)

    @classmethod
    def create_or_update_review(cls, review_value, feedback_id):
        review = cls.query.filter_by(feedback_id=feedback_id).first()

        if review:
            review.review = review_value

        else:
            new_review = cls(review=review_value, feedback_id=feedback_id)
            db.session.add(new_review)
        
        db.session.commit()
        return review
    
    @classmethod
    def delete_review(cls, feedback_id):
        review = cls.query.filter_by(feedback_id=feedback_id).first()

        if review:
            db.session.delete(review)
            db.session.commit()
            return True
        
        else:
            return False