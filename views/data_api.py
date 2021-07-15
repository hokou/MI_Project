from flask import Blueprint

data_api = Blueprint('data_api', __name__, url_prefix='/api/data')

@data_api.route("/upload", methods=["POST"])
def upload():
    pass