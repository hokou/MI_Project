from flask import Blueprint, Flask, redirect, render_template, session, url_for, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from model import db
import json
from datetime import datetime
from views.data_processing import dicom_load, dicom_renew

mi_api = Blueprint('mi_api', __name__, url_prefix='/api/mi')

# mi means Medical Imaging


@mi_api.route("/data", methods=["GET"])
def midata_get():
    if request.method == "GET":
        if "file_path" in session:
            path = session["file_path"]
            print(path)
            res = dicom_load(path)
            state = 200

            return jsonify(res), state
        else:
            return redirect("main")


@mi_api.route("/renew", methods=["POST"])
def midata_renew():
    if request.method == "POST":
        path = session["file_path"]
        midata = request.get_json()
        res = dicom_renew(path, midata)
        state = 200

        return jsonify(res), state