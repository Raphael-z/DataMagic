# coding:utf8
import tushare as ts
import string,threading,time
import json
from flask import request,render_template
from flask_restful import Resource


from app_info import db
from models import SMEList,GEMList,WholeList,WholeUpDown,WholeResourceData,WholeBig


class GetAllBills(Resource):

    def get(self):
        # sme_list = ts.get_sme_classified()
        # for i in range(0,len(sme_list)):
        #     code = sme_list.code[i]
        #     name = sme_list.name[i]
        #     sme_item = SMEList(code=code,name=name)
        #     db.session.add(sme_item)
        # gem_list = ts.get_gem_classified()
        # for i in range(0,len(gem_list)):
        #     code = gem_list.code[i]
        #     name = gem_list.name[i]
        #     gem_item = GEMList(code=code,name=name)
        #     db.session.add(gem_item)
        # db.session.commit()
        # whole_list = ts.get_area_classified()
        # for i in range(0,len(whole_list)):
        #     code = whole_list.code[i]
        #     name = whole_list.name[i]
        #     area = whole_list.area[i]
        #     whole_item = WholeList(code=code,name=name,area=area)
        #     db.session.add(whole_item)
        # db.session.commit()
        industry_list = ts.get_concept_classified()
        num = 1
        for i in range(0,len(industry_list)):
            num += 1
            print 'num'
            code = industry_list.code[i]
            c_name = industry_list.c_name[i]
            ticket = db.session.query(WholeList).filter_by(code=str(code)).first()
            if ticket:
                ticket.c_name = c_name
            db.session.commit()
        return {'msg':"完成"},200

def release_data(p_change_list,con,code_num):

    if code_num == 0:
        if p_change_list[0] > 0:
            final_data = 1
            return con,final_data
        else:
            final_data = 0
            return con,final_data
    else:
        if p_change_list[code_num] > 0:
            con += '1'
            return release_data(p_change_list,con,code_num-1)
        else:
            con += '0'
            return release_data(p_change_list,con,code_num-1)

def thread_func(result_list,code_list,count_num,end_date):
    num = 0
    for i in code_list:
        print 'start...'+i +'num...'+str(num)
        num+=1
        condition_dict = {'con':'','final':0}
        item_datas = ts.get_hist_data(str(i), end=end_date)
        try:
            if not item_datas.empty:
                con = ''
                p_change_list = item_datas.p_change
                con,final_data = release_data(p_change_list,con,count_num)
                condition_dict['final'] = final_data
                condition_dict['con'] = con
                # whole_updown_item = WholeUpDown(code=i,rule=condition_dict['con']+str(condition_dict['final']))
                # db.session.add(whole_updown_item)
                # db.session.commit()
        except:
            continue
        print 'result_list_num=====',len(result_list)
        result_list.append(condition_dict)
def test_condition(code_list,end_date):
    page_size = 50
    page_num = []
    for i in range(1,3385/50):
        page_num.append(int(i))
    result_list = []
    threads = []
    count_num = 4
    for i in page_num:
        c_list = code_list[(int(i) - 1) * int(page_size):int(page_size) * int(i)]
        threads.append(threading.Thread(target=thread_func, args=(result_list,c_list,count_num,end_date)))
    # threads.append(threading.Thread(target=thread_func, args=(result_list,code_list,count_num,end_date)))
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    result_up_dict = {}
    result_down_dict = {}

    for i in result_list:
        if i['final'] == 1:
            if i['con'] in result_up_dict.keys():
                result_up_dict[i['con']] += 1
            else:
                result_up_dict[i['con']] = 1
        elif i['final'] == 0:
            if i['con'] in result_down_dict.keys():
                result_down_dict[i['con']] += 1
            else:
                result_down_dict[i['con']] = 1
    up_prop = {}
    for i in result_up_dict.keys():
        print 'i===========',i,result_up_dict[i],result_down_dict[i]
        up_prop[str(i)] =  round(float(result_up_dict[i])/(float(result_up_dict[i])+float(result_down_dict[i])),4) * 100
    result = {'date':end_date,'up':result_up_dict,'down':result_down_dict,'up_prop':up_prop}
    result_json = json.dumps(result)
    fileobj = open('./updown.json','a+')
    fileobj.write(result_json)
    fileobj.close()
    return {'up':result_up_dict,'down':result_down_dict,'up_prop':up_prop}
class TestRule(Resource):
    def get(self):
        end_date = request.args.get('end_date')
        whole_list = db.session.query(WholeList).all()
        code_list = []
        for i in whole_list:
            code_list.append(i.code)
        result_dict = test_condition(code_list,str(end_date))
        x_data = result_dict['up_prop'].keys()
        y_data =  result_dict['up_prop'].values()
        return result_dict,200



#获取全部最近10天的交易数据

def init_each(error_list,result_list,code_list,count_num,start_date,end_date):
    num = 0
    for i in code_list:
        print 'start...'+i +'num...'+str(num)
        num+=1
        item_datas = ts.get_hist_data(str(i), start=start_date,end=end_date)
        try:
            if not item_datas.empty:
                con = ''
                p_change_list = item_datas.p_change
                for j in range(0,len(item_datas)):
                    code = i
                    date = str(item_datas.index[j])
                    open = item_datas.open[j]
                    high = item_datas.high[j]
                    close = item_datas.close[j]
                    low = item_datas.low[j]
                    volume = item_datas.volume[j]
                    price_change = item_datas.price_change[j]
                    p_change = item_datas.p_change[j]
                    ma5 = item_datas.ma5[j]
                    ma10 = item_datas.ma10[j]
                    ma20 = item_datas.ma20[j]
                    v_ma5 = item_datas.v_ma5[j]
                    v_ma10 = item_datas.v_ma10[j]
                    v_ma20 = item_datas.v_ma20[j]
                    turnover = item_datas.turnover[j] if item_datas.turnover[j] else ''
                    whole_resource = WholeResourceData(
                        code=code,
                        date=date,
                        open=open,
                        high=high,
                        close=close,
                        low=low,
                        volume=volume,
                        price_change=price_change,
                        p_change=p_change,
                        ma5=ma5,
                        ma10=ma10,
                        ma20=ma20,
                        v_ma5=v_ma5,
                        v_ma10=v_ma10,
                        v_ma20=v_ma20,
                        turnover=turnover,
                    )
                    db.session.add(whole_resource)
                    db.session.commit()

        except Exception as e:
            print 'e===',e
            error_list.append(i)
            continue
        print 'result_list_num=====',len(result_list)
        result_list.append(i)

def get_s_data(code_list,start_date,end_date):
    page_size = 25
    page_num = []
    for i in range(1,3385/25):
        page_num.append(int(i))
    result_list = []
    error_list = []
    threads = []
    count_num = 4
    for i in page_num:
        c_list = code_list[(int(i) - 1) * int(page_size):int(page_size) * int(i)]
        threads.append(threading.Thread(target=init_each, args=(error_list,result_list,c_list,count_num,start_date,end_date)))
    # threads.append(threading.Thread(target=init_each, args=(error_list,result_list,code_list,count_num,start_date,end_date)))
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return result_list,error_list

class  GetSourceData(Resource):
    def get(self):
        whole_list = db.session.query(WholeList).all()
        code_list = []
        for i in whole_list:
            code_list.append(i.code)
        # code_list = ['002797']
        suc_list,error_list = get_s_data(code_list,'2017-09-22','2017-09-22')
        result = {'suc':suc_list,'error':error_list}
        result_json = json.dumps(result)
        fileobj = open('./resource.json','w+')
        fileobj.write(result_json)
        fileobj.close()
        return '完成',200


def get_each_big(error_list,result_list,c_list,date_list):
    num = 0
    for i in c_list:
        print 'start...'+i +'num...'+str(num)
        num+=1
        for j in date_list:
            item_datas = ts.get_tick_data(str(i),date=str(j),src='tt')
            try:
                if not item_datas.empty:
                    con = ''
                    amount_buy = 0
                    amount_50_buy = 0
                    amount_100_buy = 0
                    amount_200_buy = 0
                    amount_400_buy = 0
                    amount_sell = 0
                    amount_50_sell = 0
                    amount_100_sell = 0
                    amount_200_sell = 0
                    amount_400_sell = 0
                    code = i
                    date = str(j)
                    for k in range(0,len(item_datas)):
                        if int(item_datas.amount[k]) < 500000:
                            if item_datas.type[k] == '买盘':
                                amount_buy += item_datas.amount[k]
                            elif item_datas.type[k] == '卖盘':
                                amount_sell += item_datas.amount[k]
                        elif int(item_datas.amount[k]) >= 500000 and int(item_datas.amount[k]) <1000000:
                            if item_datas.type[k] == '买盘':
                                amount_50_buy += item_datas.amount[k]
                            elif item_datas.type[k] == '卖盘':
                                amount_50_sell += item_datas.amount[k]
                        elif int(item_datas.amount[k]) >= 1000000 and int(item_datas.amount[k]) < 2000000:
                            if item_datas.type[k] == '买盘':
                                amount_100_buy += item_datas.amount[k]
                            elif item_datas.type[k] == '卖盘':
                                amount_100_sell += item_datas.amount[k]
                        elif int(item_datas.amount[k]) >= 2000000 and int(item_datas.amount[k]) < 4000000:
                            if item_datas.type[k] == '买盘':
                                amount_200_buy += item_datas.amount[k]
                            elif item_datas.type[k] == '卖盘':
                                amount_200_sell += item_datas.amount[k]
                        else:
                            if item_datas.type[k] == '买盘':
                                amount_400_buy += item_datas.amount[k]
                            elif item_datas.type[k] == '卖盘':
                                amount_400_sell += item_datas.amount[k]
                    whole_big1 = WholeBig(
                        code=code,
                        date=date,
                        type='买盘',
                        amount=round(float(amount_buy)/10000,2),
                        amount_50=round(float(amount_50_buy)/10000,2),
                        amount_100=round(float(amount_100_buy)/10000,2),
                        amount_200=round(float(amount_200_buy)/10000,2),
                        amount_400=round(float(amount_400_buy)/10000,2),
                    )
                    whole_big2 = WholeBig(
                        code=code,
                        date=date,
                        type='卖盘',
                        amount=round(float(amount_sell)/10000,2),
                        amount_50=round(float(amount_50_sell)/10000,2),
                        amount_100=round(float(amount_100_sell)/10000,2),
                        amount_200=round(float(amount_200_sell)/10000,2),
                        amount_400=round(float(amount_400_sell)/10000,2),
                    )
                    db.session.add(whole_big1)
                    db.session.add(whole_big2)
                    db.session.commit()
            except Exception as e:
                print 'e===',e
                error_list.append(i)
                continue
            print 'result_list_num=====',len(result_list)
        result_list.append(i)
def get_big_data(code_list,date_list):
    page_size = 50
    page_num = []
    for i in range(1,3385/50):
        page_num.append(int(i))
    result_list = []
    error_list = []
    threads = []
    for i in page_num:
        c_list = code_list[(int(i) - 1) * int(page_size):int(page_size) * int(i)]
        threads.append(threading.Thread(target=get_each_big, args=(error_list,result_list,c_list,date_list)))
    # threads.append(threading.Thread(target=get_each_big, args=(error_list,result_list,code_list,date_list)))
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return result_list,error_list

class GetSourceBig(Resource):
    def get(self):
        whole_list = db.session.query(WholeList).all()
        code_list = []
        for i in whole_list:
            code_list.append(i.code)
        # code_list = ['002797']
        date_list = ['2017-09-22']
        suc_list,error_list = get_big_data(code_list,date_list)
        result = {'suc':suc_list,'error':error_list}
        result_json = json.dumps(result)
        fileobj = open('./bigbill.json','w+')
        fileobj.write(result_json)
        fileobj.close()
        return '完成',200


