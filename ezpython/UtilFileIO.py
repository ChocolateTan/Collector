#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os


def write_log_to_header(file_name, save_dir, write_content):
    """
    創建/寫模擬器命令 log
    :param save_dir:
    :param file_name:
    :param write_content:
    :return:
    """
    # print write_content
    write_content = str(write_content)
    file_full = save_dir + '/' + file_name
    if not os.path.exists(save_dir):
        print('create dir', save_dir)
        os.makedirs(save_dir)

    if not os.path.exists(file_full):
        print('create file', file_full)
        f = open(file=file_full, mode='w', encoding='UTF-8')
        f.close()
    with open(file=file_full, mode='r+', encoding='UTF-8') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(write_content + '\n' + content)
        f.close()


def write_file(file_name, save_dir, write_content):
    """
    創建/寫模擬器命令 log
    :param save_dir:
    :param file_name:
    :param write_content:
    :return:
    """
    # print write_content
    write_content = str(write_content)
    file_full = save_dir + '/' + file_name

    if not os.path.exists(save_dir):
        print('create dir', save_dir)
        os.makedirs(save_dir)

    if os.path.exists(file_full):
        os.remove(file_full)

    if not os.path.exists(file_full):
        print('create file', file_full)
        f = open(file=file_full, mode='w', encoding='UTF-8')
        f.close()
    with open(file=file_full, mode='r+', encoding='UTF-8') as f:
        # content = f.read()
        f.write(write_content + '\n')
        f.close()
