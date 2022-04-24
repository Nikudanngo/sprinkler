#!/usr/bin/env python3
# -- coding: utf-8 --
import RPi.GPIO as GPIO
import time
from websocket_server import WebsocketServer
import requests
import json
import sys
import wiringpi as WIR
reload(sys)
sys.setdefaultencoding("utf-8")   #なぜかこれがないと天気を正しく通知できなかった

GREEN = 4
servo_pin = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(GREEN, GPIO.OUT)

WIR.wiringPiSetupGpio()    # 上図 pin(BOARD) の番号でピン指定するモード
WIR.pinMode(servo_pin, 2)  # 出力ピンとして指定
WIR.pwmSetMode(0)          # 0Vに指定
WIR.pwmSetRange(1024)      # レンジを0～1024に指定
WIR.pwmSetClock(375)      

# 0~180°の角度を指定
def servo_angle(set_degree):
    move_deg = int((9.5*set_degree/180 + 2.5)*(1024/100))
    WIR.pwmWrite(servo_pin, move_deg)
    time.sleep(0.3)  

servo_angle(7)    #初期化
def receivedMessage(client, server, message):
    print(message)
    if message == 'GREEN_on':
        GPIO.output(GREEN, GPIO.HIGH)
        servo_angle(100)               #サーボモータ 100°        
        notify("散水を開始します。")
    elif message == 'GREEN_off':
        GPIO.output(GREEN, GPIO.LOW)
        servo_angle(7)                 #サーボモータ  7°
        notify("散水を終了しました。")
    else:
        print("Unknown Message: {}".format(message))

def notify(message):
    url = "https://notify-api.line.me/api/notify" 
    token = "取得したアクセストークン"
    headers = {"Authorization" : "Bearer "+ token} 
    payload = {"message" :  message} 
    r = requests.post(url, headers = headers, params=payload) 

def Water_Ctrl(weather):
    if (weather == "はれ"):
        return 100
    elif (weather == "くもり"):
        return 120
    elif (weather == "あめ"):
        return 30

# 気象庁の公式.json
url = requests.get("https://www.jma.go.jp/bosai/forecast/data/forecast/290000.json")
text = url.text
data = json.loads(text)

root = data[0]
hokubu = root["timeSeries"][0]['areas'][0]['area']['name']
tenki = root["timeSeries"][0]['areas'][0]['weathers'][2]

run_time = Water_Ctrl(tenki)
notify("サーバーが立ち上がりました。")
server = WebsocketServer(5555, host="ラズパイのIP")
server.set_fn_message_received(receivedMessage)
server.run_forever()
# サーバーが落ちた場合
servo_angle(7)                 #サーボモータ  7°
GPIO.output(GREEN, GPIO.LOW)
GPIO.cleanup()
print("Bay...")
notify("サーバーがダウンしました。")