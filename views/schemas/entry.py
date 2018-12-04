from datetime import datetime
import pytz
from marshmallow import Schema, fields


class EntrySchema(Schema):
    id_ = fields.Integer(required=False, load_from="id", attribute="id")
    entry_date = fields.String(required=True)
    entry_type_id = fields.Integer(required=True)
    entry_value = fields.Float(required=True)
    description = fields.String(required=True)
    meeiro_id = fields.Integer(required=True)


def format_date(date: str) -> datetime:
    """
    transforma a data enviada no formato dd/mm/aaaa em objeto do python.
    :param date: ex: 08/08/2018
    :return: objeto datetime
    """
    america_timezone = pytz.timezone('America/Sao_Paulo')
    return america_timezone.localize(datetime.strptime(date, "%d/%m/%Y"))
