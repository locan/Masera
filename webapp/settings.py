# -*- coding:utf-8 -*-
import os

SQLALCHEMY_ECHO = False
SQLALCHEMY_DATABASE_URI = "mysql://root:1q2w3e4r5t6y@127.0.0.1:3306/masera_db?charset=utf8mb4"
SQLALCHEMY_COMMIT_ON_TEARDOWN = True

APP_PATH = '%s/views' % os.path.dirname(os.path.abspath(__file__))