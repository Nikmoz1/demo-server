from api import ma
from marshmallow import fields

from api.models import Product, ProductImage, ProductVideo


class ProductVideoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ProductVideo


class ProductImageSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ProductImage


class ProductSchema(ma.SQLAlchemyAutoSchema):

    @staticmethod
    def _get_video_field_if_exist(obj):
        if obj.video is not None:
            return obj.video.video

    categoryId = fields.Int()
    video = fields.Function(_get_video_field_if_exist)
    images = fields.List(fields.Nested(ProductImageSchema))

    class Meta:
        model = Product
        # include_relationships = True


class ProductSchemaForRequestedData(ma.Schema):
    productCode = fields.Str(default=None)
    productNameUkr = fields.Str(default=None)
    productNameRu = fields.Str(default=None)
    descriptionUkr = fields.Str(default=None)
    descriptionRu = fields.Str(default=None)
    price = fields.Float(default=None)
    quantity = fields.Int(default=None)
    categoryId = fields.Int(default=None)
    images = fields.List(fields.Str(), default=None)
    packageSize = fields.Float(default=None)
    productSize = fields.Float(default=None)
    weight = fields.Float(default=None)
    video = fields.Str(default=None)
    brand = fields.Str(default=None)
    brandCountry = fields.Str(default=None)
    discount = fields.Float(default=None)
    discountPeriodFrom = fields.Date(default=None)
    discountPeriodTo = fields.Date(default=None)
