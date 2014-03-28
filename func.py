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

#处理数据
def process_data():
    data=pd.read_csv('./data/train.csv')
    data=data.dorp_duplicates(cols=['user_id','brand_id','type'])
    data=data['user_id','brand_id','type','month','day']
    #将数据切割成训练集和测试集
    train,test=divide_data(data)
    train = np.array(train)
    test = np.array(test)
    data=np.array(data)
    
    user_id=pickle.load(open('./data/user_id','rb'))
    
    trainUI = construct_vector(train,user_id)
    testUI = construct_vector(test,user_id)
    data = construct_vector(data,user_id)
    
    sim_train = cal_sim(trainUI,user_id)
    sim_data = cal_sim(data,user_id)

    write(trainUI,'trainUI')
    write(testUI,'testUI')
    write(data,'data')
    write(sim_train,'sim_train')
    write(sim_data,'sim_data')

#写入数据
def write(dic,filename):
    f=open(filename,'wb')
    pickle.dump(dic,f)
    f.close()

#将数据切分成训练集和测试集两部分
def divide_data(data):
    a=data.month==7
    b=data.day<=15
    c=data.month<7
    train=data[(a&b)|c]
    
    d=data.day>15
    e=data.month=8
    test=data[(b&d)|e]
    return (train,test)

#对数据建立用户物品的向量
def construct_vector(data,user_id):
    UIvector = {}
    for user in user_id:
        UIvector[user] = {}
    for i in range(len(data)):
        if data[i][1] not in UIvector[data[i][1]].keys():
            UIvector[data[i][0]][data[i][1]] = item_weight(data[i][2])
        else :
            UIvector[data[i][0]][data[i][1]] = max(UIvector[data[i][0]][data[i][1]],item_weight(data[i][2]))
    return UIvector

#计算用户之间的相似度
def cal_sim(user_item,user_id):
    sim={}
    for user in user_id:
        sim[user]={}
        for user_j in user_item.keys():
            if user == user_j:
                continue
            else:
                sim[user][user_j] = cal(user_item[user],user_item[user_j])
    return sim

#通过向量计算两个用户之间的相似度
def cal(u1,u2):
    #计算一个用户向量的长度
    l1=cal_length(u1)
    l2=cal_length(u2)
    count = 0
    for i1 in u1.keys():
        if i1 in u2.keys():
            count += u1[i1]*u2[i1]
    if l1 ==0 or l2 ==0:
        return 0
    else:
        return count/l1*l2
#计算一个用户向量的长度
def  cal_length(u):
    value = u.values():
    length = 0
    for v in value:
        length += math.pow(v,2)
    length = math.sqrt(length)
    return length

#在建立用户-物品的向量过程中，行为权重赋值(点击,购买，收藏，购物车对应数值为1,4,2,3)
def item_weight(k):
    if k == 0:
        return 1
    elif k == 1:
        return 4
    elif k == 2:
        return 2:
    else:
        return 3
