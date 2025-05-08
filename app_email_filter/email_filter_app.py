import os
import imaplib
import email
from dotenv import load_dotenv
from flask import Blueprint, render_template, request, jsonify

# Load environment variables from .env file
load_dotenv()

# Initialize a Blueprint for the email filter module
# The url_prefix will be set when registering with the main app
email_filter_bp = Blueprint('email_filter', __name__,
                            template_folder='templates',
                            static_folder='static')

# Note: Secret key is configured in the main app, not here for a Blueprint

# --- Email Processing and Filtering ---
# Use imaplib, email, scikit-learn (optional), python-dotenv
# Handle secure credential storage and loading (.env)
# Implement AI/ML or rule-based filtering

def get_email_body(msg):
    """Extracts the plain text body from an email message."""
    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            cdispo = str(part.get('Content-Disposition'))

            # Look for plain text parts, avoiding attachments
            if ctype == 'text/plain' and 'attachment' not in cdispo:
                return part.get_payload(decode=True).decode()
            # If HTML is preferred and no plain text, get text from HTML (basic)
            if ctype == 'text/html' and 'attachment' not in cdispo:
                 # Basic HTML to text conversion (can be improved)
                import re
                html = part.get_payload(decode=True).decode()
                # Remove HTML tags
                text = re.sub('<[^>]*>', '', html)
                return text
    # If not multipart or no suitable parts found, try getting payload directly
    elif msg.get_content_type() == 'text/plain':
        return msg.get_payload(decode=True).decode()
    return "" # Return empty string if no body found

def extract_snippet(body, max_len=150):
    """Extracts a short snippet from the email body."""
    if not body:
        return "No body content."
    # Remove excessive whitespace and newlines
    body = ' '.join(body.split())
    if len(body) > max_len:
        return body[:max_len] + "..."
    return body

def connect_to_email():
    """Connects to the email server using credentials from environment variables."""
    imap_server = os.getenv('EMAIL_IMAP_SERVER')
    imap_port = os.getenv('EMAIL_PORT')
    email_address = os.getenv('EMAIL_ADDRESS')
    email_password = os.getenv('EMAIL_PASSWORD')

    if not all([imap_server, imap_port, email_address, email_password]):
        return {"status": "error", "message": "Email credentials not fully configured in .env"}

    try:
        # Connect to the IMAP server
        mail = imaplib.IMAP4_SSL(imap_server, int(imap_port))
        # Log in to the account
        mail.login(email_address, email_password)
        return {"status": "success", "message": "Neural Link Established.", "mail_object": mail}
    except Exception as e:
        return {"status": "error", "message": f"Connection Error: {e}"}

def fetch_and_filter_emails(criteria):
    """Fetches and filters emails based on criteria."""
    print("Scanning for incoming transmissions...")
    connection_result = connect_to_email()

    if connection_result["status"] == "error":
        return connection_result # Return error if connection failed

    mail = connection_result["mail_object"]

    try:
        # Select the inbox
        mail.select('inbox')

        # Search for emails (currently searching all emails)
        # TODO: Implement filtering based on 'criteria'
        status, messages = mail.search(None, 'ALL')

        emails = []
        if status == 'OK':
            # Process in reverse order to get most recent first
            for msg_id in messages[0].split()[::-1]:
                # Fetch the email
                status, msg_data = mail.fetch(msg_id, '(RFC822)')
                if status == 'OK':
                    raw_email = msg_data[0][1]
                    msg = email.message_from_bytes(raw_email)

                    # Extract relevant information
                    subject = msg['subject']
                    sender = msg['from']
                    body = get_email_body(msg)
                    snippet = extract_snippet(body)
                    # TODO: Implement category based on filtering logic
                    category = "Uncategorized"

                    emails.append({
                        "id": msg_id.decode(),
                        "sender": sender,
                        "subject": subject,
                        "snippet": snippet,
                        "category": category
                    })

        # Logout from the email server
        mail.logout()

        # TODO: Apply filtering rules/ML model to the fetched emails
        # For now, returning all fetched emails (or mock data if fetching fails)
        if not emails:
             # Return mock data if no emails are fetched
            mock_emails = [
                {"id": 1, "sender": "corpo@arasaka.com", "subject": "Urgent: Q3 Projections", "snippet": "Your quarterly projections are due...", "category": "Urgent Comms"},
                {"id": 2, "sender": "spam@nightcityads.net", "subject": "Get Rich Quick in Watson!", "snippet": "Invest in our new cyber-enhancement scheme...", "category": "Corpo-Spam"},
                {"id": 3, "sender": "netrunner@hidden.net", "subject": "Intel Drop: Location of Relic", "snippet": "Meet me at the Afterlife...", "category": "Intel Drops"},
            ]
            return {"status": "success", "message": "No new transmissions. Displaying cached data.", "emails": mock_emails}


        return {"status": "success", "message": "Transmissions sorted.", "emails": emails}

    except Exception as e:
        return {"status": "error", "message": f"Email Processing Error: {e}"}

def delete_email_by_id(email_id_to_delete):
    """Deletes an email by its ID."""
    print(f"Attempting to delete email with ID: {email_id_to_delete}")
    connection_result = connect_to_email()

    if connection_result["status"] == "error":
        return connection_result

    mail = connection_result["mail_object"]

    try:
        mail.select('inbox')
        # Mark the email for deletion
        result, data = mail.store(email_id_to_delete.encode(), '+FLAGS', '\\Deleted')
        if result == 'OK':
            # Expunge to permanently delete
            expunge_result, expunge_data = mail.expunge()
            if expunge_result == 'OK':
                # Check if any emails were expunged. expunge_data will list IDs of expunged emails.
                # If expunge_data is [None] or empty for some servers, it means no messages were expunged (e.g., ID not found or already deleted)
                # A successful deletion of a specific ID would typically result in that ID (or a list containing it) being in expunge_data.
                # However, the response can vary. A simple "OK" from expunge is often sufficient.
                print(f"Expunge result: {expunge_result}, Data: {expunge_data}")
                mail.logout()
                return {"status": "success", "message": f"Email ID {email_id_to_delete} marked for deletion and expunged."}
            else:
                mail.logout()
                return {"status": "error", "message": f"Failed to expunge email ID {email_id_to_delete}. Server response: {expunge_result}"}
        else:
            mail.logout()
            return {"status": "error", "message": f"Failed to mark email ID {email_id_to_delete} for deletion. Server response: {result}"}
    except Exception as e:
        # Ensure logout even if an error occurs
        if 'mail' in locals() and mail and mail.state == 'SELECTED':
            mail.logout()
        return {"status": "error", "message": f"Error deleting email: {e}"}


# --- Routes ---
@email_filter_bp.route('/')
def index():
    """
    Renders the main HTML page for the email filter application (to be embedded in iframe).
    This route is relative to the blueprint's url_prefix ('/email_filter').
    """
    return render_template('email_filter_index.html')

@email_filter_bp.route('/connect', methods=['POST'])
def connect():
    """
    Handles email server connection request.
    Attempts to connect using credentials from environment variables.
    """
    # No longer need to get credentials from request
    result = connect_to_email()
    # Remove mail_object from result before jsonify as it's not serializable
    if "mail_object" in result:
        del result["mail_object"]
    return jsonify(result)

@email_filter_bp.route('/fetch_and_filter', methods=['POST'])
def fetch_filter():
    """
    Handles request to fetch and filter emails.
    """
    criteria = request.get_json()
    result = fetch_and_filter_emails(criteria)
    return jsonify(result)

@email_filter_bp.route('/delete_email', methods=['POST'])
def delete_email_route():
    """
    Handles request to delete a specific email.
    Expects JSON payload with 'email_id'.
    """
    data = request.get_json()
    email_id = data.get('email_id')

    if not email_id:
        return jsonify({"status": "error", "message": "Email ID not provided."}), 400

    result = delete_email_by_id(email_id)
    return jsonify(result)

# This __main__ block is removed as the module will be run via the main app.