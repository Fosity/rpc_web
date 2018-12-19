# -*- coding: utf-8 -*-

mode = 'development'

#### redis ########
redis_host = "127.0.0.1"
redis_port = 6379
redis_db = 4
redis_expire = 60 * 60 * 24

################  mysql ###############
database = {
    'db': 'baseuser',
    'user': 'root',
    'host': '127.0.0.1',
    'port': 3306,
    'password': 'qqqwwweee123@@'
}

############## token #################
token_header = "sc_school"
token_expire = 60 * 60 * 6  # 6hours

################# others ################
white_url = ['/login', '/csrf', '/register']
auth = "auth:"
csrf = "csrf:"
csrf_name = "_csrf"
csrf_expire = 15

#################  csrf ###############
csrf_redis_path = "csrf:redis:path:"
