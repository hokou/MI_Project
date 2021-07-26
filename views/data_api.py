from flask import Blueprint, Flask, redirect, render_template, session, url_for, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from model import db
import json
from datetime import datetime

data_api = Blueprint('data_api', __name__, url_prefix='/api/data')

@data_api.route("/upload", methods=["POST"])
def upload():
    
    print(request.files['files'])
    pass