from extensions import ma
from marshmallow import fields
from models import User, Product, Order

class OrderProductSchema(ma.Schema):
    product_id = fields.Integer(required=True)
    quantity = fields.Integer(required=True, validate=lambda n: n > 0)

class OrderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Order
        include_fk = True
        load_instance = True

    id = ma.auto_field(dump_only=True)
    created_at = ma.auto_field(dump_only=True)
    user_id = ma.auto_field(required=True)
    products = fields.List(fields.Nested(OrderProductSchema), required=True)

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        include_relationships = True

    id = ma.auto_field(dump_only=True)
    username = ma.auto_field(required=True)
    email = ma.auto_field(required=True)

    # Use the orders_ids property to output list of order IDs
    orders = fields.List(fields.Integer(), dump_only=True, attribute="orders_ids")

class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        load_instance = True
        include_fk = True

    id = ma.auto_field(dump_only=True)
    name = ma.auto_field(required=True)
    description = ma.auto_field()
    price = ma.auto_field(required=True)

user_schema = UserSchema()
users_schema = UserSchema(many=True)

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)
