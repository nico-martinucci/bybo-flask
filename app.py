import os
import jwt
from jwt.exceptions import InvalidSignatureError
from dotenv import load_dotenv
from flask import (Flask, g, request, session, jsonify)
from flask_cors import CORS
from files import post_new_file
from models import (db, connect_db, User, Listing, Message, Booking)
from sqlalchemy.exc import IntegrityError

load_dotenv()

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ['DATABASE_URI'].replace("postgres://", "postgresql://"))
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

connect_db(app)
db.create_all()

# post_new_file("pictures/3_Backyard-Oasis-Ideas.jpg")


def verify_jwt(auth):
    """
    Takes in a JWT and authenticates it
    Throws an error if no token or invalid token
    """

    token = auth.split()[1]

    try:
        user_auth = jwt.decode(
            token,
            os.environ['SECRET_KEY'],
            algorithms=["HS256"]
        )
    except InvalidSignatureError:
        serialized = {
            "error": "invalid token"
        }

        return jsonify(serialized)

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
    try:
        user = User.authenticate(
            username = request.json["username"],
            password = request.json["password"]
        )
    except:
        return # TODO: add in better error handling for bad login

    serialized = jwt.encode(
        {"username": user.username, "id": user.id},
        "secret",
        algorithm="HS256"
    )

    return jsonify(token=serialized)


# - post signup user
@app.post("/api/users/register")
def signup_new_user():
    """
    Registers a new user
    Needs {email, firstName, lastName, username, password}
    Returns JWT (that includes username and id)
    """
    try:
        newUser = User.signup(
            email = request.json["email"],
            first_name = request.json["firstName"],
            last_name = request.json["lastName"],
            username = request.json["username"],
            password = request.json["password"],
        )
        db.session.commit()

    except IntegrityError:
        return # TODO: add in better error handling for bad signup

    serialized = jwt.encode(
        {"username": newUser.username, "id": newUser.id},
        "secret",
        algorithm="HS256"
    )

    return jsonify(token=serialized)


# - get user detail (incl. user's current bookings)
@app.get("/api/users/<user_id>")
def get_user_detail(user_id):
    """
    Retrieves detailed information about a user, including their current
    bookings and their listings
    Returns {id, username, email, firstName, lastName, bio, [listings], [bookings]}
        where listings = [{id, name, description, location, photo}, ... ]
        where bookings = [{id, name, description, location, photo}, ... ]
    """

    user = User.query.get_or_404(user_id)
    listings = [
        {
            "id": listing.id,
            "name": listing.name,
            "description": listing.description,
            "location": listing.location,
            "photo": listing.photo,
            "price": listing.price
        }
        for listing in user.managed_listings
    ]

    serialized = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "bio": user.bio,
        "listings": listings,
        "bookings": [] # TODO: turn this into a real thing
    }

    return jsonify(user=serialized)

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

    # TODO: add filtering capbility to this

    listings = Listing.query.all()

    serialized = [
        {
            "id": listing.id,
            "name": listing.name,
            "description":listing.description,
            "location":listing.location,
            "photo":listing.photo,
            "price":listing.price
        }
        for listing in listings
    ]

    return jsonify(listings = serialized)


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

    listing = Listing.query.get_or_404(id)

    serialized = {
        "name": listing.name,
        "description": listing.description,
        "location": listing.location,
        "size": listing.size,
        "photo": listing.photo,
        "price": listing.price,
        "has_pool": listing.has_pool,
        "is_fenced": listing.is_fenced,
        "has_barbecue": listing.has_barbecue,
        "host": {
            "id": listing.user_id,
            "username": listing.managed_by.username
        },
        "bookings": [] # TODO: make this real!
    }

    return jsonify(listing = serialized)

# - post new listing
@app.post("/api/listings")
def add_new_listing():
    """
    Create a new listing
    Needs {name, description, location, size, photo, price, has_pool, is_fenced,
            has_barbecue, user_id, token}
    Returns {id, name, description, location, size, photo, price, has_pool,
            is_fenced, has_barbecue, {host}, [bookings]}
        where host = {id, username}
        where bookings = [day, day, day, ... ]
    Requires authenticated user
    """

    verify_jwt(request.headers["Authorization"])

    print("request.files photo value:", request.files["photo"])

    #send picture to AWS and get back URL
    photo_url = post_new_file(request.files["photo"])

    # try:
    newListing = Listing(
        name=request.form["name"],
        description=request.form["description"],
        location=request.form["location"],
        size=request.form["size"],
        photo=photo_url,
        has_pool=bool(request.form["hasPool"]),
        is_fenced=bool(request.form["isFenced"]),
        has_barbecue=bool(request.form["hasBarbecue"]),
        user_id=request.form["userId"],
        price=request.form["price"],
    )

    db.session.add(newListing)
    # except:
    #     return # TODO: better error handling here

    db.session.commit()

    host = User.query.get_or_404(newListing.user_id)

    serialized = {
        "id": newListing.id,
        "name": newListing.name,
        "description": newListing.description,
        "location": newListing.location,
        "size": newListing.size,
        "photo": newListing.photo,
        "has_pool": newListing.has_pool,
        "is_fenced": newListing.is_fenced,
        "has_barbecue": newListing.has_barbecue,
        "price": newListing.price,
        "host": {
            "id": host.id,
            "username": host.username
        },
        "bookings": [] # TODO: make this real!
    }

    return jsonify(listing=serialized)

# - post new booking
@app.post("/api/listings/<listing_id>/bookings")
def create_new_booking(listing_id):
    """
    Creates a new booking
    Needs {user_id, [days]}
        where days = [day, day, day, ... ]
    Returns [day, day, day, ... ]
    Requires authenticated user
    """

    verify_jwt(request.headers["Authorization"])

    days = request.json["days"]

    for day in days:
        try:
            newBooking = Booking(
                day_of_week=day,
                user_id=request.json["user_id"],
                listing_id=listing_id,
            )
            db.session.add(newBooking)
        except:
            return # TODO: add better error handling

    db.session.commit()

    serialized = {
        "booked": days
    }

    return jsonify(serialized)

# - delete existing booking
@app.delete("/api/listings/<listing_id>/bookings/<booking_id>")
def delete_booking(listing_id, booking_id):
    """
    Deletes an existing booking;
    Needs {username, JWT}
    Returns {deleted: booking_id}
    Requires authenticated user TODO: implement this
    """

# ******************************************************************************
# Message routes
# - get all messages to user
@app.get("/api/messages/<user_id>/to")
def get_to_user_messages(id):
    """
    Retrieve list of messages sent TO identified user
    Returns [{id, text, timestamp, from_user_id, is_read}, ... ]
    Requires authenticated user TODO: implement this
    """

# - get all messages from user
@app.get("/api/messages/<user_id>/from")
def get_from_user_messages(id):
    """
    Retrieve list of messages sent FROM identified user
    Returns [{id, text, timestamp, to_user_id, is_read}, ... ]
    Requires authenticated user TODO: implement this
    """

# - post new message
@app.post("/api/messages")
def send_new_message():
    """
    Creates a new message from one user to another
    Needs {text, from_user_id, to_user_id}
    Returns {id}
    Requires authenticated user TODO: implement this
    """
















