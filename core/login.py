#!/usr/bin/env python
#_*_ coding:utf-8 _*_
# Author:bear

import os,sys,time,json,pickle

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
print(BASE_DIR)
# from core import main
# from core import shopping
# from conf import setting
# from data import goods_list

account_info = {
    "name":None,
    "status":False,
    "accout_data":None
}

def user_status(func):
    '''
    装饰器，用来判断用户登录状态
    :param func:
    :return:
    '''
    def wrapper(*args,**kwargs):
        if not account_info["status"]:
            #return func(*args,**kwargs)
            login()
        func(*args,**kwargs)
    return wrapper


def login():
    '''
    用户登录模块，没有注册功能，认证三次失败退出程序
    :return:
    '''
    count = 0
    login_status = False
    while login_status is not True and count < 3:
        user_name = input("您还没有登录，请输入用户名：")
        user_passwd = input("请输入密码：")
        global acc_auth
        acc_auth = auth(user_name,user_passwd)
        if acc_auth:
            # print(acc_auth)
            login_status = True
            account_info["status"] = True
            account_info["name"] = user_name
            return acc_auth
        else:
            print("认证失败")
            count+=1
    else:
        sys.exit("登录重试次数过多，程序退出!")
    # if user_name != "":
    #     if user_name

def auth(username,userpasswd):
    '''
    认证的接口，参数由login（）传入
    判断用户输入的用户名的json文件是否存在
    存在则获取用户信息在判断密码，不存在提示用户
    :param username:
    :param userpasswd:
    :return:
    '''
    user_info_file = "%s\data\\account\%s.json" %(BASE_DIR,username)
    #print(user_info_file)
    if os.path.isfile(user_info_file):
        with open(user_info_file,"r") as f:
            user_info = json.load(f)
            #print(user_info)
            if user_info["password"] == userpasswd:
                return user_info
            else:
                print("您输入的用户名或密码有误！")
# login()

