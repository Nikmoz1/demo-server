from datetime import datetime
import os
from http import HTTPStatus
from pprint import pprint

from flask import request, send_file
from flask_restx import Resource
from flask_restx.reqparse import RequestParser
from werkzeug.datastructures import FileStorage

from api.services.product import ProductService
from api import schemas
from .dto import ProductDto
from config import BASEDIR


api = ProductDto.api

product = ProductDto.product
product_upload_data = ProductDto.product_upload_data
product_for_response = ProductDto.product_for_response
product_response = ProductDto.product_response
products_with_pagination = ProductDto.products_with_pagination
upload_file_response = ProductDto.upload_file_response

path_to_folder_with_products_data_files = f"{BASEDIR}/files_with_products_data/"


@api.route("/all")
class ProductAll(Resource):

    @api.doc(description="Get all products")
    @api.doc(params={
        "page": "Page number",
        "size": "Number of elements on page",
        "categoryId": "Category id",
        "productName": "Product name",
        "productCode": "Product code"
    })
    @api.response(int(HTTPStatus.OK), "Successful get all products", products_with_pagination)
    def get(self):
        page = request.args.get("page", default=1, type=int)
        size = request.args.get("size", default=20, type=int)
        category_id = request.args.get("categoryId", default=None, type=int)
        product_name = request.args.get("productName", default=None, type=str)
        product_code = request.args.get("productCode", default=None, type=str)

        response = ProductService.get_all_products(
            page=page, size=size, category_id=category_id, product_name=product_name, product_code=product_code
        )
        return response, HTTPStatus.OK


@api.route("/create")
class ProductCreate(Resource):

    @api.doc(description="Create product")
    @api.expect(product_upload_data)
    @api.response(int(HTTPStatus.CREATED), "Successful created product", product_response)
    @api.response(int(HTTPStatus.BAD_REQUEST), "Bad request")
    def post(self):
        data = request.get_json()

        for key, value in data.items():
            if value == "":
                data[key] = None

        if "discount" in data and data["discount"] is not None:
            data["discountPeriodFrom"] = datetime.strptime(data["discountPeriodFrom"], '%Y-%m-%d').date()
            data["discountPeriodTo"] = datetime.strptime(data["discountPeriodTo"], '%Y-%m-%d').date()

        product_schema = schemas.ProductSchemaForRequestedData()
        product_data = product_schema.dump(data)
        response = ProductService.create_product(product_data=product_data)
        return {
            "status": HTTPStatus.CREATED,
            "message": "successful created",
            "product": response,
        }, HTTPStatus.CREATED


@api.route("/<int:product_id>")
class ProductOperationsById(Resource):

    @api.doc(description="Get product by id")
    @api.marshal_with(product_for_response)
    def get(self, product_id):
        response = ProductService.get_product_by_id(product_id=product_id)

        product_schema = schemas.ProductSchema()
        result = product_schema.dump(response)

        return result, HTTPStatus.OK

    @api.doc(description="Edit product by id")
    @api.expect(product_upload_data)
    @api.response(int(HTTPStatus.OK), "Successful edit product", product_response)
    @api.response(int(HTTPStatus.NOT_FOUND), "Product not found")
    def patch(self, product_id):
        edit_data = request.get_json()

        for key, value in edit_data.items():
            if value == "":
                edit_data[key] = None

        response = ProductService.edit_product(product_id=product_id, edit_data=edit_data)
        return {
            "status": HTTPStatus.OK,
            "message": "successful edit",
            "product": response,
        }, HTTPStatus.OK

    @api.doc(description="Delete product by id")
    @api.response(int(HTTPStatus.OK), "Successful delete product")
    @api.response(int(HTTPStatus.NOT_FOUND), "Product not found")
    def delete(self, product_id):
        ProductService.delete_product_by_id(product_id=product_id)
        return {
            "status": HTTPStatus.OK,
            "message": "successful delete"
        }, HTTPStatus.OK


@api.route("/upload_file")
class ProductsUploadFile(Resource):
    req_parser = RequestParser()

    req_parser.add_argument("file", type=FileStorage, location="files", required=True)

    @api.doc(description="Upload exel file")
    @api.expect(req_parser)
    @api.marshal_with(upload_file_response)
    @api.response(int(HTTPStatus.OK), "File successfully upload", upload_file_response)
    @api.response(int(HTTPStatus.BAD_REQUEST), "Bad request", upload_file_response)
    def post(self):
        args = self.req_parser.parse_args()
        if not os.path.exists(path_to_folder_with_products_data_files):
            os.makedirs(path_to_folder_with_products_data_files)

        file = args["file"]
        if "." in file.filename:
            file_extension = file.filename.split(".")[-1]

            if file_extension in ["xlsx", "xls", "xlsm"]:
                path_to_file = path_to_folder_with_products_data_files + file.filename

                file.save(path_to_file)
                ProductService.upload_file(path_to_file=path_to_file)

                return {
                    "statusCode": HTTPStatus.OK,
                    "message": "Successful upload file"
                }, HTTPStatus.OK
            else:
                return {
                    "statusCode": HTTPStatus.BAD_REQUEST,
                    "message": "Cannot interact with this file type. "
                               "Check if the file extension is one of ['xlsx', 'xls', 'xlsm']"
                }, HTTPStatus.BAD_REQUEST
        else:
            return {
                "statusCode": HTTPStatus.BAD_REQUEST,
                "message": "Check the correctness of the data sent"
            }, HTTPStatus.BAD_REQUEST


@api.route("/image/<int:product_id>/<int:image_id>")
class ProductImage(Resource):

    @api.doc(description="Get image by product id and image id")
    def get(self, product_id, image_id):

        product_image_path = ProductService.get_product_image_path(product_id=product_id, image_id=image_id)

        return send_file(product_image_path, mimetype="image/jpg")


@api.route("/video/<int:product_id>")
class ProductVideo(Resource):

    @api.doc(description="Get video by product id")
    def get(self, product_id):

        product_video_path = ProductService.get_product_video_path(product_id=product_id)

        return send_file(product_video_path, mimetype="video/mp4")
