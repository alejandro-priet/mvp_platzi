from helpers import login_required
from werkzeug.security import check_password_hash, generate_password_hash
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from datetime import timedelta
from models import *
import re

app = Flask(__name__)

ENV = 'development'

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.permanent_session_lifetime = timedelta(minutes=5)
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
def mmap():
    username = session['username']
    return render_template('map.html', username=username)


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
            session['username'] = username
            session["user_id"] = personid
            session.permanent = True
            # Redirect user to home page
            return redirect("/category_selection")
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route('/category_selection')
@login_required
def category_selection():
    return render_template('category_selection.html')


@app.route('/selected_successfully', methods=['GET', 'POST'])
@login_required
def selected_successfully():
    if request.method == 'POST':
        if request.form.get('sport') is not None:
            # Todo: set array of multiple category selections and send it to database in a query (maybe a for or direct an array)
        return redirect('/')
    else:
        return redirect('/category_selection')


@app.route("/logout")
@login_required
def logout():
    """Log user out"""
    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/forgot_password")
def forgot_password():
    # Todo: add a password reset method
    pass


@app.route('/profile')
@login_required
def profile():
    username = session['username']
    return render_template('profile.html', username=username)


@app.route("/success")
@login_required
def success():
    return render_template('success.html')


@app.route('/discover')
@login_required
def discover():
    username = session['username']
    return render_template('discover.html', username=username)


@app.route('/add_event')
@login_required
def add_event():
    return render_template('add_event.html')


@app.route('/notifications')
@login_required
def notifications():
    return render_template('notifications.html')


@app.route('/sidebar')
@login_required
def sidebar():
    return render_template('sidebar.html')


if __name__ == '__main__':
    app.run()
