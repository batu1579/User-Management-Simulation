#!/usr/bin/env python
# coding=utf-8
'''
Author: BATU1579
CreateDate: 2022-06-28 16:15:44
LastEditor: BATU1579
LastTime: 2022-06-29 03:24:00
FilePath: \\src\\util\\json_operation.py
Description: JSON 文件操作
'''
from json import load, dump


def load_file(filename: str) -> dict:
    with open(filename, 'r', encoding='utf-8') as fp:
        return load(fp)


def update_file(filename: str, data: dict) -> dict:
    with open(filename, 'w', encoding='utf-8') as fp:
        return dump(data, fp, indent=4)
