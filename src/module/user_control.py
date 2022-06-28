#!/usr/bin/env python
# coding=utf-8
'''
Author: BATU1579
CreateDate: 2022-06-28 16:51:07
LastEditor: BATU1579
LastTime: 2022-06-29 04:05:11
FilePath: \\src\\module\\user_control.py
Description:
'''
from random import randint
from hashlib import md5
from typing import Callable

from util.json_operation import load_file, update_file
from util.input import Form, Confirm, SingleChoice

FILE_DIR = ".\\src\\database\\password.json"


class AuthenticationException(Exception):
    def __init__(self, username: str):
        self.username = username
        self.set_msg()

    def __str__(self):
        return self.message


class UserNotFoundException(AuthenticationException):
    def set_msg(self):
        self.message = f'User {self.username} not found'


class UserExistsException(AuthenticationException):
    def set_msg(self):
        self.message = f'User {self.username} already exists'


class VerificationFailure(AuthenticationException):
    def set_msg(self):
        self.message = 'User verification failed. Please try again'


class UserControlCore(object):
    def __init__(self):
        self.user_data: dict = load_file(FILE_DIR)

    def login(self, username: str, password: str) -> int:
        # 检查是否存在用户
        if username not in self.user_data:
            raise UserNotFoundException(username)

        user: dict = self.user_data[username]
        # 检查用户密码是否正确
        result: dict = self.hash_password(password, user['salt'])
        if result["password"] != user['password']:
            raise VerificationFailure(username)

        return user['role']

    def register(self, username: str, password: str) -> int:
        # 检查用户是否已经存在
        if username in self.user_data:
            raise UserExistsException(username)

        # 添加用户
        self.user_data[username] = {
            **self.hash_password(password),
            'role': 1,
        }

        # 更新数据
        update_file(FILE_DIR, self.user_data)

        return 1

    @staticmethod
    def hash_password(password: str, salt: str = None) -> dict:
        '''
        转换密码
        '''
        assert type(password) == str, "password needs to be a string"
        salt = str(randint(10000, 99999)) if salt is None else salt
        assert type(salt) == str, "salt needs to be a string"
        assert len(salt) == 5, "salt needs to be 5 characters long"
        hash_pwd = md5((password + salt).encode('utf-8')).hexdigest()

        return {
            "salt": salt,
            "password": hash_pwd
        }


class UserController:
    def __init__(self):
        self.core = UserControlCore()

    def loop(self) -> int:
        while True:
            select = SingleChoice("Operation", ["login", "register", "exit"])
            selection = select.get_input()

            if selection == 2:
                exit()

            op = self.__login if selection == 0 else self.__register
            while True:
                result = op()
                if result["state"] == 1:
                    return result["role"]
                elif result["exit"] == 1:
                    break

    def __framework(self, callback: Callable):
        try:
            return {
                "state": 1,
                "role": callback()
            }
        except AuthenticationException as err:
            confirm = Confirm("Warning", err)
            return {
                "state": 0,
                "exit": confirm.get_input()
            }
        except Exception as err:
            raise err

    def __login(self) -> int:

        def callback():
            form = Form("Login", ["username", "password"])
            return self.core.login(**form.get_input())

        return self.__framework(callback)

    def __register(self):

        def callback():
            form = Form("Register", ["username", "password"])
            return self.core.register(**form.get_input())

        return self.__framework(callback)
