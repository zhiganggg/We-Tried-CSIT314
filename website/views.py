from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, current_app
from flask_login import login_required, current_user
from .models import Note, User, Listing
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
  if request.method =='POST':
    note = request.form.get('note')

    if len(note) < 1:
      flash('Note is too short!', category='error')
    else:
      new_note = Note(data=note, user_id=current_user.id)
      db.session.add(new_note)
      db.session.commit()
      flash('Note added!', category='success')

  return render_template("home.html", user=current_user)
  
@views.route('/delete-note', methods=['POST'])
def delete_note():
  note = json.loads(request.data)
  noteId = note['noteId']
  note = Note.query.get(noteId)
  if note:
    if note.user_id == current_user.id:
      db.session.delete(note)
      db.session.commit()
      flash('Note deleted!', category='error')
      
  return jsonify({})

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