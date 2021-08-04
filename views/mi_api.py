from flask import Blueprint, Flask, redirect, render_template, session, url_for, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from model import db, LabelData
import json
from datetime import datetime
from views.data_processing import dicom_load, dicom_renew

mi_api = Blueprint('mi_api', __name__, url_prefix='/api/mi')

# mi means Medical Imaging

# 錯誤訊息
error_message = {
    "1":"資料重複",
    "2":"伺服器錯誤"
}

@mi_api.route("/data", methods=["GET"])
def midata_get():
    if request.method == "GET":
        if "file_path" in session:
            path = session["file_path"]
            file_id = session["file_id"]
            res = dicom_load(path, file_id=file_id)
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


@mi_api.route("/label", methods=["GET"])
def labeldata_get():
    if request.method == "GET":
        if "file_id" in session:
            file_id = session["file_id"]
            res = label_get(file_id)
            state = 200

            return jsonify(res), state
        else:
            return redirect("main")


@mi_api.route("/labelsave", methods=["POST"])
def label_save():
    if request.method == "POST":
        try:
            user_id = session["id"]
            data = request.get_json()
            res = label_add_or_update(data, user_id)
            state = 200

            return jsonify(res), state
        except Exception as e:
            print(e)
            res = error_json(error_message["2"])
            state = 500

            return jsonify(res), state


def label_get(file_id):
    query = LabelData.query.filter_by(file_id=file_id).first()
    if query != None:
        res = {
            "data":{
                "id": query.user_id,
                "fileid":query.file_id,
                "num":query.label_num,
                "label":eval(query.data)
            }
        }
    else:
        res = {
            "data":None,
        }
    return res


def label_add_or_update(data, user_id):
    file_id = data["fileid"]
    query = LabelData.query.filter_by(file_id=file_id).first()
    label_num = data["num"]
    label_data = data["label"]
    if query == None:
        label_add = LabelData(user_id=int(user_id), file_id=int(file_id), label_num=int(label_num), data=str(label_data))
        db.session.add(label_add)
        db.session.commit()
    else:
        query.label_num = int(label_num)
        query.data = str(label_data)
        db.session.commit()
    res = {
        "ok": True
    }

    return res


def error_json(error_message):
    '''
    錯誤訊息 JSON
    '''
    res = {
        "error": True,
        "message": error_message
    }
    return res
