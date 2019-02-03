# -*- coding: utf-8 -*-
import re
import tempfile

import os
import xml.etree.cElementTree as ET


class UtilAdbElement(object):
    """
    通过元素定位,需要Android 4.0以上
    """

    def __init__(self, adb_target, dump_dir, pull_dir, xml_name):
        """
        初始化，获取系统临时文件存储目录，定义匹配数字模式
        """
        self.pattern = re.compile(r"\d+")
        self.adb_target = adb_target
        self.dump_dir = dump_dir + '/' + xml_name
        self.pull_dir = pull_dir + '/' + xml_name
        self.xml_name = xml_name
        if not os.path.exists(pull_dir):
            print 'create dir', pull_dir
            os.makedirs(pull_dir)

    def uidump(self):
        """
        获取当前Activity控件树
        """
        os.popen('adb -s {0} shell uiautomator dump {1}'.format(self.adb_target, self.dump_dir)).close()
        os.popen('adb -s {0} pull {1} {2}'.format(self.adb_target, self.dump_dir, self.pull_dir)).close()

    def element(self, attrib, name):
        """
        同属性单个元素，返回单个坐标元组
        """
        self.uidump()
        tree = ET.ElementTree(file=self.pull_dir)
        tree_iter = tree.iter(tag="node")
        for elem in tree_iter:
            if elem.attrib[attrib] == name:
                bounds = elem.attrib["bounds"]
                coord = self.pattern.findall(bounds)
                x_point = (int(coord[2]) - int(coord[0])) / 2.0 + int(coord[0])
                y_point = (int(coord[3]) - int(coord[1])) / 2.0 + int(coord[1])

                return x_point, y_point

        return None

    def elements(self, attrib, name):
        """
        同属性多个元素，返回坐标元组列表
        """
        list = []
        self.uidump()
        tree = ET.ElementTree(file=self.pull_dir)
        tree_iter = tree.iter(tag="node")
        for elem in tree_iter:
            if elem.attrib[attrib] == name:
                bounds = elem.attrib["bounds"]
                coord = self.pattern.findall(bounds)
                x_point = (int(coord[2]) - int(coord[0])) / 2.0 + int(coord[0])
                y_point = (int(coord[3]) - int(coord[1])) / 2.0 + int(coord[1])
                list.append((x_point, y_point))
        return list

    def public_find_element_by_name(self, name):
        """
        通过元素名称定位
        usage: findElementByName(u"相机")
        """
        return self.element("text", name)

    def public_find_elements_by_name(self, name):
        return self.elements("text", name)

    def public_find_element_by_class(self, class_name):
        """
        通过元素类名定位
        usage: findElementByClass("android.widget.TextView")
        """
        return self.element("class", class_name)

    def public_find_elements_by_class(self, class_name):
        return self.elements("class", class_name)

    def public_find_element_by_id(self, id):
        """
        通过元素的resource-id定位
        usage: findElementsById("com.android.deskclock:id/imageview")
        """
        return self.element("resource-id", id)

    def public_find_elements_by_id(self, id):
        return self.elements("resource-id", id)

    def public_find_element_by_content_desc(self, content_desc):
        """
        通过元素的content-desc定位
        usage: findElementsById("More options")
        """
        return self.element("content-desc", content_desc)

    def public_find_elements_by_content_desc(self, content_desc):
        return self.elements("content-desc", content_desc)
