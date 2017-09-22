#coding:utf-8

from app_info import db
import datetime

class BBhistory(db.Model):
    __tablename__ = 'BBhistory'

    id = db.Column(db.Integer,primary_key = True)
    code = db.Column(db.String(10))
    name = db.Column(db.String(40))
    time = db.Column(db.DateTime())
    price = db.Column(db.Float)
    volume = db.Column(db.Integer)
    preprice = db.Column(db.Float)
    type = db.Column(db.String(20))

