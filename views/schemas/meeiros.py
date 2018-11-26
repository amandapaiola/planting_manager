from marshmallow import Schema, fields


class MeeiroSchema(Schema):
    name = fields.String(required=True)
    rg = fields.String(required=True)
    cpf = fields.String(required=True)
    id_ = fields.Integer(required=False, load_from="id", attribute="id")
