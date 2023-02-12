# BYBO
Backend application for "Backyards By Owner" web application built with Flask

Full application deployed at: https://bybo-react-nm.surge.sh/

Front-end repository: https://github.com/nico-martinucci/bybo-react

## Features
- RESTful API for authentication, authorization, and posting/listing bookings
- AWS S3 image upload functionality to show photos for posted listings

## Setting it up
1. Create a virtual environment and install requirements:
```
$ python3 -m venv venv
$ source venv/bin/activate
$ pip3 install -r requirements.txt
```
2. Set up the database (PostgreSQL):
```
$ psql
=# CREATE DATABASE bybo;
(ctrl+D)
```
3. Add a .env file with:
```
SECRET_KEY=(any secret key you want)
DATABASE_URL=postgresql:///warbler
```
4. Run the server:
```
$ flask run -p 5001
```
5. View at `localhost:5001`

## // TODO
- Write better error handling
- Add tests