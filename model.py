from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.BigInteger, autoincrement=True, primary_key=True)
    name = db.Column(db.VARCHAR(255), nullable=False)
    email = db.Column(db.VARCHAR(255), nullable=False)
    password = db.Column(db.VARCHAR(255), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password