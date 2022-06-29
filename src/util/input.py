#!/usr/bin/env python
# coding=utf-8
'''
Author: BATU1579
CreateDate: 2022-06-28 22:30:19
LastEditor: BATU1579
LastTime: 2022-06-29 06:05:28
FilePath: \\src\\util\\input.py
Description: 交互控制器
'''
from abc import ABCMeta, abstractmethod
from os import system
from pynput.keyboard import Listener, Key
from typing import Callable, List, Dict

MAX_ITEMS_PER_PAGE = 5


class InputController(metaclass=ABCMeta):
    '''
    输入基类
    '''

    def __init__(self, title: str, data: list[str] = None):
        self.title = title
        self.data = data

    def show_title(self):
        system("cls")
        print(f"{'=' * 15} {self.title} {'=' * 15}\n")

    @abstractmethod
    def get_input(self): pass


class Form(InputController):
    '''
    表单输入
    '''

    def get_input(self) -> Dict[str, str]:
        self.show_title()
        return {question: input(f"[{question}]: ") for question in self.data}


class Select(InputController):
    '''
    单选输入
    '''

    def get_input(self) -> int:
        pitch_on = 0

        self.show_all(pitch_on)

        def check():
            # pitch_on 的边界检查
            nonlocal pitch_on
            if pitch_on < 0:
                pitch_on = len(self.data) - 1
            elif pitch_on == len(self.data):
                pitch_on = 0

        def on_press(key: Key):
            nonlocal pitch_on
            if key == Key.up:
                pitch_on -= 1
            if key == Key.down:
                pitch_on += 1
            if key == Key.enter:
                # 捕获回车
                input()
                return False
            check()
            self.show_all(pitch_on)

        with Listener(on_press=on_press) as listener:
            listener.join()

        return pitch_on

    def show_choice(self, pitch_on: int):
        assert 0 <= pitch_on < len(
            self.data), "pitch on number is out of range"

        print('''Tips: Use the up and down arrow keys to select.
        Press Enter to enter.
        ''')
        if type(self.data[0]) == dict:
            for index, choice in enumerate(self.data):
                if index == pitch_on:
                    print(f" => {choice['title']} - {choice['info']}")
                else:
                    print(f"    {choice['title']}")
        else:
            for index, choice in enumerate(self.data):
                print(f"{' => ' if index == pitch_on else '    '} {choice}")

    def show_all(self, pitch_on: int):
        self.show_title()
        self.show_choice(pitch_on)


class MultiPageSelect(InputController):
    def __init__(self, title: str, data: List[dict] = None):
        self.title = title
        self.data = []

        for index in range(0, len(data), MAX_ITEMS_PER_PAGE):
            pages = data[index: index + MAX_ITEMS_PER_PAGE]
            cache = []
            for i in pages:
                key = list(i.keys())[0]
                other_info = ' '.join([f"{k}: {v}" for k, v in i[key].items()])
                cache.append(f'{key} -- {other_info}')
            self.data.append(cache)

    def get_input(self) -> int:
        pages = 0
        pitch_on = 0

        self.show_all(pitch_on, pages)

        def check():
            # pages 的边界检查
            nonlocal pages
            if pages < 0:
                pages = len(self.data) - 1
            if pages == len(self.data):
                pages = 0

            # pitch_on 的边界检查
            nonlocal pitch_on
            if pitch_on < 0:
                pitch_on = len(self.data[pages]) - 1
            elif pitch_on == len(self.data[pages]):
                pitch_on = 0

        def on_press(key: Key):
            nonlocal pitch_on
            nonlocal pages
            if key == Key.up:
                pitch_on -= 1
            if key == Key.down:
                pitch_on += 1
            if key == Key.left:
                pages -= 1
            if key == Key.right:
                pages += 1
            if key == Key.enter:
                # 捕获回车
                input()
                return False
            check()
            self.show_all(pitch_on, pages)

        with Listener(on_press=on_press) as listener:
            listener.join()

        return pitch_on + pages * MAX_ITEMS_PER_PAGE

    def show_choice(self, pitch_on: int, current_page: int):
        assert 0 <= pitch_on < len(
            self.data[current_page]), "pitch on number is out of range"

        print('''Tips: Use the up and down arrow keys to select.
        Press Enter to enter.
        ''')
        for index, choice in enumerate(self.data[current_page]):
            print(f"{' => ' if index == pitch_on else '    '} {choice}")

    def show_pages(self, current_page: int):
        print(f"\n{'=' * 15} {current_page + 1} of {len(self.data)} pages {'=' * 15}")

    def show_all(self, pitch_on: int, current_page: int):
        self.show_title()
        self.show_choice(pitch_on, current_page)
        self.show_pages(current_page)


class Confirm(Select):
    def __init__(self, title: str, info: str, confirm_action: Callable = None,
                 cancel_action: Callable = None):
        super().__init__(title, ['confirm', 'cancel'])
        self.info = info
        self.confirm_action = confirm_action
        self.cancel_action = cancel_action

    def show_all(self, pitch_on: int):
        self.show_title()
        print(f"\n     {self.info}    \n\n")
        self.show_choice(pitch_on)

    def get_input(self) -> int:
        result = super().get_input()

        if result == 0 and self.confirm_action is not None:
            self.confirm_action()
        elif result != 0 and self.cancel_action is not None:
            self.cancel_action()

        return result


def main():
    controller = Select("title", [
        "A", "B", "C", "D", "E", "F"
    ])
    print(controller.get_input())

    controller = Form("title", ['username', 'password'])
    print(controller.get_input())

    controller = Confirm("title", "xxxxx", lambda: print(
        "yes"), lambda: print("no"))
    print(controller.get_input())


if __name__ == "__main__":
    main()
