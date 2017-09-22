#coding:utf-8

from app_info import db
import datetime

class WholeList(db.Model):
    __tablename__ = 'WholeList'

    id = db.Column(db.Integer,primary_key = True)
    code = db.Column(db.String(10))
    name = db.Column(db.String(40))
    c_name = db.Column(db.String(40))
    area = db.Column(db.String(40))

class WholeUpDown(db.Model):
    __tablename__ = 'WholeUpDown'

    id = db.Column(db.Integer,primary_key = True)
    code = db.Column(db.String(10))
    rule = db.Column(db.String(200))

class SMEList(db.Model):
    __tablename__ = 'SMEList'

    id = db.Column(db.Integer,primary_key = True)
    code = db.Column(db.String(10))
    name = db.Column(db.String(40))

class GEMList(db.Model):
    __tablename__ = 'GEMList'

    id = db.Column(db.Integer,primary_key = True)
    code = db.Column(db.String(10))
    name = db.Column(db.String(40))

class WholeResourceData(db.Model):
    __tablename__ ='WholeResource'

    id = db.Column(db.Integer,primary_key = True)
    code = db.Column(db.String(10))
    date = db.Column(db.DateTime)
    open = db.Column(db.String(10))
    high = db.Column(db.String(10))
    close = db.Column(db.String(10))
    low = db.Column(db.String(10))
    volume = db.Column(db.String(20))
    price_change = db.Column(db.String(10))
    p_change = db.Column(db.String(10))
    ma5 = db.Column(db.String(10))
    ma10 = db.Column(db.String(10))
    ma20 = db.Column(db.String(10))
    v_ma5 = db.Column(db.String(20))
    v_ma10 = db.Column(db.String(20))
    v_ma20 = db.Column(db.String(20))
    turnover = db.Column(db.String(20))

class WholeBig(db.Model):
    __tablename__ = 'WholeBig'

    id = db.Column(db.Integer,primary_key = True)
    code = db.Column(db.String(10))
    date = db.Column(db.DateTime())
    amount = db.Column(db.String(20))
    amount_50 = db.Column(db.String(20))
    amount_100 = db.Column(db.String(20))
    amount_200 = db.Column(db.String(20))
    amount_400 = db.Column(db.String(20))
    type = db.Column(db.String(20))




