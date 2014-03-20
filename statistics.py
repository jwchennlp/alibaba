#!/usr/bin/env python
#coding:utf-8

import pickle
import numpy as np
import pandas as pd
from pandas import *
import func
import csv


'''
现在我想做一个统计，查看每个用户的行为中，购买，点击和收藏的行为的个数
'''
def make_sta(click_user_item,buy_user_item,collect_user_item,cart_user_item,user_id):
    behavior={}
    for user in user_id:
        behavior[user]={}
        for i in range(4):
            behavior[user][i] = 0
    behavior = add(behavior,buy_user_item,1)
    behavior = add(behavior,click_user_item,0)
    behavior = add(behavior,collect_user_item,2)
    behavior = add(behavior,cart_user_item,3)
    
    write(behavior)
    

def add(behavior,dic,k):
    for user in dic.keys():
        for item in dic[user].keys():
            if k in behavior[user].keys():
                behavior[user][k] += dic[user][item]
            else:
                behavior[user][k] = dic[user][item]
    return behavior

def write(behavior):
    f=open('./data/behavior.csv','wb')
    f.write('%s\n'%('user,click,buy,collect,cart'))
    for user in behavior.keys():
        values=behavior[user].values()
        f.write('%s,%d,%d,%d,%d\n'%( user,values[0],values[1],values[2],values[3]))
    f.close()

if __name__=="__main__":
    data=pd.read_csv('./data/train.csv')
    user_id=pickle.load(open('./data/user_id','rb'))
    item_id=pickle.load(open('./data/item_id','rb'))
    
    train_click=func.get_data(data,0)
    train_buy=func.get_data(data,1)
    train_collect=func.get_data(data,2)
    train_cart=func.get_data(data,3)
    
    click_user_item=func.get_user_item_dic(train_click,user_id)
    buy_user_item=func.get_user_item_dic(train_buy,user_id)
    collect_user_item=func.get_user_item_dic(train_collect,user_id)
    cart_user_item=func.get_user_item_dic(train_cart,user_id)
    
    make_sta(click_user_item,buy_user_item,collect_user_item,cart_user_item,user_id)
