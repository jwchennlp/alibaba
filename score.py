#!/user/bin/env python 
#coding:utf-8

import pandas as pd
import numpy as np
from pandas import *
import func 
import cal_sim,cal_rec,handle_rec
import pickle

if __name__=="__main__":
    
    data=pd.read_csv('./data/train.csv')
    user_id=pickle.load(open('./data/user_id','rb'))
    item_id=pickle.load(open('./data/item_id','rb'))
    #获取训练数据
    train_click=func.get_train(data,0)
    train_buy=func.get_train(data,1)
    train_collect=func.get_train(data,2)
    train_cart=func.get_train(data,3)
    
    #获取测试数据
    test_click=func.get_test(data,0)
    test_buy=func.get_test(data,1)
    test_collect=func.get_test(data,2)
    test_cart=func.get_test(data,3)
    
    #获取用户-物品表
    click_user_item=func.get_user_item_dic(train_click,user_id)
    buy_user_item=func.get_user_item_dic(train_buy,user_id)
    collect_user_item=func.get_user_item_dic(train_collect,user_id)
    cart_user_item=func.get_user_item_dic(train_cart,user_id)

    #获取物品-用户表
    click_item_user=func.get_item_user_dic(train_click,item_id)
    buy_item_user=func.get_item_user_dic(train_buy,item_id)
    collect_item_user=func.get_item_user_dic(train_collect,item_id)
    cart_item_user=func.get_item_user_dic(train_cart,item_id)
    
    #获取用户行为的物品数(里面计算的是数的平方和)
    click_user_item_count=func.get_user_item_count(click_user_item,user_id)
    buy_user_item_count=func.get_user_item_count(buy_user_item,user_id)
    collect_user_item_count=func.get_user_item_count(collect_user_item,user_id)
    cart_user_item_count=func.get_user_item_count(cart_user_item,user_id)
    

    #在这里要设置的参数是weight
    weight=[1,0,0,0]

    similarity=cal_sim.cal_sim(buy_item_user,click_item_user,collect_item_user,cart_item_user,buy_user_item_count,click_user_item_count,collect_user_item_count,cart_user_item_count,weight,user_id)

    #计算推荐列表,参数是设定取与用户相似的用户值，K
    k=10
    weight_rec=[1,0,0,0]
    rec_user_item=cal_rec.cal_rec(similarity,buy_user_item,click_user_item,collect_user_item,cart_user_item,weight_rec,user_id,k)
    
    #对于推荐列表，要进行一下处理，因为每个用户推荐的物品数不相同，一个物品推荐给用户的概率也不一样
    #处事设定为每个用户推荐10个物品
    item_numer=5
    result=handle_rec.handle_rec(rec_user_item,item_numer,user_id)
    
    #检验一下,查看准确率和召回率，以及F1值
    test_user_item=func.get_user_item_dic(test_buy,user_id)
    precision,recall,hitbrand,pbrand,bbrand=func.cal_result(result,test_user_item,rec_user_item)
    
    print '权重参数为(点击，购买，收藏，购物车)',weight
    print '推荐物品的权重(点击，购买，收藏，购物车)',weight_rec
    print '相似用户参数为(k)',k
    print '每个用户推荐物品为',item_numer
    print 'hitbrand',hitbrand,'pbrand',pbrand,'bbrand',bbrand
    print 'precision',precision,'recall',recall,'F_1',2*precision*recall/(precision+recall)
