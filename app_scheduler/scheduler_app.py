import os
from flask import Blueprint, render_template, request, jsonify
# from datetime import timedelta # Uncomment when implementing dateparser

# Initialize a Blueprint for the scheduler module
# The url_prefix will be set when registering with the main app
scheduler_bp = Blueprint('scheduler', __name__,
                         template_folder='templates',
                         static_folder='static')

# Note: Secret key is configured in the main app, not here for a Blueprint

# --- Google Calendar Integration (Placeholder) ---
# In a real application, you would handle Google OAuth flow here
# and store/load user credentials securely.
# For now, this is just a placeholder.
def create_google_calendar_event(task_description, start_time, end_time):
    """
    Placeholder function to create a Google Calendar event.
    Requires Google Calendar API setup and authentication.
    """
    print(f"Attempting to schedule: {task_description} from {start_time} to {end_time}")
    # TODO: Implement actual Google Calendar API call
    # Use google-api-python-client and google-auth-oauthlib
    # Handle authentication, token storage, and event creation
    return {"status": "success", "message": f"Directive logged: '{task_description}'."}
    # return {"status": "error", "message": "Relic Error - Chrono-Sync Failed."}


# --- Routes ---
@scheduler_bp.route('/')
def index():
    """
    Renders the main HTML page for the scheduler application (to be embedded in iframe).
    This route is relative to the blueprint's url_prefix ('/scheduler').
    """
    return render_template('scheduler_index.html')

@scheduler_bp.route('/log_task', methods=['POST'])
def log_task():
    """
    Receives natural language task description and attempts to schedule it.
    """
    data = request.get_json()
    task_input = data.get('task_input', '').strip()

    if not task_input:
        return jsonify({"status": "error", "message": "Directive input empty. Access Denied."}), 400

    # --- Natural Language Parsing (Placeholder) ---
    # TODO: Implement dateparser logic here
    # Example using dateparser (install with: pip install dateparser)
    # import dateparser
    # settings = {'RETURN_AS_TIMEZONE_AWARE': True, 'TIMEZONE': 'UTC'} # Adjust timezone as needed
    # parsed_date = dateparser.parse(task_input, settings=settings)
    # if parsed_date:
    #     # Attempt to extract duration or end time
    #     start_time = parsed_date
    #     end_time = start_time + timedelta(hours=1) # Default 1 hour duration
    #     task_description = task_input # Refine description extraction if needed
    #     result = create_google_calendar_event(task_description, start_time, end_time)
    # else:
    #     result = {"status": "error", "message": "Chrono-Sync Failed: Unable to parse directive."}

    # Placeholder result for now
    result = create_google_calendar_event(task_input, "now", "now + 1hr") # Replace with parsed times

    return jsonify(result)

# This __main__ block is removed as the module will be run via the main app.