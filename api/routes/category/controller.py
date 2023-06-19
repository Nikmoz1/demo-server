from http import HTTPStatus
from flask import request, send_file
from flask_restx import Resource

from api.services.category import CategoryService
from .dto import CategoryDto
from api import schemas


api = CategoryDto.api

category_data = CategoryDto.category
category_resp_to_status = CategoryDto.category_resp_to_status
category_list = CategoryDto.category_list
category_tree = CategoryDto.category_tree
categories_tree = CategoryDto.categories_tree
category_last_child = CategoryDto.category_last_child
category_edit = CategoryDto.category_edit
category_response = CategoryDto.category_response


@api.route("/all")
class CategoryAll(Resource):

    @api.doc(description="Get all category")
    @api.response(int(HTTPStatus.OK), "Successful get all category", category_list)
    def get(self):
        response = CategoryService.get_all_categories()
        return {"categories": response}, HTTPStatus.OK


@api.route("/all/trees")
class CategoryTreeAll(Resource):

    @api.doc(description="Get categories trees")
    @api.response(int(HTTPStatus.OK), "Successful get all category tees", categories_tree)
    def get(self):
        response = CategoryService.get_categories_tree()
        return {"categories": response}, HTTPStatus.OK


@api.route("/all/last_children")
class CategoryAllLastChildren(Resource):

    @api.doc(discription="Get all last children categories")
    @api.response(int(HTTPStatus.OK), "Successful get all last children categories", category_last_child)
    def get(self):
        response = CategoryService.get_all_last_children_categories()
        return {"categories": response}, HTTPStatus.OK


@api.route("/create")
class CategoryCreate(Resource):

    @api.doc(description="Create category")
    @api.expect(category_data)
    @api.response(int(HTTPStatus.CREATED), "Successful created category", category_resp_to_status)
    def post(self):
        data = request.get_json()

        for key, value in data.items():
            if value == "":
                data[key] = None

        response = CategoryService.create_category(data)

        return {
            "status": HTTPStatus.CREATED,
            "message": "successful created",
            "category": response,
        }, HTTPStatus.CREATED


@api.route("/<int:category_id>")
class CategoryOperationsById(Resource):

    @api.doc(description="Get category")
    @api.response(int(HTTPStatus.OK), "Successful get category", category_tree)
    @api.response(int(HTTPStatus.NOT_FOUND), "Category not found")
    def get(self, category_id):
        response = CategoryService.get_category_tree_by_id(category_id=category_id)
        return response, HTTPStatus.OK

    @api.doc(description="Edit category")
    @api.expect(category_edit)
    @api.response(int(HTTPStatus.OK), "Successful edit category", category_resp_to_status)
    @api.response(int(HTTPStatus.NOT_FOUND), "Category not found")
    def patch(self, category_id):
        edit_data = request.get_json()

        for key, value in edit_data.items():
            if value == "":
                edit_data[key] = None

        response = CategoryService.edit_category(category_id=category_id, edit_data=edit_data)
        return {
            "status": HTTPStatus.OK,
            "message": "successful edit",
            "category": response,
        }, HTTPStatus.OK

    @api.doc(description="Delete category")
    @api.response(int(HTTPStatus.OK), "Successful delete category")
    @api.response(int(HTTPStatus.NOT_FOUND), "Category not found")
    def delete(self, category_id):
        CategoryService.delete_category(category_id=category_id)
        return {
            "status": HTTPStatus.OK,
            "message": "successful delete"
        }, HTTPStatus.OK


@api.route('/image/<int:category_id>')
class CategoryImage(Resource):

    @api.doc(description="Get image by category id")
    def get(self, category_id):

        category_image_path = CategoryService.get_category_image_path(category_id=category_id)

        return send_file(category_image_path, mimetype="image/jpg")
