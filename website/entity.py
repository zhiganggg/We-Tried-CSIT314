from .models2 import *

class user_entity:
    def get_user():
        return User.query.all()
    
    def get_user_by_email(user_email):
        return User.query.filter_by(email=user_email).first()
    
    def get_user_by_userId(user_id):
        return User.query.get(user_id)

class role_entity:
    pass

class agent_entity:
    def get_agent_by_id(agent_id):
        return Agent.query.filter_by(agent_id).first()

class listing_entity:
    def get_listing():
        return Listing.query.all()

    def get_listing_by_agent(agentId):
        return Listing.query.filter_by(agent_id=agentId).all()
    
    def get_listing_by_user(userId):
        return Listing.query.filter_by(user_id=userId).all()
    
    def get_listing_by_id(id):
        return Listing.query.get(id)
    
    def get_listing_by_type(type):
        return Listing.query.filter_by(type=type).all()
    
    def get_listing_by_price(min_price=0, max_price=0, type='between'):
        if type == 'between':
            return Listing.query.filter(Listing.price.between(min_price, max_price)).all()
        elif type == 'min':
            return Listing.query.filter(Listing.price >= min_price).all()
        elif type == 'max':
            return Listing.query.filter(Listing.price <= max_price).all()
        else:
            return Listing.query.all()
        
    def get_listing_by_bedrooms(bedrooms):
        if bedrooms == '5':
            return Listing.query.filter(Listing.bedrooms >= 5).all()
        else:
            return Listing.query.filter_by(bedrooms=bedrooms).all()

    
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
    
    def delete_listing(listing):
        db.session.delete(listing)
        db.session.commit()
        return True
    
    def update_listing(listing, title, description,type,price,bedrooms,bathrooms,size_sqft,location):
        listing.title = title
        listing.description = description
        listing.type = type
        listing.price = price
        listing.bedrooms = bedrooms
        listing.bathrooms = bathrooms
        listing.size_sqft = size_sqft
        listing.location = location
        db.session.commit()
        return True

    def get_listing_by_agent(agentId):
        return db.session.query(Listing, Agent).join(Listing, Listing.agent_id == agentId).all()

class shortlist_entity:
    def get_shortlist_past_week(start_date, end_date, listing_id):
        return Shortlist.query.filter(Shortlist.date_created >= start_date, Shortlist.date_created <= end_date, Shortlist.listing_id.in_(listing_id)).all()

    def get_shortlist_by_id(user_id, listing_id):
        return Shortlist.query.filter_by(user_id=user_id, listing_id=listing_id).first()
    
    def delete_shortlist(shortlist):
        db.session.delete(shortlist)
        db.session.commit()
        return True

    def add_shortlist(user_id, listing_id):
        shortlist = Shortlist(user_id=user_id, listing_id=listing_id)
        db.session.add(shortlist)
        db.session.commit()
        return True

class view_entity:
    def get_views_past_week(start_date, end_date, listing_id):
       return View.query.filter(View.date_created >= start_date, View.date_created <= end_date, View.listing_id.in_(listing_id)).all()
    
    def add_view(user_id, listing_id):
        view = View(user_id=user_id, listing_id=listing_id)
        db.session.add(view)
        db.session.commit()
        return True

class review_entity:
    def get_review_by_agentId(agent_id):
        return Review.query.filter_by(agent_id=agent_id).all()
    
    def get_review_by_agentId_userId(agent_id, userId):
        return Review.query.filter_by(agent_id=agent_id, user_id=userId).first()
    
    def add_review(agent_id, user_id):
        review = Review(agent_id=agent_id, user_id=user_id)
        db.session.add(review)
        db.session.commit()
        return True

class rating_entity:
    def get_rating_by_reviewId(id):
        return Rating.query.filter_by(review_id=id).first()
    
    def add_rating(rating_value, reviewId):
        rating = Rating(rating=rating_value, review_id=reviewId)
        db.session.add(rating)
        db.session.commit()
        return True

class comment_entity:
    def get_comment_by_reviewId(reviewId):
        return Comment.query.filter_by(review_id=reviewId).first()
    
    def add_comment(comment, reviewId):
        comment = Comment(comment=comment, review_id=reviewId)
        db.session.add(comment)
        db.session.commit()
        return True