import os
from dotenv import load_dotenv
from flask import (Flask, g, request, session, jsonify)
from flask_cors import CORS
from files import post_new_file
from models import (db, connect_db, User, Listing, Message, Booking)

load_dotenv()

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ['DATABASE_URI'].replace("postgres://", "postgresql://"))
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
db.create_all()

post_new_file("pictures/3_Backyard-Oasis-Ideas.jpg")

# ******************************************************************************
# User routes
# - post login user
@app.post("/api/users/authenticate")
def login_existing_user():
    """ 
    Logs in an existing user
    Needs {username, password} 
    Returns JWT (that includes username and id)
    """

# - post signup user
@app.post("/api/users/register")
def signup_new_user():
    """ 
    Registers a new user
    Needs {email, firstName, lastName, username, password}  
    Returns JWT (that includes username and id)
    """

# - post logout user
@app.post("/api/users/logout")
def logout_user():
    """ 
    Logout current user 
    """

# - get user detail (incl. user's current bookings)
@app.get("/api/users/<id>")
def get_user_detail(id):
    """ 
    Retrieves detailed information about a user, including their current
    bookings and their listings
    Returns {username, email, firstName, lastName, bio, [listings], [bookings]}
        where listings = [{id, name, description, location, photo}, ... ]
        where bookings = [{id, name, description, location, photo}, ... ]
    """

# ******************************************************************************
# Listing routes
# - get listings (all or optional filtering)
@app.get("/api/listings")
def get_all_listings():
    """ 
    Retrieves list of all listings, optionally filtered by query parameter (for
    now just by name of listing - maybe more to come later???)
    Returns [{id, name, description, location, photo, price}, ... ] 
    """

# - get listing detail (incl. listing's current bookings)
@app.get("/api/listings/<id>")
def get_listing_detail(id):
    """ 
    Retrieves detailed information about a listing, including summary 
    information on host and current reservations
    Returns {name, description, location, size, photo, price, has_pool, is_fenced, 
            has_barbecue, {host}, [bookings]}
        where host = {id, username}
        where bookings = [day, day, day, ... ]
    """

# - post new listing
@app.post("/api/listings")
def add_new_listing():
    """
    Create a new listing
    Needs {name, description, location, size, photo, price, has_pool, is_fenced, 
            has_barbecue, user_id}
    Returns {name, description, location, size, photo, has_pool, is_fenced, 
            has_barbecue, {host}, [bookings]}
    """

# - post new booking
@app.post("/api/listings/<id>/bookings")
def create_new_booking(id):
    """ 
    Creates a new booking
    Needs {user_id, [days]}
        where days = [day, day, day, ... ]
    Returns [day, day, day, ... ]
    """

# - delete existing booking
@app.delete("/api/listings/<listing_id>/bookings/<booking_id>")
def delete_booking(listing_id, booking_id):
    """
    Deletes an existing booking; 
    Needs {username, JWT}
    Returns {deleted: booking_id}
    """

# ******************************************************************************
# Message routes
# - get all messages to user
@app.get("/api/messages/<user_id>/to")
def get_to_user_messages(id):
    """
    Retrieve list of messages sent TO identified user
    Returns [{id, text, timestamp, from_user_id, is_read}, ... ]
    """

# - get all messages from user
@app.get("/api/messages/<user_id>/from")
def get_from_user_messages(id):
    """
    Retrieve list of messages sent FROM identified user
    Returns [{id, text, timestamp, to_user_id, is_read}, ... ]
    """

# - post new message
@app.post("/api/messages")
def send_new_message():
    """
    Creates a new message from one user to another
    Needs {text, from_user_id, to_user_id}
    Returns {id}
    """
















