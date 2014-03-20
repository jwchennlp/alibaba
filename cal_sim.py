#!/usr/bin/env python 
#coding:utf-8

import numpy as np
import pandas as pd 
import func
import pickle
import math


#计算用户之间的相似度
def cal_sim(buy,click,collect,cart,buy_count,click_count,collect_count,cart_count,weight,user_id):
    #首先计算每个用户的各种行为的总次数
    behavior_count={}
    for user in buy_count.keys():
        behavior_count[user]=buy_count[user]+click_count[user]+collect_count[user]+cart_count[user]
    #计算各种行为的用户之间的交集
    buy_same_item_count=cal_same_item_count(buy,user_id)
    click_same_item_count=cal_same_item_count(click,user_id)
    collect_same_item_count=cal_same_item_count(collect,user_id)
    cart_same_item_count=cal_same_item_count(cart,user_id)

    #将上述四种行为的交集的结果进行累加
    same_item_count=add_same_item_count(buy_same_item_count,click_same_item_count,collect_same_item_count,cart_same_item_count,weight,user_id)
    
    similarity=cal_similarity(same_item_count,behavior_count)
    
    #同时将所得到的信息存储起来
    write(similarity,'similarity')
    write(same_item_count,'same_item_count')
    write(behavior_count,'behavior_count_dic')
    return similarity


#计算用户间购买行为的交集
def cal_same_item_count(item_user,user_id):
    same_item_count={}
    for user in user_id.keys():
        same_item_count[user]={}
    for item in item_user.keys():
        for user_i in item_user[item].keys():
            for user_j in item_user[item].keys():
                if user_i == user_j:
                    continue
                else:
                    if user_j in same_item_count[user_i].keys():
                        same_item_count[user_i][user_j] += item_user[item][user_i]*item_user[item][user_j]
                    else:
                        same_item_count[user_i][user_j] = item_user[item][user_i]*item_user[item][user_j]
    return same_item_count

#四种购买行为交集的累加
def add_same_item_count(buy_same_item_count,click_same_item_count,collect_same_item_count,cart_same_item_count,weight,user_id):
    same_item_count={}
    for user in user_id.keys():
        same_item_count[user]={}
    #将点击行为交集，直接赋值，提高运算
    for user_i in click_same_item_count.keys():
        for user_j in click_same_item_count[user_i].keys():
            if user_j in same_item_count[user_i].keys():
                same_item_count[user_i][user_j] += weight[0]*click_same_item_count[user_i][user_j]
            else:
                same_item_count[user_i][user_j] = weight[0]*click_same_item_count[user_i][user_j]
    for user_i in buy_same_item_count.keys():
        for user_j in buy_same_item_count[user_i].keys():
            if user_j in same_item_count[user_i].keys():
                same_item_count[user_i][user_j] += weight[1]*buy_same_item_count[user_i][user_j]
            else:
                same_item_count[user_i][user_j] = weight[1]*buy_same_item_count[user_i][user_j]
        
    for user_i in collect_same_item_count.keys():
        for user_j in collect_same_item_count[user_i].keys():
            if user_j in same_item_count[user_i].keys():
                same_item_count[user_i][user_j] += weight[2]*collect_same_item_count[user_i][user_j]
            else:
                same_item_count[user_i][user_j] = weight[2]*collect_same_item_count[user_i][user_j]

    for user_i in cart_same_item_count.keys():
        for user_j in cart_same_item_count[user_i].keys():
            if user_j in same_item_count[user_i].keys():
                same_item_count[user_i][user_j] += weight[3]*cart_same_item_count[user_i][user_j]
            else:
                same_item_count[user_i][user_j] = weight[3]*cart_same_item_count[user_i][user_j]
    return same_item_count

#计算用户相似度
def cal_similarity(same_item_count,behavior_count):
    similarity={}
    for user_i in same_item_count.keys():
        similarity[user_i]={}
        for user_j in same_item_count[user_i].keys():
            if behavior_count[user_i] == 0 or behavior_count[user_j] == 0 :
                similarity[user_i][user_j] = 0
            else:
                similarity[user_i][user_j] = float(same_item_count[user_i][user_j])/math.sqrt(behavior_count[user_i]*behavior_count[user_j])
    return similarity

def write(dic,file_name):
    pickle.dump(dic,open('./data/'+file_name,'wb'))
