import base64
import os
from http import HTTPStatus
from pprint import pprint

from flask import send_file, url_for
from flask_restx import abort
from sqlalchemy import select
from api import models, schemas, db
from config import BASEDIR

path_to_categories_images_folder = f"{BASEDIR}/images/categories"


def category_tree_to_dict(category):
    tree = {
        "id": category.id,
        "name": category.name,
        "nameTranslate": category.nameTranslate,
        "parentId": category.parentId,
        "image": category.image,
        "children": []
    }
    if category.children:
        for child in category.children:
            tree["children"].append(category_tree_to_dict(child))
    return tree


class CategoryService:

    @staticmethod
    def get_category_by_id(category_id):
        result = db.session.execute(select(models.Category).filter(
            models.Category.id == category_id
        ))
        result = result.scalars().first()
        if result is None:
            abort(HTTPStatus.NOT_FOUND, "Category not found")
        return result

    @staticmethod
    def get_all_categories():
        categories = db.session.execute(select(models.Category)).scalars().all()

        categories_list = list()

        for category in categories:
            categories_list.append(category_tree_to_dict(category))

        return categories_list

    @staticmethod
    def get_category_tree_by_id(category_id):
        category = db.session.execute(select(models.Category).filter(
            models.Category.id == category_id
        )).scalars().first()

        category_tree = category_tree_to_dict(category)

        return category_tree

    @staticmethod
    def get_categories_tree():
        root_categories = db.session.execute(select(models.Category).filter(
            models.Category.parentId == None
        )).scalars().all()

        categories_list = list()

        for root_category in root_categories:
            categories_list.append(category_tree_to_dict(root_category))

        return categories_list

    @staticmethod
    def get_all_last_children_categories():
        last_children_categories = db.session.execute(select(models.Category).filter(
            models.Category.children == None
        )).scalars().all()
        categories_schema = schemas.CategorySchema(many=True)
        data = categories_schema.dump(last_children_categories)
        return data

    @staticmethod
    def get_category_image_path(category_id):
        category = CategoryService.get_category_by_id(category_id=category_id)

        if category.image is None:
            abort(HTTPStatus.NOT_FOUND, "Category image not found")

        return f"{path_to_categories_images_folder}/{category.id}.jpg"

    @staticmethod
    def add_image_to_category(category, image_data):
        if image_data == category.image:
            category.image = image_data
        else:
            try:
                image = base64.b64decode(image_data.split(',')[1])
                path_to_img = path_to_categories_images_folder + f"/{category.id}.jpg"
                with open(path_to_img, "wb") as f:
                    f.write(image)
                    category.image = f"/category/image/{category.id}"
            except IndexError:
                abort(
                    HTTPStatus.BAD_REQUEST,
                    'The image must be base64 encoded. Example: "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQ..."'
                )

        return category

    @staticmethod
    def create_category(category_data: dict):

        try:
            if category_data.get("image") is not None:
                base64.b64decode(category_data.get("image").split(',')[1])
        except IndexError:
            abort(
                HTTPStatus.BAD_REQUEST,
                'The image must be base64 encoded. Example: "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQ..."')

        if not os.path.exists(path_to_categories_images_folder):
            os.makedirs(path_to_categories_images_folder)

        if category_data.get("name") is None:
            abort(HTTPStatus.BAD_REQUEST, "The name field must not be empty")

        category = models.Category(
            name=category_data.get("name"),
            nameTranslate=category_data.get("nameTranslate"),
            parentId=category_data.get("parentId"),
        )

        db.session.add(category)
        db.session.commit()
        db.session.refresh(category)

        if category_data.get("image") is not None:
            CategoryService.add_image_to_category(
                category=category, image_data=category_data.get("image")
            )

            db.session.commit()
            db.session.refresh(category)

        category_schema = schemas.CategorySchema()
        data = category_schema.dump(category)

        return data

    @staticmethod
    def edit_category(category_id, edit_data):
        category = CategoryService.get_category_by_id(category_id=category_id)

        if edit_data.get("image") is not None:
            CategoryService.add_image_to_category(
                category=category, image_data=edit_data.get("image")
            )
        else:
            category.image = None

        if edit_data.get("name") is not None:
            category.name = edit_data.get("name")
        else:
            abort(HTTPStatus.BAD_REQUEST, "The name field must not be empty")

        category.nameTranslate = edit_data.get("nameTranslate")

        db.session.commit()
        db.session.refresh(category)

        result = category_tree_to_dict(category)

        category_schema = schemas.CategorySchema()
        data = category_schema.dump(result)
        pprint(data)
        return data

    @staticmethod
    def delete_category(category_id):
        category = CategoryService.get_category_by_id(category_id=category_id)
        try:
            if category.image is not None:
                os.remove(f"{path_to_categories_images_folder}/{category.id}.jpg")
            db.session.delete(category)
            db.session.commit()
        except FileNotFoundError:
            db.session.delete(category)
            db.session.commit()
