from flask_restx import Namespace, fields


class CategoryDto:
    api = Namespace("category", description="Operations are associated with categories")

    category = api.model(
        "Category object",
        {
            "name": fields.String(),
            "nameTranslate": fields.String(defoult=None),
            "parentId": fields.Integer(defoult=None),
            "image": fields.String(defoult=None)
        }
    )

    category_edit = api.model(
        "Category edit object",
        {
            "name": fields.String(),
            "nameTranslate": fields.String(defoult=None),
            "image": fields.String(defoult=None)
        }
    )

    category_last_child = api.model(
        "Category Tree Last Child",
        {
            "id": fields.Integer(),
            "name": fields.String(),
            "parentId": fields.Integer(),
            "nameTranslate": fields.String(),
            "image": fields.String()
        }
    )

    category_response = api.model(
        "Category Data Response",
        {
            "id": fields.Integer(),
            "name": fields.String(),
            "nameTranslate": fields.String(),
            "parentId": fields.Integer(),
            "image": fields.String(),
            "children": fields.List(fields.Raw)
        }
    )

    category_resp_to_status = api.model(
        "Category Response Answer",
        {
            "status": fields.Integer(),
            "message": fields.String(),
            "category": fields.Nested(category_response),
        }
    )

    category_list = api.model(
        "Category Data List",
        {
            "categories": fields.List(fields.Nested(category_response))
        }
    )

    category_tree = api.model(
        "Category Tree Parent",
        {
            "id": fields.Integer(),
            "name": fields.String(),
            "nameTranslate": fields.String(),
            "parentId": fields.Integer(),
            "image": fields.String(),
            "children": fields.List(fields.Raw)
        }
    )

    categories_tree = api.model(
        "Category Tree List",
        {
            "categories": fields.List(fields.Nested(category_tree))
        }
    )
