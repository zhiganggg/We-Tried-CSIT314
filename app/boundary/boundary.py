# app/boundary/boundary.py
from flask import Blueprint, render_template, request, flash, redirect, url_for, send_from_directory, jsonify
from app.entity.entity import *
from app.controller.controller import *
from flask.views import MethodView
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta

boundary = Blueprint("boundary", __name__)

# loginPage
class loginBoundary(MethodView):
    def get(self):

        return render_template("user/loginPage.html", user=current_user)

    def post(self):
        email = request.form["email"]
        password = request.form["password"]

        user = retrieveUserByEmailController.get(email)
        if user:
            if user.status.value == "ENABLED":
                if check_password_hash(user.password, password):
                    flash("Logged in successfully!", category="success")
                    login_user(user, remember=True)
                    return redirect(url_for("boundary.home"))
                
                else:
                    flash("Incorrect password, try again.", category="error")

            else:
                flash("Your account is disabled. Please contact support.", category="error")

        else:
            flash("Email does not exist.", category="error")

        return render_template("user/loginPage.html", user=current_user)
              
#views
boundary.add_url_rule("/login", view_func=loginBoundary.as_view("login"))

#logoutBoundary
class logoutBoundary(MethodView):
    def get(self):
        logout_user()
        return redirect(url_for("boundary.login"))
    
#views
boundary.add_url_rule("/logout", view_func=logoutBoundary.as_view("logout"))

#signupBoundary
class signupBoundary(MethodView):
    def get(self):
        profiles = retrieveAllProfileController.get()

        return render_template("user/signupPage.html", user=current_user, profiles=profiles)
    
    def post(self):
        email = request.form["email"]
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        password = request.form["password"]
        verify_password = request.form["verify_password"]
        profile_id = request.form["profile"]

        profile = retrieveProfileByIdController.get(profile_id)

        cea_registration_no = request.form["cea_registration_no"]
        agency_license_no = request.form["agency_license_no"]

        existing_user = retrieveUserByEmailController.get(email)
        if existing_user:
            flash("Email already exists", category="error")
        
        elif len(email) < 4:
            flash("Email must be greater than 3 characters.", category="error")
        
        elif len(first_name) < 2:
            flash("First name must be greater than 1 characters.", category="error")
        
        elif password != verify_password:
            flash("Passwords don\"t match.", category="error")
        
        elif len(password) < 7:
            flash("Passwords must be at least 7 characters.", category="error")
        
        else:
            agent = retrieveCeaController.get(cea_registration_no)

            if agent:
                flash("Agent with CEA registration number {} already exists.".format(cea_registration_no))
            
            else:
                new_user = createUserController.get(email, first_name, last_name, generate_password_hash(password, method="pbkdf2:sha256"), profile.id)

                if profile.name == "Agent":
                    new_agent = createAgentController.get(cea_registration_no, agency_license_no, new_user.id)

                login_user(new_user, remember=True)
                flash("Account created!", category="success")
                return redirect(url_for("boundary.home"))
            
#views
boundary.add_url_rule("/sign-up", view_func=signupBoundary.as_view("signup"))

#updateAccountBoundary
class updateAccountBoundary(MethodView):
    def get(self):

        return render_template("user/updateAccountPage.html", user=current_user)

    def post(self):
        email = request.form["email"]
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]

        update_user = updateUserController.get(current_user.id, email, first_name, last_name)

        if update_user is None:
            flash("User not found.", category="error")

        elif update_user is False:
            flash("User email already exists.", category="error")

        else:
            flash("User updated successfully.", category="success")

        return render_template("user/updateAccountPage.html", user=current_user)
    
#views
boundary.add_url_rule("/update-account", view_func=updateAccountBoundary.as_view("updateAccount"))

#updatePasswordBoundary
class updatePasswordBoundary(MethodView):
    def get(self):

        return render_template("user/updatePasswordPage.html", user=current_user)

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
            update_password = updatePasswordController.get(current_user.id, generate_password_hash(new_password, method="pbkdf2:sha256"))

            if update_password:
                flash("Password changed successfully.", category="success")

            else:
                flash("User not found.", category="error")

        return render_template("user/updatePasswordPage.html", user=current_user)
    
#views
boundary.add_url_rule("/update-password", view_func=updatePasswordBoundary.as_view("updatePassword"))

#homeBoundary
class homeBoundary(MethodView):
    def get(self):
        user = retrieveUserByIdController.get(current_user.id)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)

        if user.profile.name == "Admin":
            return render_template("admin/homePage.html", user=current_user)

        else:

            if current_user.agent:
                user_listings = retrieveListingByAgentController.get(current_user.agent.id)
            else:
                user_listings = retrieveListingByUserController.get(current_user.id)

            listing_ids = [listing.id for listing in user_listings]

            views = retrieveViewsInPeriodController.get(listing_ids, start_date, end_date)
            shortlists = retrieveShortlistInPeriodController.get(listing_ids, start_date, end_date)

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

            return render_template('user/homePage.html', user=current_user, table_data=table_data, labels=labels,
                                views_data=views_data, shortlists_data=shortlists_data,
                                percentage_change_views=percentage_change_views,
                                percentage_change_shortlists=percentage_change_shortlists)

#views
boundary.add_url_rule("/home", view_func=homeBoundary.as_view("home"))

#profileBoundary
class profileBoundary(MethodView):
    def get(self):
        profiles = retrieveAllProfileController.get()

        return render_template("admin/profilePage.html", user=current_user, profiles=profiles)
    
#views
boundary.add_url_rule("/profile", view_func=profileBoundary.as_view("profile"))

#createProfileBoundary   
class createProfileBoundary(MethodView):
    def post(self):
        name = request.form["name"]
        description = request.form["description"]

        existing_profile = retrieveProfileByNameController.get(name)
        if existing_profile:
            flash("Profile name already exists.", category="error")
        
        else:
            new_profile = createProfileController.get(name, description)
            flash("Profile created successfully.", category="success")
            
        return redirect(url_for("boundary.profile"))
    
#views
boundary.add_url_rule("/create-profile", view_func=createProfileBoundary.as_view("createProfile"))

#updateProfileBoundary
class updateProfileBoundary(MethodView):
    def post(self):
        profile_id = request.form["profile_id"]
        name = request.form["name"]
        description = request.form["description"]

        update_profile = updateProfileController.get(profile_id, name, description)

        if update_profile is None:
            flash("Profile not found.", category="error")
        
        elif update_profile is False:
            flash("Profile name already exists.", category="error")

        else:
            flash("Profile updated successfully.", category="success")

        return redirect(url_for("boundary.profile"))
    
#views
boundary.add_url_rule("/update-profile", view_func=updateProfileBoundary.as_view("updateProfile"))

#deleteProfileBoundary
class deleteProfileBoundary(MethodView):
    def post(self, id):
        delete_profile = deleteProfileController.get(id)

        if delete_profile:
            flash("Profile deleted successfully", category="success")
        
        else:
            flash("An error occurred while deleting the profile", category="error")

        return redirect(url_for("boundary.profile"))
    
#views
boundary.add_url_rule("/delete-profile/<int:id>", view_func=deleteProfileBoundary.as_view("deleteProfile"))

#userBoundary
class userBoundary(MethodView):
    def get(self):
        users = retrieveUserController.get()

        return render_template("admin/userPage.html", user=current_user, users=users)
    
#views
boundary.add_url_rule("/user", view_func=userBoundary.as_view("user"))

#updateUserBoundary
class updateUserBoundary(MethodView):
    def post(self):
        user_id = request.form["user_id"]
        email = request.form["email"]
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]

        update_user = updateUserController.get(user_id, email, first_name, last_name)
        
        if update_user is None:
            flash("User not found.", category="error")

        elif update_user is False:
            flash("User email already exists.", category="error")

        else:
            flash("User updated successfully.", category="success")

        return redirect(url_for("boundary.user"))
    
#views
boundary.add_url_rule("/update-user", view_func=updateUserBoundary.as_view("updateUser"))

#updateUserStatusBoundary
class updateUserStatusBoundary(MethodView):
    def post(self, id):
        update_ustatus = updateUserStatusController.get(id)

        if update_ustatus is None:
            flash("User not found.", category="error")

        else:
            flash(f"User status updated to {update_ustatus.value}.", category="success")

        return redirect(url_for("boundary.user"))
    
#views
boundary.add_url_rule("/update-ustatus/<int:id>", view_func=updateUserStatusBoundary.as_view("updateUserStatus"))

#searchUserBoundary
class searchUserBoundary(MethodView):
    def get(self):
        search_query = request.args.get("search")
        filtered_users = searchUserController.get(search_query)

        return render_template("admin/userPage.html", user=current_user, users=filtered_users)
    
#views
boundary.add_url_rule("/search-user", view_func=searchUserBoundary.as_view("searchUser"))

#mediaBoundary
class mediaBoundary(MethodView):
    def get(self, filename):
        return send_from_directory('../media', filename)

boundary.add_url_rule('/media/<path:filename>', view_func=mediaBoundary.as_view('media'))

#buyBoundary
class retrieveListingBoundary(MethodView):
    def get(self):
        listings = retrieveAllListingController.get()

        return render_template("user/buyPage.html", user=current_user, listings=listings)
    
#views
boundary.add_url_rule("/buy", view_func=retrieveListingBoundary.as_view("buy"))

#searchListingLocationBoundary
class searchListingLocationBoundary(MethodView):
    def get(self):
        search_query = request.args.get("search")
        filtered_listings = searchListingLocationController.get(search_query)

        return render_template("user/buyPage.html", user=current_user, listings=filtered_listings)
    
#views
boundary.add_url_rule("/search-location", view_func=searchListingLocationBoundary.as_view("searchListingLocation"))

#searchListingTypeBoundary
class searchListingTypeBoundary(MethodView):
    def get(self):
        type = request.args.get("type")

        if type == "All" or type == "clear":
            filtered_listings = retrieveAllListingController.get()

        else:
            filtered_listings = searchListingTypeController.get(type)

        return render_template("user/buyPage.html", user=current_user, listings=filtered_listings)
    
#views
boundary.add_url_rule("/search-type", view_func=searchListingTypeBoundary.as_view("searchListingType"))

#searchListingPriceBoundary
class searchListingPriceBoundary(MethodView):
    def get(self):
        min_price = request.args.get("minPrice")
        max_price = request.args.get("maxPrice")

        if min_price and max_price:
            filtered_listings = searchListingByPriceRangeController.get(min_price, max_price)
        
        elif min_price:
            filtered_listings = searchListingByMinPriceController.get(min_price)

        elif max_price:
            filtered_listings = searchListingByMaxPriceController.get(max_price)

        else:
            filtered_listings = retrieveAllListingController.get()

        return render_template("user/buyPage.html", user=current_user, listings=filtered_listings)
    
#views
boundary.add_url_rule("/search-price", view_func=searchListingPriceBoundary.as_view("searchListingPrice"))

#searchListingBedroomBoundary
class searchListingBedroomBoundary(MethodView):
    def get(self):
        bedrooms = request.args.get("bedrooms")

        if bedrooms == "clear":
            filtered_listings = retrieveAllListingController.get()
        
        else:
            if bedrooms == "5":
                filtered_listings = Listing.search_by_min_bedrooms(5)

            else:
                filtered_listings = searchListingByBedrooms.get(bedrooms)

        return render_template("user/buyPage.html", user=current_user, listings=filtered_listings)
    
#views
boundary.add_url_rule("/search-bedrooms", view_func=searchListingBedroomBoundary.as_view("searchListingBedrooms"))
    
#sellBoundary
class sellBoundary(MethodView):
    def get(self):
        listings = retrieveAllListingController.get()

        return render_template("user/sellPage.html", user=current_user, listings=listings)
 
#views
boundary.add_url_rule("/sell", view_func=sellBoundary.as_view("sell"))

#createListingBoundary
class createListingBoundary(MethodView):
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

                user = User.get_user_email(user_email)
                if not user:
                    flash("User with provided email does not exist.", category="error")

                else:
                    new_listing =createListingController.get(title, description, type, price, bedrooms, 
                                    bathrooms, size_sqft, location, file_path, user.id, current_user.agent.id)
                    
                    photo.save(file_path)
                    flash("Listing created!", category="success")
                    return redirect(url_for("boundary.sell"))
                
#views
boundary.add_url_rule("/create-listing", view_func=createListingBoundary.as_view("createListing"))

#updateListingBoundary
class updateListingBoundary(MethodView):
    def get(self, id):
        listing = retrieveListingByIdController.get(id)

        return render_template("agent/updateListingPage.html", user=current_user, listing=listing)
    
    def post(self, id):
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
            
            update_listing = updateListingController.get(id, title, description, type, price, bedrooms, 
                                                    bathrooms, size_sqft, location, file_path)
            
            if update_listing is None:
                flash("Listing not found.", category="error")
            
            else:
                flash("Listing updated!", category="success")
                return redirect(url_for("boundary.sell"))
    
#views
boundary.add_url_rule("/update-listing/<int:id>", view_func=updateListingBoundary.as_view("updateListing"))

#updateListingStatusBoundary
class updateListingStatusBoundary(MethodView):
    def post(self, id):
        update_lstatus = updateListingStatusByIdController.get(id)

        if update_lstatus is None:
            flash("Listing not found.", category="error")

        else:
            flash(f"Listing updated to {update_lstatus.value}.", category="success")

        return redirect(url_for("boundary.sell"))
    
#views
boundary.add_url_rule("/update-lstatus/<int:id>", view_func=updateListingStatusBoundary.as_view("updateListingStatus"))

#deleteListingBoundary
class deleteListingBoundary(MethodView):
    def post(self, id):
        delete_listing = deleteListingByIdController.get(id)

        if delete_listing:
            flash("Listing deleted successfully", category="success")
        
        else:
            flash("An error occurred while deleting the listing", category="error")

        return redirect(url_for("boundary.sell"))
    
#views
boundary.add_url_rule("/delete-listing/<int:id>", view_func=deleteListingBoundary.as_view("deleteListing"))

#viewListingController
class viewListingBoundary(MethodView):
    def get(self, title, listing_id):
        listing = retrieveListingByIdController.get(listing_id)

        if not listing:
            flash("Listing does not exist.", category="error")
            return redirect(url_for("boundary.buy"))
        
        View.create_view(current_user.id, listing_id)

        return render_template("user/listingPage.html", user=current_user, listing=listing)
    
#views
boundary.add_url_rule("/listing/<string:title>-<int:listing_id>", view_func=viewListingBoundary.as_view("viewListing"))

#shortlistListingBoundary
class shortlistListingBoundary(MethodView):
    def post(self, id):
        listing = retrieveListingByIdController.get(id)
        shortlist = retrieveShortlistByUserIdController.get(current_user.id, id)

        if not listing:
            return jsonify({"error": "Listing does not exist."}, 400)
        
        elif shortlist:
            deleteShortlistByUserIDController.get(shortlist.user_id, shortlist.listing_id)
        
        else:
            createShortlistByUserIDController.get(current_user.id, id)

        return jsonify({"shortlists": len(listing.shortlists), "shortlisted": current_user.id in map(lambda x: x.user_id, listing.shortlists)})
    
#views
boundary.add_url_rule("/shortlist-listing/<int:id>", view_func=shortlistListingBoundary.as_view("shortlistListing"))

#viewShortlistListingController
class viewShortlistListingBoundary(MethodView):
    def get(self):

        return render_template("user/myActivitiesPage.html", user=current_user)

#views
boundary.add_url_rule("/my-activities", view_func=viewShortlistListingBoundary.as_view("viewShortlistListing"))

#findAgentController
class findAgentBoundary(MethodView):
    def get(self):
        query_result = retrieveListingWithAgentsController.get()
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
    
#views
boundary.add_url_rule("/find-agent", view_func=findAgentBoundary.as_view("findAgent"))

#viewAgentController
class viewAgentController(MethodView):
    def get(self, first_name, last_name, agent_id):
        agent = Agent.get_agent_id(agent_id)
        reviews = Review.get_review_by_agent(agent_id)

        return render_template("user/agentPage.html", user=current_user, agent=agent, reviews=reviews)
    
#views
boundary.add_url_rule("/find-agent/<string:first_name>-<string:last_name>-<int:agent_id>", view_func=viewAgentController.as_view("viewAgent"))

#createRatingController
class createRatingBoundary(MethodView):
    def post(self, agent_id):
        rating_value = request.form["rating"]
        agent = retrieveAgentByIdController.get(agent_id)

        if not agent:
            flash("Agent does not exist.", category="error")
        
        else:
            review = retrieveReviewByIdController.get(agent_id, current_user.id)

            if not review:
                review = createReviewByIdController.get(agent_id, current_user.id)

            if rating_value:
                createUpdateRatingController.get(rating_value, review.id)

        return redirect(url_for("boundary.viewAgent", first_name=agent.user.first_name, last_name=agent.user.last_name, agent_id=agent_id))
    
#views
boundary.add_url_rule("/create-rating/<int:agent_id>", view_func=createRatingBoundary.as_view("createRating"))

#createCommentController
class createCommentBoundary(MethodView):
    def post(self, agent_id):
        comment_value = request.form["comment"]
        agent = Agent.get_agent_id(agent_id)

        if not agent:
            flash("Agent does not exist.", category="error")
        
        else:
            review = retrieveReviewByIdController.get(agent_id, current_user.id)

            if not review:
                review = createReviewByIdController.get(agent_id, current_user.id)

            if comment_value:
                Comment.create_or_update_comment(comment_value, review.id)

        return redirect(url_for("boundary.viewAgent", first_name=agent.user.first_name, last_name=agent.user.last_name, agent_id=agent_id))
    
#views
boundary.add_url_rule("/create-comment/<int:agent_id>", view_func=createCommentBoundary.as_view("createComment"))

