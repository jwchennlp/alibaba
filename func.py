#!/usr/bin/env python 
#coding:utf-8

import pandas as pd 
import numpy as np
from pandas import *
import pickle
import math
'''
功能模块的实现
'''


#将数据切分成训练集
def get_train(data,shop_behavior):
    
    #训练集为4.15-7.15的数据，有四种购买行为
    a=data.month==7
    b=data.day<=15
    train_month_7=data[['user_id','brand_id']][a&b][data.type==shop_behavior]
    train_month_less_7=data[['user_id','brand_id']][data.month<7][data.type==shop_behavior]

    train=np.array(train_month_7.append(train_month_less_7))

    return train

#获取训练集数据
def get_test(data,shop_behavior):
    #测试集数据为7.15-8.15的数据，有四种购买行为
    a=data.month==7
    b=data.day>15
    test_month_7=data[['user_id','brand_id']][a&b][data.type==shop_behavior]
    test_month_8=data[['user_id','brand_id']][data.month==8][data.type==shop_behavior]
    
    test=np.array(test_month_7.append(test_month_8))

    return test

#获取全部数据
def get_data(data,shop_behavior):
    #获取全部数据
    train=np.array(data[['user_id','brand_id']][data.type==shop_behavior])
    return train


#获取用户-物品表:
def get_user_item_dic(train,user_id):
    user_item={}
    for user in user_id.keys():
        user_item[user]={}
    for i in range(len(train)):
        if train[i][1] in user_item[train[i][0]].keys():
            user_item[train[i][0]][train[i][1]] += 1
        else:
            user_item[train[i][0]][train[i][1]] = 1
    return user_item

#获取物品-用户表：
def get_item_user_dic(train,item_id):
    item_user={}
    for item in item_id.keys():
        item_user[item]={}
    for i in range(len(train)):
        if train[i][0] in item_user[train[i][1]].keys():
            item_user[train[i][1]][train[i][0]] += 1
        else:
            item_user[train[i][1]][train[i][0]] =1
    return item_user

#获取每个用户行为的物品数
def get_user_item_count(user_item,user_id):
    user_item_count={}
    for user in user_id.keys():
        user_item_count[user]=0
    for user in user_item.keys():
        for item in user_item[user].keys():
            user_item_count[user] += math.pow(user_item[user][item],2)
    return user_item_count
            
#计算准确率和召回率
def cal_result(result,test_user_item,rec_user_item):
    hit_user_item=cal_hit_user_item(result,test_user_item,rec_user_item)
    precision,hitbrand,pbrand=cal_precison(hit_user_item,result)
    recall,bbrand=cal_recall(hit_user_item,test_user_item)
    
    return (precision,recall,hitbrand,pbrand,bbrand)


def cal_hit_user_item(result,test_user_item,rec_user_item):
    #保存下结果
    f=open('./data/hit_user_item.csv','wb')
    f.write('%s,%s,%s\n'%('用户','物品','概率'))
    hit_user_item={}
    for user in result.keys():
        hit_user_item[user] = 0
        for item in result[user].keys():
            if item in test_user_item[user].keys():
                hit_user_item[user] += 1
                f.write('%s,%s,%s\n'%(user,item,rec_user_item[user][item]))
    f.close()
    return hit_user_item
                
def  cal_precison(hit_user_item,result):
    hitbrand=0
    pbrand=0
    for user in hit_user_item.keys():
        hitbrand += hit_user_item[user]
        pbrand += len(result[user])
    return (float(hitbrand)/float(pbrand),hitbrand,pbrand)

def cal_recall(hit_user_item,test_user_item):
    hitbrand=0
    bbrand=0
    for user in hit_user_item.keys():
        hitbrand += hit_user_item[user]
        for item in test_user_item[user].keys():
            bbrand += test_user_item[user][item]
    return (float(hitbrand)/float(bbrand),bbrand)
