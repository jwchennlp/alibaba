#!user/bin/env python
#coding:utf-8

import math
'''
为每个用户建立一个用户模型，所有的行为都是以品牌为单位
协同过滤算法不适用，对每个用户建立建立，主要在下个月对用户推荐
之前点击过的商品
'''

#建立用户模型
def build_user_model(user_item_time,T,day_count):
    rec_user_item = {}
    for user in user_item_time.keys():
        rec_user_item[user] = {}
        for item in user_item_time[user].keys():
            #首先判断用户时候买过此物品
            temp = is_buy_before(user_item_time[user][item])
            if temp == 0:
                #根据用户之间的行为记录，计算给用户推荐此物品的概率
                rec_user_item[user][item] = cal_pro(user_item_time[user][item],T,day_count)
            else:
                #对于用户购买过得物品，首先将购买之前的序列都删除，再考虑在此时间之后是否存在点击等行为
                record = delete_buy_before(user_item_time[user][item])
                if len(record) > 0:
                    rec_user_item[user][item] = cal_pro(record,T,day_count)
    return rec_user_item

'''
计算给用户推荐物品i的概率，在模型里引入时间衰减因子T,day_count代表的时时间序列的长度
缺点时，没有考虑各行为的差异，在后阶段的调参过程中，需要考虑收藏和购物车行为对结果的影响
'''
def cal_pro(record,T,day_count):
    pro = 0
    for time in record.keys():
        factor = math.exp(-1/float(T)*(day_count-time))
        pro += sum(record[time])*factor
    return pro
        
def is_buy_before(record):
    for time in record.keys():
        if record[time][1] >= 1:
            return 1
    return 0

#删除购买时间点之前的所有行为
def delete_buy_before(record):
    for time in record.keys():
        if record[time][1] == 0:
            del(record[time])
        else:
            del(record[time])
            break
    for time in record.keys():
        del(record[time])
        break
    return record
