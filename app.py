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
from src.database import Database, DishTable, OrdersTable, CartTable, DishToOrders
from src.config import CONFIG
from src.model import Dish, Orders
from werkzeug.utils import secure_filename
import hashlib


app = Flask(__name__,
            static_folder="src/static",
            template_folder="src/templates")
app.config["SECRET_KEY"] = "SHPI"
app.config["UPLOAD_FOLDER"] =  os.path.join("src", "static", "uploads")

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.before_request
def initialize_database():
    Database.open()



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

    
    
    DishTable.add(name=name, describtion=describtion, image=image_filename, price=price)
   
    return redirect(url_for('add_menu', error=True))




@app.route("/")
@app.route("/index")
def index():

    dishes = DishTable.get_all_dishes()
    count_in_group = 4

    groups = []
    for i in range(0,len(dishes),count_in_group):
        groups.append(dishes[i:i + count_in_group])
    
    user_email = session.get('email')  
    
    return render_template("index.html",groups=groups,user_count=DishTable.get_count_of_users(),user_email=user_email)


@app.route("/choose")
def choose():
    return render_template("choose.html")

@app.route("/client_side")
def client_side():
    return render_template("client_side.html")

@app.route("/admin_side")
def admin_side():
    return render_template("admin_side.html")



@app.route("/dish/<name>")
def get_dish(name):
    dish = DishTable.find_dish_by_name(name)
    if dish is None:
        return "<h1>Такого блюда нет в меню!</h1>"

    return render_template(
        "dish.html",
        dish=dish
        )



@app.route("/add_to_cart/<dish_id>", methods=["GET","POST"])
def add_to_cart(dish_id):
    user_id = session.get("id")
    if user_id is None:
        flash('Вы должны сначала войти в свой аккаунт, чтобы добавлять блюда в корзину.')
        return redirect(url_for('login'))



    CartTable.add_to_cart(user_id=user_id, dish_id=dish_id)


    return redirect(url_for('show_cart'))







@app.route("/show_cart", methods=['GET','POST'])
def show_cart():
    if request.method == "GET":
        return render_template('show_cart.html',error=request.args.get("error"))
    
    user_id = session.get("id")
    print(session)
    if user_id is None:
        flash('Вы должны сначала войти в свой аккаунт, перед тем как заказать еду ')
        return redirect(url_for('login'))  # Перенаправление на страницу входа
    


    dishes = CartTable.get_dishes_from_user(user_id)
    return render_template("show_cart.html", dishes=dishes)

    
    





@app.route('/create_order', methods=['GET', 'POST'])
def create_order():
    if request.method == "GET":
        return render_template('create_order.html',error=request.args.get("error"))
    
    user_id = session.get("id")
    print(session)
    if user_id is None:
        flash('Вы должны сначала войти в свой аккаунт, перед тем как заказать еду ')
        return redirect(url_for('login'))  # Перенаправление на страницу входа




    cart_dishes = CartTable.get_dishes_from_user(user_id)
    if not cart_dishes:
        flash('Ваша корзина пуста. Добавьте блюда перед оформлением заказа.')
        return redirect(url_for('show_cart'))


    customer_name = request.form.get("customer_name")
    phone = request.form.get("phone")
    address = request.form.get("address")
    delivery_time = request.form.get("delivery_time")
    payment_method = request.form.get("payment_method")
    status = request.form.get("status")  

    

    
    OrdersTable.create_new_order(user_id=user_id, customer_name=customer_name, phone=phone, address=address, 
                                  delivery_time=delivery_time, 
                                 payment_method=payment_method,
                                 status=status)
    
    order_id = OrdersTable.find_order_id_by_user_id(user_id)
    print(order_id)
    print(user_id)
    print(cart_dishes)


    for dish in cart_dishes:
        DishToOrders.add_dish_to_order(order_id, dish["id"], dish["quantity"])


    CartTable.clear_cart(user_id)

    
    flash("Заказ успешно оформлен!")
    return redirect(url_for('index', error=True))






@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    email = request.form.get("email")
    password = request.form.get("password")
    repeat_password = request.form.get("repeat_password")

    if not email:
        flash("Электронная почта не может быть пустой")
        return redirect(request.url)

    if not password or not repeat_password:
        flash("Пароль и его подтверждение обязательны")
        return redirect(request.url)

    if password != repeat_password:
        flash("Пароли не совпадают")
        return redirect(request.url)
    
    
    saved = Database.register_user(email,password)
    if not saved:
        flash("Пользователь с такой почтой уже существует")
        return redirect(request.url)

    flash("Регистрация прошла успешно. Войдите в систему.")
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    email = request.form.get("email")
    password = request.form.get("password")

    if not email or not password:
        flash("Введите почту и пароль")
        return redirect(request.url)



    user = Database.fetchall("SELECT * FROM Users WHERE email = %s", (email,))
    if not user:
        flash("Пользователь не найден")
        return redirect(request.url)

    password_hash = hashlib.md5(password.encode()).hexdigest()
    if user[0][2] != password_hash:
        flash("Неверный пароль")
        return redirect(request.url)

    session["id"] = user[0][0]
    session["email"] = email
    flash("Вы вошли в систему")
    return redirect(url_for("index"))  # или на главную

@app.route("/logout", methods=["POST"])
def logout():
    session.pop('id', None)
    session.pop('email', None)
    flash("Вы вышли из системы.")
    return redirect(url_for("index"))
    



app.run(debug=True, port=8080)

