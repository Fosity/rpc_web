# -*- coding: utf-8 -*-
from utils.form import BaseForm
from utils.field import CharField


class AuthForm(BaseForm):
    username = CharField(func=lambda n: 4<= len(n) <= 30 ,errors="中文名")
    password = CharField(func=lambda n: 4<= len(n) <= 30 ,errors="bac")
    class meta:
        csrf_token = True

class AuthRegisterForm(BaseForm):
    username = CharField(func=lambda n: 4<= len(n) <= 30 ,errors="bac")
    password = CharField(func=lambda n: 4<= len(n) <= 30 ,errors="bac")
    class meta:
        csrf_token = True
