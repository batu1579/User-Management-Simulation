#!/usr/bin/env python
# coding=utf-8
'''
Author: BATU1579
CreateDate: 2022-06-28 22:30:19
LastEditor: BATU1579
LastTime: 2022-06-28 23:55:56
FilePath: \\src\\util\\controller.py
Description: 交互控制器
'''
from abc import ABCMeta, abstractmethod
from os import system
from pynput.keyboard import Listener, Key


class InputController(metaclass=ABCMeta):
    def __init__(self, title: str, data: list[str] = None):
        self.title = title
        self.data = data

    def show_title(self):
        print(f"{'=' * 15} {self.title} {'=' * 15}\n")

    @abstractmethod
    def get_input(self): pass


class Form(InputController):
    def get_input(self):
        self.show_title()
        return {question: input(f"[{question}]: ") for question in self.data}


class SingleChoice(InputController):
    def get_input(self):
        pitch_on = 0

        self._show_choice(pitch_on)

        def check():
            '''
            pitch_on 的边界检查
            '''
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
            if key == Key.enter or key == Key.esc:
                return False
            check()
            self._show_choice(pitch_on)

        with Listener(on_press=on_press) as listener:
            listener.join()

        return pitch_on

    def _show_choice(self, pitch_on: int):
        assert 0 <= pitch_on < len(self.data), "pitch on number is out of range"

        # 显示选项
        system("cls")

        self.show_title()

        if type(self.data[0]) == dict:
            for index, choice in enumerate(self.data):
                if index == pitch_on:
                    print(f" => {choice['title']} - {choice['info']}")
                else:
                    print(f"    {choice['title']}")
        else:
            for index, choice in enumerate(self.data):
                print(f"{' => ' if index == pitch_on else '    '} {choice}")


def main():
    controller = SingleChoice("title", [
        "A", "B", "C", "D", "E", "F"
    ])
    controller.get_input()


if __name__ == "__main__":
    main()
