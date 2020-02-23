#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/2/23 23:29
# @Author  : tanxw

#  *_* coding:utf8 *_*
import ctypes
import os
import cv2
import itchat
import numpy
from PIL import ImageGrab
from itchat.content import *

## 安装依赖模块
# pip install itchat
# pip install numpy
# pip install opencv-python

# itchat模块的使用:  https://blog.csdn.net/z_ipython/article/details/93300845
# SystemParametersinfo 用法 : https://www.cnblogs.com/china1/p/3415473.html

# 通过如下命令登陆，即使程序关闭，一定时间内重新开启也可以不用重新扫码。 hotReload 热重载
itchat.auto_login(hotReload=True)

"""
图片或表情（PICTURE）、录制（RECORDING）、附件（ATTACHMENT）、小视频（VIDEO）、文本（TEXT），地图（MAP），名片（CARD），通知（NOTE），分享（SHARING），好友邀请（FRIENDS）、语音（RECORDING）、系统消息（SYSTEM）
"""
print(itchat.get_friends())
boom_obj = itchat.search_friends(nickName=input("请输入对方昵称："))[0]['UserName']

@itchat.msg_register([TEXT, PICTURE, RECORDING, ATTACHMENT, VIDEO])
def info_handle(msg):
    print(msg)
    print(msg["Type"])
    if msg["Type"] == "Text":
        text = msg["Content"]
        # print(itchat.search_friends(remarkName=input("请输入对方昵称")))
        # boom_obj = itchat.search_friends(remarkName=input("请输入对方昵称"))[0]['UserName']
        if text == "拍照":
            capture = cv2.VideoCapture(0)
            ret, frame = capture.read()
            if ret:
                cv2.imwrite("photo.png", frame)
                capture.release()
                print(boom_obj)
                itchat.send_image(fileDir="photo.png", toUserName=boom_obj)
        elif text == "截屏":
            screen = ImageGrab.grab()
            cv2.imwrite("screen.png", numpy.array(screen))

            itchat.send_image(fileDir="screen.png", toUserName=boom_obj)

    elif msg["Type"] == "Picture":
        msg.download(msg["FileName"])

        filepath = os.path.join(os.path.dirname(__file__), msg["FileName"])
        print(filepath)

        # UINT uiAction，UIN T uiParam，PVOID pvParam，UINT fWinlni
        # uiAction: SPI_SETDESKWALLPAPER：设置桌面壁纸。
        # uiParam: 设置失败是否提示
        # pvParam:  查询或设置的系统参数
        # fWinlni:  是否更新用户配置文件,亦或是否要将消息广播给所有顶层窗口，以通知它们新的变化内容
        ctypes.windll.user32.SystemParametersInfoW(20, True, filepath, 0)  # 设置桌面壁纸


itchat.run()