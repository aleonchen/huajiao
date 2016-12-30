# -*- coding: utf-8 -*-
# @Author: fasthro
# @Date:   2016-12-29 21:14:57
# @Last Modified by:   fasthro
# @Last Modified time: 2016-12-29 21:14:57

import urllib2
import requests
import re
from lxml import etree
import bs4


'''
 抓取花椒直播网主播个人相关数据
'''


class Huajiao():
    def __init__(self):
        pass

    def get_hot(self):
        '''
        抓取热门推荐
        :return:
        '''

        t_url = 'http://www.huajiao.com/category/1000'
        parme = ''
        page_total = 0

        # 分析总页数
        page_total = self.get_total_page(t_url)

        page = page_total
        #分析每一页的具体数据
        url_list = ['http://www.huajiao.com/category/1000?pageno={page}'.format(page) for page in range(1, page + 1)]
        print url_list

    def get_total_page(self, url):
        '''

        
        获取目标总页数
        :param url:
        :return:
        '''
        num_html = requests.get(url).content
        num_tree = etree.HTML(num_html).xpath('.//div[@id="doc-bd"]//div[@class="container clearfix"]//ul/li')
        if len(num_tree) > 0:
            num_env = num_tree[len(num_tree) - 1]
            page_total = num_env.get("tabindex")
            return int(page_total)
        return 1

if __name__ == "__main__":
    client = Huajiao()
    client.get_hot();