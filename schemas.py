from extensions import ma
from marshmallow import fields, validates_schema, ValidationError
from models import User, Product, Order

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        include_relationships = True

    id = ma.auto_field(dump_only=True)
    username = ma.auto_field(required=True)
    email = ma.auto_field(required=True)

class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        load_instance = True
        include_fk = True

    id = ma.auto_field(dump_only=True)
    name = ma.auto_field(required=True)
    description = ma.auto_field()
    price = ma.auto_field(required=True)

class OrderProductSchema(ma.Schema):
    product_id = fields.Integer(required=True)
    quantity = fields.Integer(required=True, validate=lambda n: n > 0)

class OrderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Order
        load_instance = True
        include_fk = True

    id = ma.auto_field(dump_only=True)
    created_at = ma.auto_field(dump_only=True)
    user_id = ma.auto_field(required=True)
    products = fields.List(fields.Nested(OrderProductSchema), required=True)

    @validates_schema
    def validate_products(self, data, **kwargs):
        products = data.get('products', [])
        if not products:
            raise ValidationError('Order must contain at least one product.', 'products')
        product_ids = [p['product_id'] for p in products]
        if len(product_ids) != len(set(product_ids)):
            raise ValidationError('Duplicate product_id in products list.', 'products')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)
