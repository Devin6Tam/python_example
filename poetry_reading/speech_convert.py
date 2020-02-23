#  *_* coding:utf8 *_*
# pip install baidu-aip
from aip import AipSpeech
import os

""" 你的 APPID AK SK """
APP_ID ="182288981"
API_KEY = "BXWISwcCnInrfWkBdA3O9iH81"
SECRET_KEY = "E5uz4CsLM4WTG48Xa4FByCz2jzCz60i31"

speech_client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)


def generate_speech(str_or_filepath, audio_name):

    text_list = []
    if os.path.isfile(str_or_filepath):
        with open(str_or_filepath, "r", encoding="utf8") as f:
            while True:
                text_content = f.read(1024)
                if not text_content:
                    break
                text_list.append(text_content)

    elif isinstance(str_or_filepath, str):
        text_part = len(str_or_filepath) // 200 + 1
        text_list = [str_or_filepath[200 * i: 200 * (i + 1)] for i in range(text_part)]

    else:
        print("输入格式错误!")
        return

    result_audio = b""
    # 第一个是文本， 第二个是语言， 第三个是平台，第四个是声音
    for text in text_list:
        print(text)
        result = speech_client.synthesis(text, "zh", 1, {
            "vol": 5,  # 音量
            "spd": 5,  # 语速
            "pit": 9,  # 语调
            "per": 0,  # 0：女 1：男 3：逍遥 4：小萝莉
        })
        if not isinstance(result, dict):
            result_audio += result
        else:
            print(result_audio)

    with open(audio_name, 'wb+') as f:
        f.write(result_audio)


if __name__ == '__main__':
    while True:
        generate_speech("1", "audio.mp3")
        generate_speech("2", "audio.mp3")



