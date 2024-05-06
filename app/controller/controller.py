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