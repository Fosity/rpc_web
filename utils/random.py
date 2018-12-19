# -*- coding: utf-8 -*-
import hashlib
import random
import string
import time


def random_eight_password():
    """随机生成八位密码，其中一定包含数字，小写字符，大写字母"""
    src = string.ascii_letters + string.digits
    list_passwd = random.sample(src, 5)  # 从字母和数字中随机取5位
    list_passwd.extend(random.sample(string.digits, 1))  # 让密码中一定包含数字
    list_passwd.extend(
        random.sample(string.ascii_lowercase, 1))  # 让密码中一定包含小写字母
    list_passwd.extend(
        random.sample(string.ascii_uppercase, 1))  # 让密码中一定包含大写字母
    random.shuffle(list_passwd)  # 打乱列表顺序
    str_passwd = ''.join(list_passwd)  # 将列表转化为字符串
    return str_passwd


def random_ten_str():
    def str_md5(url):
        result = hashlib.md5(url.encode(encoding='utf8')).hexdigest()
        return result

    time_now = time.time()
    str = "{0}{1}".format(random_eight_password(), time_now)
    str_ = str_md5(str)
    return str_


def str_md5(str):
    result = hashlib.md5(str.encode(encoding='utf8')).hexdigest()
    return result
