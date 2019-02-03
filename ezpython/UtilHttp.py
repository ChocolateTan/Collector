#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import urllib

import requests


def get(url):
    return requests.get(url, timeout=10)


def post(url, data=None, files=None):
    if data is None and files is None:
        return requests.post(url)
    elif data is not None and files is None:
        return requests.post(url, data=data)
    elif data is None and files is not None:
        return requests.post(url, files=files)
    elif data is not None and files is not None:
        return requests.post(url, data=data, files=files)
    else:
        return requests.post(url)


def download_file(file_dirs, url, file_name):
    """
    網絡下載到本地 pc
    :param file_dirs:
    :param url:
    :param file_name:
    :return:
    """
    file_path = file_dirs + '/' + file_name
    if not os.path.exists(file_dirs):
        os.makedirs(file_dirs)
    # 下载图片，并保存到文件夹中
    urllib.urlretrieve(url, filename=file_path)
