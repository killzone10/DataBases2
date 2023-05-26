from base64 import decode
from threading import currentThread
from flask import Flask, render_template,url_for,request,redirect,Response,session,send_file,flash
from numpy import product
from app.forms import RegistrationForm,LoginForm,UpdateAccountForm,OrderForm
from flask_sqlalchemy import SQLAlchemy
from app.models import *
from app import app,db,bcrypt
from flask_login import login_user,current_user,logout_user,login_required
from datetime import datetime,date

@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        if request.form.get('Log') == 'Zaloguj':
            return redirect(url_for('login'))   
        elif request.form.get('Sign') == 'Zarejestruj':
            return redirect(url_for('register'))
        elif request.form.get('Products') == 'Produkty':
            return redirect(url_for('products'))
        elif request.form.get('Cart') == 'Koszyk':
            return redirect(url_for('cart'))
    elif request.method == 'GET':
        return render_template('index.html')

@app.route("/about")
def about():
    return render_template('error.html', title = "Ekran")


@app.route("/products", methods=['POST', 'GET'])
def products():
    if request.method == "POST":
        product_type_title = request.form.get('product_type')
        if product_type_title == "Wszystkie":
            products = Product.query.order_by(Product.id).all()
        else:
            product_type = Product_type.query.filter(Product_type.title == request.form.get('product_type')).one()
            products = Product.query.filter(Product.type_id == product_type.id).all()

        product_types = Product_type.query.order_by(Product_type.id).all()
        return render_template('products.html', title="Products", products=products, product_types=product_types)
    if request.method == "GET":
        products = Product.query.order_by(Product.id).all()
        product_types = Product_type.query.order_by(Product_type.id).all()
        return render_template('products.html', title="Products", products=products, product_types=product_types)

@app.route("/products/<int:product_id>", methods=['POST', 'GET'])
def specific_product(product_id):
    if request.method == "GET":

        product = Product.query.filter(Product.id == product_id).one()
        product_type = Product_type.query.filter(Product_type.id == product.type_id).one()
        return render_template('specific_product.html', title="Products", product=product, product_type=product_type.title)

@app.route("/register",methods = ['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        cart = Cart()
        db.session.add(cart)
        db.session.commit()
        user = User(username=form.username.data
       ,email = form.email.data, password = hashed_password,cart_id = cart.id)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account have been created, you can log in!','success')
        return redirect(url_for('login'))
    return render_template('register.html',title = "Register",form = form)

@app.route("/login",methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember = form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Login unsucesfull. Please check your username and password','danger')
    return render_template('login.html',title ="Login",form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/account",methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.first_name = form.first_name.data
        current_user.second_name = form.second_name.data
        current_user.phone = form.phone.data
        db.session.commit()
        flash('Your account has been updated','success')
        return redirect(url_for('account'))
    elif request.method == "GET":
        form.username.data =  current_user.username
        form.email.data =  current_user.email
        form.first_name.data =  current_user.first_name
        form.second_name.data =  current_user.second_name
        form.phone.data =  current_user.phone
        
    return render_template('account.html',title ="Account",form = form)


@app.route("/delete",methods=['GET', 'POST'])
@login_required
def delete():
    if request.method =="POST":
        if request.form.get('Delete') == 'Delete':  

            order_id = Order.query.filter(Order.user_id == current_user.id).all()
            print(order_id)
            for i in order_id:
                print("I ID",i.id)
                order_product = Product.query.join(product_has_order).join(Order).filter((product_has_order.c.order_id == i.id)).all()
                invoice = Invoice.query.filter_by(order_id = i.id).delete()
                for i,clear in enumerate(order_product):
                    order_product[i].has_order.clear()
                    db.session.commit()
            
          
            db.session.commit()
            order = Order.query.filter_by(user_id = current_user.id).delete()
            db.session.commit()
            
            user = User.query.filter_by(username =current_user.username).delete()          
            db.session.commit()
            flash('Your account has been deleted','danger')
            return redirect(url_for('logout'))
    elif request.method =="GET":
        return render_template("delete.html")


@app.route("/add_to_cart",methods =['GET','POST'])
@login_required
def add_to_cart():
    if request.method =="POST":
        if request.form.get("Add to cart") == "Do koszyka":
            product_id = request.form.get("hidden")
            cart_id = current_user.cart_id
            product_update = Product.query.filter(Product.id == product_id).all()
            query_cart = Cart.query.filter(Cart.id == cart_id).all()
            product_update[0].has_cart.append(query_cart[0])
            db.session.commit()
            flash(f'Produkt dodany do koszyka!','success')
    return redirect(url_for('products')) 

@app.route("/cart",methods=['GET', 'POST'])
@login_required
def cart():

    if request.method =="GET":
        cart_id = current_user.cart_id
        total_price = 0
        cart_product = Product.query.join(product_has_cart).join(Cart).filter((product_has_cart.c.cart_id == cart_id)).all()
        for price in cart_product:
            total_price = total_price + price.price
        return render_template('cart.html',title = "Cart", cart=cart_product,total_price=total_price)
    elif request.method =="POST":
        if request.form.get("Remove") == "Usuń":
            product_id = request.form.get("hidden")
            cart_product = Product.query.join(product_has_cart).join(Cart).filter((product_has_cart.c.product_id == product_id)).all()
            cart_product[0].has_cart.clear()
            db.session.commit()
            flash(f'Produkt usunięty z koszyka!','success')
            return redirect(url_for('cart')) 
        if request.form.get('Buy') == 'Zamów':
            cart_id = current_user.cart_id
            cart_product = Product.query.join(product_has_cart).join(Cart).filter((product_has_cart.c.cart_id == cart_id)).all()
            if(len(cart_product) == 0 ):
                flash(f'No product in cart','danger')
                return redirect(url_for('cart'))
            else:
                return redirect(url_for('order'))

@app.route("/like",methods =['GET','POST'])
@login_required
def like():
    return render_template("cart.html")

@app.route("/order",methods =['GET','POST'])
@login_required
def order():
    cart_id = current_user.cart_id
    total_price = 0
    cart_product = Product.query.join(product_has_cart).join(Cart).filter((product_has_cart.c.cart_id == cart_id)).all()
    for price in cart_product:
        total_price = total_price + price.price
    form = OrderForm()
    if form.validate_on_submit():
        city = City(name = form.city.data)
        db.session.add(city)
        db.session.commit()
        adress = Address(street = form.street.data,house_nr=form.number.data,postal_code=form.postal_code.data,city_id=city.id)
        db.session.add(adress)
        db.session.commit()
        order = Order(date = datetime.date(datetime.now()),status = 1,total_price = total_price ,user_id =current_user.id,adress_id = adress.id)      
        db.session.add(order)
        db.session.commit()
        for product in cart_product:
            if (product.quantity == 0):
                print("Error")
            else:
                product.quantity = product.quantity - 1
                db.session.commit()

        if (form.invoice.data):
            invoice = Invoice(data = datetime.date(datetime.now()),seller = "RYBEX", identification_number=form.nip.data,order_id=order.id)
            db.session.add(invoice)
            db.session.commit()
        for products_update in cart_product:
            p = products_update.id
            product = Product.query.filter_by(id = p).first()
            product.has_order.append(order)
            db.session.commit()

        for i,clear in enumerate(cart_product):
            cart_product[i].has_cart.clear()

        db.session.commit()
        flash('Sucesfully created order','success')
        return redirect(url_for('index'))
    elif request.method == "GET":
        form.email.data = current_user.email
        form.first_name.data = current_user.first_name
        form.second_name.data = current_user.second_name
        form.phone.data =  current_user.phone
        form.country.data = "Poland"
        form.city.data = "Warszawa"
        


    return render_template("order.html",form=form,total_price = total_price)



@app.route("/my_order",methods =['GET','POST'])
@login_required
def my_order():
    order = []
    user_id = current_user.id
    order_id = Order.query.filter(Order.user_id == user_id).all()
    total_price = 0
    for o in order_id:
        order_product = Product.query.join(product_has_order).join(Order).filter((product_has_order.c.order_id == o.id)).all()
        order.append(order_product)
        for price in order_product:
            total_price = total_price + price.price
    return render_template("my_order.html",order = order,total_price = total_price)