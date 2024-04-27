from flask import Blueprint, render_template, request, flash, redirect, url_for, send_from_directory, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from .models import *
from . import db
from datetime import datetime

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():

  return render_template("home.html", user=current_user)

@views.route('/media/<path:filename>')
def get_image(filename):
  return send_from_directory('../media', filename)

@views.route('/buy', methods=['GET', 'POST'])
@login_required
def buy():
  listings = Listing.query.all()

  return render_template("buy.html", user=current_user, listings=listings)

@views.route('/sell', methods=['GET', 'POST'])
@login_required
def sell():
  listings = Listing.query.all()
  return render_template('sell.html', user=current_user, listings=listings)

@views.route('/create-listing', methods=['GET', 'POST'])
@login_required
def create_listing():
  if request.method == "POST":
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
      if not photo:
        flash('Please insert a photo.', category='error')
      else:
        file_name = secure_filename(photo.filename)
        file_path = f'./media/{file_name}'

        new_listing = Listing(title=title, description=description, type=type, price=price, 
                          bedrooms=bedrooms, bathrooms=bathrooms, size_sqft=size_sqft, 
                          location=location, availability=Availability.AVAILABLE, photo=file_path, user_id=current_user.id)
        db.session.add(new_listing)
        db.session.commit()
        photo.save(file_path)
        flash('Listing created!', category='success')
        return redirect(url_for('views.sell'))

  return render_template("create_listing.html", user=current_user)

@views.route("/delete-listing/<id>")
@login_required
def delete_listing(id):
  listing = Listing.query.filter_by(id=id).first()

  if not listing:
    flash('Listing does not exist.', category='error')
  elif current_user.id != listing.id:
    flash('You do not have permission to delete this listing.', category='error')
  else:
    db.session.delete(listing)
    db.session.commit()
    flash('Listing deleted.', category='success')

  return redirect(url_for('views.sell'))

@views.route('/update-listing/<id>', methods=['GET', 'POST'])
@login_required
def update_listing(id):
    listing = Listing.query.get(id)

    if not listing:
        flash('Listing does not exist.', category='error')
        return redirect(url_for('views.sell'))

    if request.method == 'POST':
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

            listing.title = title
            listing.description = description
            listing.type = type
            listing.price = price
            listing.bedrooms = bedrooms
            listing.bathrooms = bathrooms
            listing.size_sqft = size_sqft
            listing.location = location

            db.session.commit()
            flash('Listing updated!', category='success')
            return redirect(url_for('views.sell'))

    return render_template("update_listing.html", user=current_user, listing=listing)


@views.route('/shortlist-listing/<listing_id>', methods=['POST'])
@login_required
def shortlist(listing_id):
  listing = Listing.query.filter_by(id=listing_id).first()
  shortlist = Shortlist.query.filter_by(user_id=current_user.id, listing_id=listing_id).first()

  if not listing:
    return jsonify({'error': 'Listing does not exist.'}, 400)
  elif shortlist:
    db.session.delete(shortlist)
    db.session.commit()
  else:
    shortlist = Shortlist(user_id=current_user.id, listing_id=listing_id)
    db.session.add(shortlist)
    db.session.commit()
  
  return jsonify({"shortlists": len(listing.shortlists), "shortlisted": current_user.id in map(lambda x: x.user_id, listing.shortlists)})

@views.route('/listing/<title>-<id>', methods=['GET', 'POST'])
@login_required
def listing(title, id):
  listing = Listing.query.filter_by(id=id).first()
  tag_user = User.query.get(listing.user_id)
  agent = Agent.query.filter_by(user_id=tag_user.id).first()

  print(agent)

  return render_template('listing.html', user=current_user, listing=listing, id=id, agent=agent)

@views.route('/find-agent', methods=['GET', 'POST'])
@login_required
def find_agent():
  query_result = db.session.query(User, Listing, Agent).\
    join(Listing, Listing.user_id == User.id).\
    join(Agent, Agent.user_id == User.id).all()
  
  def get_types(query_result):
    types = set()
    for _, listing, _ in query_result:
      types.add(listing.type)
    
    return types
  
  types = get_types(query_result)

  return render_template('find_agent.html', user=current_user, query_result=query_result, types=types)

@views.route('/find-agent/<first_name>-<last_name>-<agent_id>', methods=['GET', 'POST'])
@login_required
def agent(first_name, last_name, agent_id):
  agent_id = agent_id
  query_result = db.session.query(User, Listing, Agent).\
    join(Listing, Listing.user_id == User.id).\
    join(Agent, Agent.user_id == User.id).\
    filter(Agent.id == agent_id).\
    all()
  
  reviews = Review.query.filter_by(agent_id=agent_id).all()

  return render_template('agent.html', user=current_user, query_result=query_result, reviews=reviews)

@views.route('/create-comment/<agent_id>', methods=['POST'])
@login_required
def create_comment(agent_id):
  rating_value = request.form.get('rating')
  comment_value = request.form.get('comment')
  
  agent = Agent.query.filter_by(id=agent_id).first()

  if not agent:
    flash('Agent does not exist.', category='error')
  
  else:
    review = Review.query.filter_by(agent_id=agent_id, user_id=current_user.id).first()

    if not review:
      review = Review(agent_id=agent_id, user_id=current_user.id)
      db.session.add(review)

    if rating_value:
      rating = Rating.query.filter_by(review_id=review.id).first()

      if rating:
        rating.rating = rating_value

      else:
        rating = Rating(rating=rating_value, review_id=review.id)
        db.session.add(rating)

    elif comment_value:
      comment = Comment.query.filter_by(review_id=review.id).first()
      
      if comment:
        comment.comment = comment_value

      else:
        comment = Comment(comment=comment_value, review_id=review.id)
        db.session.add(comment)

    else:
      flash('No rating or comment is submitted', category='error')
  
  db.session.commit()
  
  user_id = agent.user_id
  user = User.query.get(user_id)

  return redirect(url_for('views.agent', first_name=user.first_name, last_name=user.last_name, agent_id=agent_id))

from flask import request

@views.route('/search_filter', methods=['GET'])
def search():
    search_query = request.args.get('search')

    if search_query:
        filtered_listings = [listing for listing in Listing.query.all() if search_query.lower() in listing.location.lower()]
    else:
        filtered_listings = Listing.query.all()

    return render_template('buy.html', user=current_user, listings=filtered_listings)

@views.route('/type_filter', methods=['GET'])
def type_filter():
  type = request.args.get('type')

  if type == 'All' or type == 'clear':
    listings = Listing.query.all()
  else:
    listings = Listing.query.filter_by(type=type).all()

  return render_template('buy.html', user=current_user, listings=listings)

@views.route('/price_filter', methods=['GET'])
def price_filter():
    min_price = request.args.get('minPrice')
    max_price = request.args.get('maxPrice')

    if min_price and max_price:
        listings = Listing.query.filter(Listing.price.between(min_price, max_price)).all()
    elif min_price:
        listings = Listing.query.filter(Listing.price >= min_price).all()
    elif max_price:
        listings = Listing.query.filter(Listing.price <= max_price).all()
    else:
        listings = Listing.query.all()

    return render_template('buy.html', user=current_user, listings=listings)

@views.route('/bedroom_filter', methods=['GET'])
def bedroom_filter():
  bedrooms = request.args.get('bedrooms')

  if bedrooms == 'clear':
    listings = Listing.query.all()
  else:
    if bedrooms == '5':
      listings = Listing.query.filter(Listing.bedrooms >= 5).all()
    else:
      listings = Listing.query.filter_by(bedrooms=bedrooms).all()

  return render_template('buy.html', user=current_user, listings=listings)