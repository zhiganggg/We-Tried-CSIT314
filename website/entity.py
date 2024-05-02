from .models2 import *

class user_entity:
    def get_user():
        return User.query.all()
    
    def get_user_by_email(user_email):
        return User.query.filter_by(email=user_email).first()

class role_entity:
    pass

class agent_entity:
    pass

class listing_entity:
    def get_listing():
        return Listing.query.all()

    def get_listing_by_agent(agentId):
        return Listing.query.filter_by(agent_id=agentId).all()
    
    def get_listing_by_user(userId):
        return Listing.query.filter_by(user_id=userId).all()
    
    def get_listing_by_id(id):
        return Listing.query.get(id)
    
    def add_listing(title, description, type, price, bedrooms, bathrooms, size_sqft, location, availability, photo, user_id, agent_id):
        new_listing = Listing(title=title, description=description, type=type, price=price, 
                          bedrooms=bedrooms, bathrooms=bathrooms, size_sqft=size_sqft, 
                          location=location, availability=availability, photo=photo, 
                          user_id=user_id, agent_id=agent_id)
        db.session.add(new_listing)
        db.session.commit()
        return True
    
    def update_listing_availability(listing, available):
        listing.availability = available
        db.session.commit()
        return True
    



class shortlist_entity:
    def get_shortlist_past_week(start_date, end_date, listing_id):
        return Shortlist.query.filter(Shortlist.date_created >= start_date, Shortlist.date_created <= end_date, Shortlist.listing_id.in_(listing_id)).all()

class view_entity:
    def get_views_past_week(start_date, end_date, listing_id):
       return View.query.filter(View.date_created >= start_date, View.date_created <= end_date, View.listing_id.in_(listing_id)).all()

class review_entity:
    pass

class rating_entity:
    pass

class comment_entity:
    pass