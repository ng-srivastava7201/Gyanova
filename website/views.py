from flask import Blueprint, render_template, redirect, url_for, request, abort, current_app, send_file
from flask_login import login_required, current_user
import os
from werkzeug.utils import secure_filename
from .models import Content
from . import db


views = Blueprint('views', __name__)


@views.route('/', methods=['GET'])
@login_required
def home():
    if current_user.role == 'teacher':
        return redirect(url_for('views.teacher_dashboard'))
    elif current_user.role == 'student':
        return redirect(url_for('views.student_dashboard'))
    else:
        return "Role not assigned"


@views.route('/teacher')
@login_required
def teacher_dashboard():
    if current_user.role != 'teacher':
        return redirect(url_for('views.home'))

    uploads = Content.query.filter_by(teacher_name=current_user.name).order_by(Content.upload_date.desc()).all()

    return render_template(
        "teacher_dashboard.html",
        user=current_user,
        uploads=uploads
    )


@views.route('/student')
@login_required
def student_dashboard():
    if current_user.role != 'student':
        return redirect(url_for('views.home'))

    from .models import User

    selected_subject = request.args.get('subject')
    selected_chapter = request.args.get('chapter')
    selected_teacher = request.args.get('teacher')
    selected_school  = request.args.get('school')

    # Populate each dropdown from DB
    def distinct_col(col):
        rows = Content.query.with_entities(col).distinct().all()
        return sorted([r[0] for r in rows if r[0]])

    subjects = distinct_col(Content.subject)
    chapters = distinct_col(Content.chapter)
    teachers = distinct_col(Content.teacher_name)
    schools  = sorted([
        r[0] for r in
        User.query.with_entities(User.school).distinct().all()
        if r[0]
    ])

    # Filter content based on selections
    contents_query = Content.query

    if selected_subject:
        contents_query = contents_query.filter(Content.subject == selected_subject)

    if selected_chapter:
        contents_query = contents_query.filter(Content.chapter == selected_chapter)

    if selected_teacher:
        contents_query = contents_query.filter(Content.teacher_name == selected_teacher)

    if selected_school:
        contents_query = contents_query.join(
            User, User.name == Content.teacher_name
        ).filter(User.school == selected_school)

    contents = contents_query.all()

    return render_template(
        "student_dashboard.html",
        contents=contents,
        subjects=subjects,
        chapters=chapters,
        teachers=teachers,
        schools=schools,
        selected_subject=selected_subject,
        selected_chapter=selected_chapter,
        selected_teacher=selected_teacher,
        selected_school=selected_school,
    )


@views.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if current_user.role != 'teacher':
        return redirect(url_for('views.home'))

    if request.method == 'POST':
        subject = request.form.get('subject')
        chapter = request.form.get('chapter')
        file = request.files.get('file')

        if file and file.filename != '':
            base_dir = current_app.config['UPLOAD_FOLDER']
            chapter_folder = os.path.join(base_dir, subject, chapter)
            os.makedirs(chapter_folder, exist_ok=True)

            filename = secure_filename(file.filename)
            file_path = os.path.join(chapter_folder, filename)
            file.save(file_path)

            new_content = Content(
                subject=subject,
                chapter=chapter,
                filename=filename,
                youtube_link=request.form.get('youtube'),
                teacher_name=current_user.name
            )
            db.session.add(new_content)
            db.session.commit()
            return redirect(url_for('views.teacher_dashboard'))

    return render_template("upload.html")


def _get_file_path(content):
    return os.path.join(
        current_app.config['UPLOAD_FOLDER'],
        content.subject,
        content.chapter,
        content.filename
    )


@views.route('/download/<int:content_id>')
@login_required
def download_file(content_id):
    content = Content.query.get_or_404(content_id)
    file_path = _get_file_path(content)
    if not os.path.exists(file_path):
        abort(404)
    return send_file(file_path, as_attachment=True)


@views.route('/preview/<int:content_id>')
@login_required
def preview(content_id):
    content = Content.query.get_or_404(content_id)
    file_url = None
    file_ext = None
    if content.filename:
        file_ext = content.filename.rsplit('.', 1)[-1].lower()
        file_url = url_for('views.serve_file', content_id=content.id)
    return render_template('preview.html', content=content, file_ext=file_ext, file_url=file_url)


@views.route('/serve/<int:content_id>')
@login_required
def serve_file(content_id):
    content = Content.query.get_or_404(content_id)
    if not content.filename:
        abort(404)
    file_path = _get_file_path(content)
    if not os.path.exists(file_path):
        abort(404)
    return send_file(file_path)