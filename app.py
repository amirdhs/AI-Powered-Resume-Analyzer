from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
import bcrypt
import os
from werkzeug.utils import secure_filename
import resume_analyzer
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:4181@localhost/resumeanalyzer'
app.config['SECRET_KEY'] = 'thisissecretkey'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Swagger configuration
SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = '/static/swagger.json'  # Our API url (can be a static file or a dynamic URL)

# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Resume Analyzer API"
    },
)

# Register blueprint at URL
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Models (unchanged)
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
    resume = db.Column(db.Text)

    def __init__(self, user_id, resume):
        self.user_id = user_id
        self.resume = resume

# Routes (unchanged except for the dashboard route)
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

    feedback = None

    if request.method == 'POST':
        # Check if a file was uploaded
        if 'resume' not in request.files:
            flash('No file uploaded', 'danger')
            return redirect(url_for('dashboard'))

        file = request.files['resume']

        # Check if the file is empty
        if file.filename == '':
            flash('No file selected', 'danger')
            return redirect(url_for('dashboard'))

        # Check if the file is a PDF
        if file and allowed_file(file.filename):
            # Save the file to the upload folder
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Extract text from the PDF
            resume_text = resume_analyzer.extract_text_from_pdf(file_path)

            # Analyze the resume text and get the formatted version
            feedback = resume_analyzer.analyze_resume(resume_text)
            formatted_resume = feedback.get("formatted_resume", "No formatted resume available.")

            # Save the formatted resume to the database
            new_resume = Resume(user_id=session['user_id'], resume=formatted_resume)
            db.session.add(new_resume)
            db.session.commit()

            flash('Resume uploaded and analyzed successfully', 'success')
        else:
            flash('Invalid file type. Please upload a PDF file.', 'danger')
            return redirect(url_for('dashboard'))

    # Fetch user's resumes
    user_id = session['user_id']
    resumes = Resume.query.filter_by(user_id=user_id).all()

    return render_template('dashboard.html', name=session['user_name'], resumes=resumes, feedback=feedback)

@app.route('/delete_resume/<int:resume_id>', methods=['POST'])
def delete_resume(resume_id):
    if 'user_id' not in session:
        flash('Please log in to perform this action', 'danger')
        return redirect(url_for('login'))

    # Fetch the resume from the database
    resume = Resume.query.get_or_404(resume_id)

    # Ensure the resume belongs to the logged-in user
    if resume.user_id != session['user_id']:
        flash('You do not have permission to delete this resume', 'danger')
        return redirect(url_for('dashboard'))

    # Delete the resume
    db.session.delete(resume)
    db.session.commit()

    flash('Resume deleted successfully', 'success')
    return redirect(url_for('dashboard'))


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