# from sqlalchemy import null

from app import bcrypt
from app.models import *


def insert_user(username, email, password, first_name=None, second_name=None, phone=None, address_id=None):
    cart = Cart()
    db.session.add(cart)
    db.session.commit()

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user = User(username=username, email=email, password=hashed_password, first_name=first_name,
                second_name=second_name, phone=phone, cart=cart, address_id=address_id)

    db.session.add(user)
    db.session.commit()
    return user


def insert_city(city_name):
    city = City(name=city_name)
    db.session.add(city)
    db.session.commit()
    return city


def insert_address(street, house_nr, postal_code, city_id):
    address = Address(street=street, house_nr=house_nr, postal_code=postal_code, city_id=city_id)
    db.session.add(address)
    db.session.commit()
    return address


def insert_user_with_all_attributes(username, email, password, first_name=None, second_name=None, phone=None,
                                    city_name=None, street=None, house_nr=None, postal_code=None):
    city = insert_city(city_name)
    address = insert_address(street, house_nr, postal_code, city.id)
    insert_user(username, email, password, first_name, second_name, phone, address.id)


def insert_product_type(title, parent_id=None):
    product_type = Product_type(title=title, parent_id=parent_id)
    db.session.add(product_type)
    db.session.commit()
    return product_type


def insert_product(name, photo, price, quantity, description, type_id, brand_id=None):
    product = Product(name=name, photo=photo, price=price, quantity=quantity, description=description,
                      type_id=type_id, brand_id=brand_id)
    db.session.add(product)
    db.session.commit()
    return product


def insert_brand(name):
    brand = Brand(name=name)
    db.session.add(brand)
    db.session.commit()
    return brand
