#!/usr/bin/env python3
# -- coding: utf-8 --
import RPi.GPIO as GPIO
import time
import json
import sys
import wiringpi as WIR
import requests
reload(sys)
sys.setdefaultencoding("utf-8")

RELAY_PIN = 4              # リレーをGPIO4に設定
servo_pin = 18             # サーボピンをGPIO18に設定
GPIO.setmode(GPIO.BCM)     
GPIO.setup(RELAY_PIN, GPIO.OUT)

WIR.wiringPiSetupGpio()    # 上図 pin(BOARD) の番号でピン指定するモード
WIR.pinMode(servo_pin, 2)  # 出力ピンとして指定
WIR.pwmSetMode(0)          # 0Vに指定
WIR.pwmSetRange(1024)      # レンジを0～1024に指定
WIR.pwmSetClock(375)      



# 0~180°の角度を指定
def servo_angle(set_degree):
    move_deg = int((9.5*set_degree/180 + 2.5)*(1024/100))
    WIR.pwmWrite(servo_pin, move_deg)
    time.sleep(0.8)  

def notify(message):
    url = "https://notify-api.line.me/api/notify" 
    token = "取得したアクセストークン"
    headers = {"Authorization" : "Bearer "+ token} 
    payload = {"message" :  message} 
    r = requests.post(url, headers = headers, params=payload) 

def Water_Ctrl(weather):
    if (weather < 300 and weather >= 200):
        return 30
    elif(weather < 200 and weather >= 100):
        return 60
    elif(weather < 100 and weather >= 0):
        return 120
    else:
        return 0

def Sprinc(weather_code):
    sleeptime = Water_Ctrl(weather_code)
    servo_angle(100)
    # notify("散水開始!!")
    time.sleep(sleeptime)
    servo_angle(0)
    time.sleep(0.5)
    # notify("散水終了!!")

def WeatherCheck():
    # 気象庁から天気情報を取得
    url = requests.get("https://www.jma.go.jp/bosai/forecast/data/forecast/130000.json")
    text = url.text
    data = json.loads(text)

    root = data[0]["timeSeries"][0]['areas'][0]
    hokubu = root['area']['name']
    tenki = root['weathers'][0]
    tenki = ' '.join(tenki.split())   #全角スペースを半角スペースにする
    code = int(root['weatherCodes'][0])
    return tenki,code

