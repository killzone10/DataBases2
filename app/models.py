import time,datetime
from app import db,login_manager
from flask_login import UserMixin

from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref

product_is_favourite = db.Table('product_is_favourite', db.Model.metadata,
    db.Column('product_id', db.Integer,db.ForeignKey('product.id')),
    db.Column('user_id', db.Integer,db.ForeignKey('user.id'))
    )

product_has_cart = db.Table('product_has_cart', db.Model.metadata,
    db.Column('product_id', db.Integer,db.ForeignKey('product.id')),
    db.Column('cart_id', db.Integer,db.ForeignKey('cart.id'))
    )

product_has_order = db.Table('product_has_order', db.Model.metadata,
    db.Column('product_id', db.Integer,db.ForeignKey('product.id')),
    db.Column('order_id', db.Integer,db.ForeignKey('order.id'))
    )
class Product(db.Model):
    __tablename__ ="product"
    id = db.Column(db.Integer,primary_key = True)
    photo = db.Column(db.String(40))
    name = db.Column(db.String(40))
    price = db.Column(db.Float)
    quantity = db.Column(db.Integer)
    description = db.Column(db.String(200))

    favourite = db.relationship("User",secondary = product_is_favourite)
    comments = db.relationship("Comment",backref = "Comment")
    has_cart = db.relationship("Cart",secondary = product_has_cart)
    brand_id = db.Column(db.Integer,db.ForeignKey('brand.id'),nullable = True) ## sprawdz te nulle
    type_id = db.Column(db.Integer,db.ForeignKey('product_type.id'),nullable = True)
    has_order = db.relationship("Order", secondary = product_has_order)
    sectors = db.Column(db.Integer,db.ForeignKey('sector.id'),nullable = True)
    warehouses = db.Column(db.Integer,db.ForeignKey('warehouse.id'),nullable = True)



    def __repr__(self):
        return f"Product('{self.name}','{self.price}','{self.quantity}')"


class Order(db.Model):
    __tablename__="order"
    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.DateTime, nullable = False)
    status = db.Column(db.Integer, nullable = False)
    total_price = db.Column(db.Float, nullable = False)
    adress_id = db.Column(db.Integer,db.ForeignKey("address.id"))
    address = relationship("Address")
    # phone = db.Column(db.Integer, nullable = True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'), nullable = True)
    def __repr__(self):
        return f"Order('{self.date}','{self.total_price}','{self.adress_id}')"


class Invoice(db.Model):
    __tablename__="invoice"
    id = db.Column(db.Integer, primary_key = True)
    data = db.Column(db.DateTime, nullable = False, default = datetime.datetime.now())
    seller = db.Column(db.String(15), nullable = False)
    identification_number = db.Column(db.Integer)
    order_id = db.Column(db.Integer,db.ForeignKey('order.id'),nullable = False, unique = True)

    def __repr__(self):
        return f"Invoice('{self.data}','{self.seller}','{self.identification_number}')"




class Brand(db.Model):
    __tablename__="brand"
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(25),nullable = False)
    def __repr__(self):
        return f"Brand('{self.id}','{self.description}','{self.product_id}')"


class Product_type(db.Model):
    __tablename__="product_type"
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(45), nullable = False)
    parent_id = db.Column(db.Integer, db.ForeignKey('product_type.id'), nullable = True)


class Cart(db.Model):
     __tablename__ ="cart"
     id = db.Column(db.Integer,primary_key = True)
     User = relationship("User",back_populates="cart",uselist = False)





class Comment(db.Model):
    __tablename__ ="comment"
    id = db.Column(db.Integer,primary_key=True)
    description=db.Column(db.Text,unique=True,nullable=False)
    title = db.Column(db.String(100),nullable=False)
    data_posted = db.Column(db.DateTime, nullable = False, default = datetime.datetime.now())
    star_amount = db.Column(db.Integer)

    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable = False) # tutaj id z clasy user
    product_id = db.Column(db.Integer,db.ForeignKey('product.id'), nullable = False)

    def __repr__(self):
        return f"Comment('{self.title}','{self.data_posted}')"

user_role = db.Table('user_role', db.Model.metadata,
    db.Column('user.id', db.Integer,db.ForeignKey('user.id')),
    db.Column('role.id',db.Integer, db.ForeignKey('role.id'))
    )

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin): #1
    __tablename__ ="user"
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20),unique=True,nullable=False)# unique  - jeden username dla jednego uzytkownika, nullable  =  musi istniec #default
    password = db.Column(db.String(70),nullable=False)
    email = db.Column(db.String(20),unique=True,nullable=False)
    first_name = db.Column(db.String(40),nullable=True)
    second_name = db.Column(db.String(40),nullable=True)
    phone = db.Column(db.Integer)
    comments = db.relationship('Comment',backref = 'author', lazy = True) # backref dodajemy kolumne do Comment lazy true sql alchemy load TRUE asap
    roles = db.relationship("Role",secondary = user_role)
    orders = db.relationship('Order',backref = 'Order', lazy = True) # backref dodajemy kolumne do Comment lazy true sql alchemy load TRUE asap


    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'),unique = True)
    cart = db.relationship("Cart",back_populates = "User")
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'), nullable=True)


    def __repr__(self): # wyspeciikujemy klase z relacja
        return f"User('{self.username}','{self.password}','{self.email}')"

class Role(db.Model):
    __tablename__ ="role"
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20),nullable=False)# unique  - jeden username dla jednego uzytkownika, nullable  =  musi istniec #default



class Warehouse(db.Model):
    __tablename__ ="warehouse"
    id = db.Column(db.Integer, primary_key = True)
    max_capacity = db.Column(db.Integer, nullable=False)
    product_id = db.relationship('Product',backref = "Product")
    sectors = db.relationship('Sector', backref = 'Warehouse')

    address_id = db.Column(db.Integer,db.ForeignKey('address.id'))
    def __repr__(self):
        return f"Warehouse('{self.max_capacity}','{self.id}')"

class Sector(db.Model):
    __tablename__ ="sector"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20), nullable=False)
    max_capacity = db.Column(db.Integer, nullable=False)

    warehouse_id = db.Column(db.Integer,db.ForeignKey('warehouse.id'), nullable = False)
    workers = db.relationship('Worker', backref = 'Sector')
    product_id = db.relationship('Product',backref = "Product1")
    def __repr__(self):
        return f"Sector('{self.max_capacity}','{self.name}')"

class Worker(db.Model):
    __tablename__ ="worker"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20), nullable=False)
    surname = db.Column(db.String(20), nullable=False)
    position = db.Column(db.String(15), nullable=False) #!!! position zrobic jako odzielna encje w 3PN

    parent_id = db.Column(db.Integer, db.ForeignKey('worker.id'), nullable = True)
    sector_id = db.Column(db.Integer,db.ForeignKey('sector.id'), nullable = False)
    parent = db.relationship('Worker', remote_side=[id])
    def __repr__(self):
        return f"Worker('{self.name}','{self.surname}','{self.position}')"


class Address(db.Model):
    __tablename__ = "address"
    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(70), nullable=True)
    house_nr = db.Column(db.Integer, nullable=False)
    postal_code = db.Column(db.String(15), nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'), nullable=False)

    # city relationship


class City(db.Model):
    __tablename__ = 'city'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), nullable=False)
    # address_id = db.relationship('Address',backref = "Address")
