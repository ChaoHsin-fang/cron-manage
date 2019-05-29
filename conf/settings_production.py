# -*- coding: utf-8 -*-
"""
用于正式环境的全局配置
"""
import logging

from settings import APP_ID
import os

# ===============================================================================
# 数据库设置, 本地开发境数据库设置
# ===============================================================================
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',  # 默认用mysql
#         'NAME': APP_ID,                        # 数据库名 (默认与APP_ID相同)
#         'USER': 'root',                            # 你的数据库user
#         'PASSWORD': 'mz0712',                        # 你的数据库password
#         'HOST': '127.0.0.1',                   		   # 数据库HOST
#         'PORT': '3306',                        # 默认3306
#     },
# }

# 测试环境数据库
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # 默认用mysql
        'NAME': APP_ID,                        # 数据库名 (默认与APP_ID相同)
        'USER': 'root',                        # 你的数据库user
        'PASSWORD': '123456',                        # 你的数据库password
        'HOST': '10.20.11.119',                   # 开发的时候，使用localhost
        'PORT': '3306',                        # 默认3306
    },
}
# 数据库设置, 正式环境数据库设置
# ===============================================================================
# DB_USERNAME = os.environ.get('BKAPP_DB_USERNAME', '')
# DB_PASSWORD = os.environ.get('BKAPP_DB_PASSWORD', '')
# DB_HOST = os.environ.get('BKAPP_DB_HOST', '')
# DB_PORT = os.environ.get('BKAPP_DB_PORT', '')
#
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',  # 默认用mysql
#         'NAME': APP_ID,  # 数据库名 (默认与APP_ID相同)
#         'USER': os.environ.get('DB_USERNAME', DB_USERNAME),
#         'PASSWORD': os.environ.get('DB_PASSWORD', DB_PASSWORD),
#         'HOST': os.environ.get('DB_HOST', DB_HOST),
#         'PORT': os.environ.get('DB_PORT', DB_PORT),
#     }
# }
# logging.info(APP_ID)
