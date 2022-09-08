from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required, error
import sqlite3


# Configuration
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Load the database
def get_db_connection():
    conn = sqlite3.connect('marks.db')
    conn.row_factory = sqlite3.Row
    return conn





@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/login", methods=["GET", "POST"])
def login():
    '''
    Logs the user in, default landing page if not logged in.

    '''
    # Forget user id
    session.clear()

    # If from POST
    if request.method == "POST":
        if not request.form.get("username"):
            return error("Username not entered")
        if not request.form.get("password"):
            return error("Password not entered")
        # Get username and password
        username = request.form.get("username")
        password = request.form.get("password")

        # Query for hash which matches username
        conn = get_db_connection()
        hash = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchall()
        conn.close()
        # Check if correct
        if len(hash) != 1 or not check_password_hash(hash[0]["hash"], password):
            return error("Invalid username or password")

         # Remember which user logs in
        session["user_id"] = hash[0]["id"]

        # Redirect user to home page

        return redirect("/")

    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == "POST":
        if not request.form.get("username"):
            return error("username not entered")
        if not request.form.get("password"):
            return error("password not entered")
        if not request.form.get("confirmation"):
            return error("confirmation not entered")
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if password != confirmation:
            return error("password and confirmation do not match")
        db = get_db_connection()
        check = db.execute ("SELECT username FROM users WHERE username = ?", (username,)).fetchall()
        if len(check) != 0:
            return error("username already taken")

        db.execute("INSERT INTO users(username, hash) VALUES(?, ?)", (username, generate_password_hash(password)))
        db.commit()
        db.close()
        return redirect("/login")
    else:
        return render_template("register.html")

@app.route("/", methods = ["GET", "POST"])
@login_required
def homepage():
    user_id = session["user_id"]
    if request.method == "GET":
        obt = 0
        tot = 0
        db = get_db_connection()
        subjects = db.execute("SELECT * FROM subjects WHERE userid = ?", (user_id,)).fetchall()
        types = db.execute("SELECt * FROM types WHERE userid = ?", (user_id,)).fetchall()

        rows = db.execute("SELECT * FROM tests WHERE userid = ?", (user_id,)).fetchall()
        db.close()
        for tests in rows:
            obt += tests["marksobtained"]
            tot += tests["markstotal"]
        if tot == 0:
            percentage = 0
        else:
            percentage = (obt / tot) * 100
        round(percentage, 2)

        return render_template("index.html", rows=rows, obt=obt, tot=tot, percentage=percentage, subjects=subjects, types=types)
    if request.method == "POST":
        user_id = session["user_id"]
        subject = request.form.get("subject")
        db = get_db_connection()
        subjects = db.execute("SELECT * FROM subjects WHERE userid = ?", (user_id,)).fetchall()
        types = db.execute("SELECt * FROM types WHERE userid = ?", (user_id,)).fetchall()



        type = request.form.get("type")
        if subject == "Subject":
            subject = "%"

        if type == "Type":
            type = "%"


        marksorder = request.form.get("marksobtained")
        if marksorder == "Ascending":
            rows = db.execute("SELECT * FROM tests WHERE subject LIKE ? AND type LIKE ? AND userid = ? ORDER BY percentage ", (subject, type, user_id )).fetchall()
        elif marksorder == "Descending":
            rows = db.execute("SELECT * FROM tests WHERE subject LIKE ? AND type LIKE ? AND userid = ? ORDER BY percentage DESC", (subject, type, user_id)).fetchall()
        else:
            rows = db.execute("SELECT * FROM tests WHERE subject LIKE ? AND type LIKE ? AND userid = ?", (subject, type, user_id)).fetchall()
        db.close()
        obt = 0
        tot = 0

        for tests in rows:
            obt += tests["marksobtained"]
            tot += tests["markstotal"]
        if tot == 0:
            percentage = 0
        else:
            percentage = (obt / tot) * 100
        round(percentage, 2)
        return render_template("index.html", rows=rows, obt=obt, tot=tot, percentage=percentage, subjects=subjects, types=types, user_id=user_id)

@app.route("/configure", methods = ["GET", "POST"])
@login_required
def configure():
    user_id = session["user_id"]
    if request.method == "GET":
        db = get_db_connection()
        subjects = db.execute("SELECT * FROM subjects WHERE userid = ?", (user_id,)).fetchall()
        types = db.execute("SELECt * FROM types WHERE userid = ?", (user_id,)).fetchall()
        db.close()
        return render_template("configure.html", subjects=subjects, types=types)

@app.route("/addsubject", methods = ["POST"])
@login_required
def addsubject():
    user_id = session["user_id"]
    subject = request.form.get("subject")
    db = get_db_connection()
    db.execute("INSERT INTO subjects(subject, userid) VALUES(?, ?)", (subject, user_id))
    db.commit()
    db.close()
    return redirect("/configure")

@app.route("/addtype", methods = ["POST"])
@login_required
def addtype():
    user_id = session["user_id"]
    type = request.form.get("type")
    db = get_db_connection()
    db.execute("INSERT INTO types(type, userid) VALUES(?, ?)", (type, user_id))
    db.commit()
    db.close()
    return redirect("/configure")

@app.route("/add", methods = ["GET", "POST"])
@login_required
def add():
    user_id = session["user_id"]
    if request.method == "GET":
        db = get_db_connection()
        subjects = db.execute("SELECT * FROM subjects WHERE userid = ?", (user_id,)).fetchall()
        types = db.execute("SELECt * FROM types WHERE userid = ?", (user_id,)).fetchall()
        db.close()

        return render_template("addtest.html", subjects=subjects, types=types)
    if request.method == "POST":
        marksobt = int(request.form.get("marksobt"))
        markstot = int(request.form.get("markstot"))
        if markstot == 0:
            return error("total marks cant be 0")
        day = request.form.get("day")
        month = request.form.get("month")
        year = request.form.get("year")
        subject = request.form.get("subject")
        type = request.form.get("type")
        if subject == "Subject":
            return error('Please Select a subject')
        if type == "type":
            return error('Please Select a type')
        percentage = marksobt/markstot * 100
        round(percentage, 2)
        db = get_db_connection()
        db.execute("INSERT INTO tests(subject, type, date, month, year, marksobtained, markstotal, percentage, userid) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   (subject, type, day, month, year, marksobt, markstot, percentage, user_id))
        db.commit()
        db.close()
        return redirect("/add")

@app.route("/remove", methods = ["POST"])
@login_required
def remove():
    if request.method == "POST":
        user_id = session["user_id"]
        id = request.form.get("id")
        db = get_db_connection()
        db.execute("DELETE FROM tests WHERE id = ? AND userid = ?", (id, user_id))
        db.commit()
        db.close()
        return redirect("/")
