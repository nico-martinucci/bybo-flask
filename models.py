from datetime import datetime

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

class User(db.Model):
    """User in the system"""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    email = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    first_name = db.Column(
        db.Text,
        nullable=False,
        unique=False,
    )

    last_name = db.Column(
        db.Text,
        nullable=False,
        unique=False,
    )

    username = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    bio = db.Column(
        db.Text,
    )

    password = db.Column(
        db.Text,
        nullable=False,
    )

class Message(db.Model):
    """All messages."""

    __tablename__ = 'messages'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    text = db.Column(
        db.String(140),
        nullable=False,
    )

    timestamp = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    from_user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
    )

    to_user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
    )

    is_read = db.Column(
        db.Boolean,
        nullable=False,
    )

class Listings(db.Model):
    """All listings"""

    __tablename__ = 'listings'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    name = db.Column(
        db.String,
        nullable=False
    )

    description = db.Column(
        db.String(140),
        nullable=False,
    )

    location = db.Column(
        db.String,
        nullable=False,
    )

    size = db.Column(
        db.String,
        nullable=False,
    )

    photo = db.Column(
        db.Text,
        nullable=False,
    )

    has_pool = db.Column(
        db.Boolean,
        nullable=False,
    )

    is_fenced = db.Column(
        db.Boolean,
        nullable=False,
    )

    has_barbecue = db.Column(
        db.Boolean,
        nullable=False,
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
    )

class Booking(db.Model):
    """All Bookings"""

    __tablename__ = 'bookings'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    day_of_week = db.Column(
        db.String,
        nullable=False,
    )

    user_id= db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
    )

    listing_id = db.Column(
        db.Integer,
        db.ForeignKey('listings.id', ondelete='CASCADE'),
        nullable=False,
    )



