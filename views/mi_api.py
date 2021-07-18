from flask import Blueprint, Flask, redirect, render_template, session, url_for, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from model import db
import json
from datetime import datetime
from views.data_processing import dicom_load

mi_api = Blueprint('mi_api', __name__, url_prefix='/api/mi')

# mi means Medical Imaging

path = ""

@mi_api.route("/data", methods=["GET"])
def midata_get():
    if request.method == "GET":
        res = dicom_load(path)
        state = 200

        return jsonify(res), state
