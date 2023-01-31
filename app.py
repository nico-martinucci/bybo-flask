import os
from dotenv import load_dotenv
from flask import (Flask, g, request, session, jsonify)
from flask_cors import CORS
from files import post_new_file

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ['DATABASE_URI'].replace("postgres://", "postgresql://"))
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

post_new_file("pictures/3_Backyard-Oasis-Ideas.jpg")
