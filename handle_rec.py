#!/uer/bin/env python
#coding:utf-8
import pickle

def handle_rec(rec_user_item,item_numer,user_id):
    result={}
    for user in user_id.keys():
        result[user]={}
    #第一步 限定推荐物品个数，删去多余的物品
    for user in rec_user_item.keys():
        if len(rec_user_item[user])<=item_numer:
            result[user] = rec_user_item[user]
        else:
            item_list=sorted(rec_user_item[user],key=rec_user_item[user].get,reverse=True)
            item_list=item_list[0:item_numer-1]
            for item in item_list:
                result[user][item]=rec_user_item[user][item]
    pickle.dump(result,open('./data/result','wb'))
    return result
