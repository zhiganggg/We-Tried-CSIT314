from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from .models2 import *
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
            if user.status == UserStatus.ENABLED:
                if check_password_hash(user.password, password):
                    flash('Logged in successfully!', category='success')
                    login_user(user, remember=True)
                    return redirect(url_for('views.dashboard'))
            
                else:
                    flash('Incorrect password, try again.', category='error')
            
            else:
                flash('Your account is disabled. Please contact support.', category='error')

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
    roles = Role.query.all()

    if request.method == "POST":
        email = request.form.get('email')
        first_name = request.form.get('first-name')
        last_name = request.form.get('last-name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        role_id = request.form.get('role')

        role = Role.query.get(role_id)

        cea_registration_no = request.form.get('cea-registration-no', '')
        agency_license_no = request.form.get('agency-license-no', '')

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            flash('Email already exists', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 characters.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Passwords must be at least 7 characters.', category='error')
        else:
            agent = Agent.query.filter_by(cea_registration_no=cea_registration_no).first()
            if agent:
                flash('Agent with CEA registration number {} already exists.'.format(cea_registration_no))
            else:
                new_user = User(email=email, first_name=first_name, last_name=last_name, password=generate_password_hash(password1, method='pbkdf2:sha256'), role=role, status=UserStatus.ENABLED)
                db.session.add(new_user)
                db.session.commit()

                if role.name == 'Agent':
                    new_agent = Agent(user_id=new_user.id, cea_registration_no=cea_registration_no, agency_license_no=agency_license_no)
                    db.session.add(new_agent)
                    db.session.commit()              

                login_user(new_user, remember=True)
                flash('Account created!', category='success')
                return redirect(url_for('views.dashboard'))

    return render_template('sign_up.html', user=current_user, roles=roles)

@auth.route('/update-profile', methods=['GET', 'POST'])
@login_required
def update_profile():
    if current_user.role == "agent":
        agent = Agent.query.filter_by(user_id=current_user.id).first()

        return render_template('update_profile.html', user=current_user, agent=agent)
    
    if request.method == "POST":
        first_name = request.form.get('first-name')
        last_name = request.form.get('last-name')
        email = request.form.get('email')

        current_user.first_name = first_name
        current_user.last_name = last_name
        current_user.email = email

        db.session.commit()

        flash('Profile updated!', category='success')
        return redirect(url_for('views.dashboard'))
    
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
            return redirect(url_for('views.dashboard'))

    return render_template('change_password.html', user=current_user)

@auth.route('/users', methods=['GET', 'POST'])
@login_required
def users():
    users = User.query.all()

    return render_template('users.html', user=current_user, users=users, UserStatus=UserStatus)

@auth.route('/edit-user', methods=['GET', 'POST'])
@login_required
def edit_user():
    if request.method == "POST":
        user_id = request.form.get('user_id')
        email = request.form.get('email')
        first_name = request.form.get('first-name')
        last_name = request.form.get('last-name')

        user = User.query.get(user_id)
        if user:
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            db.session.commit()

            flash('User updated successfully.', category='success')
        else:
            flash('User not found.', category='error')
    
    return redirect(url_for('auth.users'))

@auth.route('/disable-user/<int:user_id>', methods=['POST'])
@login_required
def disable_user(user_id):
    user = User.query.get(user_id)
    if user:
        user.status = UserStatus.DISABLED
        db.session.commit()
        flash('User disabled successfully.', category='success')
    else:
        flash('User not found.', category='error')
    return redirect(url_for('auth.users'))

@auth.route('/enable-user/<int:user_id>', methods=['POST'])
@login_required
def enable_user(user_id):
    user = User.query.get(user_id)
    if user:
        user.status = UserStatus.ENABLED
        db.session.commit()
        flash('User enabled successfully.', category='success')
    else:
        flash('User not found.', category='error')
    return redirect(url_for('auth.users'))

@auth.route('/search_user', methods=['GET'])
def search():
    search_query = request.args.get('search')

    if search_query:
        filtered_users = [user for user in User.query.all() if 
                          search_query.lower() in user.email.lower() or 
                          search_query.lower() in user.first_name.lower() or 
                          search_query.lower() in user.last_name.lower()]
    else:
        filtered_users = User.query.all()

    return render_template('users.html', user=current_user, users=filtered_users)

@auth.route('/roles', methods=['GET', 'POST'])
@login_required
def roles():
    roles = Role.query.all()

    return render_template('roles.html', user=current_user, roles=roles)

@auth.route('/create-role', methods=['POST'])
@login_required
def create_role():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')

        existing_role = Role.query.filter_by(name=name).first()
        if existing_role:
            flash('Role name already exists.', category='error')
        else:
            new_role = Role(name=name, description=description)
            db.session.add(new_role)
            db.session.commit()
            flash('Role created successfully.', category='success')

    return redirect(url_for('auth.roles'))

@auth.route('/edit-role', methods=['POST'])
@login_required
def edit_role():
    if request.method == 'POST':
        role_id = request.form.get('role_id')
        name = request.form.get('name')
        description = request.form.get('description')

        role = Role.query.get(role_id)
        if role:
            role.name = name
            role.description = description
            db.session.commit()
            flash('Role updated successfully.', category='success')
        else:
            flash('Role not found.', category='error')

    return redirect(url_for('auth.roles'))

@auth.route('/delete-role/<int:role_id>', methods=['POST'])
@login_required
def delete_role(role_id):
    role = Role.query.get_or_404(role_id)

    try:
        db.session.delete(role)
        db.session.commit()
        flash('Role deleted successfully', category='success')
    except Exception as e:
        flash('An error occurred while deleting the role', category='error')
        print(e)

    return redirect(url_for('auth.roles'))

@auth.route('/create-admin', methods=['GET', 'POST'])
def create_admin():
    role = Role(name='Admin', description='Admin role')
    db.session.add(role)
    db.session.commit()
    print('Admin role created successfully.')

    return render_template('create_admin.html', user=current_user, role=role)

@auth.route('/create-accounts', methods=['POST'])
def create_accounts():
    data = request.json
    
    if data:
        created_accounts = []
        for entry in data:
            email = entry.get('email')
            first_name = entry.get('first_name')
            last_name = entry.get('last_name')
            password = entry.get('password')
            role_id = entry.get('role_id')
            
            # Omit cea_registration_no and agency_license_no
            # Generate user only if all required fields are present
            if email and first_name and last_name and password and role_id:
                existing_user = User.query.filter_by(email=email).first()
                if existing_user:
                    created_accounts.append({'email': email, 'status': 'Already exists'})
                else:
                    role = Role.query.get(role_id)
                    if not role:
                        created_accounts.append({'email': email, 'status': 'Role not found'})
                    else:
                        new_user = User(email=email, first_name=first_name, last_name=last_name, password=generate_password_hash(password, method='pbkdf2:sha256'), role=role, status=UserStatus.ENABLED)
                        db.session.add(new_user)
                        db.session.commit()
                        created_accounts.append({'email': email, 'status': 'Created'})
                        
                        if role.name == 'Agent':
                            cea_registration_no = entry.get('cea_registration_no')
                            agency_license_no = entry.get('agency_license_no')
                            
                            if cea_registration_no and agency_license_no:
                                new_agent = Agent(user=new_user, cea_registration_no=cea_registration_no, agency_license_no=agency_license_no)
                                db.session.add(new_agent)
                                db.session.commit()
                            else:
                                created_accounts[-1]['status'] = 'Agent data missing'
            else:
                created_accounts.append({'email': email, 'status': 'Incomplete data'})

        return jsonify({'message': 'Accounts created', 'created_accounts': created_accounts}), 201
    else:
        return jsonify({'message': 'No data received for user creation.'}), 400

