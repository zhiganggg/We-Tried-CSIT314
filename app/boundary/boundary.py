# app/boundary/boundary.py
from flask import Blueprint, render_template, request, current_app, flash, redirect, url_for, send_from_directory, jsonify
from app.controller.controller import *
from flask.views import MethodView
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta

boundary = Blueprint("boundary", __name__)

#LoginManger API
class loginManager:
    def get(id):
        return loginManagerController.get(id)
    
#FileDirectory API
class fileDirectory(MethodView):
    def get(self, filename):
        return send_from_directory("../media", filename)

boundary.add_url_rule('/media/<path:filename>', view_func=fileDirectory.as_view('media'))

#57, 83
#LoginPage
class loginPage(MethodView):    
    def get(self):

        return render_template("user/loginPage.html", user=current_user)
    
    def post(self):
        email = request.form["email"]
        password = request.form["password"]

        user = loginController().get(email)
        if user:
            if user.status.value == "ENABLED":
                if check_password_hash(user.password, password):
                    login_user(user, remember=True)
                    flash("Logged in successfully!", category="success")
                    return redirect(url_for("boundary.home"))
                
                else:
                    flash("Incorrect password, try again.", category="error")
            else:
                flash("Your account is disabled. Please contact support.", category="error")
        else:
            flash("User does not exist.", category="error")

        return render_template("user/loginPage.html", user=current_user)

boundary.add_url_rule("/login", view_func=loginPage.as_view("login"))

#LogoutPage
class logoutPage(MethodView):
    @login_required
    def get(self):
        logout_user()
        return redirect(url_for("boundary.login"))
    
boundary.add_url_rule("/logout", view_func=logoutPage.as_view("logout"))

#SignupPage
class signupPage(MethodView):
    def get(self):
        profiles = profileController().get()

        return render_template("user/signupPage.html", user=current_user, profiles=profiles)
    
    def post(self):
        profiles = profileController().get()

        email = request.form["email"]
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        password = request.form["password"]
        verify_password = request.form["verify_password"]
        profile_id = request.form["profile"]

        cea_registration_no = request.form["cea_registration_no"]
        agency_license_no = request.form["agency_license_no"]
   
        if len(email) < 4:
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
                new_user = signupController().get(email, first_name, last_name, generate_password_hash(password, method="pbkdf2:sha256"), 
                                               profile_id, cea_registration_no, agency_license_no)
                if new_user:
                    login_user(new_user, remember=True)
                    flash("Account created!", category="success")
                    return redirect(url_for("boundary.buy"))

                else:
                    flash("User already exists", category="error")

            return render_template("user/signupPage.html", user=current_user, profiles=profiles)
               
boundary.add_url_rule("/sign-up", view_func=signupPage.as_view("signup"))

#UpdateAccount
class updateAccount(MethodView):
    @login_required
    def get(self):

        return render_template("user/updateAccountPage.html", user=current_user)
    
    @login_required
    def post(self):
        email = request.form["email"]
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]

        update_user = updateUserController().get(current_user.id, email, first_name, last_name)

        if update_user is None:
            flash("User not found.", category="error")

        elif update_user is False:
            flash("User email already exists.", category="error")

        else:
            flash("User updated successfully.", category="success")

        return render_template("user/updateAccountPage.html", user=current_user)
    
boundary.add_url_rule("/update-account", view_func=updateAccount.as_view("updateAccount"))

#UpdatePassword
class updatePassword(MethodView):
    @login_required
    def get(self):

        return render_template("user/updatePasswordPage.html", user=current_user)

    @login_required
    def post(self):
        current_password = request.form["current_password"]
        new_password = request.form["new_password"]
        confirm_password = request.form["confirm_password"]

        if not check_password_hash(current_user.password, current_password):
            flash("Incorrect current password.", category="error")
        
        elif new_password != confirm_password:
            flash("New passwords do not match.", category="error")
        
        elif len(new_password) < 7:
            flash("New password must be at least 7 characters.", category="error")
        
        else:
            update_password = updateUserPasswordController().get(current_user.id, generate_password_hash(new_password, method="pbkdf2:sha256"))

            if update_password:
                flash("Password changed successfully.", category="success")

            else:
                flash("User not found.", category="error")

        return render_template("user/updatePasswordPage.html", user=current_user)
    
boundary.add_url_rule("/update-password", view_func=updatePassword.as_view("updatePassword"))

#HomePage
class homePage(MethodView):
    @login_required
    def get(self):
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)

        if current_user.profile.name == "Admin":

            listings = viewListingsController().get()

            users = userController().get()
            
            return render_template("admin/homePage.html", user=current_user, listings=listings, users=users)
        
        else:

            user_listings = userListingController().get(current_user)

            listing_ids = [listing.id for listing in user_listings]

            views = getViewsInPeriodController().get(listing_ids, start_date, end_date)
            shortlists = getShortlistsInPeriodController().get(listing_ids, start_date, end_date)

            views_count = {}
            shortlists_count = {}

            for view in views:
                date_str = view.date_created.strftime('%Y-%m-%d')
                views_count[date_str] = views_count.get(date_str, 0) + 1

            for shortlist in shortlists:
                date_str = shortlist.date_created.strftime('%Y-%m-%d')
                shortlists_count[date_str] = shortlists_count.get(date_str, 0) + 1

            labels = list(views_count.keys())
            views_data = list(views_count.values())
            shortlists_data = [shortlists_count.get(date, 0) for date in labels]

            table_data = [{'date': label, 'shortlists': shortlists_count.get(label, 0), 'views': views_count.get(label, 0)} for label in labels]

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
    
boundary.add_url_rule("/home", view_func=homePage.as_view("home"))

#ProfilePage
class profilePage(MethodView):
    @login_required
    def get(self):
        profiles = profileController().get()

        return render_template("admin/profilePage.html", user=current_user, profiles=profiles)
    
boundary.add_url_rule("/profile", view_func=profilePage.as_view("profile"))

#CreateProfile
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

        return redirect(url_for("boundary.profile"))
    
boundary.add_url_rule("/create-profile", view_func=createProfile.as_view("createProfile"))

#UpdateProfile
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
        
        return redirect(url_for("boundary.profile"))
    
boundary.add_url_rule("/update-profile", view_func=updateProfile.as_view("updateProfile"))
    
#DeleteProfile
class deleteProfile(MethodView):
    @login_required
    def post(self, profile_id):
        
        delete_profile = deleteProfileController().get(profile_id)
        if delete_profile:
            flash("Profile deleted successfully", category="success")

        else:
            flash("An error occurred while deleting the profile", category="error")

        return redirect(url_for("boundary.profile"))

boundary.add_url_rule("/delete-profile/<int:profile_id>", view_func=deleteProfile.as_view("deleteProfile"))

#SearchProfile
class searchProfile(MethodView):
    @login_required
    def get(self):

        search_query = request.args.get("search")
        filtered_profiles = searchProfileController().get(search_query)

        return render_template("admin/profilePage.html", user=current_user, profiles=filtered_profiles)

    
boundary.add_url_rule("/search-profile", view_func=searchProfile.as_view("searchProfile"))

#UserPage
class userPage(MethodView):
    @login_required
    def get(self):
        users = userController().get()

        return render_template("admin/userPage.html", user=current_user, users=users)
    
boundary.add_url_rule("/user", view_func=userPage.as_view("user"))

#UpdateUser
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

        return redirect(url_for("boundary.user"))
    
boundary.add_url_rule("/update-user", view_func=updateUser.as_view("updateUser"))

#UpdateUserStatus
class updateUserStatus(MethodView):
    @login_required
    def post(self, user_id):
        
        update_ustatus = updateUserStatusController().get(user_id)

        if update_ustatus is None:
            flash("User not found.", category="error")

        else:
            flash(f"User status updated to {update_ustatus.value}.", category="success")        

        return redirect(url_for("boundary.user"))
    
boundary.add_url_rule("/update-ustatus/<int:user_id>", view_func=updateUserStatus.as_view("updateUserStatus"))

#SearchUser
class searchUser(MethodView):
    @login_required
    def get(self):

        search_query = request.args.get("search")
        filtered_users = searchUserController().get(search_query)

        return render_template("admin/userPage.html", user=current_user, users=filtered_users)
    
boundary.add_url_rule("/search-user", view_func=searchUser.as_view("searchUser"))

#BuyPage
class buyPage(MethodView):
    @login_required
    def get(self):
        listings = viewListingsController().get()

        return render_template("user/buyPage.html", user=current_user, listings=listings)
    
boundary.add_url_rule("/buy", view_func=buyPage.as_view("buy"))

#SearchListingLocation
class searchListingLocation(MethodView):
    def get(self):
        search_query = request.args.get("search")
        filtered_listings = searchListingLocationController.get(search_query)

        return render_template("user/buyPage.html", user=current_user, listings=filtered_listings)
    
boundary.add_url_rule("/search-location", view_func=searchListingLocation.as_view("searchListingLocation"))

#SearchListingType
class searchListingType(MethodView):
    def get(self):
        type = request.args.get("type")

        if type == "All" or type == "clear":
            filtered_listings = viewListingsController().get()

        else:
            filtered_listings = searchListingTypeController().get(type)

        return render_template("user/buyPage.html", user=current_user, listings=filtered_listings)
    
boundary.add_url_rule("/search-type", view_func=searchListingType.as_view("searchListingType"))

#SearchListingPrice
class searchListingPrice(MethodView):
    def get(self):
        min_price = request.args.get("minPrice")
        max_price = request.args.get("maxPrice")

        filtered_listings = searchListingPriceController().get(min_price, max_price)

        return render_template("user/buyPage.html", user=current_user, listings=filtered_listings)
    
boundary.add_url_rule("/search-price", view_func=searchListingPrice.as_view("searchListingPrice"))

#SearchListingBedroom
class searchListingBedroom(MethodView):
    def get(self):
        bedrooms = request.args.get("bedrooms")

        if bedrooms == "clear":
            filtered_listings = viewListingsController().get()
        
        else:
            filtered_listings = searchListingBedroomController().get(bedrooms)

        return render_template("user/buyPage.html", user=current_user, listings=filtered_listings)
    
boundary.add_url_rule("/search-bedrooms", view_func=searchListingBedroom.as_view("searchListingBedrooms"))

#sellPage
class sellPage(MethodView):
    def get(self):
        listings = viewListingsController().get()

        return render_template("user/sellPage.html", user=current_user, listings=listings)

boundary.add_url_rule("/sell", view_func=sellPage.as_view("sell"))

#CreateListing
class createListing(MethodView):
    def get(self):

        return render_template("agent/createListingPage.html", user=current_user)
    
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

        if not title or not description or not type or not price or not bedrooms or not bathrooms or not size_sqft or not location or not user_email:
            flash("All fields are required.", category="error")
        
        else:
            photo = request.files["photo"]

            if not photo:
                flash("Please insert a photo.", category="error")
            
            else:
                file_name = secure_filename(photo.filename)
                file_path = f"./media/{file_name}"

                user = loginController().get(user_email)
                if not user:
                    flash("User with provided email does not exist.", category="error")

                else:
                    new_listing = createListingController().get(title, description, type, price, bedrooms, 
                                    bathrooms, size_sqft, location, file_path, user.id, current_user.agent.id)
                    
                    if not new_listing:
                        flash("Error creating listing.", category="error")

                    else:
                        photo.save(file_path)
                        flash("Listing created!", category="success")

                    return redirect(url_for("boundary.sell"))
                
boundary.add_url_rule("/create-listing", view_func=createListing.as_view("createListing"))

#UpdateListing
class updateListing(MethodView):
    def get(self, listing_id):
        listing = getListingController().get(listing_id)

        return render_template("agent/updateListingPage.html", user=current_user, listing=listing)
    
    def post(self, listing_id):
        title = request.form["title"]
        description = request.form["description"]
        type = request.form["type"]
        price = request.form["price"]
        bedrooms = request.form["bedrooms"]
        bathrooms = request.form["bathrooms"]
        size_sqft = request.form["size_sqft"]
        location = request.form["location"]

        if not title or not description or not type or not price or not bedrooms or not bathrooms or not size_sqft or not location:
            flash("All fields are required.", category="error")
        
        else:
            photo = request.files["photo"]

            if photo:
                file_name = secure_filename(photo.filename)
                file_path = f"./app/media/{file_name}"
                photo.save(file_path)
            
            else:
                file_path = None
            
            update_listing = updateListingController().get(listing_id, title, description, type, price, bedrooms, 
                                                    bathrooms, size_sqft, location, file_path)
            
            if update_listing is None:
                flash("Listing not found.", category="error")
            
            else:
                flash("Listing updated!", category="success")
                return redirect(url_for("boundary.sell"))
    
boundary.add_url_rule("/update-listing/<int:listing_id>", view_func=updateListing.as_view("updateListing"))

#SpdateListingStatus
class updateListingStatus(MethodView):
    def post(self, listing_id):
        
        update_lstatus = updateListingStatusController().get(listing_id)

        if update_lstatus is None:
            flash("Listing not found.", category="error")

        else:
            flash(f"Listing updated to {update_lstatus.value}.", category="success")

        return redirect(url_for("boundary.sell"))
    
boundary.add_url_rule("/update-lstatus/<int:listing_id>", view_func=updateListingStatus.as_view("updateListingStatus"))

#DeleteListing
class deleteListing(MethodView):
    def post(self, listing_id):
        delete_listing = deleteListingController().get(listing_id)

        if delete_listing:
            flash("Listing deleted successfully", category="success")
        
        else:
            flash("An error occurred while deleting the listing", category="error")

        return redirect(url_for("boundary.sell"))
    
boundary.add_url_rule("/delete-listing/<int:listing_id>", view_func=deleteListing.as_view("deleteListing"))

#viewListing
class viewListing(MethodView):
    def get(self, title, listing_id):
        listing = viewListingController().get(current_user.id, listing_id)

        if not listing:
            flash("Listing does not exist.", category="error")
            return redirect(url_for("boundary.buy"))

        return render_template("user/listingPage.html", user=current_user, listing=listing)
    
boundary.add_url_rule("/listing/<string:title>-<int:listing_id>", view_func=viewListing.as_view("viewListing"))

#ShortlistListingController
class shortlistListing(MethodView):
    def post(self, listing_id):
        listing = getListingController().get(listing_id)

        shortlist = shortlistListingController().get(current_user.id, listing_id)
        
        if not listing:
            return jsonify({"error": "Listing does not exist."}, 400)

        return jsonify({"shortlists": len(listing.shortlists), "shortlisted": current_user.id in map(lambda x: x.user_id, listing.shortlists)})
    
boundary.add_url_rule("/shortlist-listing/<int:listing_id>", view_func=shortlistListing.as_view("shortlistListing"))

#ViewShortlistListing
class viewShortlistListing(MethodView):
    def get(self):

        return render_template("user/myActivitiesPage.html", user=current_user)

boundary.add_url_rule("/my-activities", view_func=viewShortlistListing.as_view("viewShortlistListing"))

#findAgentController
class findAgentPage(MethodView):
    def get(self):
        query_result = viewListingsByAgentController().get()
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
    
boundary.add_url_rule("/find-agent", view_func=findAgentPage.as_view("findAgent"))

#viewAgentController
class agentPage(MethodView):
    def get(self, first_name, last_name, agent_id):
        agent = getAgentController().get(agent_id)
        reviews = getReviewsController().get(agent_id)

        return render_template("user/agentPage.html", user=current_user, agent=agent, reviews=reviews)
    
boundary.add_url_rule("/find-agent/<string:first_name>-<string:last_name>-<int:agent_id>", view_func=agentPage.as_view("viewAgent"))

#CreateRating
class createRating(MethodView):
    def post(self, agent_id):
        rating_value = request.form["rating"]

        rating = createRatingController().get(agent_id, current_user.id, rating_value)
        if not rating:
            flash("An error occurred while rating the agent.", category="error")

        return redirect(url_for("boundary.viewAgent", first_name=rating.review.agent.user.first_name, last_name=rating.review.agent.user.last_name, agent_id=agent_id))
    
boundary.add_url_rule("/create-rating/<int:agent_id>", view_func=createRating.as_view("createRating"))

#CreateComment
class createComment(MethodView):
    def post(self, agent_id):
        comment_value = request.form["comment"]

        comment = createCommentController().get(agent_id, current_user.id, comment_value)
        if comment is False:
            flash("An error occurred while rating the agent.", category="error")

        return redirect(url_for("boundary.viewAgent", first_name=comment.review.agent.user.first_name, last_name=comment.review.agent.user.last_name, agent_id=agent_id))
    
boundary.add_url_rule("/create-comment/<int:agent_id>", view_func=createComment.as_view("createComment"))