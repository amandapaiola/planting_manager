from flask import Blueprint, render_template

mod = Blueprint('general', __name__)


@mod.route('/', methods=['GET'])
def index():
    return render_template('general/index.html', latest_release=1)

