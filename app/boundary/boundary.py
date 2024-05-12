# app/boundary/boundary.py
from flask import Blueprint, render_template, request, current_app, flash, redirect, url_for, send_from_directory, jsonify
from app.controller.controller import *
from flask.views import MethodView
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta

boundary = Blueprint("boundary", __name__)

#1
#[LoginManager] => LoginManagerController
class loginManager: #API
    def get(id):
        return loginManagerController.get(id)
    
#FileDirectory
class fileDirectory(MethodView): #API
    def get(self, filename):
        return send_from_directory("../media", filename)

boundary.add_url_rule("/media/<path:filename>", view_func=fileDirectory.as_view("media"))

#2
#[DisplayLandingPage] => DisplayLandingController
class displayLandingPage(MethodView):
    def get(self):
        listings = displayLandingController().get()

        return render_template("user/landingPage.html", user=current_user, listings=listings)
    
boundary.add_url_rule("/", view_func=displayLandingPage.as_view("displayLanding"))

#[DisplayLoginPage]
class displayLoginPage(MethodView): #57, 69, 83, 92
    def get(self):

        return render_template("user/loginPage.html", user=current_user)

boundary.add_url_rule("/login", view_func=displayLoginPage.as_view("displayLogin"))

#3
#[LoginUser] => LoginUserController
class loginUser(MethodView): #57, 69, 83, 92
    def post(self):
        email = request.form["email"]
        password = request.form["password"]

        user = loginUserController().get(email)
        if user:
            if user.status.value == "ENABLED":
                if check_password_hash(user.password, password):
                    login_user(user, remember=True)
                    flash("Logged in successfully!", category="success")
                    return redirect(url_for("boundary.displayHome"))
                
                else:
                    flash("Incorrect password, try again.", category="error")
            else:
                flash("Your account is disabled. Please contact support.", category="error")
        else:
            flash("User does not exist.", category="error")

        return redirect(url_for("boundary.displayLogin"))
    
boundary.add_url_rule("/login", view_func=loginUser.as_view("loginUser"))

#[LogoutUser]
class logoutUser(MethodView): #58, 70, 84, 93
    @login_required
    def get(self):
        logout_user()
        return redirect(url_for("boundary.displayLogin"))
    
boundary.add_url_rule("/logout", view_func=logoutUser.as_view("logoutUser"))

#4
#[DisplaySignupPage] => DisplaySignupController
class displaySignupPage(MethodView): #68, 82, 91
    def get(self):
        profiles = displaySignupController().get()

        return render_template("user/signupPage.html", user=current_user, profiles=profiles)
    
boundary.add_url_rule("/sign-up", view_func=displaySignupPage.as_view("displaySignup"))

#5, 6
#[SignupUser] => CEAController
#             => SignupUserController
class signupUser(MethodView): #68, 82, 91
    def post(self):
        email = request.form["email"]
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        password = request.form["password"]
        verify_password = request.form["verify_password"]
        profile_id = request.form["profile"]

        cea_registration_no = request.form["cea_registration_no"]
        agency_license_no = request.form["agency_license_no"]

        if not email or not first_name or not last_name or not password or not verify_password:
            flash("All fields are required.", category="error")
   
        elif len(email) < 4:
            flash("Email must be greater than 3 characters.", category="error")
        
        elif len(first_name) < 2:
            flash("First name must be greater than 1 characters.", category="error")
        
        elif password != verify_password:
            flash("Passwords don\"t match.", category="error")
        
        elif len(password) < 7:
            flash("Passwords must be at least 7 characters.", category="error")
        
        else:

            agent = ceaController().get(cea_registration_no)

            if agent:
                flash("Agent with CEA registration number {} already exists.".format(cea_registration_no), category="error")
            
            else:
                new_user = signupUserController().get(email, first_name, last_name, generate_password_hash(password, method="pbkdf2:sha256"), 
                                               profile_id, cea_registration_no, agency_license_no)
                if new_user:
                    print(new_user)
                    login_user(new_user, remember=True)
                    flash("Account created!", category="success")
                    return redirect(url_for("boundary.displayBuy"))

                else:
                    flash("User already exists", category="error")

        return redirect(url_for("boundary.displaySignup"))
               
boundary.add_url_rule("/sign-up", view_func=signupUser.as_view("signupUser"))

#[DisplayUpdateAccount]
class displayUpdateAccount(MethodView): #71, 112, 113
    @login_required
    def get(self):

        return render_template("user/updateAccountPage.html", user=current_user)

boundary.add_url_rule("/update-account", view_func=displayUpdateAccount.as_view("displayUpdateAccount"))

#7
#[UpdateUserAccount] => UpdateUserAccountController
class updateUserAccount(MethodView): #72, 85, 94
    @login_required
    def post(self):
        email = request.form["email"]
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]

        if not email or not first_name or not last_name:
            flash("All fields are required.", category="error")
            return redirect(url_for("boundary.displayUpdateAccount"))

        update_user = updateUserAccountController().get(current_user.id, email, first_name, last_name)

        if update_user is None:
            flash("User not found.", category="error")

        elif update_user is False:
            flash("User email already exists.", category="error")

        else:
            flash("User updated successfully!", category="success")

        return redirect(url_for("boundary.displayUpdateAccount"))
    
boundary.add_url_rule("/update-account", view_func=updateUserAccount.as_view("updateUserAccount"))

#[DisplayUpdatePassword]
class displayUpdatePassword(MethodView): #71, 112, 113
    @login_required
    def get(self):

        return render_template("user/updatePasswordPage.html", user=current_user)
    
boundary.add_url_rule("/update-password", view_func=displayUpdatePassword.as_view("displayUpdatePassword"))

#8
#[UpdateUserPassword] => UpdateUserPasswordController
class updateUserPassword(MethodView): #72, 85, 94
    @login_required
    def post(self):
        current_password = request.form["current_password"]
        new_password = request.form["new_password"]
        confirm_password = request.form["confirm_password"]

        if not current_password or not new_password or not confirm_password:
            flash("All fields are required.", category="error")

        elif not check_password_hash(current_user.password, current_password):
            flash("Incorrect current password.", category="error")
        
        elif new_password != confirm_password:
            flash("New passwords do not match.", category="error")
        
        elif len(new_password) < 7:
            flash("New password must be at least 7 characters.", category="error")
        
        else:
            update_password = updateUserPasswordController().get(current_user.id, generate_password_hash(new_password, method="pbkdf2:sha256"))

            if update_password:
                flash("Password changed successfully!", category="success")

            else:
                flash("User not found.", category="error")

        return redirect(url_for("boundary.displayUpdatePassword"))
    
boundary.add_url_rule("/update-password", view_func=updateUserPassword.as_view("updateUserPassword"))

#9, 10
#[DisplayHomePage] => DisplayAdminHomeController
#                  => DisplayHomeController
class displayHomePage(MethodView):
    @login_required
    def get(self):
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)

        if current_user.profile.name == "Admin":

            listings, users = displayAdminHomeController().get()
            
            return render_template("admin/homePage.html", user=current_user, listings=listings, users=users)
        
        else:

            views, shortlists = displayHomeController().get(current_user, start_date, end_date)

            views_count = {}
            shortlists_count = {}

            for view in views:
                date_str = view.date_created.strftime("%Y-%m-%d")
                views_count[date_str] = views_count.get(date_str, 0) + 1

            for shortlist in shortlists:
                date_str = shortlist.date_created.strftime("%Y-%m-%d")
                shortlists_count[date_str] = shortlists_count.get(date_str, 0) + 1

            labels = list(views_count.keys())
            views_data = list(views_count.values())
            shortlists_data = [shortlists_count.get(date, 0) for date in labels]

            table_data = [{"date": label, "shortlists": shortlists_count.get(label, 0), "views": views_count.get(label, 0)} for label in labels]

            views_last_week = sum(views_data[:-1]) if views_data else 0
            views_this_week = sum(views_data)
            shortlists_last_week = sum(shortlists_data[:-1]) if shortlists_data else 0
            shortlists_this_week = sum(shortlists_data)
            shortlists_this_week = sum(shortlists_data)

            percentage_change_views = ((views_this_week - views_last_week) / views_last_week) * 100 if views_last_week != 0 else 0
            percentage_change_shortlists = ((shortlists_this_week - shortlists_last_week) / shortlists_last_week) * 100 if shortlists_last_week != 0 else 0

            return render_template("user/homePage.html", user=current_user, table_data=table_data, labels=labels,
                                   views_data=views_data, shortlists_data=shortlists_data,
                                   percentage_change_views=percentage_change_views,
                                   percentage_change_shortlists=percentage_change_shortlists)
    
boundary.add_url_rule("/home", view_func=displayHomePage.as_view("displayHome"))

#11
#[DisplayBuyPage] => DisplayBuyController
class displayBuyPage(MethodView):
    @login_required
    def get(self):
        listings = displayBuyController().get()

        return render_template("user/buyPage.html", user=current_user, listings=listings)
    
boundary.add_url_rule("/buy", view_func=displayBuyPage.as_view("displayBuy"))

#12
#[SearchListingLocation] => SearchListingLocationController
class searchListingLocation(MethodView):
    @login_required
    def get(self):
        search_query = request.args.get("search")
        filtered_listings = searchListingLocationController().get(search_query)

        return render_template("user/buyPage.html", user=current_user, listings=filtered_listings)
    
boundary.add_url_rule("/search-location", view_func=searchListingLocation.as_view("searchListingLocation"))

#13
#[SearchListingType] => SearchListingTypeController
class searchListingType(MethodView):
    @login_required
    def get(self):
        type = request.args.get("type")

        if type == "All" or type == "clear":
            return redirect(url_for("boundary.displayBuy"))

        else:
            filtered_listings = searchListingTypeController().get(type)

        return render_template("user/buyPage.html", user=current_user, listings=filtered_listings)
    
boundary.add_url_rule("/search-type", view_func=searchListingType.as_view("searchListingType"))

#14
#[SearchListingPrice] => SearchListingPriceController
class searchListingPrice(MethodView): 
    @login_required
    def get(self):
        min_price = request.args.get("minPrice")
        max_price = request.args.get("maxPrice")

        filtered_listings = searchListingPriceController().get(min_price, max_price)

        return render_template("user/buyPage.html", user=current_user, listings=filtered_listings)
    
boundary.add_url_rule("/search-price", view_func=searchListingPrice.as_view("searchListingPrice"))

#15
#[SearchListingBedroom] => SearchListingBedroomController
class searchListingBedroom(MethodView): 
    @login_required
    def get(self):
        bedrooms = request.args.get("bedrooms")

        if bedrooms == "clear":
            return redirect(url_for("boundary.displayBuy"))
        
        else:
            filtered_listings = searchListingBedroomController().get(bedrooms)

        return render_template("user/buyPage.html", user=current_user, listings=filtered_listings)
    
boundary.add_url_rule("/search-bedrooms", view_func=searchListingBedroom.as_view("searchListingBedrooms"))

#16
#[ShortlistListing] => ShortlistListingController
class shortlistListing(MethodView): #77, 78
    @login_required
    def post(self, listing_id):
        listing, shortlist = shortlistListingController().get(current_user.id, listing_id)
        
        if not listing:
            return jsonify({"error": "Listing does not exist."}, 400)

        return jsonify({"shortlists": len(listing.shortlists), "shortlisted": current_user.id in map(lambda x: x.user_id, listing.shortlists)})
    
boundary.add_url_rule("/shortlist-listing/<int:listing_id>", view_func=shortlistListing.as_view("shortlistListing"))

#ViewShortlistListing
class viewShortlistListing(MethodView):
    @login_required
    def get(self):

        return render_template("user/myActivitiesPage.html", user=current_user)

boundary.add_url_rule("/my-activities", view_func=viewShortlistListing.as_view("viewShortlistListing"))

#17
#[ViewListing] => ViewListingController
class viewListing(MethodView): 
    @login_required
    def get(self, title, listing_id):
        listing = viewListingController().get(current_user.id, listing_id)

        if not listing:
            flash("Listing does not exist.", category="error")
            return redirect(url_for("boundary.displayBuy"))

        return render_template("user/listingPage.html", user=current_user, listing=listing)
    
boundary.add_url_rule("/listing/<string:title>-<int:listing_id>", view_func=viewListing.as_view("viewListing"))

#18
#[DisplaySellPage] => DisplaySellController
class displaySellPage(MethodView): 
    @login_required
    def get(self):
        listings = displaySellController().get()

        return render_template("user/sellPage.html", user=current_user, listings=listings)

boundary.add_url_rule("/sell", view_func=displaySellPage.as_view("displaySell"))

#DisplayCreateListing done
class displayCreateListing(MethodView):
    @login_required
    def get(self):

        return render_template("agent/createListingPage.html", user=current_user)
    
boundary.add_url_rule("/create-listing", view_func=displayCreateListing.as_view("displayCreateListing"))

#19
#[CreateListing] => CreateListingController
class createListing(MethodView): 
    @login_required
    def post(self):
        title = request.form["title"]
        description = request.form["description"]
        type = request.form["type"]
        price = request.form["price"]
        bedrooms = request.form["bedrooms"]
        bathrooms = request.form["bathrooms"]
        size_sqft = request.form["size_sqft"]
        location = request.form["location"]
        user_email = request.form["user_email"]
        photo = request.files["photo"]

        if all([title, description, type, price, bedrooms, bathrooms, size_sqft, location, user_email]):

            if photo:
                file_name = secure_filename(photo.filename)
                file_path = f"./media/{file_name}"

                new_listing = createListingController().get(title, description, type, price, bedrooms, 
                                                            bathrooms, size_sqft, location, file_path, user_email, current_user.agent.id)
                
                if new_listing:
                    photo.save(file_path)
                    flash("Listing created!", category="success")
                    return redirect(url_for("boundary.displaySell"))

                elif new_listing is None:
                    flash("User with provided email does not exist.", category="error")
                
                else:
                    flash("Error creating listing.", category="error")

            else:
                flash("Please insert a photo.", category="error")

        else:
            flash("All fields are required.", category="error")

        return redirect(url_for("boundary.displayCreateListing"))
                
boundary.add_url_rule("/create-listing", view_func=createListing.as_view("createListing"))

#20
#[DisplayUpdateListing] => DisplayUpdateListingController
class displayUpdateListing(MethodView):
    @login_required
    def get(self, listing_id):
        listing = displayUpdateListingController().get(listing_id)

        return render_template("agent/updateListingPage.html", user=current_user, listing=listing)
    
boundary.add_url_rule("/update-listing/<int:listing_id>", view_func=displayUpdateListing.as_view("displayUpdateListing"))

#21
#UpdateListing => UpdateListingController
class updateListing(MethodView):
    @login_required
    def post(self, listing_id):
        title = request.form["title"]
        description = request.form["description"]
        type = request.form["type"]
        price = request.form["price"]
        bedrooms = request.form["bedrooms"]
        bathrooms = request.form["bathrooms"]
        size_sqft = request.form["size_sqft"]
        location = request.form["location"]
        photo = request.files["photo"]

        if all([title, description, type, price, bedrooms, bathrooms, size_sqft, location]):        

            if photo:
                file_name = secure_filename(photo.filename)
                file_path = f"./app/media/{file_name}"
                photo.save(file_path)

            else:
                file_path = None

            update_listing = updateListingController().get(listing_id, title, description, type, price, bedrooms, 
                                                bathrooms, size_sqft, location, file_path)
                
            if update_listing: 
                flash("Listing updated!", category="success")
                return redirect(url_for("boundary.displaySell"))
            
            else:
                flash("Listing not found.", category="error")

        else:
            flash("All fields are required.", category="error")

        return redirect(url_for("boundary.displaySell"))                
    
boundary.add_url_rule("/update-listing/<int:listing_id>", view_func=updateListing.as_view("updateListing"))

#22
#[UpdateListingStatus] => UpdateListingStatusController
class updateListingStatus(MethodView):
    @login_required
    def post(self, listing_id):
        
        update_lstatus = updateListingStatusController().get(listing_id)

        if update_lstatus is None:
            flash("Listing not found.", category="error")

        else:
            flash(f"Listing updated to {update_lstatus.value}.", category="success")

        return redirect(url_for("boundary.sell"))
    
boundary.add_url_rule("/update-lstatus/<int:listing_id>", view_func=updateListingStatus.as_view("updateListingStatus"))

#23
#[DeleteListing] => DeleteListingController
class deleteListing(MethodView):
    @login_required
    def post(self, listing_id):
        delete_listing = deleteListingController().get(listing_id)

        if delete_listing:
            flash("Listing deleted successfully", category="success")
        
        else:
            flash("An error occurred while deleting the listing", category="error")

        return redirect(url_for("boundary.sell"))
    
boundary.add_url_rule("/delete-listing/<int:listing_id>", view_func=deleteListing.as_view("deleteListing"))

#24
#[DisplayFindAgent] => DisplayFindAgentController
class displayFindAgent(MethodView):
    @login_required
    def get(self):
        query_result = displayFindAgentController().get()
        types = self.get_types(query_result)

        return render_template("user/findAgentPage.html", user=current_user, types=types)
    
    def get_types(self, query_result):
        types = {}
        for listing, agent in query_result:
            if listing.type not in types:
                types[listing.type] = []
            
            if agent not in types[listing.type]:
                types[listing.type].append(agent)

        return types
    
boundary.add_url_rule("/find-agent", view_func=displayFindAgent.as_view("displayFindAgent"))

#25
#[ViewAgent] => ViewAgentController
class viewAgent(MethodView):
    @login_required
    def get(self, first_name, last_name, agent_id):

        agent, reviews = viewAgentController().get(agent_id)

        return render_template("user/agentPage.html", user=current_user, agent=agent, reviews=reviews)
    
boundary.add_url_rule("/find-agent/<string:first_name>-<string:last_name>-<int:agent_id>", view_func=viewAgent.as_view("viewAgent"))

#26
#[CreateRating] => CreateRatingController
class createRating(MethodView):
    @login_required
    def post(self, agent_id):
        rating_value = request.form["rating"]

        rating, agent = createRatingController().get(agent_id, current_user.id, rating_value)

        if rating is False:
            flash("An error occurred while rating the agent.", category="error")

        return redirect(url_for("boundary.viewAgent", first_name=agent.user.first_name, last_name=agent.user.last_name, agent_id=agent_id))
    
boundary.add_url_rule("/create-rating/<int:agent_id>", view_func=createRating.as_view("createRating"))

#27
#[CreateReview] => CreateReviewController
class createReview(MethodView):
    @login_required
    def post(self, agent_id):
        review_value = request.form["review"]

        review, agent = createReviewController().get(agent_id, current_user.id, review_value)

        if review is False:
            flash("An error occurred while rating the agent.", category="error")

        return redirect(url_for("boundary.viewAgent", first_name=agent.user.first_name, last_name=agent.user.last_name, agent_id=agent_id))
    
boundary.add_url_rule("/create-review/<int:agent_id>", view_func=createReview.as_view("createReview"))

#28
#DeleteRating => DeleteRatingController
class deleteRating(MethodView):
    @login_required
    def post(self, agent_id):
        rating, agent = deleteRatingController().get(agent_id, current_user.id)

        if rating:
            flash("Rating deleted successfully!", category="success")

        else:
            flash("An error occurred while deleting the rating.", category="error")

        return redirect(url_for("boundary.viewAgent", first_name=agent.user.first_name, last_name=agent.user.last_name, agent_id=agent_id))

boundary.add_url_rule("/delete-rating/<int:agent_id>", view_func=deleteRating.as_view("deleteRating"))

#29
#[DeleteReview] => DeleteReviewController
class deleteReview(MethodView):
    @login_required
    def post(self, agent_id):
        review, agent = deleteReviewController().get(agent_id, current_user.id)

        if review:
            flash("Review deleted successfully!", category="success")

        else:
            flash("An error occurred while deleting the review.", category="error")

        return redirect(url_for("boundary.viewAgent", first_name=agent.user.first_name, last_name=agent.user.last_name, agent_id=agent_id))
    
boundary.add_url_rule("/delete-review/<int:agent_id>", view_func=deleteReview.as_view("deleteReview"))

#30
#[DisplayUserPage] => DisplayUserController
class displayUserPage(MethodView):
    @login_required
    def get(self):
        users = displayUserController().get()

        return render_template("admin/userPage.html", user=current_user, users=users)
    
boundary.add_url_rule("/user", view_func=displayUserPage.as_view("displayUser"))

#31
#[UpdateUser] => UpdateUserController
class updateUser(MethodView):
    @login_required
    def post(self):
        user_id = request.form["user_id"]
        email = request.form["email"]
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]

        update_user = updateUserController().get(user_id, email, first_name, last_name)
        if update_user is None:
            flash("User not found.", category="error")

        elif update_user is False:
            flash("User email already exists.", category="error")

        else:
            flash("User updated successfully.", category="success")        

        return redirect(url_for("boundary.displayUser"))
    
boundary.add_url_rule("/update-user", view_func=updateUser.as_view("updateUser"))

#32
#[UpdateUserStatus] => UpdateUserStatusController
class updateUserStatus(MethodView):
    @login_required
    def post(self, user_id):
        
        update_ustatus = updateUserStatusController().get(user_id)

        if update_ustatus is None:
            flash("User not found.", category="error")

        else:
            flash(f"User status updated to {update_ustatus.value}.", category="success")        

        return redirect(url_for("boundary.displayUser"))
    
boundary.add_url_rule("/update-ustatus/<int:user_id>", view_func=updateUserStatus.as_view("updateUserStatus"))

#33
#[SearchUser] => SearchUserController
class searchUser(MethodView):
    @login_required
    def get(self):

        search_query = request.args.get("search")
        filtered_users = searchUserController().get(search_query)

        return render_template("admin/userPage.html", user=current_user, users=filtered_users)
    
boundary.add_url_rule("/search-user", view_func=searchUser.as_view("searchUser"))

#34
#[DisplayProfilePage] => DisplayProfileController
class displayProfilePage(MethodView):
    @login_required
    def get(self):
        profiles = displayProfileController().get()

        return render_template("admin/profilePage.html", user=current_user, profiles=profiles)
    
boundary.add_url_rule("/profile", view_func=displayProfilePage.as_view("displayProfile"))

#35
#[CreateProfile] => CreateProfileController
class createProfile(MethodView):
    @login_required
    def post(self):
        name = request.form["name"]
        description = request.form["description"]

        create_profile = createProfileController().get(name, description)
        
        if create_profile:
            flash("Profile created successfully.", category="success")
        
        else:    
            flash("Profile name already exists.", category="error")

        return redirect(url_for("boundary.displayProfile"))
    
boundary.add_url_rule("/create-profile", view_func=createProfile.as_view("createProfile"))

#36
#[UpdateProfile] => UpdateProfileController
class updateProfile(MethodView):
    @login_required
    def post(self):
        profile_id = request.form["profile_id"]
        name = request.form["name"]
        description = request.form["description"]

        update_profile = updateProfileController().get(profile_id, name, description)
        if update_profile is None:
            flash("Profile not found.", category="error")

        elif update_profile is False:
            flash("Profile name already exists.", category="error")

        else:
            flash("Profile updated successfully.", category="success")
        
        return redirect(url_for("boundary.displayProfile"))
    
boundary.add_url_rule("/update-profile", view_func=updateProfile.as_view("updateProfile"))
    
#37
#[DeleteProfile] => DeleteProfileController
class deleteProfile(MethodView):
    @login_required
    def post(self, profile_id):
        
        delete_profile = deleteProfileController().get(profile_id)
        if delete_profile:
            flash("Profile deleted successfully!", category="success")

        else:
            flash("An error occurred while deleting the profile.", category="error")

        return redirect(url_for("boundary.displayProfile"))

boundary.add_url_rule("/delete-profile/<int:profile_id>", view_func=deleteProfile.as_view("deleteProfile"))

#38
#[SearchProfile] => SearchProfileController
class searchProfile(MethodView):
    @login_required
    def get(self):

        search_query = request.args.get("search")
        filtered_profiles = searchProfileController().get(search_query)

        return render_template("admin/profilePage.html", user=current_user, profiles=filtered_profiles)

boundary.add_url_rule("/search-profile", view_func=searchProfile.as_view("searchProfile"))