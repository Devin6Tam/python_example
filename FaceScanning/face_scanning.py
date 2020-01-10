#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/1/9 15:00
# @Author  : tanxw
# opencv-python 开源框架--> python java C C++
# pip install opencv-python
import cv2

# 创建视频捕捉
cap = cv2.VideoCapture(0)

# 窗口名称
face_window = 'face_window'
# 创建一个窗口
cv2.namedWindow(face_window)

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

while True:
    # 读取视频 --> 矩形数组
    ret, frame = cap.read()
    print(ret,frame)
    # 如果没有采集到人脸数据
    if not ret:
        continue

    # 设置灰色的背景
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # 开启人脸扫描
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 1)

    # 人脸显示
    cv2.imshow(face_window, frame)

    # 等待输入
    keyvalue = cv2.waitKey(1)

    if keyvalue == ord('q'):
        break

cv2.destroyAllWindows()
cap.release()
