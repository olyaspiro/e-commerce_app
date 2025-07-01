from flask import Flask
from extensions import db, ma

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Coding28*@localhost/ecommerce_api'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions with app
db.init_app(app)
ma.init_app(app)

# Import models and routes AFTER db & ma are initialized
from models import User, Product, Order, OrderProduct
from schemas import user_schema, users_schema, product_schema, products_schema, order_schema, orders_schema
from routes import register_user_routes, register_product_routes, register_order_routes

register_user_routes(app)
register_product_routes(app)
register_order_routes(app)

@app.route('/')
def home():
    return 'Welcome to the Shop API!'

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

