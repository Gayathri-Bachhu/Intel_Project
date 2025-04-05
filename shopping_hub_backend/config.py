import os

# Find the absolute path of the directory containing config.py
basedir = os.path.abspath(os.path.dirname(__file__))
# Define the instance folder path relative to the base directory
instance_path = os.path.join(basedir, 'instance')

# Create the instance folder if it doesn't exist
os.makedirs(instance_path, exist_ok=True)

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-should-really-change-this-secret-key'
    # Use the constructed instance_path for the database URI
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(instance_path, 'database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # You might add other configs like mail server details for real password reset