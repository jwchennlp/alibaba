#!/user/bin/env python 
#coding:utf-8

import pandas as pd
import numpy as np
from pandas import *
import cal_rec,cal_sim
import pickle

def read(filename):
    f=open('./data/'+filename,'rb')
    return pickle.load(f)
def write(dic,filename):
    f=open('./data/'+filename,'wb')
    pickle.dump(dic,f)

if __name__=="__main__":

    #读取数据
    trainUI = read('trainUI')
    testUI = read('testUI')
    sim_train = read('sim_train')
    #计算推荐列表,参数是设定取与用户相似的用户值，K,返回结果是推荐的每个物品的概率
    k=20
    
    train_mean = cal_sim.cal_mean(trainUI)
    proI = cal_rec.cal_rec(trainUI,sim_train,k,train_mean)
    #对于推荐列表，要进行一下处理，因为每个用户推荐的物品数不相同，一个物品推荐给用户的概率也不一样
    #处事设定为每个用户推荐5个物品
    i_numer=5
    result=cal_rec.setnumber(proI,i_numer)
    
    #检验一下,查看准确率和召回率，以及F1值
    testBUI=cal_rec.cal_buyUI(testUI)
    #write(testBUI,'testBUI')
    
    #查看准确率，召回率和F值
    precision,recall,F,hitbrand,pbrand,bbrand=cal_rec.cal_result(result,testBUI)
    print '相似用户参数为(k)',k
    print '每个用户推荐物品为',i_numer
    print 'hitbrand',hitbrand,'pbrand',pbrand,'bbrand',bbrand
    print 'precision',precision,'recall',recall,'F_1',F
