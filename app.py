from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "<h1>Muistiinpanot</h1><p>Sovellus toimii.</p>"