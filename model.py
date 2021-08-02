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

    db_user_group = db.relationship("Group", backref="user")

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password


class Group(db.Model):
    __tablename__ = 'group'
    group_id = db.Column(db.BigInteger, autoincrement=True, primary_key=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey('user.id'), nullable=False)
    group_num = db.Column(db.BigInteger, nullable=False)
    group_name = db.Column(db.VARCHAR(255), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)

    db_group_files = db.relationship("Files", backref="group")

    def __init__(self, user_id, group_num, group_name):
        self.user_id = user_id
        self.group_num = group_num
        self.group_name = group_name


class Files(db.Model):
    __tablename__ = 'files'
    file_id = db.Column(db.BigInteger, autoincrement=True, primary_key=True)
    group_id = db.Column(db.BigInteger, db.ForeignKey('group.group_id'), nullable=False)
    file_name = db.Column(db.VARCHAR(255), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)

    db_files_filedata = db.relationship("FileData", backref="files")

    def __init__(self, group_id, file_name):
        self.group_id = group_id
        self.file_name = file_name


class FileData(db.Model):
    __tablename__ = 'filedata'
    id = db.Column(db.BigInteger, autoincrement=True, primary_key=True)
    user_id = db.Column(db.BigInteger, nullable=False)
    group_num = db.Column(db.BigInteger, nullable=False)
    file_id = db.Column(db.BigInteger, db.ForeignKey('files.file_id'), nullable=False)
    file_name = db.Column(db.VARCHAR(255), nullable=False)
    patient_ID = db.Column(db.VARCHAR(255), nullable=False)
    patient_name = db.Column(db.VARCHAR(255), nullable=False)
    rows = db.Column(db.VARCHAR(255), nullable=False)
    columns = db.Column(db.VARCHAR(255), nullable=False)
    ww = db.Column(db.VARCHAR(255), nullable=False)
    wl = db.Column(db.VARCHAR(255), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, user_id, group_num, file_id, file_name, patient_ID, patient_name, rows, columns, ww, wl):
        self.user_id = user_id
        self.group_num = group_num
        self.file_id = file_id
        self.file_name = file_name
        self.patient_ID = patient_ID
        self.patient_name = patient_name
        self.rows = rows
        self.columns = columns
        self.ww = ww
        self.wl = wl


class LabelData(db.Model):
    __tablename__ = 'labeldata'
    id = db.Column(db.BigInteger, autoincrement=True, primary_key=True)
    user_id = db.Column(db.BigInteger, nullable=False)
    file_id = db.Column(db.BigInteger, nullable=False)
    label_num = db.Column(db.Integer, nullable=False)
    data = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, onupdate=datetime.now, default=datetime.now)

    def __init__(self, user_id, file_id, label_num, data):
        self.user_id = user_id
        self.file_id = file_id
        self.label_num = label_num
        self.data = data