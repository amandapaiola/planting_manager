import os
import json

from flask import Flask, render_template

from orm.postgres_connection import Connection
from views.general import mod as general_view
from views.meeiro import mod as meeiro_view
from views.entry import mod as entry_view
from views.entry_type import mod as entry_type_view


app = Flask(__name__)

config_path = os.path.join(os.path.dirname(__file__), '.config.json')
configs = json.loads(open(config_path).read())

connection = Connection(user=configs['username'], pwd=configs['password'], host='127.0.0.1:5432',
                        db=configs['database'])

app.config['database'] = connection.session()


@app.errorhandler(Exception)
def handler_errors(error):
    app.config['database'].rollback()
    app.config['database'].close()


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


app.register_blueprint(general_view)
app.register_blueprint(meeiro_view)
app.register_blueprint(entry_view)
app.register_blueprint(entry_type_view)
