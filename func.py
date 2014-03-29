#!/usr/bin/env python
#coding:utf-8

import pandas as pd
import numpy as np
from pandas import *
import pickle

'''
对用户行为进行建模，将时间因素考虑进去，建立用户-时间-物品行为词典
'''
def build_user_time_item(data,user_id):
    user_time_item = {}
    for user in user_id.keys():
        user_time_item[user] = {}
    for i in range(len(data)):
        user,item,types,month,day = data[i]
        time = convert_date_day(month,day)
        #如果某日期的购买行为没有出现在用户词典中，则需要先将日期加入词典中
        if time not in user_time_item[user].keys():
            user_time_item[user][time] = {}
            #用户的行为[0,0,0,0]分别表示某用户在某天的点击，购买，收藏，购物车四种行为的次数
            user_time_item[user][time][item] = [0,0,0,0]
            user_time_item[user][time][item] = add_behavior(user_time_item[user][time][item],types)
        else:
            if item in user_time_item[user][time].keys():
                user_time_item[user][time][item] = add_behavior(user_time_item[user][time][item],types)
            else:
                #如果用户的行为没有出现在用户-时间词典中，则需要做以下处理
                user_time_item[user][time][item] = [0,0,0,0]
                user_time_item[user][time][item] = add_behavior(user_time_item[user][time][item],types)
    return user_time_item
                 
#对用户行为进行建模，将时间因素考虑进去，建立用户-物品行为-时间词典
def build_user_item_time(data,user_id):
    user_item_time = {}
    for user in user_id.keys():
        user_item_time[user] = {}
    for i in range(len(data)):
        user,item,types,month,day = data[i]
        time = convert_date_day(month,day)
        if item not in user_item_time[user].keys():
            user_item_time[user][item] = {}
            #用户在某一天对某个物品的行为初始设定都为0
            user_item_time[user][item][time] = [0,0,0,0]
            user_item_time[user][item][time] = add_behavior(user_item_time[user][item][time],types)
        else:
            if time in user_item_time[user][item].keys():
                user_item_time[user][item][time] = add_behavior(user_item_time[user][item][time],types)
            else:
                user_item_time[user][item][time] = [0,0,0,0]
                user_item_time[user][item][time] = add_behavior(user_item_time[user][item][time],types)
    return user_item_time
#将日期格式直接以日来进行度量
def convert_date_day(month,day):
    m={4:0,5:30,6:61,7:91,8:122}
    return m[month]+day-14
#添加行为
def add_behavior(behavior,types):
    behavior[types] += 1
    return behavior
    

def write(dic,file_name):
    pickle.dump(dic,open('./data/'+file_name,'wb'))
def read(file_name):
    dic = pickle.load(open('./data/'+file_name,'rb'))
    return dic

#将数据划分成训练集和测试集
def divide_data():
    data = pd.read_csv('./data/train.csv')
    data = data[['user_id','brand_id','type','month','day']]
    
    a=data.month==7
    b=data.day<=15
    c=data.month<7
    train=data[(a&b)|c]
    train = np.array(train)
    
    a=data.month==7
    d=data.day>15
    e=data.month==8
    test=data[(a&d)|e]
    test = np.array(test)
    return (train,test)

#建立测试集的用户-物品模型
def build_user_item(test,user_id):
    user_item = {}
    for user in user_id:
        user_item[user] = {}
    for i in range(len(test)):
        user,item,types,month,day = test[i]
        if item not in user_item[user].keys():
            user_item[user][item] = [0,0,0,0]
            user_item[user][item] = add_behavior(user_item[user][item],types)
        else:
            user_item[user][item] = add_behavior(user_item[user][item],types)
    return user_item
     
#对推荐列表进行处理，对每个用户设定推荐的物品的个数，K为设定的物品的个数
def set_rec_item_num(rec_user_item,k,M):
    '''
    此处进行修改，主要进行如下操作，查看对每个用户推荐物品的概率，如果推荐的物品推荐值大于1的物品大于5个，这直接取5个，如果推荐的物品的推荐值大于1的物品不足五个，则推荐推荐值大于1的物品
    '''
    #用户推荐物品序列大于1的物品个数词典
    rec_item_big_1 = {}
    #主要实现的功能是统计对每个用户的推荐列表中，推荐值大于M的物品的个数
    for user in rec_user_item.keys():
        count = 0 
        rec_values = sorted(rec_user_item[user].values(),reverse = True)
        for value in rec_values:
            if value > M:
                count += 1
            else:
                break
        rec_item_big_1[user] = count 

    user_item = {}
    for user in rec_user_item.keys():
        user_item[user] = {}
        #首先当对用户的推荐物品长度大于K时
        if len(rec_user_item[user]) > k:
            #当对间的物品列表中对物品推荐值大于M的物品的个数
            if rec_item_big_1[user] >= k:
                items = sorted(rec_user_item[user],key = rec_user_item[user].get,reverse = True)
                items = items[0:k]
                for item in items:
                    user_item[user][item] = rec_user_item[user][item]
            else:
                items = sorted(rec_user_item[user],key = rec_user_item[user].get,reverse = True)
                #此处做了一下处理，当推荐值小于限定最小推荐值M的个数小雨K个时，会额外推荐一个物品概率小于M值的物品
                items = items[0:rec_item_big_1[user]+1]
                for item  in items:
                    user_item[user][item] = rec_user_item[user][item]
        #当对用户体检物品的长度小于K时
        else:
            items = sorted(rec_user_item[user],key = rec_user_item[user].get,reverse = True)
            items = items[0:rec_item_big_1[user]+1]
            for item in items:
                user_item[user][item] = rec_user_item[user][item]
    return user_item

#计算准确率，召回率，F值等参数
def cal_hit_user_item(rec_user_item,test_u_i):
    hit_user_item = {}
    for user in rec_user_item.keys():
        hit_user_item[user] = {}
        for item in rec_user_item[user].keys():
            if item in test_u_i[user].keys() and test_u_i[user][item][1] > 0 :
                hit_user_item[user][item] = rec_user_item[user][item]
    return hit_user_item

def cal_result(rec_user_item,test_u_i,hit_user_item):
    hitbrand = 0
    pbrand = 0
    bbrand = 0
    for user in rec_user_item.keys():
        hitbrand += len(hit_user_item[user])
        pbrand += len(rec_user_item[user])
        for item in test_u_i[user].keys():
            bbrand += test_u_i[user][item][1]
    precision = hitbrand/float(pbrand)
    recall = hitbrand/float(bbrand)
    F = 2*precision*recall/(precision+recall)
    precision = str(precision*100)+'%'
    recall = str(recall*100)+'%'
    F = str(F*100)+'%'
    return (precision,recall,F,hitbrand,pbrand,bbrand)
        
#查看为用户推荐物品的个数分布
def distribution(rec_user_item):
    items = [7868,2683,11196,8869,14020]
    for user in rec_user_item.keys():
        if len(rec_user_item[user]) <5:
            count = 5-len(rec_user_item[user])
            for i in range(count):
                rec_user_item[user][items[i]] = 'add'
    return rec_user_item
#查看推荐的物品的分布情况
def look_distribuction(rec_user_item,K):
    dis = {}
    for i in range(0,K+1):
        dis[i] = 0
    for user in rec_user_item.keys():
        dis[len(rec_user_item[user])] += 1
    print dis

def getresult(rec_user_item):
    #对于那些推荐物品为0的用户，主要是只存在购买行为，没有点击行为
    rec_user_item[8327250][14917] = 'add'
    rec_user_item[6458000][1681] = 'add'
    rec_user_item[3001000][21995] = 'add'
    rec_user_item[12027000][2322] = 'add'
    rec_user_item[4054000][11304] = 'add'
    rec_user_item[9035750][7868] = 'add'
    f=open('./data/result.txt','wb')
    rec={}
    for user in rec_user_item.keys():
        rec[user] = []
        for item in rec_user_item[user].keys():
            rec[user].append(str(int(item)))
    for user in rec.keys():
        f.write('%s\t%s\n'%(user,','.join(rec[user])))
    f.close()
