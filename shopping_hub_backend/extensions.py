# extensions.py
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# Define the extension instances here, but don't initialize them with the app yet
db = SQLAlchemy()
bcrypt = Bcrypt()