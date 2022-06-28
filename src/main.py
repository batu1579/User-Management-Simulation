#!/usr/bin/env python
# coding=utf-8
'''
Author: BATU1579
CreateDate: 2022-06-28 15:28:17
LastEditor: BATU1579
LastTime: 2022-06-29 04:32:00
FilePath: \\src\\main.py
Description:
'''
from module.user_control import UserController
from util.json_operation import load_file
from util.input import Confirm

# 登录
controller = UserController()
controller.loop()

# 显示信息
info = []
for key, value in load_file(".\\src\\database\\company.json").items():
    info.append(f"{key} - {value}")
confirm = Confirm("Company Info", '\n     '.join(info), cancel_action=exit)
confirm.get_input()
