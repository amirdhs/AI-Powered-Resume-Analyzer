from datetime import datetime, timedelta
from flask import Blueprint, render_template, redirect, url_for, flash, session, request, current_app, make_response, abort, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Resume, User, Feedback, Subscription
import os
from werkzeug.utils import secure_filename
from app.services import resume_analyzer

main_routes = Blueprint('main', __name__)

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

    user_id = session['user_id']
    resumes = Resume.query.filter_by(user_id=user_id).all()
    user = User.query.get(user_id)
    subscription = Subscription.query.filter_by(user_id=user_id).first()

    return render_template('dashboard.html', resumes=resumes, user=user, subscription=subscription)

@main_routes.route('/upload', methods=['POST'])
def upload():
    if 'user_id' not in session:
        flash('Please log in to upload a resume', 'danger')
        return redirect(url_for('auth.login'))

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

        new_resume = Resume(user_id=session['user_id'], resume=resume_text)
        db.session.add(new_resume)
        db.session.flush()

        new_feedback = Feedback(resume_id=new_resume.id, feedback=feedback)
        db.session.add(new_feedback)
        db.session.commit()

        flash('Resume uploaded and analyzed successfully', 'success')
        return redirect(url_for('main.dashboard'))

@main_routes.route('/subscription')
def subscription():
    if 'user_id' not in session:
        flash('Please log in to view your subscription', 'danger')
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    subscription = Subscription.query.filter_by(user_id=user_id).first()
    return render_template('subscription.html', subscription=subscription)

@main_routes.route('/subscription/update', methods=['POST'])
def update_subscription():
    if 'user_id' not in session:
        flash('Please log in to update your subscription', 'danger')
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    plan = request.form['plan']
    subscription = Subscription.query.filter_by(user_id=user_id).first()
    subscription.plan = plan
    subscription.end_date = datetime.utcnow() + timedelta(days=30)
    db.session.commit()

    flash('Subscription updated successfully', 'success')
    return redirect(url_for('main.subscription'))

@main_routes.route('/feedback/<int:resume_id>', methods=['GET', 'POST'])
def feedback(resume_id):
    if 'user_id' not in session:
        flash('Please log in to access this page', 'danger')
        return redirect(url_for('login'))

    resume = Resume.query.get_or_404(resume_id)

    if resume.user_id != session['user_id']:
        flash('You do not have permission to view this resume', 'danger')
        return redirect(url_for('dashboard'))

    resume = Resume.query.get_or_404(resume_id)
    feedback = resume_analyzer.analyze_resume(resume.resume)
    db.session.add(feedback)
    db.session.commit()


    flash('Feedback generated successfully', 'success')
    return render_template('dashboard/resume_detail.html', resume=resume, feedback=feedback)


@main_routes.route('/check_job/<int:resume_id>', methods=['POST'])
def check_job(resume_id):
    if 'user_id' not in session:
        flash('Please log in to access this page', 'danger')
        return redirect(url_for('auth.login'))

    resume = Resume.query.get_or_404(resume_id)
    if resume.user_id != session['user_id']:
        flash('You do not have permission to view this resume', 'danger')
        return redirect(url_for('main.dashboard'))

    job_role = request.form.get('job_title')
    job_check_result = resume_analyzer.check_for_job(resume.resume, job_role)

    # Update or create feedback with job check results
    feedback = Feedback.query.filter_by(resume_id=resume.id).first()
    if feedback:
        feedback.check_job = job_check_result
    else:
        feedback = Feedback(resume_id=resume.id, feedback={}, check_job=job_check_result)
        db.session.add(feedback)

    db.session.commit()

    return redirect(url_for('main.view_resume', resume_id=resume_id))

@main_routes.route('/resume/<int:resume_id>/view', methods=['GET'])
def view_resume(resume_id):
    resume = Resume.query.get_or_404(resume_id)
    feedback = Feedback.query.filter_by(resume_id=resume.id).first()

    feedback_data = feedback.feedback if feedback else None
    job_check_data = feedback.check_job if feedback else None

    return render_template('dashboard/resume_detail.html',
                           resume=resume,
                           feedback=feedback_data,
                           job_check=job_check_data)


@main_routes.route('/resume/<int:resume_id>/delete', methods=['POST'])
def delete_resume(resume_id):
    if 'user_id' not in session:
        flash('Please login first', 'danger')
        return redirect(url_for('auth.login'))

    resume = Resume.query.get_or_404(resume_id)
    if resume.user_id != session['user_id']:
        abort(403)

    # Delete associated feedback first
    Feedback.query.filter_by(resume_id=resume.id).delete()

    # Then delete the resume
    db.session.delete(resume)
    db.session.commit()

    flash('Resume deleted successfully', 'success')
    return redirect(url_for('main.dashboard'))

@main_routes.route('/logout', methods=['GET'])
def logout():
    session.clear()
    flash('You have been logged out', 'success')
    return redirect(url_for('auth.login'))


@main_routes.route('/me')
def me():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    user = User.query.get(session['user_id'])
    return jsonify({
        "id": user.id,
        "email": user.email,
        "name": user.name
    })