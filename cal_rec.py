#!/usr/bin/env python 
#coding:utf-8
import numpy as np
import pickle
import func

#获取推荐列表
def cal_rec(similarity,buy_user_item,click_user_item,collect_user_item,cart_user_item,weight_rec,user_id,k):
    rec={}
    for user in user_id:
        rec[user]={}
    #获取推荐用户列表
    rec_user=get_rec_user(similarity,user_id,k)
    #获取推荐商品列表
    rec_item=get_rec_item(rec_user,buy_user_item)
    #计算推荐物品的概率
    rec_item_pro=cal_rec_item_pro(rec_user,rec_item,buy_user_item,click_user_item,collect_user_item,cart_user_item,weight_rec,similarity,user_id)
    pickle.dump(rec_user,open('./data/rec_user','wb'))
    pickle.dump(rec_item,open('./data/rec_item','wb'))
    pickle.dump(rec_item_pro,open('./data/rec_item_pro','wb'))
    return rec_item_pro

#获取推荐用户列表
def get_rec_user(similarity,user_id,k):
    rec_user={}
    for user in user_id.keys():
        rec_user[user]={}
    for user in similarity.keys():
        if len(similarity[user])<=k:
            rec_user[user]=similarity[user]
        else:
            user_list=sorted(similarity[user],key=similarity[user].get,reverse=True)
            user_list=user_list[0:k-1]
            for user_j in user_list:
                rec_user[user][user_j]=similarity[user][user_j]
    return rec_user

#获取推荐商品列表
def get_rec_item(rec_user,buy_user_item):
    rec_item={}
    for user in buy_user_item.keys():
        rec_item[user]={}
        for user_j in rec_user[user].keys():
            if user == user_j:
                continue
            else:
                for item in buy_user_item[user_j].keys():
                    if item not in buy_user_item[user].keys():
                        if item not in rec_item[user].keys():
                            rec_item[user][item] = 1
    return rec_item

#计算物品的概率
def cal_rec_item_pro(rec_user,rec_item,buy_user_item,click_user_item,collect_user_item,cart_user_item,weight_rec,similarity,user_id):
    rec_item_pro={}
    rec_item_count={}
    #buy_user_item_count=func.get_user_item_count(buy_user_item,user_id)
    #click_user_item_count=func.get_user_item_count(click_user_item,user_id)
    for user in rec_user.keys():
        rec_item_pro[user]={}
        rec_item_count[user]={}
        for user_j in rec_user[user].keys():
            for item in rec_item[user].keys():
                if item in buy_user_item[user_j].keys():
                    if item in rec_item_pro[user].keys():
                        rec_item_pro[user][item] += similarity[user][user_j]*weight_rec[1]
                        rec_item_count[user][item] += 1
                    else:
                        rec_item_pro[user][item] = similarity[user][user_j]*weight_rec[1]
                        rec_item_count[user][item] = 1
                if item in click_user_item[user_j].keys():
                    if item in rec_item_pro[user].keys():
                        print user,user_j,similarity[user][user_j],click_user_item[user_j][item]
                        rec_item_pro[user][item] += similarity[user][user_j]*weight_rec[0]
                        rec_item_count[user][item] += 1
                    else:
                        rec_item_pro[user][item] = similarity[user][user_j]*weight_rec[0]
                        rec_item_count[user][item] = 1
                if item in collect_user_item[user_j].keys():
                    if item in rec_item_pro[user].keys():
                        rec_item_pro[user][item] += similarity[user][user_j]*weight_rec[2]
                        rec_item_count[user][item] += 1
                    else:
                        rec_item_pro[user][item] = similarity[user][user_j]*weight_rec[2]
                        rec_item_count[user][item] = 1
                if item in cart_user_item[user_j].keys():
                    if item in rec_item_pro[user].keys():
                        rec_item_pro[user][item] += similarity[user][user_j]*weight_rec[3]
                        rec_item_count[user][item] += 1
                    else:
                        rec_item_pro[user][item] = similarity[user][user_j]*weight_rec[3]
                        rec_item_count[user][item] = 1

    return rec_item_pro
