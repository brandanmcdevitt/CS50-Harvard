# application.py

# Brandan McDevitt
# Harvard Computer Science 50
# Final Project

# A website for struggling students to find available mentoring teachers to help them.

import os
import datetime

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///management.db")


@app.route("/")
@login_required
def index():
    """Show menu"""

    # get the user_id stored in the session to grab the logged in user
    admin_id = session["user_id"]
    # querying the database with the admin_id
    rows = db.execute("SELECT * FROM admin WHERE admin_id = :admin_id", admin_id=admin_id)
    # setting the username from the database column
    username = rows[0]["username"]

    # return the index.html page and pass in the username
    return render_template("index.html", username=username)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            userError = "No username entered"
            return render_template("login.html", userError=userError)

        # Ensure password was submitted
        elif not request.form.get("password"):
            passError = "No password entered"
            return render_template("login.html", passError=passError)

        # Query database for username
        rows = db.execute("SELECT * FROM admin WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            bothError = "Invalid username/password"
            return render_template("login.html", bothError=bothError)

        # Remember which user has logged in
        session["user_id"] = rows[0]["admin_id"]

        # Redirect user to home page
        return redirect("/")

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


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register admin"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM admin")

        # check to see if username already exists in database
        for i in range(len(rows)):
            if request.form.get("username").lower() == rows[i]["username"].lower():
                return apology("username already exists", 400)

        # if the password or confirmation input is empty
        if not request.form.get("password") or not request.form.get("confirmation"):
            return apology("password/confirm password must not be empty", 400)

        # checking to make sure that the password and confirmation match
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords do not match", 400)
        # if they match then hash the password input
        else:
            password = generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8)

        # INSERT the username and hashed password to the database
        db.execute("INSERT INTO admin (username, hash) VALUES (:username, :password)", username=request.form.get("username"), password=password)

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/teacher-registration", methods=["GET", "POST"])
@login_required
def teacherRegistration():
    """Register Teachers to the system"""

    # setting up an empty list
    subjects = []

    # querying the database
    rows = db.execute("SELECT * FROM subjects")

    # for loop to append each subject into the list
    for i in range(len(rows)):
        subjects.append(rows[i]["subject"])

    if request.method == "POST":

        # declaring variables
        forename = request.form.get("forename")
        surname = request.form.get("surname")
        address = request.form.get("address")
        town = request.form.get("town")
        county = request.form.get("county")
        post_code = request.form.get("postcode")
        contact_type = request.form.get("contact_type")
        phone = request.form.get("phone")
        email = request.form.get("email")
        subject = request.form.get("subject")

        # inserting registered user into the database
        db.execute("INSERT INTO staff (forename, surname, address, town, county, post_code, contact_type, phone, email, subject) VALUES" +
        " (:forename, :surname, :address, :town, :county, :post_code, :contact_type, :phone, :email, :subject)",
        forename=forename, surname=surname, address=address, town=town, county=county, post_code=post_code, contact_type=contact_type,
        phone=phone, email=email, subject=subject)

        return redirect("/")

    else:
        return render_template("teacher-registration.html", subjects=subjects)

@app.route("/teacher-details", methods=["GET", "POST"])
@login_required
def teacherDetails():
    """Select teacher to view details"""

    # declaring empty lists
    forenames = []
    surnames = []

    # zipping the names as tuples
    names = zip(forenames, surnames)

    # querying the database
    rows = db.execute("SELECT * FROM staff")

    # looping through rows to appened the forename and surname to their lists
    for i in range(len(rows)):
        forenames.append(rows[i]["forename"])
        surnames.append(rows[i]["surname"])

    if request.method == "POST":

        details = db.execute("SELECT * FROM staff WHERE forename = :forename", forename=request.form.get("name"))

        return render_template("details.html", details=details[0])

    else:
        return render_template("teacher-details.html", names=names)

@app.route("/select-update", methods=["GET", "POST"])
@login_required
def selectUpdate():
    """Select teacher to update availability in database"""

    # declaring empty lists
    forenames = []
    surnames = []

    # zipping lists as tuples
    names = zip(forenames, surnames)

    # querying the database
    rows = db.execute("SELECT * FROM staff")

    # appending info to their lists
    for i in range(len(rows)):
        forenames.append(rows[i]["forename"])
        surnames.append(rows[i]["surname"])

    if request.method == "POST":

        details = db.execute("SELECT * FROM staff WHERE forename = :forename", forename=request.form.get("name"))

        return render_template("update.html", details=details[0])

    else:
        return render_template("select-update.html", names=names)

@app.route("/update", methods=["GET", "POST"])
@login_required
def update():
    """Update availability in the database"""

    if request.method == "POST":

        # declaring variables
        forename = request.form.get("forename")
        surname = request.form.get("surname")
        subject = request.form.get("subject")
        date = request.form.get("date")
        start = request.form.get("start")
        finish = request.form.get("finish")

        # inserting information into the database for teacher availability
        db.execute("INSERT INTO availability (forename, surname, subject, date, start, finish) VALUES (:forename, :surname, :subject, :date, :start, :finish)",
        forename=forename, surname=surname, subject=subject, date=date, start=start, finish=finish)

        return redirect("/")

    else:
        return render_template("update.html")

@app.route("/select-availability", methods=["GET", "POST"])
@login_required
def selectAvailability():
    """View availability"""

    # declaring lists and dicts
    subjects = []
    available = {}
    teachers = []

    rows = db.execute("SELECT * FROM availability")

    # looping through rows and appending the subject to subjects if the list does not already contain the subject
    for i in range(len(rows)):
        if rows[i]["subject"] not in subjects:
            subjects.append(rows[i]["subject"])

    if request.method == "POST":

        details = db.execute("SELECT * FROM availability WHERE subject = :subject", subject=request.form.get("subject"))

        # getting the date time information
        oldTime = datetime.datetime.now().strftime('%H:%M:%S')
        currDate = str(datetime.datetime.now().date())
        currTime = datetime.datetime.now().strftime('%H')

        # appening the teachers name to the teachers list
        for j in range(len(details)):
            if details[j]["forename"] not in teachers:
                teachers.append(details[j]["forename"])

            # checking if the current date is equal to the date of the available teacher
            if details[j]["date"] == currDate:
                startSplit = details[j]["start"].split(':', 1)[0]
                finishSplit = details[j]["finish"].split(':', 1)[0]
                # checking if the current time is within the start and finish time of the teacher
                if startSplit < currTime and finishSplit > currTime:
                    available[details[j]["forename"] + " " + details[j]["surname"]] = "green"
                else:
                    available[details[j]["forename"] + " " + details[j]["surname"]] = "red"

        subject = details[0]["subject"]

        return render_template("availability.html", available=available, subject=subject, date=currDate, time=oldTime)

    else:
        return render_template("select-availability.html", subjects=subjects)