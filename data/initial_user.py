#!/usr/bin/env python
#_*_ coding:utf-8 _*_
# Author:bear


import json,sys,os

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# sys.path.append(BASE_DIR)
# print(BASE_DIR)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)



acc_dic = {
    'id': 1234,
    'password': 'abc',
    'credit': 15000,
    'balance': 15000,
    'enroll_date': '2016-01-02',
    'expire_date': '2021-01-01',
    'pay_day': 22,
    'status': 0 # 0 = normal, 1 = locked, 2 = disabled
}

acc_dic1 = {
    'id': "alex",
    'password': 'abc',
    'credit': 15000,
    'balance': 15000,
    'enroll_date': '2016-01-02',
    'expire_date': '2021-01-01',
    'pay_day': 22,
    'status': 0 # 0 = normal, 1 = locked, 2 = disabled
}

acc_dic2 = {
    'id': "laoan",
    'password': 'abc',
    'credit': 15000,
    'balance': 15000,
    'enroll_date': '2016-01-02',
    'expire_date': '2021-01-01',
    'pay_day': 22,
    'status': 1 # 0 = normal, 1 = locked, 2 = disabled
}

print(json.dumps(acc_dic))
username = acc_dic["id"]
username1 = acc_dic1["id"]
username2 = acc_dic2["id"]

with open("%s\data\\account\%s.json" %(BASE_DIR,username),"w") as f:
    f.write(json.dumps(acc_dic))
with open("%s\data\\account\%s.json" %(BASE_DIR,username1),"w") as f:
    f.write(json.dumps(acc_dic1))
with open("%s\data\\account\%s.json" %(BASE_DIR,username2),"w") as f:
    f.write(json.dumps(acc_dic2))