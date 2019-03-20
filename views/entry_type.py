from flask import Blueprint, request, current_app, render_template
from marshmallow import ValidationError

from controllers.entry import EntryController
from controllers.entry_type import EntryTypeController
from views.schemas.entry_type import EntryTypeSchema

mod = Blueprint('entry_type', __name__, url_prefix='/entry_type')


@mod.route('/insert', methods=['POST'])
def insert():
    try:
        loaded = EntryTypeSchema().load(request.form)
        if loaded.errors:
            return render_template('invalid_schema.html', latest_release=1)
        controller = EntryTypeController(db_connection=current_app.config['database'])
        inserted, msg = controller.insert(name=loaded.data['name'])
        return render_template('entries/e_index.html', latest_release=1, **{'inserted': inserted,
                                                                            'message': msg})
    except ValidationError as error:
        return render_template('invalid_schema.html', latest_release=1, **{'schema_error': error})
