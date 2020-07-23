# coding=utf8
import json

import requests


def post(url, api, param):
    r = requests.post(url=url + api, json=param)
    res = json.loads(r.content.decode("utf-8"))
    data = {'header': dict(r.headers), 'status': r.status_code, 'content': res, 'url': r.url}
    return data


def post_param(url, api, param):
    r = requests.post(url=url + api, json=param, params=param)
    try:
        res = json.loads(r.content.decode("utf-8"))
    except Exception as ex:
        res = r.content.decode("utf-8")
    data = {'header': dict(r.headers), 'status': r.status_code, 'content': res, 'url': r.url}
    return data


def get(url, api, param):
    r = requests.get(url=url + api, params=param)
    res = json.loads(r.content.decode("utf-8"))
    data = {'header': dict(r.headers), 'status': r.status_code, 'content': res, 'url': r.url}
    return data


def print_response(r):
    if r >= 500:
        return "Server error!!!"
    elif r >= 400:
        return "Client error!!!"
    elif r >= 300:
        return "Redirects!!!"
    elif r >= 200:
        return "Success!!!"
    elif r >= 100:
        return "Informational!!!"
