#!/usr/bin/env python
#_*_ coding:utf-8 _*_
# Author:bear

import json,sys,os,datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)


# def user_name(func):
#     def warpper(*args,**kwargs):
#         user_name = input("请输入您想要修改的用户名：").strip()
#         if user_name != "":
#             func(*args,**kwargs)
#         else:
#             print("输入的用户名不能为空！")
#     return warpper

def select():
    '''
    查看任意用户信息
    :param acc_data:
    :return:
    '''
    # print(acc_data)
    acc_name = input("输入要查询的用户名：").strip()
    user_info_file = "%s\data\\account\%s.json" %(BASE_DIR,acc_name)
    if os.path.isfile(user_info_file):
        with open(user_info_file,"r") as f:
            acc_data = json.load(f)
        if acc_data["status"] == 0:
            info_normal = '''
            用户姓名：%s
            用户密码：%s
            信用卡额度：%s
            账户余额：%s
            发卡日期：%s
            有效期：%s
            信用卡状态：正常
            '''%(acc_data["id"],acc_data["password"],acc_data["credit"],acc_data["balance"],acc_data["enroll_date"],acc_data["expire_date"])
            print(info_normal)
        else:
            info_nonormal = '''
            用户姓名：%s
            用户密码：%s
            信用卡额度：%s
            账户余额：%s
            发卡日期：%s
            有效期：%s
            \033[31;1m信用卡状态：冻结\033[0m
            '''%(acc_data["id"],acc_data["password"],acc_data["credit"],acc_data["balance"],acc_data["enroll_date"],acc_data["expire_date"])
            print(info_nonormal)
    else:
        print("您要查询的用户不存在！")

def add_account():
    '''
    添加用户功能
    添加用户输入格式：{'id': '1234','password': 'abc','credit': 15000,'balance': 15000,'enroll_date': '2016-01-02','expire_date': '2021-01-01','pay_day': 22,'status': 0}
    :param args:
    :param kwargs:
    :return:
    '''
    username = input("请输入添加的用户名：").strip()
    user_info_file = "%s\data\\account\%s.json" %(BASE_DIR,username)
    #print(user_info_file)
    if os.path.isfile(user_info_file):
        print("您要添加的用户已经存在！")
    else:
        acc_dic = input("请输入用户信息：").strip()
        acc_dic = eval(acc_dic)
        with open(user_info_file, "w") as f_w:
            f_w.write(json.dumps(acc_dic))
        with open(user_info_file, "r") as f_r:
            user_info = json.load(f_r)
        if username == user_info["id"]:
            print("\033[31;1m用户%s添加成功!\033[0m" %username)
            dir_log = "%s\logs\\admin.log" % (BASE_DIR)
            with open(dir_log, "a", encoding="utf-8") as log_f:
                now_time = now = datetime.datetime.now()
                log_f.write("%s\t操作类型：添加用户\t用户名：%s\t信用额度：%s\t余额：%s\t发卡日期：%s\t有效期：%s\t卡状态：%s\n"
                            %(now_time,user_info["id"],user_info["credit"],user_info["balance"],user_info["enroll_date"],user_info["expire_date"],user_info["status"]))
        else:
            print("\033[31;1m您输入的用户信息与用户名不符\033[0m")
            os.remove(user_info_file)

def change_account():
    '''
    修改用户信息
    :param args:
    :param kwargs:
    :return:
    '''
    user_name = input("请输入您想要修改的用户名：").strip()
    if user_name != "":
        user_info_file = "%s\data\\account\%s.json" % (BASE_DIR, user_name)
        if os.path.isfile(user_info_file):
            with open(user_info_file,"r") as f_r:
                acc_data = json.load(f_r)
                info_normal = '''
                --------当前用户信息-------
                用户姓名：%s
                用户密码：%s
                信用卡额度：%s
                账户余额：%s
                发卡日期：%s
                有效期：%s
                信用卡状态：%s
                ''' % (acc_data["id"], acc_data["password"],acc_data["credit"], acc_data["balance"], acc_data["enroll_date"],acc_data["expire_date"],acc_data["status"])
                print(info_normal)
            # print(acc_data)
            change_status = input("可修改用户信息的类型：\n1.用户名\n2.用户密码\n3.信用卡额度\n4.有效期(example:2021-01-01)\n5.信用卡状态(0 = normal, 1 = locked, 2 = disabled)\n6.返回上一级\n请输入ID：").strip()
            if change_status == "1":
                change_name = input("请输入新的用户名称：").strip()
                if change_name != "":
                    old_info = acc_data["id"]
                    acc_data["id"] = change_name
                    with open(user_info_file,"w") as f:
                        f.write(json.dumps(acc_data))
                    os.rename("%s\data\\account\%s.json" % (BASE_DIR, user_name),"%s\data\\account\%s.json" % (BASE_DIR, change_name))
                    with open("%s\data\\account\%s.json" % (BASE_DIR, change_name),"r") as new_f:
                        new_acc_name = json.load(new_f)
                        print("原用户名：%s,修改后用户名：%s" %(old_info,new_acc_name["id"]))
                    dir_log = "%s\logs\\admin.log" % (BASE_DIR)
                    with open(dir_log, "a", encoding="utf-8") as log_f:
                        now_time = now = datetime.datetime.now()
                        log_f.write("%s\t操作类型：修改用户信息\t原用户名：%s\t修改后用户名：%s\n" %(now_time,old_info,new_acc_name["id"]))
                else:
                    print("输入新用户名不能为空！")
            elif change_status == "2":
                change_passwd = input("请输入新的用户密码：").strip()
                if change_passwd != "":
                    old_info = acc_data["password"]
                    acc_data["password"] = change_passwd
                    with open(user_info_file,"w") as f:
                        f.write(json.dumps(acc_data))
                    with open(user_info_file,"r") as new_f:
                        new_acc_passwd = json.load(new_f)
                        print("原密码：%s,修改后密码：%s" %(old_info,new_acc_passwd["password"]))
                    dir_log = "%s\logs\\admin.log" % (BASE_DIR)
                    with open(dir_log, "a", encoding="utf-8") as log_f:
                        now_time = now = datetime.datetime.now()
                        log_f.write("%s\t用户名：%s\t操作类型：修改用户信息\t原密码：%s\t修改后密码：%s\n" %(now_time,new_acc_passwd["id"],old_info,new_acc_passwd["password"]))
                else:
                    print("输入新密码不能为空！")
            elif change_status == "3":
                change_credit = input("请输入用户新的信用额度：").strip()
                if change_credit != "":
                    old_info = acc_data["credit"]
                    acc_data["credit"] = int(change_credit)
                    with open(user_info_file,"w") as f:
                        f.write(json.dumps(acc_data))
                    with open(user_info_file,"r") as new_f:
                        new_acc_credit = json.load(new_f)
                        print("原信用卡额度：%s,修改信用卡额度：%s" %(old_info,new_acc_credit["credit"]))
                    dir_log = "%s\logs\\admin.log" % (BASE_DIR)
                    with open(dir_log, "a", encoding="utf-8") as log_f:
                        now_time = now = datetime.datetime.now()
                        log_f.write("%s\t用户名：%s\t操作类型：修改用户信息\t原信用额度：%s\t修改后信用额度：%s\n" %(now_time,new_acc_credit["id"],old_info,new_acc_credit["credit"]))
                else:
                    print("输入新额度不能为空！")
            elif change_status == "4":
                change_expire_date = input("请输入新的信用卡有效期：").strip()
                if change_expire_date != "":
                    old_info = acc_data["expire_date"]
                    acc_data["expire_date"] = change_expire_date
                    with open(user_info_file,"w") as f:
                        f.write(json.dumps(acc_data))
                    with open(user_info_file,"r") as new_f:
                        new_acc_expire_date = json.load(new_f)
                        print("原有效期：%s,修改后有效期：%s" %(old_info,new_acc_expire_date["expire_date"]))
                    dir_log = "%s\logs\\admin.log" % (BASE_DIR)
                    with open(dir_log, "a", encoding="utf-8") as log_f:
                        now_time = now = datetime.datetime.now()
                        log_f.write("%s\t用户名：%s\t操作类型：修改用户信息\t原有效期：%s\t修改后有效期：%s\n" %(now_time,new_acc_expire_date["id"],old_info,new_acc_expire_date["expire_date"]))
                else:
                    print("输入新的日期不能为空！")
            elif change_status == "5":
                change_cart_status = input("请输入用户卡的状态：").strip()
                if change_cart_status != "":
                    old_info = acc_data["status"]
                    acc_data["status"] = int(change_cart_status)
                    with open(user_info_file,"w") as f:
                        f.write(json.dumps(acc_data))
                    with open(user_info_file,"r") as new_f:
                        new_acc_status = json.load(new_f)
                        print("原信用卡状态：%s,修改后信用卡状态：%s" %(old_info,new_acc_status["status"]))
                    dir_log = "%s\logs\\admin.log" % (BASE_DIR)
                    with open(dir_log, "a", encoding="utf-8") as log_f:
                        now_time = now = datetime.datetime.now()
                        log_f.write("%s\t用户名：%s\t操作类型：修改用户信息\t原卡状态：%s\t修改后卡状态：%s\n" %(now_time,new_acc_status["id"],old_info,new_acc_status["status"]))
                else:
                    print("输入用户卡状态不能为空！")
            elif change_status == "6":
                pass
            else:
                print("输入修改信息类型有误！")
        else:
            print("您输入的用户不存在！")
    else:
        print("输入不能为空！")

def menu_list():
    '''
    管理后台可操作列表
    :return:
    '''
    menu = '''
    --------欢迎进入ATM管理后台----------
    1.添加用户
    2.修改用户信息
    3.查询
    4.退出
    '''
    menu_dic = {
        "1":add_account,
        "2":change_account,
        "3":select,
        "4":"logout"
    }
    flag = True
    while flag:
        print(menu)
        admin_choise = input("请输入要进行操作的ID：").strip()
        if admin_choise == "4":
            sys.exit("安全退出！")
        elif admin_choise in menu_dic:
            menu_dic[admin_choise]()
        else:
            print("\033[31;1m您输入的ID不存在，请重新输入!\033[0m")

def run():
    admin_info_file = "%s\data\\admin.json" %BASE_DIR
    with open(admin_info_file, "r") as f:
        admin_info = json.load(f)
        admin_name = input("请输入管理员用户名：").strip()
        admin_passwd = input("请输入管理员密码：").strip()
        if admin_name == admin_info["id"] and admin_passwd == admin_info["password"]:
            menu_list()
        else:
            print("您输入的用户名或密码错误！")
