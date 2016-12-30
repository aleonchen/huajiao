# -*- coding: utf-8 -*-
# @Author: fasthro
# @Date:   2016-12-29 21:14:57
# @Last Modified by:   fasthro
# @Last Modified time: 2016-12-29 21:14:57

import requests
from lxml import etree
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

'''
 抓取花椒直播网主播个人相关数据
'''

class ZbData():
    def __init__(self):
        # 昵称
        self.nickname = None
        # 主页连接
        self.href = None
        # 主页宣传图片
        self.img_src = None
        # 作者id
        self.author_id = None
        # 关注
        self.follow = None
        # 粉丝数量
        self.fans = None
        # 赞
        self.praises = None
        # 花椒币
        self.gold = None
        # 观看人数
        self.watches = None

    def __str__(self):
        return "昵称：%s\n作者ID：%s\n关注：%s\n粉丝：%s\n赞：%s\n花椒币：%s" %(self.nickname, self.author_id, self.follow, self.fans, self.praises, self.gold)



class Huajiao():
    def __init__(self):
        self.num = 0
        self.zb_data_list = {}

    def get_data(self):

        self.num = 0

        hot = 'http://www.huajiao.com/category/1000'
        god = 'http://www.huajiao.com/category/2'
        talent = 'http://www.huajiao.com/category/666'
        school = 'http://www.huajiao.com/category/999'

        music_talent = 'http://www.huajiao.com/category/1001'
        network_performance = 'http://www.huajiao.com/category/5'
        entertainment_stars = 'http://www.huajiao.com/category/1'

        print "热门推荐"
        self.get_zb(hot)
        print "女神驾到"
        self.get_zb(god)
        print "才艺主播"
        self.get_zb(talent)
        print "校园女生"
        self.get_zb(school)
        print '音乐达人'
        self.get_zb(music_talent)
        print "网络表演"
        self.get_zb(network_performance)
        print "娱乐明星"
        self.get_zb(entertainment_stars)

        for i in self.zb_data_list:
            self.get_zb_data(i)
            print str(self.zb_data_list[i]) + "\n"

        print "一共抓取%s个主播" % self.num

    def get_zb(self, t_url):
        '''
        抓取花椒主播列表
        :param t_url:
        :return:
        '''
        page_total = 0

        # 分析总页数
        page_total = self.get_total_page(t_url)

        page = 0
        #分析每一页的具体数据
        url_list = [t_url + '?pageno={page}'.format(page = page) for page in range(1, page_total + 1)]

        for p_url in url_list:
            p_html = requests.get(p_url).content
            p_tree = etree.HTML(p_html).xpath('.//div[@class="box-bd"]//ul//li[@class="item"]')
            for child in p_tree:
                try:
                    href = child.xpath('.//div/a')[0].get("href")
                    img_src = child.xpath('.//div/a//div[@class="pic"]/img')[0].get("src")

                    zbd = ZbData()
                    zbd.img_src = img_src
                    zbd.href = href

                    self.zb_data_list[href] = zbd
                    self.num += 1
                except:
                    print '获取主播列表出错[%s]' % p_url



    def get_zb_data(self, zb_href):

        utl = 'http://www.huajiao.com' + zb_href
        '''
        抓取每个主播数据
        :return:
        '''
        html = requests.get(utl).content
        tree_html = etree.HTML(html)

        #基本数据解析
        anthor_info = tree_html.xpath('.//div[@id="doc-bd"]//div[@id="author-info"]')[0]
        nickname = anthor_info.xpath('.//div[@class="base-info"]//a')[0].xpath('string()')
        author_id = anthor_info.xpath('.//div[@class="base-info"]//p[@class="author-id"]')[0].xpath('string()')
        follow = anthor_info.xpath('.//div[@class="counts clearfix"]//div[@class="follows"]/h4')[0].xpath('string()')
        fans = anthor_info.xpath('.//div[@class="counts clearfix"]//div[@class="fans"]/h4')[0].xpath('string()')
        praises = anthor_info.xpath('.//div[@class="counts clearfix"]//div[@class="praises"]/h4')[0].xpath('string()')

        gold = anthor_info.xpath('.//div[@class="currency hide"]/strong')[0].xpath('string()')
        watches = anthor_info.xpath('.//div[@class="watches"]/strong')[0].xpath('string()')

        if self.zb_data_list[zb_href]:
            self.zb_data_list[zb_href].nickname = nickname.strip()
            self.zb_data_list[zb_href].author_id = author_id
            self.zb_data_list[zb_href].follow = follow
            self.zb_data_list[zb_href].fans = fans
            self.zb_data_list[zb_href].praises = praises
            self.zb_data_list[zb_href].gold = gold
            self.zb_data_list[zb_href].watches = watches


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
    client.get_data()