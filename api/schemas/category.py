from api import ma
from marshmallow import fields


class CategorySchema(ma.Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    nameTranslate = fields.Str(default=None)
    parentId = fields.Int()
    image = fields.Str(default=None)
    children = fields.List(fields.Dict(), default=None)


class CategoryChildSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    nameTranslate = fields.Str(default=None)
    parentId = fields.Int()
    image = fields.Str(default=None)
