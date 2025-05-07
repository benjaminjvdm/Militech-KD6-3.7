# Cyberpunk 2077-themed Flask Productivity Suite

A suite of modular Flask web applications with a unified Cyberpunk 2077 aesthetic, displayed on a single dashboard page after a themed login.

## Project Structure

```
/cyberpunk_suite_project
├── main_suite_app.py         # Main Flask app
├── .env                      # Environment variables (sensitive data)
├── .gitignore                # Specifies intentionally untracked files
├── requirements.txt          # Python dependencies
├── /app_scheduler            # Chrono-Scheduler module
│   ├── scheduler_app.py      # Flask app logic
│   ├── /templates            # HTML templates for scheduler UI
│   │   └── scheduler_index.html
│   └── /static               # Static files (if any, specific to scheduler)
├── /app_email_filter         # Signal Sorter module
│   ├── email_filter_app.py   # Flask app logic
│   ├── /templates            # HTML templates for email filter UI
│   │   └── email_filter_index.html
│   └── /static               # Static files (if any, specific to email filter)
├── /app_news_aggregator      # DataStream Aggregator module
│   ├── news_aggregator_app.py# Flask app logic
│   ├── /templates            # HTML templates for news aggregator UI
│   │   └── news_aggregator_index.html
│   └── /static               # Static files (if any, specific to news aggregator)
├── /suite_templates          # Templates for the main suite (login, dashboard)
│   ├── login.html
│   └── suite_dashboard.html
└── /shared_static            # Common static files (CSS, fonts, images)
    └── cyberpunk_theme.css
    └── /fonts                # Placeholder for font files
    └── /img                  # Placeholder for image files
```

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd cyberpunk_suite_project
    ```

2.  **Create a Python virtual environment:**
    ```bash
    python -m venv venv
    ```

3.  **Activate the virtual environment:**
    *   On macOS and Linux:
        ```bash
        source venv/bin/activate
        ```
    *   On Windows:
        ```bash
        venv\Scripts\activate
        ```

4.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Configure environment variables:**
    *   Copy the `.env.example` (if you create one, otherwise use the provided `.env`) and rename it to `.env`.
    *   Update the variables in `.env` with your actual credentials and API keys. **Do not commit your `.env` file to version control.**

    ```bash
    cp .env.example .env # If .env.example exists
    # Or just edit the existing .env file
    ```

6.  **Google Calendar API Setup (for Chrono-Scheduler):**
    *   Follow the Google Calendar API documentation to enable the API and download your `client_secret.json` file.
    *   Place the `client_secret.json` file in the `cyberpunk_suite_project` directory.
    *   The first time you use the Chrono-Scheduler, you will likely be prompted to authorize the application via your browser. A `token.json` file will be created to store your credentials securely.

7.  **NewsAPI.org Setup (for DataStream Aggregator):**
    *   Sign up for a free developer account at [https://newsapi.org/](https://newsapi.org/).
    *   Obtain your API key from your dashboard.
    *   Add your API key to the `NEWSAPI_KEY` variable in your `.env` file.
    *   Be mindful of the usage limits and attribution requirements of your chosen plan.

## Running the Application

1.  **Activate your virtual environment** (if not already active).
2.  **Navigate to the project directory:**
    ```bash
    cd cyberpunk_suite_project
    ```
3.  **Run the main Flask application:**
    ```bash
    python main_suite_app.py
    ```

The application should start and be accessible at `http://127.0.0.1:5000/` (or the port indicated in the console output).

## Application Modules

### Chrono-Scheduler

*   **Objective:** Schedule tasks in Google Calendar using natural language.
*   **Dependencies:** `dateparser`, `google-api-python-client`, `google-auth-oauthlib`.
*   **Configuration:** Requires Google Calendar API setup and `client_secret.json`.
*   **Usage:** Enter a natural language description of your task in the input field on the dashboard and click "Log Task".

### Signal Sorter

*   **Objective:** Filter and prioritize emails using AI/ML or rules.
*   **Dependencies:** `imaplib`, `email`, `scikit-learn`, `python-dotenv`. (Optional: Google OAuth for Gmail).
*   **Configuration:** Requires email account credentials (IMAP or OAuth). Filter rules/categories can be configured (implementation pending).
*   **Usage:** Authenticate your email link and then scan transmissions.

### DataStream Aggregator

*   **Objective:** Aggregate news from RSS feeds and News APIs.
*   **Dependencies:** `feedparser`, `requests`, `python-dotenv`. (Optional: `Flask-APScheduler`, `NLTK`, `spaCy`).
*   **Configuration:** Requires NewsAPI.org API key and configuration of RSS feeds/keywords (implementation pending).
*   **Usage:** Compile the datastream to view aggregated news articles.

## Theming

The suite uses a Cyberpunk 2077-inspired theme with dark colors, neon accents, and a futuristic font. The core styles are in `shared_static/cyberpunk_theme.css`. Tailwind CSS can be integrated for more advanced styling and responsiveness.

## Error Handling

Basic themed error handling is included, including the "Relic Error - 333" message for application sections that fail to load within the dashboard.

## Future Enhancements

*   Full implementation of Google Calendar integration in Chrono-Scheduler.
*   Complete email filtering logic (rule-based and/or ML) in Signal Sorter.
*   User interface for configuring filter rules and news sources.
*   Background tasks for fetching emails and news.
*   More advanced Cyberpunk visual effects and animations.
*   Integration of Tailwind CSS for a more robust frontend framework.
*   Proper error handling and display for iframe loading failures.
*   User authentication and management (beyond the themed login).