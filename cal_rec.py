#!/usr/bin/env python 
#coding:utf-8
import numpy as np
import pickle

def write(dic,filename):
    f=open('./data/'+filename,'wb')
    pickle.dump(dic,f)

def cal_rec(trainUI,sim_train,k,train_mean):
    #第一步，根据设定的K值，求出跟用户相似度最大的用户列表
    #topKU = cal_topKU(sim_train,k)
    #第二步，获取topk个相似的用户喜欢且本身未购买的商品
    #首先，需要对用户-商品向量进行处理，只考虑购买行为(效果不好)
    #buyUI = cal_buyUI(trainUI)
    #下便便是寻找那些用户未购买，而其相似用户购买的物品
    '''
    计算推荐物品i的概率
    '''
    #先计算推荐的物品集合
    rec_items=cal_items(trainUI,sim_train)
    
    pro_items = cal_pro_items(rec_items,trainUI,train_mean,sim_train,k)
    #recI = cal_recI(topKU,trainUI)
    #接下来便是根据推荐列表和用户相似度，计算给用户推荐某一物品的概率
    #proI = cal_proI(recI,topKU,trainUI,train_mean)
    #return proI
    write(pro_items,'pro_items')
    return pro_items

#计算要推荐的物品集合
def cal_items(trainUI,sim_train):
    rec_items={}
    #将相似用户购买的物品加入推荐列表
    for user in  sim_train.keys():
        rec_items[user] = []
        for user_j in sim_train[user].keys():
            for item in buyUI[user_j].keys():
                if item not in rec_items[user]:
                    rec_items[user].append(item)
    return rec_items

#计算跟用户相似度最大的前k个用户列表
def cal_topKU(sim_train,k):
    topKU={}
    for u1 in sim_train.keys():
        topKU[u1] = {}
        if len(sim_train[u1]) <= k :
            topKU[u1] = sim_train[u1]
        else:
            u = sorted(sim_train[u1],key = sim_train[u1].get,reverse=True)
            u = u[0:k-1]
            for u2 in u:
                topKU[u1][u2] = sim_train[u1][u2]
    return topKU

#对用户-商品向量进行处理，只考虑购买行为
def cal_buyUI(trainUI):
    buyUI = {}
    for u1 in trainUI.keys():
        buyUI[u1] = {}
        item = sorted(trainUI[u1],key=trainUI[u1].get,reverse=True)
        for i in item:
            if trainUI[u1][i] == 4:
                buyUI[u1][i] = 4
            else :
                break
    return buyUI

#下面便计算推荐的物品列表
def cal_recI(topKU,buyUI):
    recI = {}
    for u1 in topKU.keys():
        recI[u1] = {}
        #获取相似用户列表
        u = topKU[u1].keys()
        for u2 in u:
            #获取相似用户的购买列表
            item = buyUI[u2].keys()
            for i in item:
                #若相似用户购买商品用户未买过
                if i not in buyUI[u1].keys():
                    recI[u1][i] = 1
    return recI

#计算推荐某一物品的概率
def  cal_pro_items(rec_items,trainUI,train_mean,sim_train,k):
    pro_items={}
    simUV = {}
    for user in rec_items.keys():
        pro_items[user] = {}
        simUV[user] = {}
        for item in rec_items[user]:
            pro_items[user][item] = 0
            simUV[user][item] = 0
            #计算和用户相似的且购买过物品i的最相似的k个用户
            sim_user_item = cal_sim_user_item(sim_train[user],trainUI,item,k)
            for user_j in sim_user_item:
                pro_items[user][item] += sim_train[user][user_j]*(trainUI[user_j][item] - train_mean[user_j])
                simUV[user][item] += abs(sim_train[user][user_j])
            pro_items[user][item] += train_mean[user]
    return pro_items
            
def cal_sim_user_item(sim_user,trainUI,item,k):
    user = []
    users = sorted(sim_user,key=sim_user.get,reverse=True)
    for u in users:
        if item in trainUI[u].keys():
            user.append(u)
    if len(user) >k:
        user = user[0:k-1]
    return user
#根据用户相似度，和推荐列表计算推荐某一物品的概率
def cal_proI(recI,topKU,buyUI,train_mean):
    proI = {}
    simUV = {}
    for u1 in recI.keys():
        proI[u1] = {}
        simUV[u1] = {}
        #跟用户相似的用户列表
        for u2 in topKU[u1].keys():
            #为用户推荐的物品列表
            for i in recI[u1].keys():
                #如果推荐物品在相似用户的购买行为中
                if i in buyUI[u2].keys():
                    if i in proI[u1].keys():
                        proI[u1][i] += topKU[u1][u2]
                        simUV[u1][i] += topKU[u1][u2]
                    else :
                        proI[u1][i] = topKU[u1][u2]
                        simUV[u1][i] = topKU[u1][u2]
    '''
    for u in proI.keys():
        for i in proI[u].keys():
            if simUV[u][i] != 0:
                proI[u][i] += train_mean[u] 
    '''
    write(proI,'proI')
    return proI

#对最后确定的推荐列表，设定对每个用户推荐的用户的个数
def setnumber(proI,i_numer):
    result={}
    for u1 in proI.keys():
        result[u1] = {}
        length = len(proI[u1])
        if length <= i_numer:
            result[u1] = proI[u1]
        else:
            item = sorted(proI[u1],key=proI[u1].get,reverse=True)
            item = item[0:i_numer-1]
            for i in item:
                result[u1][i] = proI[u1][i]
    write(result,'result')
    return result

#查看准确率，召回率和F值
def cal_result(result,testBUI):
    #查看命中的用户-物品
    hitUI = cal_hitUI(result,testBUI)
    #计算准确率
    precision,hitbrand,pbrand = cal_precision(hitUI,result)
    #计算召回率
    recall,bbrand = cal_recall(hitUI,testBUI,hitbrand)
    F=2*precision*recall/(precision+recall)
    precision = str(precision*100)+'%'
    recall = str(recall*100)+'%'
    F = str(F*100)+'%'
    return (precision,recall,F,hitbrand,pbrand,bbrand)
    
def cal_hitUI(result,testBUI):
    hitUI={}
    for u1 in result.keys():
        hitUI[u1] = 0
        for i in result[u1].keys():
            if i in testBUI[u1].keys():
                hitUI[u1] += 1
    return hitUI

#计算准确率
def cal_precision(hitUI,result):
    hitbrand = 0
    pbrand = 0
    for u in hitUI.keys():
        hitbrand += hitUI[u]
        pbrand += len(result[u])
    return (float(hitbrand)/float(pbrand),hitbrand,pbrand)

#计算召回率
def cal_recall(hitUI,testBUI,hitbrand):
    bbrand = 0
    for user in testBUI.keys():
        bbrand += len(testBUI[user])
    return (float(hitbrand)/float(bbrand),bbrand)
