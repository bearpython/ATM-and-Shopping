#!/usr/bin/env python
#_*_ coding:utf-8 _*_
# Author:bear

import os,sys,json,pickle,time,datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from core import shopping
from core import login


def cart_status(func):
    '''
    用户信用卡状态装饰器
    判断用户的卡状态是否可用
    :param acc_data:
    :return:
    '''
    def wrapper(acc_data,*args,**kwargs):
        #print("main warapper====>>>", acc_data, *args, **kwargs)
        if acc_data["status"] == 0:
            return func(acc_data,*args,**kwargs)
        else:
            print("\033[31;1m您的卡处在冻结状态！无法操作\033[0m")
    return wrapper

@cart_status
def settlement_api(acc_data,all_price):
    '''
    ATM中心提供给购物商城的结算接口
    :return:
    '''
    # print("ATM结算完成！",all_price)
    user_info_file = "%s\data\\account\%s.json" %(BASE_DIR,login.account_info["name"])
    #print(user_info_file)
    if os.path.isfile(user_info_file):
        with open(user_info_file,"r") as f:
            user_info = json.load(f)
            # print(user_info)
            tmp_balance = user_info["balance"]
            print("\033[31;1m您当前的账户余额为：%s\033[0m" %tmp_balance)
        if tmp_balance >= all_price:
            user_info["balance"] = tmp_balance - all_price
            with open(user_info_file, "w") as w:
                w.write(json.dumps(user_info))
            print("\033[31;1m购买商品成功！,结算完成，您共计消费：%s元，结算后余额为：%s\033[0m" % (all_price, user_info["balance"]))
            dir_log = "%s\logs\consume.log" % (BASE_DIR)
            with open(dir_log, "a", encoding="utf-8") as log_f:
                now_time = now = datetime.datetime.now()
                log_f.write("%s\t用户：%s\t消费金额：%s\t当前余额：%s\n" % (now_time, login.account_info["name"],all_price,user_info["balance"]))
            return True
        else:
            print("您的余额不足，当前余额为： %s" %tmp_balance)

def user_info(acc_data):
    '''
    打印出当前登录的用户信息
    用户的信息来自login.py中的login()的返回值
    :param acc_data:
    :return:
    '''
    # print(acc_data)
    if acc_data["status"] == 0:
        info_normal = '''
        用户姓名：%s
        用户密码：******
        信用卡额度：%s
        账户余额：%s
        发卡日期：%s
        有效期：%s
        信用卡状态：正常
        '''%(acc_data["id"],acc_data["credit"],acc_data["balance"],acc_data["enroll_date"],acc_data["expire_date"])
        print(info_normal)
    else:
        info_nonormal = '''
        用户姓名：%s
        用户密码：******
        信用卡额度：%s
        账户余额：%s
        发卡日期：%s
        有效期：%s
        \033[31;1m信用卡状态：冻结\033[0m
        '''%(acc_data["id"],acc_data["credit"],acc_data["balance"],acc_data["enroll_date"],acc_data["expire_date"])
        print(info_nonormal)

@cart_status
def repay(acc_data):
    '''
    还款功能
    :param acc_data:
    :return:
    '''
    balance_info = '''
    信用额度：%s
    余额：%s
    '''%(acc_data["credit"],acc_data["balance"])
    print(balance_info)
    flag = True
    while flag:
        repay_amount = input("请输入您要还款的金额（元）,返回上一级请输入B：").strip()
        if repay_amount.isdigit():
            repay_amount = int(repay_amount)
            if repay_amount > 0 :
                new_balance = acc_data["balance"] + repay_amount
                acc_data["balance"] = new_balance
                user_info_file = "%s\data\\account\%s.json" % (BASE_DIR, acc_data["id"])
                with open(user_info_file,"w") as f:
                    f.write(json.dumps(acc_data))
                print("还款成功，您本次还款的金额为：%s，余额为：%s" %(repay_amount,new_balance))
                dir_log = "%s\logs\\atm.log" % (BASE_DIR)
                with open(dir_log, "a", encoding="utf-8") as log_f:
                    now_time = datetime.datetime.now()
                    log_f.write("%s\t用户：%s\t类型：还款\t还款金额：%s\t当前余额：%s\n" % (now_time, login.account_info["name"],repay_amount,acc_data["balance"]))
        elif repay_amount == "B":
            flag = False
        else:
            print("您输入的金额不正确")

@cart_status
def withdrawal(acc_data):
    '''
    提现功能，每次提现扣除5%的手续费
    :param acc_data:
    :return:
    '''
    balance_info = '''
    信用额度：%s
    余额：%s
    '''%(acc_data["credit"],acc_data["balance"])
    print(balance_info)
    flag = True
    while flag:
        withdrawal_amount = input("请输入您要提现的金额（元）,返回上一级请输入B：").strip()
        if withdrawal_amount.isdigit():
            withdrawal_amount = int(withdrawal_amount)
            if withdrawal_amount > 0 :
                service_price = withdrawal_amount * 0.05
                new_balance = acc_data["balance"] - service_price - withdrawal_amount
                acc_data["balance"] = new_balance
                user_info_file = "%s\data\\account\%s.json" % (BASE_DIR, acc_data["id"])
                with open(user_info_file,"w") as f:
                    f.write(json.dumps(acc_data))
                print("您本次提现的金额为：%s，手续费：%s，余额为：%s" %(withdrawal_amount,service_price,new_balance))
                dir_log = "%s\logs\\atm.log" % (BASE_DIR)
                with open(dir_log, "a", encoding="utf-8") as log_f:
                    now_time = datetime.datetime.now()
                    log_f.write("%s\t用户：%s\t类型：提现\t提现金额：%s\t手续费：%s\t当前余额：%s\n" % (now_time, login.account_info["name"],withdrawal_amount,service_price,acc_data["balance"]))
        elif withdrawal_amount == "B":
            flag = False
        else:
            print("您输入的金额不正确")

@cart_status
def transfer(acc_data):
    '''
    转账功能
    :param acc_data:
    :return:
    '''
    balance_info = '''
    信用额度：%s
    余额：%s
    '''%(acc_data["credit"],acc_data["balance"])
    print(balance_info)
    flag = True
    while flag:
        transferee_account = input("请输入您要转账的用户名称,返回上一级请输入B：").strip()
        transferee_info_file = "%s\data\\account\%s.json" % (BASE_DIR, transferee_account)
        if os.path.isfile(transferee_info_file):
            transfer_amount = input("请输入您要转账的金额（元）：").strip()
            if transfer_amount.isdigit():
                transfer_amount = int(transfer_amount)
                if acc_data["balance"] >= transfer_amount and transfer_amount > 0:
                    acc_data["balance"] = acc_data["balance"] - transfer_amount
                    user_info_file = "%s\data\\account\%s.json" % (BASE_DIR, acc_data["id"])
                    with open(user_info_file, "w") as f:
                        f.write(json.dumps(acc_data))
                    with open(transferee_info_file,"r") as transferee_f_r:
                        transferee_res = json.load(transferee_f_r)
                        # print(transferee_res)
                        transferee_res["balance"] = transferee_res["balance"] + transfer_amount
                    with open(transferee_info_file,"w") as transferee_f_w:
                        transferee_f_w.write(json.dumps(transferee_res))
                    print("\033[31;1m转账成功，您本次转账的金额为：%s，余额为：%s\033[0m" % (transfer_amount, acc_data["balance"]))
                    dir_log = "%s\logs\\atm.log" % (BASE_DIR)
                    with open(dir_log, "a", encoding="utf-8") as log_f:
                        now_time = datetime.datetime.now()
                        log_f.write("%s\t用户：%s\t类型：转账\t收款账户：%s\t转账金额：%s\t当前余额：%s\n" % (now_time, login.account_info["name"],transferee_account,transfer_amount,acc_data["balance"]))
                else:
                    print("您当前的余额不足！")
                    # flag = False
            else:
                print("您输入的金额有误！")
        elif transferee_account == "B":
            flag = False
        else:
            print("您输入的用户名不正确")

def check_sheet (acc_data):
    pass

def logout(acc_data):
    # sys.exit("欢迎下次光临")
    pass

def menu_list(acc_data):
    '''
    打印ATM管理中心功能菜单
    :return:
    '''
    menu = '''
    -------User Bank ---------
    \033[32;1m 1.  账户信息
    2.  还款
    3.  取款
    4.  转账
    5.  账单
    6.  退出
    \033[0m'''
    menu_dic = {
        "1": user_info,
        "2": repay,
        "3": withdrawal,
        "4": transfer,
        "5": check_sheet,
        "6": logout,
    }
    menu_flag = True
    while menu_flag:
        print(menu)
        user_choice = input("请输入您要操作的ID：").strip()
        if user_choice == "6":
            menu_flag = False
        elif user_choice in menu_dic:
            menu_dic[user_choice](acc_data)
        else:
            print("\033[31;1m您输入的ID不存在，请重新输入!\033[0m")
def run():
    user_data = login.login()
    if login.account_info["status"]:
        # print(user_data)
        menu_list(user_data)