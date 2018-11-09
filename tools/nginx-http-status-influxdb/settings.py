#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: wangziyin
# @Email: wangziyin@corp.netease.com
# @Date:   2018-11-09 11:07:36
# @Last Modified by:   wangziyin
# @Last Modified time: 2018-11-09 14:11:51

import os

# NGINX API location
# NGINX API location
NGINX_STATUS_HOST = os.environ.get('NGINX_STATUS_HOST', '127.0.0.1')
NGINX_REQ_STATUS_PORT = os.environ.get('NGINX_REQ_STATUS_PORT', '8080')
NGINX_REQ_STATUS_ENDPOINT = os.environ.get('NGINX_REQ_STATUS_ENDPOINT', 'req-status')

NGINX_SUB_STATUS_PORT = os.environ.get('NGINX_SUB_STATUS_PORT', '8080')
NGINX_SUB_STATUS_ENDPOINT = os.environ.get('NGINX_SUB_STATUS_ENDPOINT', 'nginx_status')

NGINX_REQ_STATUS_URL = os.environ.get('NGINX_REQ_STATUS_URL',
        'http://{host}:{port}/{endpoint}'.format(host = NGINX_STATUS_HOST,
                                            port =  NGINX_REQ_STATUS_PORT,
                                            endpoint = NGINX_REQ_STATUS_ENDPOINT))

NGINX_SUB_STATUS_URL = os.environ.get('NGINX_SUB_STATUS_URL',
        'http://{host}:{port}/{endpoint}'.format(host = NGINX_STATUS_HOST,
                                            port =  NGINX_SUB_STATUS_PORT,
                                            endpoint = NGINX_SUB_STATUS_ENDPOINT))

# InfluxDB
INFLUXDB_HOST = os.environ.get('INFLUXDB_HOST', '127.0.0.1')
INFLUXDB_PORT = int(os.environ.get('INFLUXDB_PORT', 8086))
INFLUXDB_DB_NAME = os.environ.get('INFLUXDB_DB_NAME', 'nginx')

# Update interval
UPDATE_INTERVAL = int(os.environ.get('UPDATE_INTERVAL', 60))


try:
    from local_settings import *
except ImportError:
    pass
