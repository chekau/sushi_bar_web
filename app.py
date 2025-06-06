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
    return redirect(url_for('index'))


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


app.run(debug=True, port=8080)
