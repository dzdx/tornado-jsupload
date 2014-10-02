#!/usr/bin/env python
# -*- coding: utf8 -*-
import base64
import os
from configs.config import upload_success
from library import myFunc


class Upload_service:
    def __init__(self, handler):
        self.handler = handler

    def uploadStart(self, filename):
        name, ext = os.path.splitext(filename)
        temp_file_name = myFunc.getRandomStr(40)
        self.handler.set_secure_cookie("temp_file_name", temp_file_name)
        self.handler.set_secure_cookie('fileext', ext)
        upload_success = set()

        for i in range(0, 5):
            filePath = os.path.join(myFunc.getUploadPath(), '%s_%s' % (temp_file_name, i))
            f = open(filePath, 'wb')
            f.write('')
            f.close()

        return {'state': 'success', 'data': ''}

    def uploadBlog(self, no, data):
        data = base64.decodestring(data)
        temp_file_name = self.handler.get_secure_cookie("temp_file_name")
        filePath = os.path.join(myFunc.getUploadPath(), '%s_%s' % (temp_file_name, no))
        f = open(filePath, 'ab')
        f.write(data)
        f.close()
        return {'state': 'success', 'data': ''}

    def uploadEnd(self, no):
        upload_success.add(no)
        if len(upload_success) == 5:
            self.mergeFile()
            return {'state': 'success', 'data': 'all_success'}
        else:
            return {'state': 'success', 'data': 'wait'}

    def mergeFile(self):
        print('ok')