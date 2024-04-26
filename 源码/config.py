# encoding:utf-8
import os
import pymysql

DEBUG = False
SECRET_KEY = os.urandom(24)

database = pymysql.connect(host='localhost', user='root', password='20030330zsy', db='bbs', port=3306)

