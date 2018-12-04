from flask import Blueprint, render_template, request, current_app

from controllers.meeiro import MeeiroController
from views.schemas.meeiro import MeeiroSchema
from marshmallow import ValidationError

mod = Blueprint('meeiros', __name__, url_prefix='/meeiros')


@mod.route('/', methods=['GET'])
def index():
    return render_template('meeiros/m_index.html', latest_release=1)


@mod.route('/get_template', methods=['GET'])
def list_template():
    # TODO melhorar isso por favor :/
    template_required = [i[0] for i in request.args.items()][0]

    controller = MeeiroController(db_connection=current_app.config['database'])
    if template_required == 'list':
        meeiros = controller.list()
        return render_template('meeiros/list.html', **{'meeiros': meeiros})
    elif template_required == 'insert':
        return render_template('meeiros/insert.html')


@mod.route('/insert', methods=['POST'])
def insert():
    try:
        loaded = MeeiroSchema().load(request.form)
        if loaded.errors:
            return render_template('invalid_schema.html', latest_release=1)
        controller = MeeiroController(db_connection=current_app.config['database'])
        inserted, msg = controller.insert_new_meeiro(name=loaded.data['name'], cpf=loaded.data['cpf'],
                                                     rg=loaded.data['rg'])
        return render_template('meeiros/m_index.html', latest_release=1, **{'inserted': inserted,
                                                                            'message': msg})
    except ValidationError as error:
        return render_template('invalid_schema.html', latest_release=1, **{'schema_error': error})


@mod.route('/update', methods=['POST'])
def update():
    try:
        loaded = MeeiroSchema().load(request.form)
        if loaded.errors:
            return render_template('invalid_schema.html', latest_release=1)
        controller = MeeiroController(db_connection=current_app.config['database'])
        inserted, msg = controller.update(name=loaded.data['name'], cpf=loaded.data['cpf'],
                                          rg=loaded.data['rg'], id_=loaded.data['id'])
        return render_template('meeiros/m_index.html', latest_release=1, **{'inserted': inserted,
                                                                            'message': msg})
    except ValidationError as error:
        return render_template('invalid_schema.html', latest_release=1, **{'schema_error': error})
