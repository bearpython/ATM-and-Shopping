#!/usr/bin/env python
#_*_ coding:utf-8 _*_
# Author:bear

import os,sys,time,json,datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
print(BASE_DIR)

from core import login
from core import main

goods_buy = []
def shop_cart():
    price_buy = 0
    with open("%s\data\goods_list.json" %BASE_DIR,"r") as f:
        goods_list = json.load(f)
        # print(goods_list)
        while True:
            print("商城商品列表：")
            for line in goods_list:
                print("%s:%s" %(line,goods_list[line]))
            user_input = input("请输入您想要购买的商品名称，结算请输入quit:")
            if user_input != "quit":
                if user_input in goods_list:
                    goods_buy.append(user_input)
                    price_buy = int(price_buy) + int(goods_list[user_input])
                    print("您当前的购物车，商品：%s,总价格：%s" %(goods_buy,price_buy))
                else:
                    print("您输入的商品名称有误！")
            else:
                # print("欢迎再次光临！")
                settlement(goods_buy, price_buy)
                break
    print("----->>>>>>%s购物车商品总价格shop_cart" %price_buy)
    return price_buy
# res_price = shop_cart()
# print(res_price)

@login.user_status
def settlement(buy_list,all_price):
    print("您当前购物车商品为：%s" %buy_list)
    print("您当前的消费总结额为：%s" %all_price)
    user_choise = input("购物车结算请输入1，取消购物输入2:")
    if user_choise == "1":
        shop_status = main.settlement_api(login.acc_auth,all_price)  #调用login.py文件中的全局变量acc_auth
        if shop_status:
            dir_log = "%s\logs\shopping.log" %(BASE_DIR)
            with open(dir_log,"a",encoding="utf-8") as log_f:
                now_time = datetime.datetime.now()
                log_f.write("%s\t用户：%s\t已购买的商品：%s\t消费金额：%s\n" %(now_time,login.account_info["name"],buy_list,all_price))
        goods_buy.clear()
        # print("购买商品成功！,结算完成，您共计消费：%s元，余额为：%s" %(all_price,shop_balance))
    if user_choise == "2":
        goods_buy.clear()
        print("欢迎下次光临")
# settlement(goods_buy,price_buy)
