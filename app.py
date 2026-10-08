import secrets
import notes

from flask import Flask
from flask import flash, redirect, render_template, request, session, abort

import users

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

def require_login():
    if "user_id" not in session:
        abort(403)

def check_csrf():
    token = request.form.get("csrf_token")
    if not token or token != session.get("csrf_token"):
        abort(403)

@app.errorhandler(403)
def forbidden(error):
    return render_template("forbidden.html"), 403

@app.route("/")
def index():
    if "user_id" in session:
        all_notes = notes.get_notes(session["user_id"])
    else:
        all_notes = []

    return render_template("index.html", notes = all_notes)


@app.route("/new_note")
def new_note():
    require_login()
    return render_template("new_note.html")


@app.route("/create_note", methods=["POST"])
def create_note():
    require_login()
    check_csrf()

    title = request.form["title"]
    content = request.form["content"]

    user_id = session["user_id"]
    note_id = notes.add_note(title, content, user_id)

    return redirect("/note/" + str(note_id))

@app.route("/note/<int:note_id>")
def show_note(note_id):
    require_login()

    note = notes.get_note(note_id)
    if not note:
        abort(404)
    #FLAW 1
    #if note["user_id"] != session["user_id"]:
        #abort(403)

    return render_template("show_note.html", note=note)

@app.route("/edit_note/<int:note_id>")
def edit_note(note_id):
    require_login()

    note = notes.get_note(note_id)
    if not note:
        abort(404)
    #FLAW 1
    #if note["user_id"] != session["user_id"]:
        #abort(403)

    return render_template("edit_note.html", note=note)


@app.route("/update_note", methods=["POST"])
def update_note():
    require_login()
    check_csrf()

    note_id = request.form["note_id"]
    note = notes.get_note(note_id)
    if not note:
        abort(404)

    #FLAW 1
    #if note["user_id"] != session["user_id"]:
        #abort(403)

    title = request.form["title"]
    content = request.form["content"]

    notes.update_note(note_id, title, content)

    return redirect("/note/" + str(note_id))


@app.route("/remove_note/<int:note_id>", methods=["GET", "POST"])
def remove_note(note_id):
    require_login()

    note = notes.get_note(note_id)
    if not note:
        abort(404)

    #FLAW 1
    #if note["user_id"] != session["user_id"]:
        #abort(403)

    if request.method == "POST":
        check_csrf()
        notes.remove_note(note_id)
        return redirect("/")

    return render_template("remove_note.html", note=note)

@app.route("/find_note")
def find_note():
    require_login()

    query = request.args.get("query", "")

    if query:
        results = notes.find_notes(query, session["user_id"])
    else:
        results = []

    return render_template(
        "find_note.html",
        query=query,
        results=results
    )

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
            #FLAW 5
            #app.logger.warning("Failed login attempt for username=%r", username)
            flash("ERROR: wrong username or password.", "error")
            return redirect("/login")
        
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")