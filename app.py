from cs50 import SQL
import os
from flask.helpers import get_flashed_messages
from helpers import login_required, lookup, usd
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from flask import Flask, redirect, render_template, request, session, flash
from flask_session import Session
from flask_login import current_user, LoginManager
from send_mail import send_mail
from models import *
import re

app = Flask(__name__)

ENV = 'development'

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


if ENV == 'development':
    POSTGRES = {
        'user': 'postgres',
        'pw': 'a2dejlnor9054',
        'db': 'mvpdb',
        'host': 'localhost',
        'port': '5432',
    }
    app.config['DEBUG'] = True
else:
    POSTGRES = {
        'user': 'yssnhbufmhvkze',
        'pw': '8fef3ac8f13467f5123dfa014bcafabc29d5d4113df3c775135277865fb850d8',
        'db': 'd24dr5l6kfgcbh',
        'host': 'ec2-34-194-14-176.compute-1.amazonaws.com',
        'port': '5432',
    }
    app.config['DEBUG'] = False

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

with app.app_context():
    db.create_all()


@app.route('/')
@login_required
def home():
    return render_template('home.html')


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")
        confirmation = request.form.get("confirmation")
        terms = request.form.get("terms")
        # Ensure the username was submitted
        if not username:
            message = 'Please insert a username'
        # Ensure the username doesn't exists
        elif db.session.query(Person).filter(Person.username == username).count() != 0:
            message = 'This username already exists'
        elif not email and not EMAIL_REGEX.match(email):
            message = 'Please provide a valid Email'
        # Ensure password was submitted
        elif not password:
            message = 'Please provide a password'
        # Ensure confirmation password was submitted
        elif not request.form.get("confirmation"):
            message = 'Please fill the confirmation'
        # Ensure passwords match
        elif not password == confirmation:
            message = 'Password and confirmation must be equal'
        elif not terms:
            message = 'Please read and accept the terms and conditions'
        else:
            # Generate the hash of the password
            password_hash = generate_password_hash(
                password, method="pbkdf2:sha256", salt_length=8
            )
            # Insert the new user
            data = Person(username, email, password_hash)
            db.session.add(data)
            db.session.commit()
            # send_mail(customer, service, rating, comments)
            # Todo : add a successfully registered pop up confirmation
            # Todo : confirmation email of register
            # Redirect user to home page
            return redirect("/")
        return render_template("register.html", message=message)
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Forget any user_id
    session.clear()
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        # Ensure username was submitted
        if not username:
            return render_template("login.html", message='Please provide a valid Username')
        # Ensure password was submitted
        elif not password:
            return render_template("login.html", message='Please provide a Password')
        # Query database for username
        query = db.session.query(Person).filter(Person.username == username).first()
        user = repr(query).split(", ")[0]
        password = repr(query).split(", ")[1]
        personid = repr(query).split(", ")[2]
        # Ensure username exists and password is correct
        if user != username or not check_password_hash(password, request.form.get("password")):
            return render_template("login.html", message='Invalid username or password')
        else:
            # Remember which user has logged in
            session["user_id"] = personid
            # Redirect user to home page
            return redirect("/success")
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""
    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/forgot_password")
def forgot_password():
    # Todo: add a password resent method
    pass


@app.route("/success")
def success():
    return render_template('success.html')


if __name__ == '__main__':
    app.run()
