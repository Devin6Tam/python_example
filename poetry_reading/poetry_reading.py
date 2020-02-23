#!/usr/bin/env python
# -*- coding: utf-8 -*-
# file poetry_reading.py
# pip install baidu-aip
# pip install playsound
# pip install requests
# 古诗文朗读
# 爬虫获取诗文 保存  语音合成  播放

# 模拟客户端数据抓取 AI  NLP
# 输入 文本  输出 音频


# 标记文档 Mark Directory as Source Root，告诉我们导入的包需要从本目录查找
# 从一个工具箱取到某个工具
from speech_convert import generate_speech
from playsound import playsound
import re
import requests
root_url = "https://so.gushiwen.org"
url = "https://so.gushiwen.org/gushi/tangshi.aspx"
# .text 提取网页数据
html = requests.get(url).text

# print(html)

# 提取诗歌网页   xpath bs4 re
# 正则 规则 匹配内容满足留下，不满足就淘汰
# 规则 匹配内容 .* 任意多个字符  . 任意字符  * 任意多个; 原生的特殊符号需要转义 \; () 限定匹配范围
# poetry_urls = re.findall(r"""<span><a href="(.*)" target="_blank">.*</a>\(.*\)</span>""", html)
poetry_urls = re.findall(r'<span><a href="(.*)" target="_blank">.*</a>\(.*\)</span>', html)
print(poetry_urls)
for url in poetry_urls:
	poetry_html = requests.get(root_url+url).text
	# print(root_url+url)
	poetry_infos = re.findall(r"""<textarea style=.*>(.*)——(.*)《(.*)》.*</textarea>""", poetry_html)[0]
	# print(poetry_infos)
	#
	with open("poetry.txt", "a", encoding="utf-8") as f:
		poetry_content = "\n".join(reversed(poetry_infos)) + "\n\n"
		f.write(poetry_content)
	#
	# 语音合成
	generate_speech(poetry_content, "radio/audio" + str(poetry_urls.index(url)) + ".mp3")
	# 播放
	playsound("radio/audio" + str(poetry_urls.index(url)) + ".mp3")


