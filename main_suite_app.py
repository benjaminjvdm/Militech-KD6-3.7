import os
from flask import Flask, render_template, request, redirect, url_for

# Import the scheduler module app
from app_scheduler.scheduler_app import scheduler_bp
# Import the email filter module blueprint
from app_email_filter.email_filter_app import email_filter_bp
# Import the news aggregator module blueprint
from app_news_aggregator.news_aggregator_app import news_aggregator_bp

# Initialize Flask app
app = Flask(__name__,
            template_folder='suite_templates',
            static_folder='shared_static')

# Set a secret key for session management (required for Flask)
# In a real app, this should be a strong, randomly generated value
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'a_very_secret_key_for_dev')

# Register the scheduler module app
app.register_blueprint(scheduler_bp, url_prefix='/scheduler')
# Register the email filter module blueprint
app.register_blueprint(email_filter_bp, url_prefix='/email_filter')
# Register the news aggregator module blueprint
app.register_blueprint(news_aggregator_bp, url_prefix='/news_aggregator')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handles the login page.
    GET: Displays the login form.
    POST: Processes the login form.
    """
    # Pre-fill username for thematic purposes
    themed_username = "Militech-KD6-3.7"

    if request.method == 'POST':
        password = request.form.get('password') # Assuming the password input field is named 'password'

        if password == 'mon':
            print("Login successful for 'mon'")
            return redirect(url_for('dashboard')) # Redirect to the current suite dashboard
        elif password == 'cash':
            print("Login successful for 'cash'")
            return redirect(url_for('cash_dashboard')) # Redirect to the cash suite dashboard
        else:
            # Handle invalid password - re-render login with an error message
            print("Invalid password")
            return render_template('login.html', themed_username=themed_username, error="Invalid password")

    # Handle GET request: Display the login form
    return render_template('login.html', themed_username=themed_username)

@app.route('/dashboard')
def dashboard():
    """
    Renders the main dashboard page displaying all three applications.
    """
    # In a real application, you might add authentication checks here
    return render_template('suite_dashboard.html')

@app.route('/cash_dashboard')
def cash_dashboard():
    """
    Renders the cash suite dashboard page with placeholders.
    """
    # In a real application, you might add authentication checks here
    return render_template('cash_dashboard.html')

@app.route('/')
def index():
    """
    Redirects the root URL to the login page.
    """
    return redirect(url_for('login'))

if __name__ == '__main__':
    # Run the Flask development server
    # In production, use a production-ready WSGI server like Gunicorn or uWSGI
    app.run(debug=True)