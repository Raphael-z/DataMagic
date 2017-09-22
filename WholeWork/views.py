# coding:utf8

import time
import operator
from flask.views import View
from flask import request, render_template


from app_info import db
from models import WholeList
from api_views import test_condition
class WholeIndexView(View):
    methods = ['GET', 'POST']

    def dispatch_request(self):
        if request.method == 'GET':
            # end_date = request.args.get('end_date')
            whole_list = db.session.query(WholeList).all()
            code_list = []
            for i in whole_list:
                code_list.append(i.code)
            result_dict = test_condition(code_list,'2017-09-22')
            rate_x = result_dict['up_prop'].keys()
            rate_y =  result_dict['up_prop'].values()
            data_x = rate_x
            data_y_up = result_dict['up'].values()
            data_y_down = result_dict['down'].values()

            # # {'up':result_up_dict,'down':result_down_dict,'up_prop':up_prop}
            # return result_dict,200
            # rate_x = [1,2,3]
            # rate_y = [2,3,4]
            # data_x = rate_x
            # data_y_up = [2,3,4]
            # data_y_down = [2,3,4]

            return render_template('/WholeWork/index.html',
                                   rate_x=rate_x,
                                   rate_y=rate_y,
                                   data_x=data_x,
                                   data_y_up=data_y_up,
                                   data_y_down=data_y_down,
                                   )

