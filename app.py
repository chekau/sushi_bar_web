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
from model import Dish
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config["SECRET_KEY"] = "SHPI"
app.config["UPLOAD_FOLDER"] =  os.path.join('static', 'uploads')

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)




@app.route("/add_menu", methods=["GET", "POST"])
def add_menu():
    if request.method == "GET":
        return render_template('add_menu.html',error=request.args.get("error"))
    
    # Далее обработка POST-запроса
    name = request.form.get("name")
    describtion = request.form.get("describtion")
    image = request.files.get("image")
    price = request.form.get("price")
    
    image_filename = None
    
    if image is not None and image.filename:
        filename = secure_filename(image.filename)
        image_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        image.save(image_path)
        image_filename = filename

    Database.open(
            host='109.206.169.221', 
            user='seschool_01', 
            password='seschool_01', 
            database='seschool_01_pks1')

    
    DishTable.add(name=name, describtion=describtion, image=image_filename, price=price)
   
    return redirect(url_for('add_menu', error=True))
    





@app.route("/")
@app.route("/index")
def index():
    Database.open(
            host='109.206.169.221', 
            user='seschool_01', 
            password='seschool_01', 
            database='seschool_01_pks1')

    dishes = DishTable.get_all_dishes()
    count_in_group = 5

    groups = []
    for i in range(0,len(dishes),count_in_group):
        groups.append(dishes[i:i + count_in_group])
    
    return render_template("index.html",groups=groups,user_count=DishTable.get_count_of_users())


@app.route("/choose")
def choose():
    return render_template("choose.html")

@app.route("/client_side")
def client_side():
    return render_template("client_side.html")

@app.route("/admin_side")
def admin_side():
    return render_template("admin_side.html")



@app.route("/dish")
def dish():
    return render_template("dish.html")



@app.route("/register",methods=["GET","POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    

    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    repeat_password = request.form.get("repeat_password")

    if not username:
        flash("имя пользователя не может быть пустым")
        return redirect(request.url)

    
    if not email:
        flash("электронная почта не может быть пустым")
        return redirect(request.url)


    
    if not password:
        flash("повторите пароль")
        return redirect(request.url)
    
    print(password)
    print(repeat_password)
    
    if password != repeat_password:
        flash("пароли не совпадают")
        return redirect(request.url)

    saved = Database.register_user(username,email,password)
    if not saved:
        flash("пользователь с таким никнеймом или почтой уже есть")
        return redirect(request.url)
    
    
    return redirect(url_for("login"))

@app.route("/login",methods=["POST","GET"])
def login():
    if request.method == "GET":
        return render_template("login.html")


    #POST ЗАПРОС

    username = request.form.get("username")
    password = request.form.get("password")

    if not Database.can_be_logged_in(username,password):
        flash("такого пользователя не существует или неверный пароль")
        return redirect(request.url)
    

    session['user_id'] = Database.find_user_id_by_name(username)
    return redirect(url_for("index"))

@app.route("/logout", methods=["POST"])
def logout():
    if "user_id" in session:
        session.clear()
    return redirect(url_for("index"))




app.run(debug=True, port=8080)
