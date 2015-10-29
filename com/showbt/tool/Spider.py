import os
import urllib
import uuid

__author__ = 'www.showbt.com'
# -*- coding:utf-8 -*-

# import urllib
import urllib2
import re

# import os

class Spider(object):
    def __init__(self, url, root=None):
        self.url = url
        self.root = root

    def getHtml(self, url):
        print(url)
        try:
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            res = response.read()
        except Exception, e:
            print(e)
            return None
        return res

    def getPage(self, page_str):
        url_str = self.url + page_str
        return self.getHtml(url_str)

    def getList(self, page_str, pattern):
        html_content = self.getPage(page_str)
        return self.resolveHtml(html_content, pattern)

    def getDetail(self, detail_url, pattern):
        detailContent = self.getHtml(detail_url)
        return self.resolveHtml(detailContent, pattern)

    def resolveHtml(self, content, pattern):
        items = re.findall(re.compile(pattern, re.S), content)
        contents = []
        for item in items:
            contents.append(item)
        return contents

    def searchHtml(self, content, pattern):
        return re.search(re.compile(pattern, re.S), content).group(1)

    def saveImage(self, image_url, file_path, file_name=None):
        if self.root is not None:
            data = urllib.urlopen(image_url)
            if file_name is None:
                extend_name = image_url.split('.')
                file_name = str(uuid.uuid1()).replace('-', '') + '.' + extend_name.pop()
            path = self.root + file_path
            self.mkdir(path)
            with open(path + file_name, 'wb') as f:
                f.write(data.read())

    def mkdir(self, file_path):
        file_path = file_path.strip()
        is_exists = os.path.exists(file_path)
        if not is_exists:
            os.mkdir(file_path)
            return True
        else:
            return False



