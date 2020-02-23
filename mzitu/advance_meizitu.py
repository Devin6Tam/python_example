# *_* coding:utf8 *_*
# @Desc 仅作为练习，学习示例，借鉴时请遵守爬虫有关法律规定
import random
import requests
import os
import re
from threading import Thread
from multiprocessing import Queue, Process

import time
import socket

# 设置socket 默认超时时间
socket.setdefaulttimeout(20)

# 开启队列
q = Queue()

# 爬取图片对象
class CrawlImage(object):
    def __init__(self, url, header):
        self.current_page_url = url
        self.header = header
        self.resource_urls = []
        self.GET_NULL_LIMIT = 3
        self.current_null_times = 0
        self.is_dormancy = False
        self.dormancy_time = 30

    # 获取当前爬取页面数据
    def get_current_page_data(self):
        if self.current_page_url:
            print("\n请求网页 {}  数据".format(self.current_page_url))
            response = requests.get(self.current_page_url, headers=self.header)
            response.close()
            response_content = response.text
            time.sleep(random.random())
            ret = re.search(r"""<a class="next page-numbers" href="(.*?)">下一页&raquo;</a>""", response_content)
            if ret:
                self.current_page_url = ret.group(1)
            else:
                self.current_page_url = None

            return response_content
        else:
            return ""

    # 获取图片链接地址
    def get_image_url(self, q):
        print(">>>>>>>>> 开始获取图片网址 <<<<<<<<<")
        while True:
            response = self.get_current_page_data()
            resource_urls = re.findall(r"data-original='(.*?)'", response)
            if resource_urls:
                q.put(resource_urls)
                self.resource_urls.extend(resource_urls)
            else:
                q.put(None)
                break

    # 静态方法，保存图片资源信息
    @staticmethod
    def save_resource(content, save_path):
        with open(save_path, "wb") as f:
            f.write(content)

    # 执行下载图片任务
    def execute_download(self, image_url, save_dir):
        response = requests.get(image_url, headers=self.header)
        response.close()
        image_name = image_url.split('/')[-1]
        save_path = os.path.join(save_dir, image_name)
        image_data = response.content

        if image_data:
            self.save_resource(image_data, save_path)
            print("{} 完成下载".format(image_name))
            self.is_dormancy = False
            self.current_null_times = 0
        elif self.current_null_times < self.GET_NULL_LIMIT:
            self.current_null_times += 1
            print("[INFO]: 图片 {} 获取失败! 数据请求网址 {} ".format(image_name, image_url))
        else:
            self.current_null_times += 1
            print("[INFO]: 图片 {} 获取失败! 数据请求网址 {} ".format(image_name, image_url))
            self.is_dormancy = True

    # 开始图片下载--开启线程执行下载
    def start_download_image(self, save_dir, q):
        print("************ 开始下载图片 *************")
        while True:
            image_urls = q.get()
            if not image_urls:
                break

            if self.is_dormancy:
                print("[WARRING]: 获取数据错误次数超阈值次!")
                print("[WARRING]: 被服务器发现了,图片下载休眠 {} 秒钟.....".format(self.dormancy_time))
                time.sleep(self.dormancy_time)
                if self.current_null_times > self.GET_NULL_LIMIT * 3:
                    print("[ERROR]: 程序退出!")
                    os.kill(os.getppid(), 9)
                    os.kill(os.getpid(), 9)
                    exit()

            for image_url in image_urls:
                Thread(target=self.execute_download, args=(image_url, save_dir)).start()
                time.sleep(random.random() / 10)

    # 开启进程--获取图片链接地址，执行图片下载任务
    def download_image(self, save_dir):
        Process(target=self.get_image_url, args=(q,)).start()
        Process(target=self.start_download_image, args=(save_dir, q)).start()




mz_url = "https://www.mzitu.com/"
mz_header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
    "Referer": "https://www.mzitu.com/",
}

if __name__ == '__main__':
    mz_image = CrawlImage(mz_url, mz_header)
    mz_image.download_image("images")
    # 开启线程等待，以便爬去图片继续进行
    while True:
        time.sleep(1000)
