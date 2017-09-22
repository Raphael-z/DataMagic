# coding:utf8

import time
import operator
from flask.views import View
from flask import request, render_template

from app_info import db
from models import BBhistory
from WholeWork.models import WholeBig

class BBhistoryIndexView(View):
    methods = ['GET', 'POST']

    def dispatch_request(self):
        if request.method == 'GET':
            code = request.args.get('code')
            vol = request.args.get('vol')
            bbhis_list = db.session.query(BBhistory).filter_by(
                code=str(code)).filter(
                BBhistory.volume >= int(vol) * 100).all()
            date_buy_dict = {}
            date_sell_dict = {}
            for i in bbhis_list:
                date_tmp = str(i.time).split(' ')[0]
                if i.type == u'买盘':
                    if date_tmp in date_buy_dict.keys():
                        date_buy_dict[date_tmp] += (float(i.volume)*float(i.price)) / 10000
                    else:
                        date_buy_dict[date_tmp] = (float(i.volume) * float(i.price)) / 10000
                else:
                    if date_tmp in date_sell_dict.keys():
                        date_sell_dict[date_tmp] += (float(i.volume)*float(i.price)) / 10000
                    else:
                        date_sell_dict[date_tmp] = (float(i.volume) * float(i.price)) / 10000
            date_list = date_buy_dict.keys()
            tmp_list = []
            for i in date_list:
                tmp_dict = {}
                tmp_dict['date'] = i
                tmp_dict['buy'] = date_buy_dict[i]
                tmp_dict['sell'] = date_sell_dict[i]
                tmp_list.append(tmp_dict)
            tmp_list = sorted(tmp_list,key=operator.itemgetter('date'))
            # records = [
            #  {'date': '2010-04-01', 'people': 1047, 'hits': 4522},
            #  {'date': '2010-04-03', 'people': 617, 'hits': 2582},
            #  {'date': '2010-04-02', 'people': 736, 'hits': 3277}
            #  ]
            # records.sort(key=lambda x: x['date'].split('-'))
            date_list = []
            buy_list = []
            sell_list = []
            for i in tmp_list:
                date_list.append(i['date'])
                buy_list.append(i['buy'])
                sell_list.append(i['sell'])
            return render_template(
                '/SingleWork/index.html',
                code = code,
                vol=vol,
                bbhis_list=bbhis_list,
                date_list=date_list,
                buy_list=buy_list,
                sell_list=sell_list)

class BBTimeView(View):
    methods = ['GET','POST']

    def dispatch_request(self):
        if request.method == 'GET':
            code = request.args.get('code')
            bills = db.session.query(WholeBig).filter_by(code=code).order_by(WholeBig.date).all()
            date_list = []
            amount_buy = []
            amount_buy_50 = []
            amount_buy_100 = []
            amount_buy_200 = []
            amount_buy_400 = []
            amount_sell = []
            amount_sell_50 = []
            amount_sell_100 = []
            amount_sell_200 = []
            amount_sell_400 = []

            for i in bills:
                print 'type=====',i.type,type(i.type)
                date_str = str(i.date).split(' ')[0]
                if date_str not in date_list:
                    date_list.append(date_str)
                if i.type == u'买盘':
                    print '111'
                    amount_buy.append(float(i.amount))
                    amount_buy_50.append(float(i.amount_50))
                    amount_buy_100.append(float(i.amount_100))
                    amount_buy_200.append(float(i.amount_200))
                    amount_buy_400.append(float(i.amount_400))
                elif i.type == u'卖盘':
                    print '2222'
                    amount_sell.append(float(i.amount)*(-1))
                    amount_sell_50.append(float(i.amount_50)*(-1))
                    amount_sell_100.append(float(i.amount_100)*(-1))
                    amount_sell_200.append(float(i.amount_200)*(-1))
                    amount_sell_400.append(float(i.amount_400)*(-1))

            print 'amount',amount_buy,amount_sell
            return render_template(
                '/SingleWork/bb_time.html',
                date_list=date_list,
                amount_buy = amount_buy,
                amount_buy_50 = amount_buy_50,
                amount_buy_100 = amount_buy_100,
                amount_buy_200 = amount_buy_200,
                amount_buy_400 = amount_buy_400,
                amount_sell = amount_sell,
                amount_sell_50 = amount_sell_50,
                amount_sell_100 = amount_sell_100,
                amount_sell_200 = amount_sell_200,
                amount_sell_400 = amount_sell_400,

            )

