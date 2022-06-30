#!/usr/bin/env python
# coding=utf-8
'''
Author: BATU1579
CreateDate: 2022-06-29 03:28:37
LastEditor: BATU1579
LastTime: 2022-06-30 11:03:42
FilePath: \\src\\module\\access_permission.py
Description: 访问权限模块
'''
from typing import List

from util.json_operation import load_file

PERMISSION_FILE_DIR = ".\\src\\database\\permissions.json"


class Permission:
    def __init__(self):
        self.permissions = load_file(PERMISSION_FILE_DIR)

    def check_permission(self, role: int) -> List[str]:
        access_permission = []
        for value in self.permissions.values():
            if role in value["role"]:
                access_permission.append(value["name"])
        return access_permission
