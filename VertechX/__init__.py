# Import necessary modules from Flask and related packages
from flask import Flask, request  # Flask core and request handling
from flask_sqlalchemy import SQLAlchemy  # SQLAlchemy for ORM and database interaction
from flask_bcrypt import Bcrypt  # Bcrypt for password hashing
from flask_login import LoginManager  # For user authentication and session management
from flask_cors import CORS # For Solve Cross-Origin Issues


# Initialize the Flask application with the specified template and static folders
app = Flask(__name__, template_folder='../Templates', static_folder='../static')

"""
This tells Flask:
- `__name__`: To base all paths relative to the current file.
- `template_folder`: HTML templates are located in '../Templates'.
- `static_folder`: Static files (CSS, JS, images, icons) are located in '../static'.
"""

# Solve Cross-Origin Issues
CORS(app)
"""
Cross-Origin Issues:-
    If you're running the frontend and backend on different ports (e.g., React on 3000 and Flask on 5000),
    you might be running into CORS (Cross-Origin Resource Sharing) issues. 
"""

# Configure The Secret Key for Forms part of the app instance
app.config['SECRET_KEY'] = '07ffbe30228892905abf8205'
"""
Set a secret key for the Flask app. This key is used to encrypt session cookies and forms for security purposes.
Make sure to keep the key secret and unique.
"""

# Set the configuration for SQLAlchemy to connect to a local SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///VerTechX.db'
"""
Configure the URI to connect to the SQLite database named 'VerTechX.db'.
- `SQLALCHEMY_DATABASE_URI`: Specifies the path to the database (local SQLite in this case).
"""

# Initialize the database with the app instance for use with SQLAlchemy
db = SQLAlchemy(app)
"""
Initialize the SQLAlchemy object with the Flask app instance.
- SQLAlchemy is used for interacting with the database through Object-Relational Mapping (ORM).
- `db` will be used to define models and manage database interactions.
"""

# Initialize the Bcrypt extension with the Flask app instance
bcrypt = Bcrypt(app)
"""
Initialize Bcrypt, which provides secure password hashing.
- Bcrypt is used to hash and check passwords securely, avoiding storing plaintext passwords in the database.
"""

# Initialize the LoginManager for user authentication
login = LoginManager(app)
login.init_app(app)  # Initialize the login manager with the Flask app
login.login_view = "Login_Page"  # Set the default route to redirect users to when they need to log in
login.login_message_category = 'info'  # Define the message category for login-related flash messages

"""
The LoginManager handles user authentication and manages user sessions.
- `login_view`: Defines the name of the route to redirect users if they attempt to access a login-required page.
- `login_message_category`: Sets the category for messages (such as login alerts or info).
"""

# Initialize all Routes in the Web App by importing the routes from the VertechX module
from VertechX import routes
"""
Import the routes for the Flask app from the VertechX module.
- This includes the definitions of all the URL endpoints and associated view functions.
"""

from VertechX import fastapiapp
