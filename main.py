#!user/bin/env python 
#coding:utf-8

import pandas as pd
import numpy as np
from pandas import *
import func,usermodel,itemmodel

'''
在这里主要实现主函数功能，如相似度的计算，推荐物品
所有的这些功能都应该调用其余模块实现
'''
def fun1():
    data = pd.read_csv('./data/train.csv')
    data = data[['user_id','brand_id','type','month','day']]
    data = np.array(data)
    user_id = func.read('user_id')
    user_time_item = func.build_user_time_item(data,user_id)
    func.write(user_time_item,'user_time_item')

def func2():
    data = pd.read_csv('./data/train.csv')
    data = data[['user_id','brand_id','type','month','day']]
    data = np.array(data)
    user_id = func.read('user_id')
    item_id = func.read('item_id')

    user_item_time = func.build_user_item_time(data,user_id)
    item_time = itemmodel.build_item_time(data,item_id)
    item_factor = itemmodel.cal_item_time_factor(item_time)
    func.write(user_item_time,'user_item_time')
    func.write(item_time,'item_time')
    return (user_item_time,item_time,item_factor)
#将数据划分成训练集和测试集
def func3():
    train,test = func.divide_data()
    user_id =  func.read('user_id')
    item_id = func.read('item_id')
    train_u_i_t = func.build_user_item_time(train,user_id)
    #建立测试集的用户-物品词典，这里不需要时间序列
    test_u_i  = func.build_user_item(test,user_id)
    #建立训练集的物品-时间词典
    train_item_time = itemmodel.build_item_time(train,item_id)
    #建立物品的时间衰减因子
    item_factor = itemmodel.cal_item_time_factor(train_item_time)

    func.write(train_u_i_t,'train_user_item_time')
    func.write(test_u_i,'test_user_item')
    func.write(train_item_time,'train_item_time')
    return (train_u_i_t,test_u_i,train_item_time,item_factor)

#交叉验证
def cross_valation(K,train_u_i_t,test_u_i,item_time,item_factor):
    day_count = 91
    #获取训练集的推荐列表
    M=3.5
    rec_user_item = usermodel.build_user_model(train_u_i_t,item_factor,day_count)
    
    #在这里进行一次测试，对用户的推荐列表，只推荐值大于某一限定的物品
    rec_user_item,former_rec = func.set_min_M(rec_user_item,M)
    #需要对推荐列表进行处理，对每个用户设定推荐的物品的个数,K为设定的物品的个数
    rec_user_item = func.set_rec_item_num(rec_user_item,K)
    #接下来想做的处理是，对冷启动用户，给其添加浏览过的热门商品（效果不好）
    #rec_user_item = func.cal_cold_start(rec_user_item,former_rec,item_time)
    #查看分布
    func.check_distribuction(rec_user_item)
    #计算准确率，召回率，F值等参数
    hit_user_item = func.cal_hit_user_item(rec_user_item,test_u_i) 
    precision,recall,F,hitbrand,pbrand,bbrand = func.cal_result(rec_user_item,test_u_i,hit_user_item)
    
    func.write(rec_user_item,'train_rec_user_item')
    func.write(hit_user_item,'hit_user_item')
    
    print '限定对每个用户推荐的物品数为:',K
    print 'hitbrand',hitbrand,'pbrand',pbrand,'precision',precision
    print 'hitbrand',hitbrand,'bbrand',bbrand,'recall',recall
    print 'F',F

def train():
    train_u_i_t,test_u_i,item_time,item_factor = func3()
    Klist = [20]
    for K in Klist:
        cross_valation(K,train_u_i_t,test_u_i,item_time,item_factor)
    
    
def func4():
    user_item_time,item_time,item_factor = func2()
    K = 20
    M=4
    day_count = 123
    
    rec_user_item = usermodel.build_user_model(user_item_time,item_factor,day_count)
    rec_user_item,former_rec = func.set_min_M(rec_user_item,M)
    rec_user_item = func.set_rec_item_num(rec_user_item,K)
    #查看为用户推荐物品的个数分布,对有那些推荐物品个数小于等于3的用户给其推荐热门商品
    #查看分布
    func.check_distribuction(rec_user_item)
    #rec_user_item=func.distribution(rec_user_item)
    func.write(rec_user_item,'rec_user_item')
    
    func.getresult(rec_user_item)

    

if __name__=="__main__":
    func4()
    
    
    
