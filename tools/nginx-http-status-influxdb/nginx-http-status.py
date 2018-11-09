#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: wangziyin
# @Email: mailofwzy@163.com
# @Date:   2018-11-09 09:53:51
# @Last Modified by:   wangziyin
# @Last Modified time: 2018-11-09 17:09:12

import datetime
import os
import socket
import re
import time
import logging
import requests
from influxdb import InfluxDBClient

from settings import UPDATE_INTERVAL, NGINX_REQ_STATUS_URL, NGINX_SUB_STATUS_URL, \
    INFLUXDB_HOST, INFLUXDB_PORT, INFLUXDB_DB_NAME

# InfluxDB
INFLUXDB_HOST = os.environ.get('INFLUXDB_HOST', '127.0.0.1')
INFLUXDB_PORT = int(os.environ.get('INFLUXDB_PORT', 8086))
INFLUXDB_DB_NAME = os.environ.get('INFLUXDB_DB_NAME', 'nginx')

# Update interval
UPDATE_INTERVAL = int(os.environ.get('UPDATE_INTERVAL', 60))

# server_name status统计的时候第一个字段的分隔符
# eg: req_status_zone server_name $host|$scheme|$uri
# 不要使用逗号
separator = "|"

####### Tags ##########
hostname = socket.getfqdn()
region = ""
group = ""
isp = ""

# InfluxDB init
influx_client = InfluxDBClient(host=INFLUXDB_HOST, port=INFLUXDB_PORT, database=INFLUXDB_DB_NAME)

sub_url = NGINX_SUB_STATUS_URL
req_url = NGINX_REQ_STATUS_URL

# 根据自己实际情况生成全局tags
def create_tags():
    __tags = dict(hostname = hostname)
    if region: tags['region'] = region
    if group: tags['group'] = group
    if isp: tags['isp'] = isp
    return __tags

def get_nginx_sub_status(url):
    metrics = {
        'active_connections': None,
        'accepts': None,
        'handled': None,
        'requests': None,
        'reading': None,
        'writing': None,
        'waiting': None,
    }
    try:
        resp = requests.get(url)
    except:
        logging.error('Error getting nginx status by url: %s' % url)
        return None
    text = resp.text

    metrics['active_connections'] = re.search('^Active connections: (\d+)', text).group(1)
    metrics['accepts'], metrics['requests'], metrics['handled'] = re.search('(\d+) (\d+) (\d+)', text).groups()
    metrics['reading'], metrics['writing'], metrics['waiting'] = re.search('Reading: (\d+) Writing: (\d+) Waiting: (\d+) ',
                                                                        text).groups()

    return metrics

def get_nginx_req_status(url):
    status_key = [
        'bytes_in_total',
        'bytes_out_total',
        'conn_total',
        'req_total',
        'code_2xx',
        'code_3xx',
        'code_4xx',
        'code_5xx',
        'code_other',
        'rt_total',
        'upstream_req',
        'upstream_rt',
        'upstream_tries',
        'code_403',
        'code_404',
        'code_499',
        'code_500',
        'code_502',
        'code_503',
        'upstream_4xx',
        'upstream_5xx',
        'upstream_502',
        'upstream_504',
    ]

    status = []

    try:
        resp = requests.get(url)
    except:
        logging.error('Error getting nginx status by url: %s' % url)
        return None
    text = resp.text.split('\n')
    if not text:
        return None
    for line in text:
        tags = {}
        if not line:
            continue
        fields = line.split(',')
        if separator not in fields[0]:
            continue
        _kv = fields[0].split(separator)

        if _kv[0] == "_":
            continue

        tags['host'] = _kv[0]

        if 2 == len(_kv):
            tags['scheme'] = _kv[1]
        elif len(_kv) > 2 and re.match('/', _kv[2]):
            tags['location'] = _kv[2]

        metrics = dict(zip(status_key, fields[1:]))
        status.append({
            'metrics': metrics,
            'tags': tags,
            })

    return status

def get_timestamp():
    return datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')

def create_influx_data(status, json_body):
    _tags = create_tags()
    # sub_status data
    if type(status) is dict:
        json_body.append({
            "measurement": "all_nginx_status",
            "time": get_timestamp(),
            "fields": status,
            "tags": _tags,
        })
    # server_name req status
    else:
        for d in status:
            _tags = dict(_tags, **d['tags'])
            metrics = d['metrics']
            _body = {
                "measurement": _tags.pop('host'),
                "tags": _tags,
                "time": get_timestamp(),
                "fields": metrics,
            }
            json_body.append(_body)

def send_stats_to_db(influx_client, json_body):
    return influx_client.write_points(json_body)

def main():
    try:
        while not time.sleep(UPDATE_INTERVAL):
            json_body = []
            nginx_sub_status = get_nginx_sub_status(sub_url)
            nginx_req_status = get_nginx_req_status(req_url)
            create_influx_data(nginx_sub_status, json_body)
            create_influx_data(nginx_req_status, json_body)
            if not send_stats_to_db(influx_client, json_body):
                logging.error("Send metrics to influxdb error")
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
