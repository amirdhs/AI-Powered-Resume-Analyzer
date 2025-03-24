from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from app import db
from app.models import User
import bcrypt

auth_routes = Blueprint('auth', __name__)

@auth_routes.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'danger')
            return redirect(url_for('auth.register'))

        user = User(name, email, password)
        db.session.add(user)
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
            session['user_id'] = user.id
            session['user_name'] = user.name
            flash('You are logged in successfully', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid credentials', 'danger')
            return redirect(url_for('auth.login'))
    return render_template('auth/login.html')

@auth_routes.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'success')
    return redirect(url_for('auth/index'))