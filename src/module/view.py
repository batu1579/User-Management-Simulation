#!/usr/bin/env python
# coding=utf-8
'''
Author: BATU1579
CreateDate: 2022-06-29 05:39:10
LastEditor: BATU1579
LastTime: 2022-06-30 12:25:49
FilePath: \\src\\module\\view.py
Description:
'''
from typing import List

from util.json_operation import load_file
from util.input import MultiPageSelect, Select, Confirm
from module.access_permission import Permission

GOODS_FILE_DIR = '.\\src\\database\\goods.json'


class EmptyView(Exception):
    def __init__(self, title: str):
        self.message = f"View {title} is empty."


class GoodsView:
    def __init__(self, data: List[dict] = None, title: str = None):
        self.data = data if data else []
        self.title = title if title else 'Goods'

    def show_all(self):
        self.check_data_empty()
        view = MultiPageSelect(self.title, self.data)
        view.get_input()

    def select_product(self) -> dict:
        self.check_data_empty()
        view = MultiPageSelect(self.title, self.data)
        index = view.get_input()
        return self.data[index]

    def check_data_empty(self):
        if not self.data:
            raise EmptyView(self.title)


class ProductView:
    def __init__(self, role: int):
        permission = Permission()
        self.operations = permission.check_permission(role)

        self.goods = GoodsView(load_file(GOODS_FILE_DIR))
        self.orders = GoodsView(title='Orders')

    def loop(self):
        while True:
            try:
                self.show_view()
            except EmptyView as err:
                confirm = Confirm("Warning", err.message)
                confirm.get_input()
            except Exception as err:
                raise err

    def show_view(self):
        menu = Select("Operation", self.operations)
        select = self.operations[menu.get_input()]

        if select == "View Products":
            self.goods.show_all()
        elif select == "Select Products":
            self.orders.data.append(self.goods.select_product())
        elif select == "View Order":
            self.orders.show_all()
        elif select == "Pay":
            self.__pay()
        elif select == "Exit":
            exit()

    def __pay(self):
        confirm = Confirm(
            "Confirm",
            "Are you sure you want to pay this order ?"
        )
        if confirm.get_input() == 1:
            return None

        self.orders.check_data_empty()

        sum_price = 0
        for product in self.orders.data:
            product = list(product.values())[0]
            sum_price += product['price']
        confirm = Confirm(
            "Congratulations",
            f"You paid $ {sum_price} successfully !"
        )
        confirm.get_input()
        exit()
