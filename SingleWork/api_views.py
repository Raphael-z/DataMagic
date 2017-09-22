# coding:utf8
import tushare as ts
from flask import request
from flask_restful import Resource

from app_info import db
from models import BBhistory

class GetBBhistory(Resource):

    def get(self):
        """
        request:http://127.0.0.1:5000/single/api/v1.0/get_bb_history?code_list=300682,300675&date_list=2017-09-13,2017-09-14&vol=400
        @code_list:300682,300675
        @date_list:2017-09-13,2017-09-14
        @vol=400
        :return: {'msg':"完成",'error_list':error_list},error_list表示错误的选项
        """
        code_list = request.args.get('code_list')
        code_list = code_list.split(',')
        vol = request.args.get('vol')
        date_list = request.args.get('date_list')
        date_list = date_list.split(',')
        # error_list 数据出错的列表
        error_list = []
        for i in code_list:
            for j in date_list:
                sina_data = ts.get_sina_dd(str(i), str(j), int(vol))
                if sina_data.empty:
                    code = i
                    date = j
                    error_list.append({'code': code, 'date': date})
                else:
                    for k in range(0, len(sina_data)):
                        code = i
                        name = sina_data.name[k]
                        time = sina_data.time[k]
                        price = sina_data.price[k]
                        volume = sina_data.volume[k]
                        preprice = sina_data.preprice[k]
                        type = sina_data.type[k]
                        bbhis = BBhistory(
                            code=code,
                            name=name,
                            time=str(j)+' '+str(time),
                            price=price,
                            volume=volume,
                            preprice=preprice,
                            type=type)
                        db.session.add(bbhis)
                        db.session.commit()

        return {'msg':"完成",'error_list':error_list},200
