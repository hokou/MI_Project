from flask import Blueprint, Flask, redirect, render_template, session, url_for, request, jsonify
from flask_sqlalchemy import SQLAlchemy
# from model import db, User
import json
from datetime import datetime

user_api = Blueprint('user', __name__, url_prefix='/api/user')

# 錯誤訊息
error_message = {
	"1":"帳號或密碼錯誤",
    "2":"帳號已經被註冊",
    "3":"輸入資料錯誤，請重新註冊",
    "4":"輸入資料錯誤，請重新登入",
	"5":"請先登出",
}


# user
@user_api.route("/", methods=["GET"])
def user_get():
	if request.method == "GET":
		# session["id"] = 1
		# session.clear()
		if "id" in session:
			print("OK")
			data = {
				"id": session["id"],
				"name": session["name"],
				"email": session["email"]
			}
			res = user_json(data)
			state = 200
		else:
			res = { 
				"data": None
			}
			state = 200
	
	return jsonify(res), state


@user_api.route("/", methods=["POST"])
def user_signup():
	if request.method == "POST":
		try:
			user_data = request.get_json()
			name = user_data['name']
			email = user_data['email']
			password = user_data['password']
			if "id" in session:
				res = error_json(error_message["5"])
				state = 400
				return jsonify(res), state
			if name == None or email == None or password == None:
				res = error_json(error_message["3"])
				state = 400
				return jsonify(res), state
			else:
				query = User.query.filter_by(email=email).first()
				print("query",query)
				if query != None:
					res = error_json(error_message["2"])
					state = 400
					return jsonify(res), state
				else:
					signup_data = User(name=name, email=email, password=password)
					db.session.add(signup_data)
					db.session.commit()
					print("signup ok")
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


@user_api.route("/a", methods=["PATCH"])
def user_login():
	if request.method == "PATCH":
		try:
			user_data = request.get_json()
			email = user_data['email']
			password = user_data['password']
			if "id" in session:
				res = error_json(error_message["5"])
				state = 400
				return jsonify(res), state
			if email == None or password == None:
				res = error_json(error_message["4"])
				state = 400
				return jsonify(res), state
			else:
				query = User.query.filter_by(email=email).first()
				print("query",query)
				if query == None:
					res = error_json(error_message["1"])
					state = 400
					return jsonify(res), state
				elif email != query.email or password != query.password:
					res = error_json(error_message["1"])
					state = 400
					return jsonify(res), state
				elif email == query.email and password == query.password:
					session["id"] = query.id
					session["name"] = query.name
					session["email"] = query.email
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


@user_api.route("/", methods=["DELETE"])
def user_logout():
	if request.method == "DELETE":
		session.pop("id", None)
		session.pop("name", None)
		session.pop("email", None)
		# session.pop("password", None)
		session.clear()
		res = {
			"ok": True
		}
		state = 200
	
	return jsonify(res), state


def user_json (data):
	user_mess = {
		"data": data
	}
	print(user_mess)
	return user_mess


def error_json(error_message):
	'''
	錯誤訊息 JSON
	'''
	res = {
		"error": True,
		"message": error_message
	}
	return res
