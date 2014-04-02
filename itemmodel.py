#!/usr/bin/env python
#coding:utf-8

import func

'''
对物品进行统计，将时间因素考虑进去，建立物品-时间词典，主要用于分析物品的行为随时间的变化,从而决定这一物品的时间衰减因子
'''
def build_item_time(data,item_id):
    item_time = {}
    for item in item_id.keys():
        item_time[item] = {}
    for i in range(len(data)):
        user,item,types,month,day = data[i]
        time = func.convert_date_day(month,day)
        if time not in item_time[item].keys():
            item_time[item][time] = [0,0,0,0]
            item_time[item][time] = func.add_behavior(item_time[item][time],types)
        else:
            item_time[item][time] = func.add_behavior(item_time[item][time],types)
    return item_time
#对不同类型的商品赋予不同的时间衰减因子
def cal_item_time_factor(item_time):
    item_factor = {}
    K = 5
    for item in item_time.keys():
        if len(item_time[item])<=5:
            item_factor[item] = 10
        else:
            item_factor[item] = K*len(item_time[item])
    return item_factor
