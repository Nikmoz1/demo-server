from flask_restx import Namespace, fields


class ProductDto:

    api = Namespace("product", description="Operations are related to the product")

    product = api.model(
        "Product object",
        {
            "productCode": fields.String(),
            "productNameUkr": fields.String(),
            "productNameRu": fields.String(),
            "descriptionUkr": fields.String(),
            "descriptionRu": fields.String(),
            "price": fields.Float(),
            "quantity": fields.Integer(),
            "categoryId": fields.Integer(),
            "packageSize": fields.Float(),
            "productSize": fields.Float(),
            "weight": fields.Float(),
            "video": fields.String(),
            "brand": fields.String(),
            "brandCountry": fields.String(),
            "discount": fields.Float(),
            "discountPeriodFrom": fields.Date(),
            "discountPeriodTo": fields.Date(),
        }
    )

    product_upload_data = api.clone(
        "Product Data For Get",
        product,
        {
            "images": fields.List(fields.String())
        }
    )

    product_image = api.model(
        "Product Image Data",
        {
            "id": fields.Integer(),
            "image": fields.String()
        }
    )

    product_for_response = api.clone(
        "Product Data For Response",
        product,
        {
            "id": fields.Integer(),
            "images": fields.List(fields.Nested(product_image))
        }
    )

    product_response = api.model(
        "Product Data Response",
        {
            "status": fields.Integer(),
            "message": fields.String(),
            "product": fields.Nested(product_for_response),
        }
    )

    upload_file_response = api.model(
        "Upload file status response",
        {
            "statusCode": fields.Integer(),
            "message": fields.String()
        }
    )

    products_with_pagination = api.model(
        "Product Data With Pagination",
        {
            "products": fields.List(fields.Nested(product_for_response)),
            "page": fields.Integer(),
            "size": fields.Integer(),
            "total": fields.Integer(),
            "pages": fields.Integer()
        }
    )
