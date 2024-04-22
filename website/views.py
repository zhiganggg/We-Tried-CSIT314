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
  print(f'login_required [listings] : {listings}')
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
  user_id = listing.user_id
  agent = Agent.query.get(user_id)

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