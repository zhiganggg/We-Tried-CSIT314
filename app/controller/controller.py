# app/control/controller.py
from app.entity.entity import *

#LoginManger API
class loginManagerController:
    def get(id):
        return User.get_user_id(id)

#57, 83
#LoginController
class loginController:
    def get(self, email):
        return User.get_user_by_email(email)

#SignupController
class signupController:
    def get(self, email, first_name, last_name, password, 
             profile_id, cea_registration_no, agency_license_no):
        
        new_user = User.create_user(email, first_name, last_name, password, profile_id)

        if not new_user:
            return False

        if new_user.profile.name == "Agent":
            Agent.create_agent(cea_registration_no, agency_license_no, new_user.id)

        return new_user

#ceaController
class ceaController:
    def get(self, cea_registration_no):
        return Agent.get_cea_no(cea_registration_no)

#ProfileController
class profileController:
    def get(self):
        return Profile.get_all_profiles()

#CreateProfileController
class createProfileController:
    def get(self, name, description):
        return Profile.create_profile(name, description)

#UpdateProfileController
class updateProfileController:
    def get(self, profile_id, name, description):
        return Profile.update_profile(profile_id, name, description)

#DeleteProfileController
class deleteProfileController:
    def get(self, profile_id):
        return Profile.delete_profile(profile_id)

#UserController
class userController:
    def get(self):
        return User.get_all_users()

#UpdateUserController
class updateUserController:
    def get(self, user_id, email, first_name, last_name):
        return User.update_user(user_id, email, first_name, last_name)

#UpdateUserStatusController
class updateUserStatusController:
    def get(self, user_id):
        return User.update_status(user_id)
    
#UpdateUserPasswordController
class updateUserPasswordController:
    def get(self, user_id, password):
        return User.update_password(user_id, password)

#SearchUserController
class searchUserController:
    def get(self, search_query):
        return User.search_user(search_query)

#ViewListingsController
class viewListingsController:
    def get(self):
        return Listing.get_all_listings()

#ViewListingController
class viewListingController:
    def get(self, user_id, listing_id):
        
        listing = Listing.get_listing_id(listing_id)
        if listing:
            View.create_view(user_id, listing_id)
            return listing
        else:
            return False

#ViewListingController
class getListingController:
    def get(self, listing_id):
        return Listing.get_listing_id(listing_id)
    
class userListingController:
    def get(self, user):

        if user.agent:
            return Listing.get_listing_by_agent(user.agent.id)
        
        else:
            return Listing.get_listing_by_user(user.id)

#SearchListingLocationController
class searchListingLocationController:
    def get(self, search_query):
        return Listing.search_listing_by_location(search_query)
    
#SearchListingTypeController
class searchListingTypeController:
    def get(self, type):
        return Listing.search_listing_by_type(type)

#SearchListingPriceController    
class searchListingPriceController:
    def get(self, min_price, max_price):
        
        if min_price and max_price:
            return Listing.search_by_price_range(min_price, max_price)
        
        elif min_price:
            return Listing.search_by_min_price(min_price)

        elif max_price:
            return Listing.search_by_max_price(max_price)

        else:
            return Listing.get_all_listings

#SearchListingBedroomController        
class searchListingBedroomController:
    def get(self, bedrooms):

        if bedrooms == "5":
            return Listing.search_by_min_bedrooms(5)

        else:
            return Listing.search_by_bedrooms(bedrooms)

#CreateListingController
class createListingController:
    def get(self, title, description, type, price, bedrooms, 
             bathrooms, size_sqft, location, file_path, user_id, agent_id):
        
        return Listing.create_listing(title, description, type, price, bedrooms, 
                                      bathrooms, size_sqft, location, file_path, user_id, agent_id)

#UpdateListingController
class updateListingController:
    def get(self, listing_id, title, description, type, price, 
             bedrooms, bathrooms, size_sqft, location, file_path):
        
        return Listing.update_listing(listing_id, title, description, type, price, 
                                      bedrooms, bathrooms, size_sqft, location, file_path)

#UpdateListingStatusController    
class updateListingStatusController:
    def get(self, listing_id):
        return Listing.update_status(listing_id)
    
#DeleteListingController
class deleteListingController:
    def get(self, listing_id):
        return Listing.delete_listing(listing_id)

#ShortlistListingController    
class shortlistListingController:
    def get(self, user_id, listing_id):
            return Shortlist.manage_shortlist(user_id, listing_id)

#ViewListingsByAgentController    
class viewListingsByAgentController:
    def get(self):
        return Listing.get_all_listings_with_agents()
    
#GetAgentController
class getAgentController:
    def get(self, agent_id):
        return Agent.get_agent_id(agent_id)
    
#GetReviewsController
class getReviewsController:
    def get(self, agent_id):
        return Review.get_review_by_agent(agent_id)
    
#CreateRatingController
class createRatingController:
    def get(self, agent_id, user_id, rating_value):

        review = Review.get_or_create_review(agent_id, user_id)

        if review:
            return Rating.create_or_update_rating(rating_value, review.id)
        else:
            return False
        
#CreateCommentController
class createCommentController:
    def get(self, agent_id, user_id, comment_value):

        review = Review.get_or_create_review(agent_id, user_id)

        if review:
            return Comment.create_or_update_comment(comment_value, review.id)
        else:
            return False
        
