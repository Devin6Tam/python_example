#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/1/9 15:00
# @Author  : tanxw
# pip install pygame
# 标记 aiplayer 选中右键 Mark Directory as --> Source Root

from aip_gesture_recognition import gesture_recognition
# 混频器
from pygame import mixer
import os


# 音乐播放路径  当前正在播放的序号  音量
music_paths, music_no, volume = [], 0, 0.2

music_names = os.listdir("music")

print(music_names)

for name in music_names:
    music_paths.append("music/"+name)

music_count = len(music_paths)

# 初始化播放器
mixer.init()

"""
手势识别功能描述：

    手势                                识别结果                            功能设置
    ---------------------------------------------------------------------------------------------
    ok                                    "1"                               播放
    竖中指                                 "2"                               暂停
    6                                     "3"                               继续播放
    点赞                                  "4"                               上一曲
    Thumb_down                            "5"                               下一曲
    5                                     "6"                               音量增加
    拳头                                  "7"                                音量减小
    作别                                  "8"                                退出

    """

# 反复操作
while True:
    print("""
            1.播放
            2.暂停
            3.继续播放
            4.上一曲
            5.下一曲
            6.音量增加
            7.音量减小
            8.退出

    """)

    # 接受指令 合法去执行，不合法重新接受指令  gesture_recognition() 手势识别
    while True:
        command = gesture_recognition()
        if command in ["1", "2", "3", "4", "5", "6", "7", "8"]:
            print("接受的指令是：", command)
            break

    # 解析指令  完成任务
    if command == "1":
        mixer.music.load(music_paths[music_no])
        mixer.music.play()
    elif command == "2":
        mixer.music.pause()
    elif command == "3":
        mixer.music.unpause()
    elif command == "4":
        if music_no > 0:
            music_no -= 1
        else:
            music_no = music_count - 1
        mixer.music.load(music_paths[music_no])
        mixer.music.play()
    elif command == "5":
        if music_no < music_count - 1:
            music_no += 1
        else:
            music_no = 0
        mixer.music.load(music_paths[music_no])
        mixer.music.play()
    elif command == "6":
        if volume < 1:
            volume += 0.1
            mixer.music.set_volume(volume)
        else:
            print("音量已经最大")
    elif command == "7":
        if volume > 0:
            volume -= 0.1
            mixer.music.set_volume(volume)
        else:
            print("音量已经最小")
    elif command == "8":
        print("正在退出播放器")
        os.kill(os.getpid(), 9)

    print("正在播放的歌曲：", music_names[music_no])
    print("当前音量：", volume)


