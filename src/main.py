#!/usr/bin/env python
# coding=utf-8
'''
Author: BATU1579
CreateDate: 2022-06-28 15:28:17
LastEditor: BATU1579
LastTime: 2022-06-29 08:17:40
FilePath: \\src\\main.py
Description:
'''
from module.user_control import UserController
from module.view import ProductView

from util.json_operation import load_file
from util.input import Confirm

# 登录
controller = UserController()
controller.loop()

# 显示公司信息
info = []
for key, value in load_file(".\\src\\database\\company.json").items():
    info.append(f"{key} - {value}")
confirm = Confirm("Company Info", '\n     '.join(info), cancel_action=exit)
confirm.get_input()

# 显示产品列表
view = ProductView()
view.loop()
