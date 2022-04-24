#!/usr/bin/env python3
# -- coding: utf-8 --
import RPi.GPIO as GPIO
import time
import json
import sys
import wiringpi as WIR
import requests
from setting import servo_angle
from setting import notify
reload(sys)
sys.setdefaultencoding("utf-8")   #なぜかこれがないと天気を正しく通知できなかった


# ここからメインプログラム
RELAY_PIN = 4                  # リレーをGPIO4に設定
servo_pin = 18             # サーボピンをGPIO18に設定
GPIO.setmode(GPIO.BCM)     
GPIO.setup(RELAY_PIN, GPIO.OUT)

WIR.wiringPiSetupGpio()    # 上図 pin(BOARD) の番号でピン指定するモード
WIR.pinMode(servo_pin, 2)  # 出力ピンとして指定
WIR.pwmSetMode(0)          # 0Vに指定
WIR.pwmSetRange(1024)      # レンジを0～1024に指定
WIR.pwmSetClock(375)     
GPIO.output(RELAY_PIN, False)# NOで接続した場合の回路が閉じた状態の処理
servo_angle(0)                  # サーボモータを5°に回転
time.sleep(0.5)
notify("QRコードにより散水を停止しました。")  # ご報告
GPIO.output(RELAY_PIN, True) # NOで接続した場合回路が開いた状態の処理
GPIO.cleanup()
