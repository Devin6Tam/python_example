"""
============================
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/1/9 15:00
# @Author  : tanxw
# @Desc    : 幻听网-有声小说
============================
"""
from urllib.parse import urljoin
from lxml import etree
import re
import requests

def downs(url):
    headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'

    }
    for i in range(1, 452):
        ss = '大明王侯'
        nsss = ss+str(i)
        response = requests.get(url, headers=headers)
        response.encoding = 'gb2312'
        # print(response.text)
        # dems = etree.HTML(response.text)
        # # print(dems)
        # nodos = dems.xapth('')
        # print(nodos)
        ns = re.findall(r'''<script>var param=getAspParas.*;var datas=(.*).split.*;</script>''',response.text)
        # print(ns)
        nss = str(ns)[4:54]
        # print(nss)

        with open('有声小说/{}.mp3'.format(nsss), 'wb')as f :
            music = requests.get(nss)
            f.write(music.content)
            print('%s下载完毕'%nsss)


def urlm():
    urls = 'http://www.ting89.com'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'

    }
    url_s = 'http://www.ting89.com/books/11165.html'
    response = requests.get(url_s, headers=headers)
    response.encoding = 'gb2312'
    # print(response.text)
    dom = etree.HTML(response.text)
    # print(dom)
    nodes = dom.xpath('//div[@class="compress"]/ul/li')
    # print(nodes)
    url_list = []
    for node in nodes:
        dic = {}
        dic['title'] = node.xpath('./a/text()')[0]
        dic['url'] = urljoin(urls, node.xpath('./a/@href')[0])
        url_list.append(dic['url'])
    urls = url_list[0:452]
    for url in urls:
        # print(url)
    # for url in url_list:
    #     if 'playbook' in url:
    #         print(url)
        downs(url)
urlm()









