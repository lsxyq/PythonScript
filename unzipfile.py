#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Author:Leslie-x
import itertools as its
import threading
import rarfile
import os

words = '0123456789abcdefghijklmnopqrstuvwxyz'

flag = True


def append_on_file(password):
    with open('password.txt', 'a', encoding='utf8') as f:
        text = password + '\n'
        f.write(text)


def get_password(min_digits, max_digits, words):
    while min_digits <= max_digits:
        pwds = its.product(words, repeat=min_digits)
        for pwd in pwds:
            yield ''.join(pwd)
        min_digits += 1


def extract(File):
    global flag
    while flag:
        p = next(passwords)
        try:
            File.extractall(pwd=p)  ###打开压缩文件,提供密码...
            flag = False
            print("password is " + p)  ###破解到密码
            append_on_file(p)
            break
        except:
            print(p)


def mainStep(file_path):
    file = rarfile.RarFile(file_path)
    for pwd in range(3):
        t = threading.Thread(target=extract, args=(file,))
        t.start()


if __name__ == '__main__':
    base_dir = r'E:\迅雷下载\rar'
    for file_info in os.listdir(base_dir):
        try:
            file_path = os.path.join(base_dir, file_info)
            file_name = file_info.split('.')[0]
            passwords = get_password(4, 11, words)
            mainStep(file_path)
        except:
            pass
