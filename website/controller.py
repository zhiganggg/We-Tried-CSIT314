from flask import Blueprint, render_template, request, flash, redirect, url_for, send_from_directory, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from .models2 import *
from .entity import *
from . import db
from datetime import datetime, timedelta
from collections import defaultdict
from flask.views import MethodView

views = Blueprint('views', __name__)

class dashboardView(MethodView):
    @login_required
    def get(self):
        # Get the current date and the date from one week ago
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)  # One week ago

        if current_user.agent:
            user_listing = Listing.query.filter_by(agent_id=current_user.agent.id).all()
        else:
            user_listing = Listing.query.filter_by(user_id=current_user.id).all()

        listing_id = [listing.id for listing in user_listing]

        # Query the database for views and shortlists within the past week
        views = View.query.filter(View.date_created >= start_date, View.date_created <= end_date,
                                    View.listing_id.in_(listing_id)).all()
        shortlists = Shortlist.query.filter(Shortlist.date_created >= start_date, Shortlist.date_created <= end_date,
                                            Shortlist.listing_id.in_(listing_id)).all()

        # Create dictionaries to store the counts for each day
        views_count = {}
        shortlists_count = {}

        # Populate the dictionaries with data from the database
        for view in views:
            date_str = view.date_created.strftime('%Y-%m-%d')
            views_count[date_str] = views_count.get(date_str, 0) + 1

        for shortlist in shortlists:
            date_str = shortlist.date_created.strftime('%Y-%m-%d')
            shortlists_count[date_str] = shortlists_count.get(date_str, 0) + 1

        # Prepare the data for Chart.js
        labels = list(views_count.keys())  # Assuming views and shortlists have the same dates
        views_data = list(views_count.values())
        shortlists_data = [shortlists_count.get(date, 0) for date in labels]

        # Inside the Flask route
        # Prepare data for rendering the table
        table_data = [{'date': label, 'shortlists': shortlists_data[index], 'views': views_data[index]} for index, label in enumerate(labels)]

        # Calculate the percentage change in views and shortlists
        views_last_week = sum(views_data[:-1])  # Views from last week
        views_this_week = sum(views_data)  # Views from this week
        shortlists_last_week = sum(shortlists_data[:-1])  # Shortlists from last week
        shortlists_this_week = sum(shortlists_data)  # Shortlists from this week

        if views_last_week != 0:
            percentage_change_views = ((views_this_week - views_last_week) / views_last_week) * 100
        
        else:
            percentage_change_views = 0
        
        if shortlists_last_week != 0:
            percentage_change_shortlists = ((shortlists_this_week - shortlists_last_week) / shortlists_last_week) * 100
        
        else:
            percentage_change_shortlists = 0
        
        print('Views:', views_data)
        print('Shortlists:', shortlists_data)

        return render_template('dashboard.html', user=current_user, table_data=table_data, labels=labels, views_data=views_data,
                                shortlists_data=shortlists_data, percentage_change_views=percentage_change_views,
                                percentage_change_shortlists=percentage_change_shortlists)
    @login_required
    def post(self):
        pass

 # Register the class-based view with the app
views.add_url_rule('/dashboard', view_func=dashboardView.as_view('dashboard'))
   

  
class getImageView(MethodView):
    def get(self,filename):
        return send_from_directory('../media', filename)
   
   # Register the class-based view with the app
views.add_url_rule('/media/<path:filename>', view_func=getImageView.as_view('media'))
   


class BuyView(MethodView):
    @login_required
    def get(self):
        listings = listing_entity.get_listing()
        return render_template('buy.html', user=current_user, listings=listings, Availability=Availability)

    @login_required
    def post(self):
        # Implement post method logic here if needed
        pass
    
# Register the class-based view with the app
views.add_url_rule('/buy', view_func=BuyView.as_view('buy'))

class SellView(MethodView):
    @login_required
    def get(self):
        listings = listing_entity.get_listing()
        return render_template('sell.html', user=current_user, listings=listings, Availability=Availability)

    @login_required
    def post(self):
        # Implement post method logic here if needed
        pass
    
# Register the class-based view with the app
views.add_url_rule('/sell', view_func=SellView.as_view('sell'))


class createListingView(MethodView):
    @login_required
    def get(self):
        users = user_entity.get_user()
        return render_template("create_listing.html", user=current_user, users=users)


    @login_required
    def post(self):
        users = user_entity.get_user()
        title = request.form.get('title')
        description = request.form.get('description')
        type = request.form.get('type')
        price = request.form.get('price')
        bedrooms = request.form.get('bedrooms')
        bathrooms = request.form.get('bathrooms')
        size_sqft = request.form.get('size_sqft')
        location = request.form.get('location')
        user_email = request.form.get('user_email')

        if not title or not description or not price or not bedrooms or not bathrooms or not size_sqft or not location:
            flash('All fields are required.', category='error')
        else:
            photo = request.files.get('photo')
            if not photo:
                flash('Please insert a photo.', category='error')
            else:
                file_name = secure_filename(photo.filename)
                file_path = f'./media/{file_name}'

                user = user_entity.get_user_by_email(user_email)
                if not user:
                    flash('User with provided email does not exist.', category='error')
                else:
                    listing_entity.add_listing(title=title, description=description, type=type, price=price, 
                                    bedrooms=bedrooms, bathrooms=bathrooms, size_sqft=size_sqft, 
                                    location=location, availability=Availability.AVAILABLE, photo=file_path, 
                                    user_id=user.id, agent_id=current_user.agent.id)
                    photo.save(file_path)
                    flash('Listing created!', category='success')
                    return redirect(url_for('views.sell'))

        return render_template("create_listing.html", user=current_user, users=users)
    
# Register the class-based view with the app
views.add_url_rule('/create-listing', view_func=createListingView.as_view('createListing'))

        
class markSoldView(MethodView):
   @login_required
   def get(self,id):
        listing = listing_entity.get_listing_by_id(id)
        if listing:
            listing_entity.update_listing_availability(listing, Availability.UNAVAILABLE)
            flash('Listing marked as sold.', category='success')
        else:
            flash('Listing not found.', category='error')
        return redirect(url_for('views.sell'))
    
# Register the class-based view with the app
views.add_url_rule('/mark-sold/<int:id>', view_func=markSoldView.as_view('markSold'))

   

class markAvailableView(MethodView):
   @login_required
   def get(self,id):
        listing = listing_entity.get_listing_by_id(id)
        if listing:
            listing_entity.update_listing_availability(listing, Availability.AVAILABLE)
            flash('Listing marked as available.', category='success')
        else:
            flash('Listing not found.', category='error')
        return redirect(url_for('views.sell'))
    
# Register the class-based view with the app
views.add_url_rule('/mark-available/<int:id>', view_func=markAvailableView.as_view('markAvailable'))

     

class deleteListingView(MethodView):
   @login_required
   def get(self,id):
        listing =listing_entity.get_listing_by_id(id)

        if not listing:
            flash('Listing does not exist.', category='error')
        elif not current_user.agent or current_user.agent.id != listing.agent_id:
            flash('You do not have permission to delete this listing.', category='error')
        else:
            listing_entity.delete_listing(listing)
            flash('Listing deleted.', category='success')

            return redirect(url_for('views.sell'))

# Register the class-based view with the app
views.add_url_rule('/delete-listing/<id>', view_func=deleteListingView.as_view('deleteListing'))
        


class updateListingView(MethodView):
    @login_required
    def get(self,id):
        listing = listing_entity.get_listing_by_id(id)

        if not listing:
            flash('Listing does not exist.', category='error')
            return redirect(url_for('views.sell'))
        
        return render_template("update_listing.html", user=current_user, listing=listing)   
    
    @login_required
    def post(self,id):
        listing = listing_entity.get_listing_by_id(id)

        if not listing:
            flash('Listing does not exist.', category='error')
            return redirect(url_for('views.sell'))
       
        title = request.form.get('title')
        description = request.form.get('description')
        type = request.form.get('type')
        price = request.form.get('price')
        bedrooms = request.form.get('bedrooms')
        bathrooms = request.form.get('bathrooms')
        size_sqft = request.form.get('size_sqft')
        location = request.form.get('location')

        if not title or not description or not price or not bedrooms or not bathrooms or not size_sqft or not location:
                flash('All fields are required.', category='error')
        else:
            photo = request.files.get('photo')
            if photo:
                file_name = secure_filename(photo.filename)
                file_path = f'./media/{file_name}'
                photo.save(file_path)
                listing.photo = file_path

                listing_entity.update_listing(listing,title,description,type,price,bedrooms,bathrooms,size_sqft,location)
                flash('Listing updated!', category='success')
                return redirect(url_for('views.sell'))

        return render_template("update_listing.html", user=current_user, listing=listing)

# Register the class-based view with the app
views.add_url_rule('/update-listing/<id>', view_func=updateListingView.as_view('updateListing'))   

class shortListView(MethodView):
    @login_required  
    def post(self,listing_id):
        listing = listing_entity.get_listing_by_id(listing_id)
        shortlist = shortlist_entity.get_shortlist_by_id(current_user.id, listing_id)

        if not listing:
            return jsonify({'error': 'Listing does not exist.'}, 400)
        elif shortlist:
            shortlist_entity.delete_shortlist(shortlist)
        else:
            shortlist_entity.add_shortlist(current_user.id, listing_id)
        
        return jsonify({"shortlists": len(listing.shortlists), "shortlisted": current_user.id in map(lambda x: x.user_id, listing.shortlists)})
    
# Register the class-based view with the app
views.add_url_rule('/shortlist-listing/<listing_id>', view_func=shortListView.as_view('shortList'))       

class listingView(MethodView):
    @login_required
    def get(self,id):
        listing = listing_entity.get_listing_by_id(id)

        if not listing:
            flash('Listing does not exist.', category='error')
        else:
            view = view_entity.add_view(current_user.id, id)

        return render_template('listing.html', user=current_user, listing=listing)

# Register the class-based view with the app
views.add_url_rule('/listing/<title>-<id>', view_func=listingView.as_view('listing'))


class findAgentView(MethodView):
    @login_required
    def get(self):
        query_result = listing_entity.get_listing_by_agent(Agent.id)
        types = self.get_types(query_result)
        return render_template('find_agent.html', user=current_user, types=types)
    
    @login_required
    def post(self):
        pass


    def get_types(self,query_result):
          types = {}
          for listing, agent in query_result:
              if listing.type not in types:
                  types[listing.type] = []
              if agent not in types[listing.type]:
                  types[listing.type].append(agent)
          return types

# Register the class-based view with the app
views.add_url_rule('/find-agent', view_func=findAgentView.as_view('findAgent'))
  
class agentView(MethodView):
    @login_required
    def get(self,first_name, last_name, agent_id):
        agent = agent_entity.get_agent_by_id(agent_id)
  
        reviews = review_entity.get_review_by_agentId(agent_id)

        return render_template('agent.html', user=current_user, agent=agent, reviews=reviews)
    
    @login_required
    def post(self):
        pass

# Register the class-based view with the app
views.add_url_rule('/find-agent/<first_name>-<last_name>-<agent_id>', view_func=agentView.as_view('agent'))


class createCommentView(MethodView):
    @login_required
    def post(self,agent_id):
        rating_value = request.form.get('rating')
        comment_value = request.form.get('comment')
  
        agent = agent_entity.get_agent_by_id(agent_id)

        if not agent:
            flash('Agent does not exist.', category='error')
    
        else:
            review = review_entity.get_review_by_agentId_userId(agent_id, current_user.id)

            if not review:
                review_entity.add_review(agent_id, current_user.id)

            if rating_value:
                rating = rating_entity.get_rating_by_reviewId(review.id)

                if rating:
                    #add this
                    rating_entity.update_rating(rating,rating_value)

                else:
                    rating_entity.add_rating(rating_value=rating_value, reviewId=review.id)

            elif comment_value:
                comment = comment_entity.get_comment_by_reviewId(review.id)
            
                if comment:
                    comment_entity.update_comment(comment,comment_value)

                else:
                    comment_entity.add_comment(comment_value, review.id)

            else:
                flash('No rating or comment is submitted', category='error')
    
  
    
        user_id = agent.user_id
        user = user_entity.get_user_by_userId(user_id)

        return redirect(url_for('views.agent', first_name=user.first_name, last_name=user.last_name, agent_id=agent_id))
    
# Register the class-based view with the app
views.add_url_rule('/create-comment/<agent_id>', view_func=createCommentView.as_view('createComment'))


class searchFilterView(MethodView):
    def get(self):
        search_query = request.args.get('search')

        if search_query:
            filtered_listings = [listing for listing in listing_entity.get_listing() if search_query.lower() in listing.location.lower()]
        else:
            filtered_listings = listing_entity.get_listing()

        return render_template('buy.html', user=current_user, listings=filtered_listings)
    
# Register the class-based view with the app
views.add_url_rule('/search_filter', view_func=searchFilterView.as_view('searchFilter'))

class typeFilterView(MethodView):
    def get(self):
        type = request.args.get('type')

        if type == 'All' or type == 'clear':
            listings = listing_entity.get_listing()
        else:
            listings = listing_entity.get_listing_by_type(type)

        return render_template('buy.html', user=current_user, listings=listings)
    
# Register the class-based view with the app
views.add_url_rule('/type_filter', view_func=typeFilterView.as_view('typeFilter'))


class priceFilterView(MethodView):
    def get(self):
        min_price = request.args.get('minPrice')
        max_price = request.args.get('maxPrice')

        if min_price and max_price:
            listings = listing_entity.get_listing_by_price(min_price=min_price, max_price=max_price, type='between')
        elif min_price:
            listings = listing_entity.get_listing_by_price(min_price=min_price, type='min')
        elif max_price:
            listings = listing_entity.get_listing_by_price(max_price=max_price, type='max')
        else:
            listings = listing_entity.get_listing()

        return render_template('buy.html', user=current_user, listings=listings)

# Register the class-based view with the app
views.add_url_rule('/price_filter', view_func=priceFilterView.as_view('priceFilter'))    


class bedroomFilterView(MethodView):
    def get(self):
        bedrooms = request.args.get('bedrooms')

        if bedrooms == 'clear':
            listings = listing_entity.get_listing()
        else:
            listings = listing_entity.get_listing_by_bedrooms(bedrooms)

        return render_template('buy.html', user=current_user, listings=listings)
    
# Register the class-based view with the app
views.add_url_rule('/bedroom_filter', view_func=bedroomFilterView.as_view('bedroomFilter'))  


class myActivitiesView(MethodView):
    def get(self):
        return render_template('my_activities.html', user=current_user)
    
    def post(self):
        pass

# Register the class-based view with the app
views.add_url_rule('/my-activities', view_func=myActivitiesView.as_view('myActivities'))  
