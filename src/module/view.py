#!/usr/bin/env python
# coding=utf-8
'''
Author: BATU1579
CreateDate: 2022-06-29 05:39:10
LastEditor: BATU1579
LastTime: 2022-06-29 08:28:56
FilePath: \\src\\module\\view.py
Description:
'''
from typing import List

from util.json_operation import load_file
from util.input import MultiPageSelect, Select, Confirm

GOODS_FILE_DIR = '.\\src\\database\\goods.json'


class EmptyView(Exception):
    def __init__(self):
        self.message = "This view is empty."


class GoodsView:
    def __init__(self, data: List[dict] = None, title: str = None):
        self.data = data if data else []
        self.title = title if title else 'Goods'

    def show_all(self):
        if not self.data:
            raise EmptyView()
        view = MultiPageSelect(self.title, self.data)
        view.get_input()

    def select_product(self) -> dict:
        view = MultiPageSelect(self.title, self.data)
        index = view.get_input()
        return self.data[index]


class ProductView:
    def __init__(self):
        self.goods = GoodsView(load_file(GOODS_FILE_DIR))
        self.orders = GoodsView(title='Orders')

    def loop(self):
        while True:
            menu = Select(
                "Operation",
                ["View Products", "Select Products", "View Order", "Pay"]
            )
            select_index = menu.get_input()

            try:
                if select_index == 0:
                    self.goods.show_all()
                elif select_index == 1:
                    self.orders.data.append(self.goods.select_product())
                elif select_index == 2:
                    self.orders.show_all()
                elif select_index == 3:
                    confirm = Confirm(
                        "Confirm",
                        "Are you sure you want to pay this order ?"
                    )
                    if confirm.get_input() == 0:
                        confirm = Confirm(
                            "Congratulations",
                            "You have paid this order successfully !"
                        )
                        confirm.get_input()
                        exit()
            except EmptyView as err:
                confirm = Confirm("Warning", err.message)
                confirm.get_input()
            except Exception as err:
                raise err
