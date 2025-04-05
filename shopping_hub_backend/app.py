# app.py
import os
from flask import Flask
# ... other imports ...
from config import Config
from extensions import db, bcrypt # Import extensions

# --- Create the App Instance FIRST ---
app = Flask(__name__)
app.config.from_object(Config)

# --- Initialize Extensions SECOND ---
db.init_app(app)
bcrypt.init_app(app)

# --- Define Models (by importing models.py) ---
# Make sure models are defined/imported before routes/commands use them
from models import User, Category # ... etc ...

# --- Define CLI Command THIRD (or later) ---
@app.cli.command("init-db")
def init_db_command():
    # ... command logic using 'app' and 'db' ...
    print("Initializing DB...")
    with app.app_context(): # Use app context if needed inside command
         db.create_all()
         # from seed_data import seed_database # Import here if not needed globally
         # seed_database()
    print("DB Initialized.")

# --- Define Routes FOURTH (or later) ---
@app.route('/')
def index():
    return "Hello!"

# --- Main Execution Block (Optional) ---
if __name__ == '__main__':
    app.run(debug=True)