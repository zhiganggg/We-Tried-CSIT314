from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, current_app
from flask_login import login_required, current_user
from .models import User, Listing, Shortlist
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():

  return render_template("home.html", user=current_user)

@views.route('/buy', methods=['GET', 'POST'])
@login_required
def buy():
  # listings = Listing.query.all()
  return render_template("buy.html", user=current_user)

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
    price = request.form.get('price')
    bedrooms = request.form.get('bedrooms')
    bathrooms = request.form.get('bathrooms')
    size_sqft = request.form.get('size_sqft')
    location = request.form.get('location')

    if not title or not description or not price or not bedrooms or not bathrooms or not size_sqft or not location:
      flash('All fields are required.', category='error')
    else:
      new_listing = Listing(title=title, description=description, price=price, 
                        bedrooms=bedrooms, bathrooms=bathrooms, size_sqft=size_sqft, 
                        location=location, user_id=current_user.id)
      db.session.add(new_listing)
      db.session.commit()
      current_app.logger.debug(f'New listing added: (new_listing)')
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