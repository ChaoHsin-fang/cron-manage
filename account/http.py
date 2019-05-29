# -*- coding: utf-8 -*-
"""
请求登录的http基础方法

Rules:
1. POST/DELETE/PUT: json in - json out, 如果resp.json报错, 则是登录接口问题
2. GET带参数 HEAD不带参数
3. 以统一的header头发送请求
"""

import requests

from django.conf import settings

from common.log import logger


def decorator_http_request(func):
    def return_wrapper(*args, **wkargs):
        try:
            import settings
            verify = True
            if 'DEVELOP' == settings.RUN_MODE:
                verify = False
            result = func(*args, verify=verify, **wkargs)
            return result
        except Exception as e:
            logger.error(str(e.message))

    return return_wrapper


def _gen_header():
    headers = {
        "Content-Type": "application/json",
        "X-APP-CODE": settings.APP_ID,
        "X-APP-TOKEN": settings.APP_TOKEN,
    }
    return headers


@decorator_http_request
def _http_request(method, url, headers=None, data=None, **kwargs):
    try:
        if method == "GET":
            resp = requests.get(url=url, headers=headers, params=data, **kwargs)
        elif method == "HEAD":
            resp = requests.head(url=url, headers=headers, **kwargs)
        elif method == "POST":
            resp = requests.post(url=url, headers=headers, json=data, **kwargs)
        elif method == "DELETE":
            resp = requests.delete(url=url, headers=headers, json=data, **kwargs)
        elif method == "PUT":
            resp = requests.put(url=url, headers=headers, json=data, **kwargs)
        else:
            return False, None
    # except Exception as e:
    #     logger.exception("login http request error! type: %s, url: %s, data: %s" % (method, url, str(data)))
    #     return False, None
    except requests.exceptions.RequestException:
        logger.exception("login http request error! type: %s, url: %s, data: %s" % (method, url, str(data)))
        return False, None
    else:
        if resp.status_code != 200:
            content = resp.content[:100] if resp.content else ''
            logger.error(
                "login http request error! type: %s, url: %s, data: %s, response_status_code: %s, response_content: %s"  # noqa
                % (method, url, str(data), resp.status_code, content))
            return False, None

        return True, resp.json()


def http_get(url, data):
    headers = _gen_header()
    return _http_request(method="GET", url=url, headers=headers, data=data)


def http_post(url, data):
    headers = _gen_header()
    return _http_request(method="POST", url=url, headers=headers, data=data)


def http_delete(url, data):
    headers = _gen_header()
    return _http_request(method="DELETE", url=url, headers=headers, data=data)
