from flask import Blueprint, Flask, redirect, render_template, session, url_for, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from model import db, Group, Files, FileData
import json
from datetime import datetime
import os
from flask import current_app
from views.data_processing import dicom_load, dicom_img_save

data_api = Blueprint('data_api', __name__, url_prefix='/api/data')

# 錯誤訊息
error_message = {
    "1":"檔案重複",
    "2":"伺服器錯誤",
    "3":"錯誤的使用者"
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
            img_path = os.path.join(upload_folder,"imgs",str(user_id),str(user_group))
            check_folder(img_path)

            # 使用 js 上傳
            files = request.files.getlist("files")
            # 使用 form 上傳 name 接收
            # uploaded_files = request.files.getlist("file_upload")
            if check_filename(files):
                save_files(files, upload_path)
                files_name = list(session["files_name_list"])
                group_id = session["group_id"]
                add_files_data(group_id, files_name, upload_path, img_path)
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


@data_api.route("/load")
def load_data():
    try:
        if "id" in session:
            user_id = session["id"]
            creat_group(int(user_id))
            group_num = session["group_num"]
            query = FileData.query.filter_by(user_id=user_id, group_num=group_num).all()
            res = load_files_data(query)
            state = 200
        else:
            res = error_json(error_message["3"])
            state = 400
        return jsonify(res), state
    except Exception as e:
        print(e)
        res = error_json(error_message["2"])
        state = 500
        return jsonify(res), state


@data_api.route("/imgs/<path:userid>/<path:groupnum>/<path:filename>")
def imgs_url(userid, groupnum, filename):
    if "id" in session:
        if int(session["id"]) == int(userid):
            dirpath = os.path.join(current_app.config['UPLOAD_FOLDER'], 'imgs', f'{userid}', f'{groupnum}')
            return send_from_directory(dirpath, filename, as_attachment=False)
        else:
            return "error id"
    else:
        return ""


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
        files_name.append(getfile.filename.replace(".dcm",""))
    group_id = session["group_id"]
    query = Files.query.filter(Files.file_name.in_(files_name)).filter(Files.group_id==group_id).first()
    session["files_name_list"] = files_name
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


def add_files_data(group_id, files_name, upload_path, img_path):
    data = []
    for name in files_name:
        user_id = session["id"]
        group_num = session["group_num"]
        query = Files.query.filter_by(group_id=int(group_id), file_name=name).first()
        file_id = query.file_id
        file_path = os.path.join(upload_path, f"{name}.dcm")
        load_data = dicom_load(file_path)
        img_save_path = os.path.join(img_path, f"{name}.jpg")
        dicom_img_save(file_path, img_save_path)
        file_data = FileData(user_id=user_id, group_num=group_num, file_id=file_id, file_name=name, patient_ID=load_data["PID"], patient_name=load_data["PName"], rows=load_data["Rows"], columns=load_data["Columns"], ww=load_data["WW"] ,wl=load_data["WL"])
        data.append(file_data)
    db.session.add_all(data)
    db.session.commit()


def load_files_data(query):
    data = []
    id = session["id"]
    group_num = session["group_num"]
    for file_data in query:
        files_data = files_json(file_data, id, group_num)
        data.append(files_data)
        
    res = {
        "id": id,
        "group_num": group_num,
        "data": data
    }

    return res


def files_json(data, id, group_num):
    form = {}
    form["file_id"] = data.file_id
    form["file_name"] = data.file_name
    form["patient_ID"] = data.patient_ID
    form["patient_name"] = data.patient_name
    form["rows"] = data.rows
    form["columns"] = data.columns
    form["ww"] = data.ww
    form["wl"] = data.wl
    form["img"] = f"/api/data/imgs/{id}/{group_num}/{data.file_name}.jpg"
    
    return form


def error_json(error_message):
    '''
    錯誤訊息 JSON
    '''
    res = {
        "error": True,
        "message": error_message
    }
    return res