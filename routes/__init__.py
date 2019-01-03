# -*- coding: utf-8 -*-
from api import AuthLogin,CsrfProtection,AuthRegister,AuthLogout,AuthRouterMap,AuthInfo


def setup_routes(app):
    # 注册路由
    app.router.add_route('*', '/login', AuthLogin)
    app.router.add_route('*', '/logout', AuthLogout)
    app.router.add_route('*', '/register', AuthRegister)
    app.router.add_route('*', '/csrf', CsrfProtection)
    app.router.add_route('*', '/router_map', AuthRouterMap)
    app.router.add_route('*', '/user_info', AuthInfo)

