from app.entity.entity import *

class retrieveUserByEmailController:
    def get(self, email):
        return User.get_user_by_email(email)
    
class retrieveAllProfileController:
    def get(self):
        return Profile.get_all_profiles()
    
class retrieveProfileByIdController:
    def get(self, profile_id):
        return Profile.get_profile_id(profile_id)
    
class retrieveCeaController:
    def get(self, cea_registration_no):
        return Agent.get_cea_no(cea_registration_no)
        
class createUserController:
    def get(self, email, fname, lname, password, profileId):
        return User.create_user(email, fname, lname, password, profileId)
    
class createAgentController:
    def get(self, cea_registration_no, agency_license_no, userId):
        return Agent.create_agent(cea_registration_no, agency_license_no, userId)
    
class updateUserController:
    def get(self, userid, email, fname, lname):
        return User.update_user(userid, email, fname, lname)
    
class updatePasswordController:
    def get(self,userid,password):
        return User.update_password(userid,password)
    
class retrieveUserByIdController:
    def get(self, userid):
        return User.get_user_id(userid)

class retrieveListingByAgentController:
    def get(self,agentId):
        return Listing.get_listing_by_agent(agentId)
    
class retrieveListingByUserController:
    def get(self,userId):
        return Listing.get_listing_by_user(userId)

class retrieveViewsInPeriodController:
    def get(self,listingId,start_date,end_date):
        return View.get_views_in_period(listingId,start_date,end_date)
    
class retrieveShortlistInPeriodController:
    def get(self,listingId,start_date,end_date):
        return Shortlist.get_shortlists_in_period(listingId,start_date,end_date)

class retrieveProfileByNameController:
    def get(self,name):
        return Profile.get_profile_name(name)

class createProfileController:
    def get(self,name,description):
        return Profile.create_profile(name, description)

class updateProfileController:
    def get(self,profileId, name, description):
        return Profile.update_profile(profileId, name, description)

class deleteProfileController:
    def get(self,id):
        return Profile.delete_profile(id)
    
class retrieveUserController:
    def get(self):
        return User.get_all_users()

class updateUserStatusController:
    def get(self,id):
        return User.update_status(id)
    
class searchUserController:
    def get(self,searchQuery):
        return User.search_user(searchQuery)
    
class retrieveAllListingController:
    def get(self):
        return Listing.get_all_listings()

class searchListingLocationController:
    def get(self,searchQuery):
        return Listing.search_listing_by_location(searchQuery)

class searchListingTypeController:
    def get(self,type):
        return Listing.search_listing_by_type(type)

class searchListingByPriceRangeController:
    def get(self,minPrice,maxPrice):
        return Listing.search_by_price_range(minPrice,maxPrice)

class searchListingByMinPriceController:
    def get(self,minPrice):
        return Listing.search_by_min_price(minPrice)

class searchListingByMaxPriceController:
    def get(self,maxPrice):
        return Listing.search_by_max_price(maxPrice)
    
class searchListingByBedrooms:
    def get(self,bedrooms):
        return Listing.search_by_bedrooms(bedrooms)

class createListingController:
    def get(self,title,description,type,price,bedrooms,bathrooms,sizeSqft,location,filePath,userId,agentId):
        return Listing.create_listing(title, description, type, price, bedrooms, 
                                    bathrooms, sizeSqft, location, filePath, userId, agentId)

class retrieveListingByIdController:
    def get(self,id):
        return Listing.get_listing_id(id)

class updateListingController:
    def get(self,id,title,description,type,price,bedrooms,bathrooms,sizeSqft,location,filePath):
        return Listing.update_listing(id, title, description, type, price, bedrooms, bathrooms, sizeSqft, location, filePath)
    
class updateListingStatusByIdController:
    def get(self,id):
        return Listing.update_status(id)

class deleteListingByIdController:
    def get(self,id):
        return Listing.delete_listing(id)

class retrieveShortlistByUserIdController:
    def get(self,userId,id):
        return Shortlist.get_shortlist(userId, id)

class deleteShortlistByUserIDController:
    def get(self,userId,listingId):
        return Shortlist.delete_shortlist(userId,listingId)
    
class createShortlistByUserIDController:
    def get(self,userId,id):
        return Shortlist.create_shortlist(userId, id)

class retrieveListingWithAgentsController:
    def get(self):
        return Listing.get_all_listings_with_agents()

class retrieveAgentByIdController:
    def get(self,agentId):
        return Agent.get_agent_id(agentId)

class retrieveReviewByIdController:
    def get(self,agentId,userId):
        return Review.get_review(agentId,userId)

class createReviewByIdController:
    def get(self,agentId,userId):
        return Review.create_review(agentId,userId)
    
class createUpdateRatingController:
    def get(self,ratingValue,reviewId):
        return Rating.create_or_update_rating(ratingValue,reviewId)

class createUpdateCommentController:
    def get(self,commentValue,reviewId):
        return Comment.create_or_update_comment(commentValue, reviewId)