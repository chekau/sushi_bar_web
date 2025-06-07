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
from database import Database, DishTable
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
    Database.open(
            host='109.206.169.221', 
            user='seschool_01', 
            password='seschool_01', 
            database='seschool_01_pks1')

    
    DishTable.add(name, description, image, price)
    return redirect(url_for('add_menu', error=True))
    



@staticmethod
def get_all_dishes():
    dishes = []
        

    for (name,describtion,image,price) in Database.fetchall(

    "SELECT * FROM dishes"):
        dishes.append(Dish(
            name=name,
            description=describtion,
            image=image,
            price=price   
    ))

    return dishes
     

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
