import base64
import os
import shutil
import requests
import pandas as pd
from http import HTTPStatus
from sqlalchemy import select, or_, and_, desc
from sqlalchemy.orm import joinedload
from flask_restx import abort
from datetime import datetime
from pprint import pprint

from api import schemas, models, services
from api import db
from config import BASEDIR


path_to_products_images_folder = f"{BASEDIR}/images/products"
path_to_products_videos_folder = f"{BASEDIR}/videos"


class ProductService:

    @staticmethod
    def get_product_by_id(product_id):
        result = db.session.execute(select(models.Product).filter(models.Product.id == product_id))
        result = result.scalars().first()

        if result is None:
            abort(HTTPStatus.NOT_FOUND, "Product Not Found")

        return result

    @staticmethod
    def get_product_by_product_code(product_code):
        result = db.session.execute(select(models.Product).filter(models.Product.productCode == product_code))
        result = result.scalars().first()

        return result

    @staticmethod
    def get_products_by_product_code(product_code):
        result = db.session.execute(select(models.Product).filter(models.Product.productCode == product_code))
        result = result.scalars().all()

        return result

    @staticmethod
    def get_all_products(page, size, category_id, product_name, product_code):
        products_query = db.session.query(models.Product).order_by(desc(models.Product.dateCreatedProduct))
        if category_id:
            products_query = products_query.filter(models.Product.categoryId == category_id)
        if product_name:
            products_query = products_query.filter(or_(
                models.Product.productNameUkr.ilike(f"%{product_name}"),
                models.Product.productNameRu.ilike(f"%{product_name}")
            ))
        if product_code:
            products_query = products_query.filter(models.Product.productCode == product_code)

        products = products_query.paginate(page=page, per_page=size, error_out=False, max_per_page=None)
        total = products.total
        pages = products.pages

        products_schema = schemas.ProductSchema(many=True)

        return {
            "products": products_schema.dump(products.items),
            "page": page,
            "size": size if size <= total else total,
            "total": total,
            "pages": pages
        }

    @staticmethod
    def get_product_by_names(name_urk, name_ru):
        result = db.session.execute(select(models.Product).filter(and_(
            models.Product.productNameUkr.ilike(f"%{name_urk}"),
            models.Product.productNameRu.ilike(f"%{name_ru}")
        ))).scalars().first()
        return result

    @staticmethod
    def get_image_by_id_and_product_id(image_id, product_id):
        result = db.session.execute(select(models.ProductImage).filter(
            models.ProductImage.id == image_id,
            models.ProductImage.productId == product_id
        )).scalars().first()

        if result is None:
            abort(HTTPStatus.NOT_FOUND, "Product image not found")

        return result

    @staticmethod
    def get_product_image_path(product_id, image_id):
        image = ProductService.get_image_by_id_and_product_id(image_id=image_id, product_id=product_id)

        return f"{path_to_products_images_folder}/{image.productId}/{image.id}.jpg"

    @staticmethod
    def get_video_by_product_id(product_id):
        result = db.session.execute(select(models.ProductVideo).filter(
            models.ProductVideo.productId == product_id
        )).scalars().first()

        if result is None:
            abort(HTTPStatus.NOT_FOUND, "Product video not found")

        return result

    @staticmethod
    def get_product_video_path(product_id):
        video = ProductService.get_video_by_product_id(product_id=product_id)

        return f"{path_to_products_videos_folder}/{video.productId}.mp4"

    @staticmethod
    def create_product(product_data):
        try:
            if product_data["categoryId"] is not None:
                category = services.CategoryService.get_category_by_id(category_id=product_data["categoryId"])
            else:
                category = None

            product = models.Product(
                productCode=product_data["productCode"],
                productNameUkr=product_data["productNameUkr"],
                productNameRu=product_data["productNameRu"],
                descriptionUkr=product_data["descriptionUkr"],
                descriptionRu=product_data["descriptionRu"],
                price=product_data["price"],
                quantity=product_data["quantity"],
                packageSize=product_data["packageSize"],
                productSize=product_data["productSize"],
                weight=product_data["weight"],
                brand=product_data["brand"],
                brandCountry=product_data["brandCountry"],
                discount=product_data["discount"],
                discountPeriodFrom=product_data["discountPeriodFrom"],
                discountPeriodTo=product_data["discountPeriodTo"],
                category=category,
            )

            if product_data["images"] is not None:
                ProductService.add_product_images(product=product, images=product_data["images"])

            if product_data["video"] is not None:
                ProductService.add_product_video(product=product, video_data=product_data["video"])

            product_schema = schemas.ProductSchema()
            product = product_schema.dump(product)
            return product
        except KeyError:
            abort(int(HTTPStatus.BAD_REQUEST), "Required field is missing")

    @staticmethod
    def add_product_images(product, images):
        path_to_concrete_products_images = path_to_products_images_folder + f"/{product.id}"

        for img in images:
            image = models.ProductImage(
                product=product,
                image=""
            )
            db.session.add(image)
            db.session.commit()
            db.session.refresh(image)

            path_to_img = path_to_concrete_products_images + f"/{image.id}.jpg"
            if "images.prom" in img:
                image.image = img
            else:
                if not os.path.exists(path_to_concrete_products_images):
                    os.makedirs(path_to_concrete_products_images)

                decoded_image = base64.b64decode(img.split(',')[1])
                with open(path_to_img, "wb") as f:
                    f.write(decoded_image)
                    image.image = f"/product/image/{image.productId}/{image.id}"

    @staticmethod
    def add_product_video(product, video_data):

        if not os.path.exists(path_to_products_videos_folder):
            os.makedirs(path_to_products_videos_folder)

        video = models.ProductVideo(
            product=product,
            video=""
        )

        db.session.add(video)
        db.session.commit()
        db.session.refresh(video)

        path_to_video = path_to_products_videos_folder + f"/{product.id}.mp4"
        decoded_video = base64.b64decode(video_data.split(',')[1])
        with open(path_to_video, "wb") as f:
            f.write(decoded_video)
            video.video = f"/product/video/{video.productId}"
            db.session.commit()

    @staticmethod
    def add_category_to_product(product, category_id):
        category = services.CategoryService.get_category_by_id(category_id=category_id)

        product.category = category
        db.session.commit()

    @staticmethod
    def edit_product(product_id, edit_data):
        product = ProductService.get_product_by_id(product_id=product_id)

        if not edit_data.keys():
            abort(HTTPStatus.BAD_REQUEST, "You don't transfer any data")

        for key, value in edit_data.items():
            if key != "video" and key != "images":
                setattr(product, key, value)
            elif key == "video":
                if value is not None:
                    if value == product.video.video:
                        product.video.video = value
                    else:
                        try:
                            path_to_video = path_to_products_videos_folder + f"/{product.id}.mp4"
                            decoded_video = base64.b64decode(value.split(',')[1])
                            with open(path_to_video, "wb") as f:
                                f.write(decoded_video)
                                product.video.video = f"/product/video/{product.id}"
                        except AttributeError:
                            ProductService.add_product_video(product=product, video_data=value)
                else:
                    if product.video is not None:
                        os.remove(f"{path_to_products_videos_folder}/{product.id}.mp4")
                        db.session.delete(product.video)

            elif key == "images":
                if value is not None and len(value) > 0:
                    for image in product.images:
                        if "images.prom" in image.image:
                            db.session.delete(image)
                        else:
                            db.session.delete(image)
                            os.remove(f"{path_to_products_images_folder}/{image.productId}/{image.id}.jpg")

                    ProductService.add_product_images(product=product, images=value)
                else:
                    for image in product.images:
                        if "images.prom" in image.image:
                            db.session.delete(image)
                        else:
                            db.session.delete(image)
                    try:
                        shutil.rmtree(f"{path_to_products_images_folder}/{product.id}")
                    except FileNotFoundError:
                        continue

        db.session.commit()
        db.session.refresh(product)

        product_schema = schemas.ProductSchema()
        data = product_schema.dump(product)

        return data

    @staticmethod
    def delete_product_by_id(product_id):
        product = ProductService.get_product_by_id(product_id=product_id)
        try:
            shutil.rmtree(f"{path_to_products_images_folder}/{product.id}")
            try:
                os.remove(f"{path_to_products_videos_folder}/{product.id}.mp4")
                db.session.delete(product)
                db.session.commit()
            except FileNotFoundError:
                db.session.delete(product)
                db.session.commit()

        except FileNotFoundError:
            try:
                os.remove(f"{path_to_products_videos_folder}/{product.id}.mp4")
                db.session.delete(product)
                db.session.commit()
            except FileNotFoundError:
                db.session.delete(product)
                db.session.commit()

    @staticmethod
    def save_uploaded_data(product_dict):
        date_now = datetime.now().date()
        if product_dict["discountPeriodTo"] is not None:

            discount_date_to = datetime.strptime(product_dict["discountPeriodTo"], "%d.%m.%Y").date()

            if discount_date_to <= date_now:
                product_dict["discount"] = None
                product_dict["discountPeriodFrom"] = None
                product_dict["discountPeriodTo"] = None
            else:
                product_dict["discountPeriodFrom"] = datetime.strptime(
                    product_dict["discountPeriodFrom"], "%d.%m.%Y"
                ).date()
                product_dict["discountPeriodTo"] = discount_date_to

        product_schema = schemas.ProductSchemaForRequestedData()
        product = product_schema.dump(product_dict)

        ProductService.create_product(product)

    @staticmethod
    def upload_file(path_to_file):
        # replacements = {
        #     "&nbsp;": " ",
        #     "&deg; ": "°",
        #     "&deg;": "°",
        # }
        #     for old, new in replacements.items():
        #         description_ukr = description_ukr.replace(old, new)
        #         description_ru = description_ru.replace(old, new)
        excel_data = pd.read_excel(path_to_file)

        for index, row in excel_data.iterrows():
            product_dict = {
                "productCode": row["Код_товара"] if not pd.isna(row["Код_товара"]) else None,
                "productNameUkr": row["Название_позиции_укр"] if not pd.isna(row["Название_позиции_укр"]) else None,
                "productNameRu": row["Название_позиции"] if not pd.isna(row["Название_позиции"]) else None,
                "descriptionUkr": row["Описание_укр"] if not pd.isna(row["Описание_укр"]) else None,
                "descriptionRu": row["Описание"] if not pd.isna(row["Описание"]) else None,
                "price": row["Цена"] if not pd.isna(row["Цена"]) else None,
                "quantity": row["Количество"] if not pd.isna(row["Количество"]) else None,
                "weight": row["Вес,кг"] if not pd.isna(row["Вес,кг"]) else None,
                "brand": row["Производитель"] if not pd.isna(row["Производитель"]) else None,
                "brandCountry": row["Страна_производитель"] if not pd.isna(row["Страна_производитель"]) else None,
                "discount": row["Скидка"] if not pd.isna(row["Скидка"]) else None,
                "discountPeriodFrom": row["Cрок действия скидки от"] if not pd.isna(
                    row["Cрок действия скидки от"]) else None,
                "discountPeriodTo": row["Cрок действия скидки до"] if not pd.isna(
                    row["Cрок действия скидки до"]) else None,
                "images": row["Ссылка_изображения"].split(", ") if not pd.isna(row["Ссылка_изображения"]) else None
            }

            if product_dict["productCode"] is None:
                products_by_name = ProductService.get_product_by_names(
                    name_urk=product_dict["productNameUkr"], name_ru=product_dict["productNameRu"]
                )
                if products_by_name is None:
                    ProductService.save_uploaded_data(product_dict=product_dict)
                    continue
                else:
                    continue

            else:
                products = ProductService.get_products_by_product_code(
                    product_code=product_dict["productCode"]
                )
                if products is not None:
                    not_exist = True
                    for product in products:
                        if product.productNameUkr == product_dict["productNameUkr"] and \
                                product.productNameRu == product_dict["productNameRu"]:
                            not_exist = False
                            break
                    if not_exist:
                        ProductService.save_uploaded_data(product_dict=product_dict)
                        continue
                else:
                    ProductService.save_uploaded_data(product_dict=product_dict)
