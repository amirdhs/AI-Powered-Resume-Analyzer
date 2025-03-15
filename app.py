from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
import bcrypt

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:4181@localhost/resumeanalyzer'
app.config['SECRET_KEY'] = 'thisissecretkey'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Models
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))  # Increased length for hashed passwords

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')  # Hash the password

class Resume(db.Model):
    __tablename__ = 'resumes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    resume = db.Column(db.String(1000))

    def __init__(self, user_id, resume):
        self.user_id = user_id
        self.resume = resume

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        # Check if the email already exists
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'danger')
            return redirect(url_for('register'))

        # Create a new user
        user = User(name, email, password)
        db.session.add(user)
        db.session.commit()

        flash('You are registered successfully', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):  # Verify hashed password
            # Set session variables
            session['user_id'] = user.id
            session['user_name'] = user.name
            flash('You are logged in successfully', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user_id' not in session:
        flash('Please log in to access the dashboard', 'danger')
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Handle resume upload
        resume_text = request.form['resume']
        new_resume = Resume(user_id=session['user_id'], resume=resume_text)
        db.session.add(new_resume)
        db.session.commit()
        flash('Resume uploaded successfully', 'success')

    # Fetch user's resumes
    user_id = session['user_id']
    resumes = Resume.query.filter_by(user_id=user_id).all()

    return render_template('dashboard.html', name=session['user_name'], resumes=resumes)

@app.route('/logout')
def logout():
    # Clear the session
    session.clear()
    flash('You have been logged out', 'success')
    return redirect(url_for('index'))



# Run the app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)