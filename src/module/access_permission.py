#!/usr/bin/env python
# coding=utf-8
'''
Author: BATU1579
CreateDate: 2022-06-29 03:28:37
LastEditor: BATU1579
LastTime: 2022-06-29 04:50:11
FilePath: \\src\\module\\access_permission.py
Description: 访问权限模块
'''
from util.json_operation import load_file

PERMISSION_FILE_DIR = ".\\src\\database\\permissions.json"


class Permission:
    def __init__(self):
        self.permissions = load_file(PERMISSION_FILE_DIR)

    def check_permission(self, permission: str, role: int):
        return role in self.permissions[permission]
