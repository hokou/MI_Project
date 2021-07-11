from flask import Flask, redirect, render_template, session, url_for, request, jsonify, Blueprint
import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from model import db
import json
import collections
from datetime import datetime
import requests
from views.user_api import user_api
from views.data_api import data_api
from views.mi_api import mi_api
from config import Config

app = Flask(__name__,
            static_folder="static",
            static_url_path="/")

app.config.from_object(Config)

db.init_app(app)

# Pages
@app.route("/")
def index():
	return render_template("index.html")

@app.route("/main")
def main():
	return render_template("main.html")

@app.route("/member")
def member():
	return render_template("member.html")

# blueprint
app.register_blueprint(user_api)
app.register_blueprint(data_api)
app.register_blueprint(mi_api)


if __name__ == "__main__":
	app.run(host="0.0.0.0",port=4500)