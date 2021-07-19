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


@mi_api.route("/renew", methods=["POST"])
def midata_renew():
    if request.method == "POST":
        ww = request.form.get("ww")
        wl = request.form.get("wl")
        inverse = request.form.get("image_inverse")
        print(ww,wl,inverse)
        res = dicom_load(path)
        state = 200

        return jsonify(res), state