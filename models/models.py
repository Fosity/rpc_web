# -*- coding: utf-8 -*-
import sqlalchemy as sa

meta = sa.MetaData()

users = sa.Table(
    'users', meta,
    sa.Column('id', sa.Integer, primary_key=True),  # 用户名 id
    sa.Column('username', sa.String(255)),  # 用户名
    sa.Column('password', sa.String(255)),  # 密码
    sa.Column('salt', sa.String(255)),  # 密码加密
)

users_to_roles = sa.Table(
    'users_to_roles', meta,
    sa.Column('id', sa.Integer, primary_key=True),  # id
    sa.Column('user_id', sa.Integer),  # user_id
    sa.Column('role_id', sa.Integer)  # role_id
)

roles = sa.Table(
    'roles', meta,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('caption', sa.String(255)),  # 角色名称
    sa.Column('level', sa.Integer)  # menu or api or ui
)
roles_to_permissions = sa.Table(
    'roles_to_permissions', meta,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('role_id', sa.Integer),
    sa.Column('permission_id', sa.Integer)
)

permissions = sa.Table(
    'permissions', meta,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('caption', sa.String(255)),  # 权限名称
    sa.Column('other_caption', sa.String(255)),
    sa.Column('url', sa.String(255)),  # api接口路由  or menu 路由
    sa.Column('ui', sa.String(255)),  # 页面渲染action ui
    sa.Column('menu', sa.String(255)),  # 所属模块
    sa.Column('level', sa.Integer),  # 判断权限是  api or ui or menu
    sa.Column('parent', sa.Integer)  # 如果level 是menu 时候，父亲权限
)

redis_info = sa.Table(
    'redis_info',meta,
    sa.Column('id',sa.Integer,primary_key=True),
    sa.Column('host',sa.String(10)), # redis host
    sa.Column('port',sa.String(10)), # port
    sa.Column('token',sa.String(16)),# redis connection token
    sa.Column('last_connect_time',sa.DateTime)
)

redis_logs = sa.Table(
    'redis_logs',meta,
    sa.Column('id',sa.Integer,primary_key=True), # id
    sa.Column('user_id',sa.Integer),# user_id
    sa.Column('action',sa.Integer), # action  select 0 ,update 1, insert 2, delete 3
    sa.Column('action_string',sa.String(10)), #
    sa.Column('redis_id',sa.Integer), # redis_info_id
    sa.Column('db',sa.Integer), # db num
    sa.Column('key',sa.String(255)),# redis key
    sa.Column('value',sa.String(255)), # redis value
    sa.Column('ttl',sa.Integer),#  -1  or others
)
