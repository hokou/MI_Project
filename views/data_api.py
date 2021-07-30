from flask import Blueprint, Flask, redirect, render_template, session, url_for, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from model import db, Group, Files
import json
from datetime import datetime
import os
from flask import current_app

data_api = Blueprint('data_api', __name__, url_prefix='/api/data')

# 錯誤訊息
error_message = {
    "1":"檔案重複",
    "2":"伺服器錯誤",
}


@data_api.route("/upload", methods=["POST"])
def upload():
    if request.method == "POST":
        try:
            session["uploadfolder"] = current_app.config['UPLOAD_FOLDER']
            upload_folder = session["uploadfolder"]
            user_id = session["id"]
            creat_group(int(user_id))
            user_group = session["group_num"] 
            upload_path = os.path.join(upload_folder,"files",str(user_id),str(user_group))
            check_folder(upload_path)

            # 使用 js 上傳
            files = request.files.getlist("files")
            # 使用 form 上傳 name 接收
            # uploaded_files = request.files.getlist("file_upload")
            if check_filename(files):
                save_files(files, upload_path)
            else:
                res = error_json(error_message["1"])
                state = 201
                return jsonify(res), state

            res = {
                "ok": True
            }
            state = 200
            return jsonify(res), state
        except Exception as e:
            print(e)
            res = error_json(error_message["2"])
            state = 500
            return jsonify(res), state


def check_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)


def creat_group(id):
    query = Group.query.filter_by(user_id=id).first()
    if query == None:
        group_num = 1
        group_name = f"group_{group_num}"
        group_add = Group(user_id=id, group_num=group_num, group_name=group_name)
        db.session.add(group_add)
        db.session.commit()
        query = Group.query.filter_by(user_id=id).first()
    session["group_id"] = query.group_id
    session["group_num"] = query.group_num
    session["group_name"] = query.group_name


def check_filename(files):
    files_name = []
    for getfile in files:
        files_name.append(getfile.filename)
    group_id = session["group_id"]
    query = Files.query.filter(Files.file_name.in_(files_name)).filter(Files.group_id==group_id).first()
    if query == None:
        add_files_name(group_id, files_name)
        return True
    else:
        return False


def save_files(files, upload_path):
    for getfile in files:
        # print(os.getcwd())
        getfile.save(f"{upload_path}/{getfile.filename}")
        # print(getfile.filename)


def add_files_name(group_id, files_name):
    data = []
    for name in files_name:
        file_data = Files(group_id=int(group_id),file_name=name)
        data.append(file_data)
    db.session.add_all(data)
    db.session.commit()


def error_json(error_message):
    '''
    錯誤訊息 JSON
    '''
    res = {
        "error": True,
        "message": error_message
    }
    return res