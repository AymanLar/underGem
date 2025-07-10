from flask import render_template, request, redirect, url_for, flash
from validators import url as validate_url
from models import db, Submission, User
from constants import GENRE_LIST
from flask_user import login_required, current_user

def init_routes(app):
    @app.route('/')
    def index():
        return render_template('index.html')

    # Flask-User authentication routes
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        return app.user_manager.login_view()

    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        return app.user_manager.register_view()

    @app.route('/user/logout')
    def logout():
        return app.user_manager.logout_view()

    @app.route('/submit', methods=['GET', 'POST'])
    def submit():
        if request.method == 'POST':
            # Validate input
            url = request.form.get('url')
            if not validate_url(url):
                flash('Please enter a valid URL', 'error')
                return redirect(url_for('submit'))

            # Create submission
            submission = Submission(
                artist_name=request.form.get('artist_name'),
                track_title=request.form.get('track_title'),
                url=url,
                description=request.form.get('description'),
                genre=request.form.get('genre'),
                region=request.form.get('region')
            )
            db.session.add(submission)
            db.session.commit()

            # Get random untraded submission
            exchange = Submission.query.filter(
                Submission.traded == False,
                Submission.id != submission.id
            ).order_by(db.func.random()).first()

            if exchange:
                exchange.traded = True
                db.session.commit()
                return render_template('exchange.html', track=exchange)
            
            return render_template('no_exchange.html')

        return render_template('submit.html')

    @app.route('/profile')
    def profile():
        submissions = Submission.query.all()  # Get all submissions for testing

        # Build activity grid (last 49 days)
        from collections import Counter
        import datetime
        today = datetime.date.today()
        
        # Calculate the start of the week (Monday) for the most recent week
        days_since_monday = today.weekday()  # 0=Monday, 6=Sunday
        start_of_week = today - datetime.timedelta(days=days_since_monday)
        
        # Create 49 days starting from 6 weeks ago
        start_date = start_of_week - datetime.timedelta(weeks=6)
        days = [start_date + datetime.timedelta(days=i) for i in range(49)]
        
        day_counts = Counter(sub.timestamp.date() for sub in submissions)
        grid = [day_counts.get(day, 0) for day in days]
        
        # 7x7 grid (7 weeks, 7 days each)
        grid_rows = [grid[i*7:(i+1)*7] for i in range(7)]

        return render_template('profile.html', grid_rows=grid_rows, days=days, submissions=submissions)

    @app.route('/edit_profile', methods=['GET', 'POST'])
    def edit_profile():
        selected_genres = []
        if request.method == 'POST':
            genres = request.form.getlist('genres_interested')
            flash('Profile updated!', 'success')
            selected_genres = genres
        return render_template('edit_profile.html', genre_list=GENRE_LIST, selected_genres=selected_genres)

    @app.route('/admin')
    @login_required
    def admin():
        # Only allow users with Admin or Owner role
        user_roles = [role.name for role in current_user.roles]
        if 'Admin' not in user_roles and 'Owner' not in user_roles:
            flash('You do not have permission to access the admin page.', 'error')
            return redirect(url_for('index'))
        submissions = Submission.query.order_by(Submission.timestamp.desc()).all()
        return render_template('admin.html', submissions=submissions)

    @app.route('/dashboard')
    def dashboard():
        # Owner dashboard example
        user_count = User.query.count()
        submission_count = Submission.query.count()
        return render_template('dashboard.html', user_count=user_count, submission_count=submission_count) 