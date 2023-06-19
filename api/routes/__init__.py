from flask import Blueprint
from flask_restx import Api

from api.routes.server_status import server_status_ns
from api.routes.product.controller import api as product_ns
from api.routes.category.controller import api as category_ns

blueprint = Blueprint("api", __name__)
api = Api(
    blueprint,
    title="Flask API for OK-Shop",
    version="0.1",
    description="Welcome to the Swagger UI documentation",
)

api.add_namespace(server_status_ns)
api.add_namespace(product_ns)
api.add_namespace(category_ns)
