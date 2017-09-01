# -*- coding:utf-8 -*-
import os

SQLALCHEMY_ECHO = False
SQLALCHEMY_DATABASE_URI = "mysql://root:tianyan123@36.110.212.164:13306/masera_db?charset=utf8mb4"
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SECRET_KEY = "test"
APP_PATH = '%s/views' % os.path.dirname(os.path.abspath(__file__))
