from datetime import datetime, timedelta
from flask_jwt_extended import create_access_token
from flask import Blueprint, render_template, redirect, url_for, flash, request, session, jsonify

from app import db
from app.models import User, Subscription
import bcrypt

auth_routes = Blueprint('auth', __name__)

@auth_routes.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        plan = request.form['plan']

        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'danger')
            return redirect(url_for('auth.register'))

        user = User(name, email, password)
        db.session.add(user)
        db.session.flush()  # Get the user ID before commit

        # Create subscription
        end_date = datetime.utcnow() + timedelta(days=30)  # Example: 30 days subscription
        subscription = Subscription(user_id=user.id, plan=plan, end_date=end_date)
        db.session.add(subscription)
        db.session.commit()

        flash('You are registered successfully', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html')



@auth_routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            # Generate JWT token
            access_token = create_access_token(identity=str(user.id))

            # Store the token in the default cookie name
            response = redirect(url_for('main.dashboard'))
            response.set_cookie('access_token_cookie', access_token, httponly=True)

            # Set session for navbar rendering
            session['user_id'] = user.id
            return response
        else:
            flash('Invalid credentials', 'danger')
            return redirect(url_for('auth.login'))

    return render_template('auth/login.html')


# app/auth.py
@auth_routes.route('/logout')
def logout():
    session.clear()  # Clear session data
    response = redirect(url_for('auth.login'))
    response.delete_cookie('access_token_cookie')  # Remove JWT cookie
    flash('You have been logged out', 'success')
    return response
