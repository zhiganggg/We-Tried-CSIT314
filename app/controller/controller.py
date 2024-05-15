# app/control/controller.py
from app.entity.entity import *

#1
#LoginManager => [LoginManagerController]
class loginManagerController: #API
    def get(id):
        return User.get_user_by_id(id)

#2
#DisplayLandingPage => [DisplayLandingController]
class displayLandingController: 
    def get(self):
        return Listing.get_all_listings()

#3
#LoginUser => [LoginUserController]
class loginUserController: #57, 69, 83, 92
    def get(self, email):
        return User.get_user_by_email(email)

#4
#DisplaySignupPage => [DisplaySignupController]
class displaySignupController: #68, 82, 91
    def get(self):
        return Profile.get_all_profiles()

# #5 [REMOVED]
# #SignupUser => [CEAController]
# class ceaController: 
#     def get(self, cea_registration_no):
#         return Agent.get_cea_no(cea_registration_no)

#6
#SignupUser => [SignupUserController]
class signupUserController: #68, 82, 91
    def get(self, email, first_name, last_name, password, 
             profile_id, cea_registration_no, agency_license_no):
        
        agent = Agent.get_cea_no(cea_registration_no)

        if agent:
            return False
        
        else:
            new_user = User.create_user(email, first_name, last_name, password, profile_id)

            if not new_user:
                return None

            if new_user.profile.name == "Agent":
                Agent.create_agent(cea_registration_no, agency_license_no, new_user.id)

            return new_user

#7
#UpdateUserAccount => [UpdateUserAccountController]
class updateUserAccountController: #72, 85, 94
    def get(self, user_id, email, first_name, last_name):
        return User.update_user(user_id, email, first_name, last_name)

#8    
#UpdateUserPassword => [UpdateUserPasswordController]
class updateUserPasswordController: #72, 85, 94
    def get(self, user_id, password):
        return User.update_password(user_id, password)

#9
#DisplayHomePage => [DisplayAdminHomeController]
class displayAdminHomeController: 
    def get(self):
        return Listing.get_all_listings(), User.get_all_users()

#10    
#DisplayHomePage => [DisplayHomeController]
class displayHomeController: 
    def get(self, user, start_date, end_date):

        if user.agent:
            user_listings = Listing.get_listing_by_agent(user.agent.id)
        else:
            user_listings = Listing.get_listing_by_user(user.id)

        listing_ids = [listing.id for listing in user_listings]

        return View.get_views_in_period(listing_ids, start_date, end_date), Shortlist.get_shortlists_in_period(listing_ids, start_date, end_date)

#11
#DisplayBuyPage => [DisplayBuyController]
class displayBuyController: 
    def get(self):
        return Listing.get_all_listings()

#12
#SearchListingLocation => [SearchListingLocationController]
class searchListingLocationController: 
    def get(self, search_query):
        return Listing.search_listing_by_location(search_query)

#13    
#SearchListingType => [SearchListingTypeController]
class searchListingTypeController: 
    def get(self, type):
        return Listing.search_listing_by_type(type)

#14
#SearchListingPrice => [SearchListingPriceController]
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

#15
#SearchListingBedroom => [SearchListingBedroomController]
class searchListingBedroomController: 
    def get(self, bedrooms):

        if bedrooms == "5":
            return Listing.search_by_min_bedrooms(5)

        else:
            return Listing.search_by_bedrooms(bedrooms)

#16    
#ShorlistListing => [ShortlistListingController]
class shortlistListingController: #77, 78
    def get(self, user_id, listing_id):
            return Listing.get_listing_by_id(listing_id), Shortlist.manage_shortlist(user_id, listing_id)

#17    
#ViewListing => [ViewListingController]
class viewListingController: 
    def get(self, user_id, listing_id):
        
        listing = Listing.get_listing_by_id(listing_id)
        if listing:
            View.create_view(user_id, listing_id)
            return listing
        else:
            return False
#18        
#DisplaySell => [DisplaySellController]
class displaySellController: 
    def get(self):
        return Listing.get_all_listings()
    
#19
#CreateListing => [CreateListingController]
class createListingController:
    def get(self, title, description, type, price, bedrooms, 
             bathrooms, size_sqft, location, file_path, user_email, agent_id):
        
        user = User.get_user_by_email(user_email)

        if user:
            return Listing.create_listing(title, description, type, price, bedrooms, 
                                        bathrooms, size_sqft, location, file_path, user.id, agent_id)
        else:
            return None

#20
#DisplayUpdateListing => [DisplayUpdateListingController]
class displayUpdateListingController:
    def get(self, listing_id):
        return Listing.get_listing_by_id(listing_id)

#21
#UpdateListing => [UpdateListingController]
class updateListingController:
    def get(self, listing_id, title, description, type, price, 
             bedrooms, bathrooms, size_sqft, location, file_path):
        
        return Listing.update_listing(listing_id, title, description, type, price, 
                                      bedrooms, bathrooms, size_sqft, location, file_path)

#22
#UpdateListingStatus => [UpdateListingStatusController]
class updateListingStatusController:
    def get(self, listing_id):
        return Listing.update_status(listing_id)
    
#23
#DeleteListing => DeleteListingController
class deleteListingController:
    def get(self, listing_id):
        return Listing.delete_listing(listing_id)
    
#24
#DisplayFindAgent => [DisplayFindAgentController]
class displayFindAgentController:
    def get(self):
        return Listing.get_all_listings_with_agents()
    
#25
#ViewAgent => [ViewAgentController]    
class viewAgentController:
    def get(self, agent_id):
        return Agent.get_agent_by_id(agent_id), Rating.get_rating_by_agent(agent_id), Review.get_rating_by_agent(agent_id)
    
#26    
#CreateRating => [CreateRatingController]
class createRatingController:
    def get(self, agent_id, user_id, rating_value):

        return Rating.create_rating(rating_value, user_id, agent_id), Agent.get_agent_by_id(agent_id)
        
#27        
#CreateReview => [CreateReviewController]
class createReviewController:
    def get(self, agent_id, user_id, review_value):

        return Review.create_review(review_value, user_id, agent_id), Agent.get_agent_by_id(agent_id)

#28
#DeleteRating => [DeleteRatingController]
class deleteRatingController:
    def get(self, agent_id, user_id):

        return Rating.delete_rating(user_id, agent_id), Agent.get_agent_by_id(agent_id)

#29
#DeleteReview => [DeleteReviewController]
class deleteReviewController:
    def get(self, agent_id, user_id):

        return Review.delete_review(user_id, agent_id), Agent.get_agent_by_id(agent_id)
    
#30
#DisplayUserPage => [DisplayUserController]
class displayUserController:
    def get(self):
        return User.get_all_users()

#31    
#UpdateUser => [UpdateUserController]
class updateUserController:
    def get(self, user_id, email, first_name, last_name):
        return User.update_user(user_id, email, first_name, last_name)

#32
#UpdateUserStatus => [UpdateUserStatusController]
class updateUserStatusController:
    def get(self, user_id):
        return User.update_status(user_id)

#33
#SearchUser => [SearchUserController]
class searchUserController:
    def get(self, search_query):
        return User.search_user(search_query)

#34
#DisplayProfilePage => [DisplayProfileController]
class displayProfileController:
    def get(self):
        return Profile.get_all_profiles()

#35
#CreateProfile => [CreateProfileController]
class createProfileController:
    def get(self, name, description):
        return Profile.create_profile(name, description)

#36
#UpdateProfle => [UpdateProfileController]
class updateProfileController:
    def get(self, profile_id, name, description):
        return Profile.update_profile(profile_id, name, description)

#37
#DeleteProfile => [DeleteProfileController]
class deleteProfileController:
    def get(self, profile_id):
        return Profile.delete_profile(profile_id)

#38    
#SearchProfile => [SearchProfileController]
class searchProfileController:
    def get(self, search_query):
        return Profile.search_profile(search_query)
    
# class createViewCountController:
#     def get(self, date_created, user_id, listing_id):
#         return View.create_view2(date_created, user_id, listing_id)
    
# class createShortlistController:
#     def get(self, date_created, user_id, listing_id):
#         return Shortlist.create_shortlist(date_created, user_id, listing_id)