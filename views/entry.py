from flask import Blueprint, render_template, request, current_app
from marshmallow import ValidationError

from controllers.entry import EntryController
from controllers.entry_type import EntryTypeController
from controllers.meeiro import MeeiroController
from views.schemas.entry import EntrySchema, format_date

mod = Blueprint('entries', __name__, url_prefix='/entries')


@mod.route('/', methods=['GET'])
def index():

    return render_template('entries/e_index.html')


@mod.route('/get_template', methods=['GET'])
def list_template():
    # TODO melhorar isso por favor :/
    template_required = [i[0] for i in request.args.items()][0]

    db = current_app.config['database']

    entry_type_controller = EntryTypeController(db_connection=db)
    meeiro_controller = MeeiroController(db_connection=db)

    entry_types = entry_type_controller.list()
    meeiros = meeiro_controller.list()

    if template_required == 'filter':
        return render_template('entries/filter.html', **{'types': entry_types, 'meeiros': meeiros})
    elif template_required == 'insert':

        return render_template('entries/insert.html',
                               **{'types': entry_types,
                                  'meeiros': meeiros})
    elif template_required == 'insert_entry_type':
        return render_template('entries/insert_entry_type.html')


@mod.route('/list', methods=['POST'])
def list():
    pass


@mod.route('/insert', methods=['POST'])
def insert():
    try:
        loaded = EntrySchema().load(request.form)
        if loaded.errors:
            return render_template('invalid_schema.html', latest_release=1)
        controller = EntryController(db_connection=current_app.config['database'])
        inserted, msg = controller.insert_new_entry(meeiro_id=loaded.data['meeiro_id'],
                                                    entry_date=format_date(date=loaded.data['entry_date']),
                                                    entry_type_id=loaded.data['entry_type_id'],
                                                    entry_value=loaded.data['entry_value'],
                                                    description=loaded.data['description'])
        return render_template('entries/e_index.html', latest_release=1, **{'inserted': inserted,
                                                                            'message': msg})
    except ValidationError as error:
        return render_template('invalid_schema.html', latest_release=1, **{'schema_error': error})
