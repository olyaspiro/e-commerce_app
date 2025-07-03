from flask import request, jsonify
from extensions import db
from models import User, Product, Order, OrderProduct
from schemas import user_schema, users_schema, product_schema, products_schema, order_schema, orders_schema

def register_user_routes(app):

    @app.route('/users', methods=['POST'])
    def create_user():
        json_data = request.get_json()
        if not json_data:
            return jsonify({"message": "No input data provided"}), 400

        try:
            user = user_schema.load(json_data)
        except Exception as err:
            return jsonify(err.messages if hasattr(err, 'messages') else str(err)), 422

        if User.query.filter((User.username == user.username) | (User.email == user.email)).first():
            return jsonify({"message": "User with that username or email already exists"}), 409

        db.session.add(user)
        db.session.commit()
        return user_schema.jsonify(user), 201

    @app.route('/users', methods=['GET'])
    def get_users():
        users = User.query.all()
        return users_schema.jsonify(users)

    @app.route('/users/<int:user_id>', methods=['GET'])
    def get_user(user_id):
        user = User.query.get_or_404(user_id)
        return user_schema.jsonify(user)

    @app.route('/users/<int:user_id>', methods=['PUT'])
    def update_user(user_id):
        user = User.query.get_or_404(user_id)
        json_data = request.get_json()
        if not json_data:
            return jsonify({"message": "No input data provided"}), 400

        try:
            data = user_schema.load(json_data, partial=True)
        except Exception as err:
            return jsonify(err.messages if hasattr(err, 'messages') else str(err)), 422

        if "username" in json_data and json_data["username"] != user.username:
            if User.query.filter_by(username=json_data["username"]).first():
                return jsonify({"message": "Username already exists"}), 409

        if "email" in json_data and json_data["email"] != user.email:
            if User.query.filter_by(email=json_data["email"]).first():
                return jsonify({"message": "Email already exists"}), 409

        user.username = data.username if data.username else user.username
        user.email = data.email if data.email else user.email
        db.session.commit()
        return user_schema.jsonify(user)

    @app.route('/users/<int:user_id>', methods=['DELETE'])
    def delete_user(user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "Deleted user"}), 200

def register_product_routes(app):

    @app.route('/products', methods=['POST'])
    def create_product():
        json_data = request.get_json()
        if not json_data:
            return jsonify({"message": "No input data provided"}), 400

        try:
            product = product_schema.load(json_data)
        except Exception as err:
            return jsonify(err.messages if hasattr(err, 'messages') else str(err)), 422

        db.session.add(product)
        db.session.commit()
        return product_schema.jsonify(product), 201

    @app.route('/products', methods=['GET'])
    def get_products():
        products = Product.query.all()
        return products_schema.jsonify(products)

    @app.route('/products/<int:product_id>', methods=['GET'])
    def get_product(product_id):
        product = Product.query.get_or_404(product_id)
        return product_schema.jsonify(product)

    @app.route('/products/<int:product_id>', methods=['PUT'])
    def update_product(product_id):
        product = Product.query.get_or_404(product_id)
        json_data = request.get_json()
        if not json_data:
            return jsonify({"message": "No input data provided"}), 400

        try:
            data = product_schema.load(json_data, partial=True)
        except Exception as err:
            return jsonify(err.messages if hasattr(err, 'messages') else str(err)), 422

        product.name = data.name if data.name else product.name
        product.description = data.description if data.description else product.description
        product.price = data.price if data.price else product.price

        db.session.commit()
        return product_schema.jsonify(product)

    @app.route('/products/<int:product_id>', methods=['DELETE'])
    def delete_product(product_id):
        product = Product.query.get_or_404(product_id)
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "Deleted product"}), 200

def register_order_routes(app):

    @app.route('/orders', methods=['POST'])
    def create_order():
        json_data = request.get_json()
        if not json_data:
            return jsonify({"message": "No input data provided"}), 400
        try:
            data = order_schema.load(json_data)
        except Exception as err:
            return jsonify(err.messages if hasattr(err, 'messages') else str(err)), 422

        user = User.query.get(data.user_id)
        if not user:
            return jsonify({"message": "User not found"}), 404

        order = Order(user_id=data.user_id)
        db.session.add(order)
        db.session.flush()  # get ID before committing

        for item in json_data.get('products', []):
            product = Product.query.get(item['product_id'])
            if not product:
                db.session.rollback()
                return jsonify({"message": f"Product with id {item['product_id']} not found"}), 404
            op = OrderProduct(order_id=order.id, product_id=product.id, quantity=item['quantity'])
            db.session.add(op)

        db.session.commit()
        return order_schema.jsonify(order), 201

    @app.route('/orders', methods=['GET'])
    def get_orders():
        orders = Order.query.all()
        return orders_schema.jsonify(orders)

    @app.route('/orders/<int:order_id>', methods=['GET'])
    def get_order(order_id):
        order = Order.query.get_or_404(order_id)
        return order_schema.jsonify(order)

    @app.route('/orders/<int:order_id>/add_product/<int:product_id>', methods=['PUT'])
    def add_product_to_order(order_id, product_id):
        order = Order.query.get_or_404(order_id)
        product = Product.query.get_or_404(product_id)

        existing = OrderProduct.query.filter_by(order_id=order.id, product_id=product.id).first()
        if existing:
            return jsonify({"message": "Product already in order"}), 400

        new_op = OrderProduct(order_id=order.id, product_id=product.id, quantity=1)
        db.session.add(new_op)
        db.session.commit()
        return jsonify({"message": f"Added product {product.id} to order {order.id}"}), 200

    @app.route('/orders/<int:order_id>/remove_product/<int:product_id>', methods=['DELETE'])
    def remove_product_from_order(order_id, product_id):
        op = OrderProduct.query.filter_by(order_id=order_id, product_id=product_id).first()
        if not op:
            return jsonify({"message": "Product not found in this order"}), 404
        db.session.delete(op)
        db.session.commit()
        return jsonify({"message": f"Removed product {product_id} from order {order_id}"}), 200

    @app.route('/orders/user/<int:user_id>', methods=['GET'])
    def get_orders_by_user(user_id):
        user = User.query.get_or_404(user_id)
        orders = Order.query.filter_by(user_id=user_id).all()
        return orders_schema.jsonify(orders)

    @app.route('/orders/<int:order_id>/products', methods=['GET'])
    def get_products_by_order(order_id):
        order = Order.query.get_or_404(order_id)
        products = [op.product for op in order.order_products]
        return products_schema.jsonify(products)

    @app.route('/orders/<int:order_id>', methods=['DELETE'])
    def delete_order(order_id):
        order = Order.query.get_or_404(order_id)
        db.session.delete(order)
        db.session.commit()
        return jsonify({"message": "Deleted order"}), 200
