Before starting building my project, I have created a new database in MySQL Workbench named ecommerce_api.
I set up and activated a virtual environment and installed dependencies.

I have built a simple RESTful E-commerce API using Python’s Flask framework. 
It uses SQLAlchemy for handling the database and Marshmallow for validating and serializing data. 
The backend connects to a MySQL database named ecommerce_api, where it manages users, products, and orders with a proper many-to-many relationship through an order_product table that also tracks product quantities in each order.

The API is designed around clean REST principles. 
It provides endpoints (GET, POST, PUT, DELETE) to perform all CRUD operations on users and products, as well as to create and manage orders linked to users. 
Additional endpoints allow adding or removing products from existing orders while preventing duplicates. 

I tested my app using Postman to ensure that all endpoints work as expected and handle relational data correctly.

Key highlights:
- Built with Flask, SQLAlchemy, Marshmallow, and MySQL.
- Models include users, products, orders, and an order-product association for many-to-many relationships.
- Full CRUD support for users, products, and orders.
- Prevents duplicate products in orders; supports adding/removing items dynamically.
- Automatically creates all tables and validates data on input.
