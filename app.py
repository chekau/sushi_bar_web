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
from database import Database
from dish import Dish


app = Flask(__name__)
app.config["SECRET_KEY"] = "SHPI"
app.config["UPLOAD_FOLDER"] = "uploads/"

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

Database.create_tables()


@app.route("/add_menu", methods=["GET", "POST"])
def add_menu():
    if request.method == "GET":
        return render_template('add_menu.html',error=request.args.get("error"))
    
    # Далее обработка POST-запроса
    name = request.form.get("name")
    description = request.form.get("description")
    image = request.files.get("image")
    price = request.form.get("price")
    
    
    if image is not None and image.filename: 
        image_path = image.filename
        print(app.config["UPLOAD_FOLDER"] + image_path)
        image.save(app.config["UPLOAD_FOLDER"] + image_path)
        

    else:
        image_path = None
    saved = Database.save(Dish(name=name, description=description, image=image_path, price=price))

    if not saved:
        return redirect(url_for('add_menu', error=True))
    return redirect(url_for('registration'))

@app.route("/")
@app.route("/registration")
def registration():
    return render_template("registration.html")

@app.route("/client_side")
def client_side():
    return render_template("client_side.html")

@app.route("/admin_side")
def admin_side():
    return render_template("admin_side.html")

@app.route("/menu")
def menu():
    return render_template("menu.html")


app.run(debug=True, port=8080)
