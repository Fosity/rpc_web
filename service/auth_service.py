# -*- coding: utf-8 -*-
import hashlib
import logging
import uuid

import sqlalchemy as sa

from models.models import users, users_to_roles, roles, permissions, roles_to_permissions
from utils.res import Res


class Auth:
    def __init__(self, request):
        self.redis_pool = request.app.redis_pool
        self.db = request.app.db

    async def __salt__(self):
        return uuid.uuid1()

    async def __encrypt_pwd__(self, salt, pwd):
        return hashlib.sha1(
            "{0}{1}{2}".format(pwd, salt, "______sc_school________").encode(encoding="utf-8")).hexdigest()

    async def login(self, name, password):

        async with self.db.acquire() as conn:
            user =await (await conn.execute(
                sa.select([users.c.password, users.c.salt, users.c.id]).where(users.c.username == name))).fetchone()
            if user is not None:
                salt = user[1]
                old_password = user[0]
                new_password =await self.__encrypt_pwd__(salt, password)
                if old_password == new_password:
                    return True, user[2]
            # return False, None
            return False, user[2]

    async def register(self, username, password, **kwargs):
        salt = str(await self.__salt__())
        new_password =await self.__encrypt_pwd__(salt=salt, pwd=password)
        async with self.db.acquire() as conn:
            resp = await conn.execute(users.insert().values(password=new_password,username = username,salt = salt))
            return resp
    async def get_user_permission(self, user_id):
        async with self.db.acquire() as conn:
            roles_resp =await (await conn.execute(sa.select([roles.c.caption]).where(users_to_roles.c.user_id == user_id).where(
                users_to_roles.c.role_id == roles.c.id))).fetchall()
            roles_detail =await (await conn.execute(
                sa.select(
                    [permissions]
                ).where(
                    permissions.c.id == roles_to_permissions.c.permission_id
                ).where(
                    roles_to_permissions.c.role_id == users_to_roles.c.role_id
                ).where(
                    users_to_roles.c.user_id == user_id
                ).where(
                    roles.c.id == users_to_roles.c.role_id
                ).where(
                    permissions.c.level != 1
                ).group_by(permissions.c.caption)
            )).fetchall()
            msg = Res()
            msg.roles = []
            list_ = []
            for role in roles_resp:
                msg.roles.append(role[0])
            for role_detail in roles_detail:
                dict_ = {role_detail.menu: role_detail.caption}
                list_.append(dict_)
            new_dict =await self._rewrite_roles_details(list_)
            msg.roles_detail = new_dict
            return msg.dict()

    async def _rewrite_roles_details(self, list_):
        """
        list_=[{'A': 'A'},{'A': 'A:query'},{'A': 'A:show'},{'B': 'B'}，{'B': 'B:query'}，{'B': 'B:show'}]
        to =[{'A': 'A'},{'B': 'B'}]
        :param list_:
        :return:
        """
        sum_ = []
        new_dict = {}
        list_.sort(key=lambda x: str(x.values()))
        for items in list_:
            key = list(items.keys())[0]
            value = list(items.values())[0]
            split_list = value.split(":")
            if new_dict.get(key) is not None:
                new_dict[key].append(split_list[1])
            else:
                new_dict[key] = []
                new_dict[key].append(split_list[1])
        return new_dict

    async def get_router_map(self):
        async with self.db.acquire() as conn:
            resp = await (await conn.execute(
                sa.select([permissions.c.url,roles.c.caption]).where(
                    permissions.c.level ==1
                ).where(
                    permissions.c.id == roles_to_permissions.c.permission_id
                ).where(
                    roles_to_permissions.c.role_id == roles.c.id
                )
            )).fetchall()
            resp = self._rewrite_router_map(resp)
            return resp

    def _rewrite_router_map(self, resp):
        """
        resp = [('/permission/A', 'a'), ('/permission/B', 'b'), ('/permission', 'p')]
        :param resp:
        :return:
        """
        router_map = []
        url_ = {}
        for items in resp:
            url = items[0]
            role = items[1]
            url_list = url.split("/")
            if len(url_list) == 2:
                if url_.get(url_list[1]) and url_.get(url_list[1]).get('roles') or url_.get(url_list[1]).get(
                        'roles') is not list:
                    url_[url_list[1]]['roles'].append(role)
                else:
                    url_[url_list[1]] = {}
                    url_[url_list[1]]['roles'] = [role]
            elif len(url_list) > 2:
                if url_.get(url_list[1]):
                    if url_.get(url_list[1]).get(url_list[2]) and url_.get(url_list[1]).get(url_list[2]).get('roles'):
                        url_[url_list[1]][url_list[2]]['roles'].append(role)
                    else:
                        url_[url_list[1]][url_list[2]] = {}
                        url_[url_list[1]][url_list[2]]['roles'] = [role]
                else:
                    url_[url_list[1]] = {}
                    url_[url_list[1]]['roles'] = []
                    url_[url_list[1]][url_list[2]] = {}
                    url_[url_list[1]][url_list[2]]['roles'] = [role]
        for key, items in url_.items():
            dict_ = {
                'path': '/' + key,
                'meta': {
                    'roles': items.get('roles')
                },
                'children': []
            }
            for k, v in items.items():
                if k == 'roles':
                    continue
                dict_c = {
                    'path': k,
                    'meta': {
                        'roles': v.get('roles')
                    }
                }
                if dict_.get('meta').get('roles') and dict_c.get('meta').get('roles') and dict_.get('meta').get(
                        'roles') not in dict_c.get('meta').get('roles'):
                    for items in dict_.get('meta').get('roles'):
                        dict_c.get('meta').get('roles').append(items)

                dict_['children'].append(dict_c)
            router_map.append(dict_)
        return router_map
