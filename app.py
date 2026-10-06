import secrets

from flask import Flask
from flask import flash, redirect, render_template, request, session

import users

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]

    if len(password1) < 4:
        flash("ERROR: Password must be at least 4 characters long", "error")
        return redirect("/register")

    if password1 != password2:
        flash("ERROR: Passwords do not match", "error")
        return redirect("/register")

    if not users.create_user(username, password1):
        flash("ERROR: Username is already taken", "error")
        return redirect("/register")

    flash("Account created succesfully. You can now log in", "succes")
    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user_id = users.check_login(username, password)
        if user_id:
            session["user_id"] = user_id
            session["username"] = username
            session["csrf_token"] = secrets.token_hex(32)
            return redirect("/")
        else:
            flash("ERROR: wrong username or password.", "error")
            return redirect("/login")
        
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")