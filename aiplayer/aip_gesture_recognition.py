#  *_* coding:utf8 *_*
# pip install baidu-aip
import os
import cv2
from aip import AipBodyAnalysis
from threading import Thread


""" 你的 APPID AK SK """
APP_ID ="你的 APPID"
API_KEY = "你的 AK"
SECRET_KEY = "你的 SK"

gesture_client = AipBodyAnalysis(APP_ID, API_KEY, SECRET_KEY)


def get_gesture_from_image(image_path):
    if isinstance(image_path, str):
        with open(image_path, "rb") as f:
            image = f.read()
            # print("image: ", image,)
            # print(type(image))
    else:
        image = image_path

    result_data = gesture_client.gesture(image)
    if "result" in result_data and result_data["result"]:
        result_str = result_data["result"][0]["classname"]
    else:
        result_str = ""

    return result_str

gesture_contrast = {
    "Ok": "1",
    "Thumb_up": "4",
    "Thumb_down": "5",
    "Insult": "2",
    "Six": "3",
    "Five": "6",
    "Fist": "7",
    "Honour": "8",
}


def gesture_testting():
    for path in os.listdir("gesture"):
        path_name = "gesture/" + path
        print("图片: ", path)
        print("手势", get_gesture_from_image(path_name), "\n")

# 0指的是摄像头的编号。如果你电脑上有两个摄像头的话，访问第2个摄像头就可以传入1。
capture = cv2.VideoCapture(0)
def camera():

    while True:
        ret, frame = capture.read()
        # cv2.imshow(窗口名称, 窗口显示的图像)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) == ord('q'):
            break

Thread(target=camera).start()


def gesture_recognition():
    ret, frame = capture.read()
    # nature_color = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    # img = Image.fromarray(nature_color)
    # img.save("gesture.png")

    # opencv图片对象转化为二进制文件流
    im = cv2.imencode(".png", frame)[1].tobytes()

    gesture = get_gesture_from_image(im)

    return gesture_contrast[gesture] if gesture in gesture_contrast else "指令未收录"

def function_prompts():
    print(
        """
    手势识别功能描述：

        手势                                识别结果
        -------------------------------------------------
        ok                                    "1"
        竖中指                                "2"
        6                                     "3"
        点赞                                  "4"
        Thumb_down                            "5"
        5                                     "6"
        拳头                                  "7"
        作别                                  "8"

        """
    )

function_prompts()

if __name__ == '__main__':
    # gesture_testting()

    while True:
        print(gesture_recognition())

