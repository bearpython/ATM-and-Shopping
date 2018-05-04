#!/usr/bin/env python
#_*_ coding:utf-8 _*_
# Author:bear

import os,sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from core import main
from core import shopping
from core import management
# from data import goods_list


while True:
    print("欢迎来到银行系统！\n1.进入购物商城\n2.进入ATM管理中心\n3.进入ATM管理后台\n4.退出")
    user_choice = input("请输入您要进行的操作：")
    if user_choice.isdigit():
        if user_choice == "1":
            shopping.shop_cart()
        elif user_choice == "2":
            main.run()
        elif user_choice == "3":
            management.run()
        elif user_choice == "4":
            exit()
        else:
            print("您输入的ID不存在请重新输入！")
    else:
        print("输入错误，请重新输入！")