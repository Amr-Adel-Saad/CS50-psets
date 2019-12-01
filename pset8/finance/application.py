import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
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

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    # Query database for username and cash corresponding to current user_id
    rows1 = db.execute("SELECT username,cash FROM users WHERE id=:userid", userid=session["user_id"])
    username = rows1[0]["username"]
    cash = rows1[0]["cash"]

    # Query database for symbol and sum shares for each one
    rows2 = db.execute("SELECT symbol, sum(shares) FROM transactions WHERE id=:userid GROUP BY symbol", userid=session["user_id"])

    stocks = []
    # Get information from each row in rows2
    for row in rows2:
        info = lookup(row["symbol"])
        # Append a new key,value pair into info dictionary
        info.update({"shares": row["sum(shares)"]})
        # Append a info into stocks list
        stocks.append(info)

    return render_template("index.html", username=username, cash=cash, stocks=stocks, usd=usd)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    # User reached route via GET
    if request.method == "GET":
        return render_template("buy.html")

    # User reached route via POST
    else:
        # Validate user entries, and apologize if invalid
        info = lookup(request.form.get("symbol"))
        if not request.form.get("symbol") or info == None:
            return apology("invalid symbol")
        if not (request.form.get("shares")).isnumeric():
            return apology("invalid No. of shares")
        else:
            shares = int(request.form.get("shares"))

        if shares <= 0:
            return apology("invalid No. of shares")
        rows = db.execute("SELECT * FROM users WHERE id=:userid", userid=session["user_id"])
        remaining = rows[0]["cash"] - (shares * info["price"])
        if remaining < 0:
            return apology("cannot afford shares")

        # User provided valid entries
        else:
            # Insert info into database and modify user cash
            db.execute("UPDATE users SET cash=:remaining", remaining=remaining)
            db.execute("INSERT INTO transactions (id, symbol, price, shares) VALUES (:userid, :symbol, :price, :shares)",
                       userid=session["user_id"], symbol=info["symbol"], price=info["price"], shares=shares)

            flash("Bought!")
            return redirect("/")


@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""

    username = request.args.get("username")
    rows = db.execute("SELECT username FROM users")
    usernames = []
    for row in rows:
        usernames.append(row["username"])

    if len(username) >= 1 and username not in usernames:
        return jsonify(True)
    else:
        return jsonify(False)


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    # Query database for username corresponding to current user_id
    rows1 = db.execute("SELECT username FROM users WHERE id=:userid", userid=session["user_id"])
    username = rows1[0]["username"]

    rows2 = db.execute("SELECT symbol, price, shares, transaction_time FROM transactions WHERE id=:userid",
                       userid=session["user_id"])

    return render_template("history.html", username=username, rows2=rows2, usd=usd)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password")

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

    # User reached route via GET
    if request.method == "GET":
        return render_template("quote.html")

    # User reached route via POST
    else:
        # Using API, lookup info for symbol provided by user
        info = lookup(request.form.get("symbol"))

        # Symbol not available, apologize
        if info == None:
            return apology("symbol not available")

        # symbol available, render html page showing symbol's name, and price
        else:
            return render_template("quoted.html", name=info["name"], price=usd(info["price"]), symbol=info["symbol"])


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via GET
    if request.method == "GET":
        return render_template("register.html")

    # User reached route via POST
    else:
        usernames = []
        username = request.form.get("username")
        rows = db.execute("SELECT username FROM users")
        for row in rows:
            usernames.append(row["username"])
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        # Validate user submitted information
        if not username:
            return apology("must provide username")
        if username in usernames:
            return apology("username already exists")
        if not password or not confirmation:
            return apology("must provide password and confirmation")
        if password != confirmation:
            return apology("confirmation must match password")

        # Hash user's password
        hashed = generate_password_hash(password)

        # Insert user's info into database
        db.execute("INSERT INTO users(username, hash) VALUES(:username, :hashed)", username=username, hashed=hashed)
        rows = db.execute("SELECT * FROM users WHERE username=:username", username=username)

        # Store user's id in session to remember user
        session["user_id"] = rows[0]["id"]

        flash("Registered!")
        # Redirect user to home page
        return redirect("/")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    rows = db.execute("SELECT symbol, sum(shares) FROM transactions WHERE id=:userid\
    GROUP BY symbol", userid=session["user_id"])
    # User reached route via GET
    if request.method == "GET":
        return render_template("sell.html", rows=rows)

    # User reached route via POST
    else:
        rows2 = db.execute("SELECT symbol, sum(shares) FROM transactions WHERE id=:userid\
        AND symbol=:symbol GROUP BY symbol", userid=session["user_id"], symbol=request.form.get("symbol"))
        shares = int(request.form.get("shares"))
        info = lookup(request.form.get("symbol"))
        # Check for the validity of symbol and shares
        if not request.form.get("symbol") or not rows2[0]:
            return apology("invalid symbol")
        if not shares or rows2[0]["sum(shares)"] - shares < 0:
            return apology("invalid quantity of shares")
        else:
            reduced = -1 * shares
            # Updata database with new information
            db.execute("INSERT INTO transactions (id, symbol, price, shares) VALUES (:userid, :symbol, :price, :shares)",
                       userid=session["user_id"], symbol=info["symbol"], price=info["price"], shares=reduced)
            db.execute("UPDATE users SET cash=cash+:sold WHERE id=:userid", sold=shares*info["price"], userid=session["user_id"])

            flash("Sold!")
            # Redirect user to history
            return redirect("/")


@app.route("/cash", methods=["GET", "POST"])
@login_required
def cash():
    # User reached route via GET
    if request.method == "GET":
        return render_template("cash.html")

    # User reached route via POST
    else:
        # Get input and update database with new cash
        cash = request.form.get("cash")
        db.execute("UPDATE users SET cash=cash+:cash WHERE id=:userid", userid=session["user_id"], cash=cash)

        flash("Cash added!")
        # Redirect user to Home page
        return redirect("/")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
