from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import *
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='erorr')

    return render_template('login.html', user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == "POST":
        email = request.form.get('email')
        first_name = request.form.get('first-name')
        last_name = request.form.get('last-name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        role = request.form.get('role')

        cea_registration_no = request.form.get('cea-registration-no', '')
        agency_license_no = request.form.get('agency-license-no', '')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists', category='error')
        if len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 characters.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Passwords must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, last_name=last_name, password=generate_password_hash(password1, method='pbkdf2:sha256'), role=role, status=UserStatus.ENABLED)
            db.session.add(new_user)
            db.session.commit()

            if role == 'agent':
                agent = Agent.query.filter_by(cea_registration_no=cea_registration_no).first()
                if agent:
                    flash('Agent with CEA registration number {} already exists.'.format(cea_registration_no))
                else:
                    new_agent = Agent(user_id=new_user.id, cea_registration_no=cea_registration_no, agency_license_no=agency_license_no)
                    db.session.add(new_agent)
                    db.session.commit()

            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template('sign_up.html', user=current_user)

@auth.route('/update-profile', methods=['GET', 'POST'])
def update_profile():
    if request.method == "POST":
        first_name = request.form.get('first-name')
        last_name = request.form.get('last-name')
        email = request.form.get('email')
        role = request.form.get('role')
        cea_registration_no = request.form.get('cea-registration-no', '')
        agency_license_no = request.form.get('agency-license-no', '')

        current_user.first_name = first_name
        current_user.last_name = last_name
        current_user.email = email
        current_user.role = role

        if role == 'agent':
            current_user.agent.cea_registration_no = cea_registration_no
            current_user.agent.agency_license_no = agency_license_no

        db.session.commit()

        flash('Profile updated!', category='success')
        return redirect(url_for('views.home'))
    
    return render_template('update_profile.html', user=current_user)

@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == "POST":
        current_password = request.form.get('current-password')
        new_password = request.form.get('new-password')
        confirm_password = request.form.get('confirm-password')

        if not check_password_hash(current_user.password, current_password):
            flash('Incorrect current password.', category='error')
        elif new_password != confirm_password:
            flash('New passwords do not match.', category='error')
        elif len(new_password) < 7:
            flash('New password must be at least 7 characters.', category='error')
        else:
            current_user.password = generate_password_hash(new_password, method='pbkdf2:sha256')

            db.session.commit()

            flash('Password changed successfully!', category='success')
            return redirect(url_for('views.home'))

    return render_template('change_password.html', user=current_user)