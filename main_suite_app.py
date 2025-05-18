import os
from flask import Flask, render_template, request, redirect, url_for

# Import the scheduler module app
from app_scheduler.scheduler_app import scheduler_bp
# Import the email filter module blueprint
from app_email_filter.email_filter_app import email_filter_bp
# Import the news aggregator module blueprint
from app_news_aggregator.news_aggregator_app import news_aggregator_bp
# Import the finance charts module
from app_finance.finance_charts import generate_dashboard_chart, generate_15min_chart, generate_1hour_chart
import base64
import io
from flask_apscheduler import APScheduler

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

# Initialize scheduler
scheduler = APScheduler()
chart_data_cache = {}

def update_charts():
    """Generates and caches the latest financial charts."""
    print("Updating charts...")
    chart_5min_bytes = generate_dashboard_chart('GBPJPY=X')
    chart_15min_bytes = generate_15min_chart('GBPJPY=X')
    chart_1hour_bytes = generate_1hour_chart('GBPJPY=X')

    chart_data_cache['GBPJPY=X_5min'] = base64.b64encode(chart_5min_bytes).decode('ascii')
    chart_data_cache['GBPJPY=X_15min'] = base64.b64encode(chart_15min_bytes).decode('ascii')
    chart_data_cache['GBPJPY=X_1hour'] = base64.b64encode(chart_1hour_bytes).decode('ascii')
    print("Charts updated and cached.")

# Schedule the chart update job
# Run the update_charts function every 5 minutes
scheduler.add_job(id='update_finance_charts', func=update_charts, trigger='interval', minutes=5)


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
    Renders the cash suite dashboard page with financial charts.
    """
    # In a real application, you might add authentication checks here
    # Use cached chart data
    return render_template('cash_dashboard.html', charts=chart_data_cache)

@app.route('/get_charts')
def get_charts():
    """
    Returns the latest cached chart data as JSON.
    """
    return chart_data_cache

@app.route('/')
def index():
    """
    Redirects the root URL to the login page.
    """
    return redirect(url_for('login'))

if __name__ == '__main__':
    # Initialize and start the scheduler
    scheduler.init_app(app)
    scheduler.start()

    # Perform initial chart update to populate the cache
    update_charts()

    # Run the Flask development server
    # In production, use a production-ready WSGI server like Gunicorn or uWSGI
    app.run(debug=True, port=5001)