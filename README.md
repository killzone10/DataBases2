# BD2_project

# This project   contains a webapplication (fish store) with connected database  to it created in SQL_Alchemy - POSTGRES (used pgAdmin4).
The creation of database is being done in models.py file. 
# How to run:
To run you have to pip install requirments.txt and have postgres database with correcnt name on correct port.
and also go to __init__.py and fill 2 variables. Step by step you have to:
  - add postgres server in pgadmin
  - add credentials to app.config['SQLALCHEMY_DATABASE_URI'] = ''  ## you have to fill that with  postgresql://login:password@name_of_database
  - add secret key to app.config['SECRET_KEY']= '' ## and add your secret key too
  - after filling that just use python3 run.py 
 
# Project goal
## The goal was to create a model ER, then logical model in 3NF: Third normal form, so the purpose of subject was to develop database from the scratch and connect application to it.
# ER Model
![ER Model](ER_model.png)
![Logical Model](logical1.png)

## Fish_shop ##
The user which comes to this site can sign up, check products, check the cart, remove items from cart, buy products and get invoice from his purchase. All of these things are connected to database. 

![Account creation](account_creation.png)
![Checking the products](products.png)
![Checking your cart with products](transaction1.png)
Used bootstrap and some CSS, but rather focused on backend. 

## TO DO
Actually there is not much to do if it comes to database. Would be cool to create a demo and deploy it
on Heroku 
If it comes to frontend there is much to do :).


