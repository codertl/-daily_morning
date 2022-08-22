from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
    url = "https://v0.yiketianqi.com/api?unescape=1&version=v91&appid=43656176&appsecret=I42og6Lm&ext=&cityid=&city=" + city
    res = requests.get(url).json()
    weather = res['data'][0]
    return weather['wea'], \
           weather['tem1'], \
           weather['tem2'], \
           weather['date'] + ' '+ weather['week'], \
           weather['win'][0],weather['win_speed'],\
           weather['win_meter'],\
           weather['humidity'],\
           weather['visibility'],\
           weather['air'],\
           weather['air_level']

def get_birthday():
    print('get_birthday', birthday)
    next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
    print('get_birthday', next)
    if next < datetime.now():
        next = next.replace(year=next.year + 1)
    return (next - today).days


def get_words():
    words = requests.get("https://api.shadiao.pro/chp")
    if words.status_code != 200:
        return get_words()
    return words.json()['data']['text']


def get_random_color():
    return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, tem1, tem2, current_date, win,win_speed,win_meter,humidity,visibility,air,air_level = get_weather()
data = {
    "city":{"value": city,"color": get_random_color()}, # 城市
    "date": {"value": current_date,"color": get_random_color()}, #日期
    "weather": {"value": wea,"color": get_random_color()}, # 天气
    "high_temperature": {"value": tem1,"color": '#E3170D'}, #高温
    "low_temperature": {"value": tem2,"color": '#FF6347'}, #低温
    "win": {"value": win,"color": '#1E90FF'}, #风向
    "win_speed": {"value": win_speed,"color": '#1E90FF'}, # 风力等级
    "win_meter": {"value": win_meter,"color": '#1E90FF'}, #风速
    "humidity": {"value": humidity,"color": '#1E90FF'}, #湿度
    "visibility": {"value": visibility,"color": '#1E90FF'}, #能见度
    "air": {"value": air,"color": '#1E90FF'}, #空气质量
    "air_level": {"value": air_level,"color": '#1E90FF'}, #空气质量等级
    "birthday_left": {"value": get_birthday(), "color": get_random_color()}, # 生日
    "words": {"value": get_words(), "color": get_random_color()}
}
res = wm.send_template(user_id, template_id, data)
