from flask import Blueprint, Flask, redirect, render_template, session, url_for, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from model import db
import json
from datetime import datetime
import os
from flask import current_app

data_api = Blueprint('data_api', __name__, url_prefix='/api/data')

@data_api.route("/upload", methods=["POST"])
def upload():
    session["uploadfolder"] = current_app.config['UPLOAD_FOLDER']
    print(session["uploadfolder"])
    
    # 使用 js 上傳
    print(request.files.getlist("files"))
    files = request.files.getlist("files")
    for getfile in files:
        print(os.getcwd())
        getfile.save(f"{os.getcwd()}/{getfile.filename}")
        print(getfile.filename)

    # 使用 form 上傳 name 接收
    # uploaded_files = request.files.getlist("file_upload")
    # for getfile in uploaded_files:
    #     print(os.getcwd())
    #     getfile.save(f"{os.getcwd()}/{getfile.filename}")
    #     print(getfile.filename)
    pass
    return ""