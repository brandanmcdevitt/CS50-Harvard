# application.py

# Brandan McDevitt
# Harvard Computer Science 50
# Problem Set 7

# Implement a website via which users can "buy" and "sell" stocks.

import os
import datetime

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

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

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    symbol = []
    dataDict = {}
    grandTotal = []
    atotal = []

    userID = session["user_id"]

    rows = db.execute("SELECT * FROM users WHERE id = :userID", userID=userID)
    username = rows[0]["username"]
    cash = float(rows[0]["cash"])

    historyRows = db.execute("SELECT * FROM history WHERE username = :username", username=username)

    for i in range(len(historyRows)):
        symbol.append(historyRows[i]["symbol"])

    for j in range(len(symbol)):

        sy = lookup(symbol[j])

        # if sy = null, return apology
        if sy == None:
            return apology("please enter a valid symbol", 403)
        # else loop through the dictionary and grab the values based on the key if found
        else:
            for key,value in sy.items():
                if key == "price":
                    bought = db.execute("SELECT SUM(purchased) FROM history WHERE username = :username AND symbol = :symbol",
                                        username=username, symbol=symbol[j])

                    sold = db.execute("SELECT SUM(sold) FROM history WHERE username = :username AND symbol = :symbol",
                                        username=username, symbol=symbol[j])

                    for sym, amo in bought[0].items():
                        total = round(amo * value, 2)

                        for key2, value2 in sold[0].items():
                            atotal.append(amo - value2)
                            dataDict[symbol[j]] = (atotal[j], value, total)

                        for key1, value1 in dataDict.items():
                            if value1[2] not in grandTotal:
                                grandTotal.append(value1[2])
    grandTotal = round(sum(grandTotal))

    return render_template("index.html", cash=cash, dataDict=dataDict, grandTotal=grandTotal)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "POST":

        if not request.form.get("symbol"):
            return apology("must provide symbol", 400)

        elif not request.form.get("shares"):
            return apology("must provide number of shares", 400)

         # if the user entered text then set it to userInput
        userInput = request.form.get("symbol")

        # sy = the dictionary value returned from lookup(userInput)
        sy = lookup(userInput)

        # if sy = null, return apology
        if sy == None:
            return apology("please enter a valid symbol", 400)
        # else loop through the dictionary and grab the values based on the key if found
        else:
            for key,value in sy.items():
                if key == "name":
                    name = value
                elif key == "price":
                    price = value
                elif key == "symbol":
                    symbol = value
        try:
            if int(request.form.get("shares")) <= 0:
                return apology("please enter a positive number", 400)
            elif request.form.get("shares").isdigit == False:
                return apology("please enter a positive number", 400)
        except:
            return apology("please enter a positive number", 400)
        else:
            shares = int(request.form.get("shares"))

        userID = session["user_id"]

        rows = db.execute("SELECT * FROM users WHERE id = :userID", userID=userID)
        cash = int(rows[0]["cash"])

        if cash >= price * shares:
            newCash = cash - price * shares

            db.execute("INSERT INTO history (username, symbol, price, purchased, transaction_date) VALUES (:username, :symbol, :price, :purchased, :transaction_date)"
            , username=rows[0]["username"], symbol=userInput, price=price, purchased=shares, transaction_date=datetime.datetime.now())

            db.execute("UPDATE users SET cash = :newCash WHERE id = :userID", newCash=newCash, userID=userID)

        total = price * shares
        gTotal = (price * shares) + newCash

        return render_template("bought.html", newCash=usd(newCash), symbol=userInput, price=usd(price), purchased=shares, total=usd(total), grandTotal=usd(gTotal))

    else:
        return render_template("buy.html")

@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    data = []

    userID = session["user_id"]

    rows = db.execute("SELECT * FROM users WHERE id = :userID", userID=userID)
    username = rows[0]["username"]

    historyRows = db.execute("SELECT * FROM history WHERE username = :username", username=username)

    for i in range(len(historyRows)):

        an_item = dict(symbol=historyRows[i]["symbol"],
                        price=historyRows[i]["price"],
                        purchased=historyRows[i]["purchased"],
                        sold=historyRows[i]["sold"],
                        transaction=historyRows[i]["transaction_date"])
        data.append(an_item)

    return render_template("history.html", data=data)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":

        # validating whether user entered a symbol in the text field
        if not request.form.get("symbol"):
            return apology("please do not leave fields empty", 400)

        # if the user entered text then set it to userInput
        userInput = request.form.get("symbol")

        # sy = the dictionary value returned from lookup(userInput)
        sy = lookup(userInput)

        # if sy = null, return apology
        if sy == None:
            return apology("please enter a valid symbol", 400)
        # else loop through the dictionary and grab the values based on the key if found
        else:
            for key,value in sy.items():
                if key == "name":
                    name = value
                elif key == "price":
                    price = usd(value)
                elif key == "symbol":
                    symbol = value

            # return the qouted.html page, passing through values name, symbol and price
            return render_template("quoted.html", name=name, symbol=symbol, price=price)

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users")

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
        db.execute("INSERT INTO users (username, hash) VALUES (:username, :password)", username=request.form.get("username"), password=password)

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    symbols = []
    bought = []
    sold = []
    total = []
    data = {}

    userID = session["user_id"]

    rows = db.execute("SELECT * FROM users WHERE id = :userID", userID=userID)
    username = rows[0]["username"]
    cash = float(rows[0]["cash"])

    historyRows = db.execute("SELECT * FROM history WHERE username = :username", username=username)

    for i in range(len(historyRows)):
        if historyRows[i]["symbol"] not in symbols:
            symbols.append(historyRows[i]["symbol"])

    for j in range(len(symbols)):

        bought = db.execute("SELECT SUM(purchased) FROM history WHERE username = :username AND symbol = :symbol",
                username=username, symbol=symbols[j])

        sold = db.execute("SELECT SUM(sold) FROM history WHERE username = :username AND symbol = :symbol",
                username=username, symbol=symbols[j])

        for key1, value1 in bought[0].items():
            for key2, value2 in sold[0].items():
                total.append(value1 - value2)

        for key, value in bought[0].items():
            data[symbols[j]] = value

    if request.method == "POST":

        if request.form.get("symbol") == "select":
            return apology("you must select a stock symbol to sell", 400)

        if not request.form.get("shares") or int(request.form.get("shares")) <= 0:
            return apology("You must select a positive number of shares to sell", 400)

        sy = lookup(request.form.get("symbol"))

        # if sy = null, return apology
        if sy == None:
            return apology("please enter a valid symbol", 400)
        # else loop through the dictionary and grab the values based on the key if found
        else:
            for key,value in sy.items():
                if key == "price":
                    price = value

        if int(request.form.get("shares")) > data[request.form.get("symbol")]:
            return apology("You do not own enough shares for this sale", 400)
        else:
            db.execute("INSERT INTO history (username, symbol, price, sold, transaction_date) VALUES (:username, :symbol, :price, :sold, :transaction_date)"
            , username=username, symbol=request.form.get("symbol"), price=price, sold=request.form.get("shares"), transaction_date=datetime.datetime.now())

            newCash = cash + (price * int(request.form.get("shares")))
            db.execute("UPDATE users SET cash = :newCash WHERE id = :userID", newCash=newCash, userID=userID)

        shares = int(request.form.get("shares"))
        symbol = request.form.get("symbol")
        mTotal = price * shares
        gTotal = (price * shares) + newCash


        return render_template("sold.html",newCash=usd(newCash), symbol=symbol, price=usd(price), sold=shares, total=usd(mTotal), grandTotal=usd(gTotal))

    else:
        return render_template("sell.html", data=data)


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
