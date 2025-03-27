from flask import Blueprint, render_template, redirect, url_for, flash, session, request, current_app, make_response, \
    abort
from app import db
from app.models import Resume
import os
from werkzeug.utils import secure_filename
from app.services import resume_analyzer

main_routes = Blueprint('main', __name__)

# Add this function to your routes.py
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'pdf'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main_routes.route('/')
def index():
    return render_template('index.html')

@main_routes.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user_id' not in session:
        flash('Please log in to access the dashboard', 'danger')
        return redirect(url_for('auth.login'))

    feedback = None

    if request.method == 'POST':
        if 'resume' not in request.files:
            flash('No file uploaded', 'danger')
            return redirect(url_for('main.dashboard'))

        file = request.files['resume']

        if file.filename == '':
            flash('No file selected', 'danger')
            return redirect(url_for('main.dashboard'))

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            resume_text = resume_analyzer.extract_text_from_pdf(file_path)
            feedback = resume_analyzer.analyze_resume(resume_text)
            formatted_resume = feedback.get("formatted_resume", "No formatted resume available.")

            new_resume = Resume(user_id=session['user_id'], resume=formatted_resume)
            db.session.add(new_resume)
            db.session.commit()

            flash('Resume uploaded and analyzed successfully', 'success')
        else:
            flash('Invalid file type. Please upload a PDF file.', 'danger')
            return redirect(url_for('main.dashboard'))

    user_id = session['user_id']
    resumes = Resume.query.filter_by(user_id=user_id).all()

    return render_template('dashboard.html', name=session['user_name'], resumes=resumes, feedback=feedback)

@main_routes.route('/resume/<int:resume_id>')
def resume_detail(resume_id):
    if 'user_id' not in session:
        flash('Please log in to access this page', 'danger')
        return redirect(url_for('login'))

    # Fetch the resume from the database
    resume = Resume.query.get_or_404(resume_id)

    # Ensure the resume belongs to the logged-in user
    if resume.user_id != session['user_id']:
        flash('You do not have permission to view this resume', 'danger')
        return redirect(url_for('dashboard'))

    # Analyze the resume text and get the feedback
    feedback = resume_analyzer.analyze_resume(resume.resume)

    return render_template('dashboard/resume_detail.html', resume=resume, feedback=feedback)


@main_routes.route('/resume/<int:resume_id>/download', methods=['GET'])
def download_resume(resume_id):
    resume = Resume.query.get_or_404(resume_id)
    # Ensure user owns the resume
    if resume.user_id != session['user_id']:
        abort(403)

    # Create response with resume content
    response = make_response(resume.resume)
    response.headers['Content-Disposition'] = f'attachment; filename=resume_{resume_id}.txt'
    response.headers['Content-type'] = 'text/plain'
    return response


@main_routes.route('/resume/<int:resume_id>/delete', methods=['POST'])
def delete_resume(resume_id):
    if 'user_id' not in session:
        flash('Please login first', 'danger')
        return redirect(url_for('auth.login'))

    resume = Resume.query.get_or_404(resume_id)
    if resume.user_id != session['user_id']:
        abort(403)

    db.session.delete(resume)
    db.session.commit()
    flash('Resume deleted successfully', 'success')
    return redirect(url_for('main.dashboard'))


@main_routes.route('/logout', methods=['GET'])
def logout():
    session.clear()
    flash('You have been logged out', 'success')
    return redirect(url_for('auth.login'))