from marshmallow import Schema, fields


class EntryTypeSchema(Schema):
    name = fields.String(required=True)
