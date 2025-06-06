from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    send_from_directory,
    abort,
    flash,
    session)
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = "SHPI"
app.config["UPLOAD_FOLDER"] = "uploads/"

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route("/")
@app.route("/menu")
def menu():
    return render_template("menu.html")
















app.run(debug=True, port=8080)
