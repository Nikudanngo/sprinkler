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

# ここからメインプログラム
RELAY_PIN = 4              # リレーのピンをGPIO4に設定
servo_pin = 18             # サーボピンをGPIO18に設定

GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PIN, GPIO.OUT)

WIR.wiringPiSetupGpio()    # 上図 pin(BOARD) の番号でピン指定するモード
WIR.pinMode(servo_pin, 2)  # 出力ピンとして指定
WIR.pwmSetMode(0)          # 0Vに指定
WIR.pwmSetRange(1024)      # レンジを0～1024に指定
WIR.pwmSetClock(375)     
GPIO.output(RELAY_PIN, False)# NOで接続した場合の回路が閉じた状態の処理
servo_angle(100)                  # サーボモータを100°に回転
notify("QRコードにより散水を開始しました。")  # ご報告

# 消し忘れ防止処理
time.sleep(200)
GPIO.output(RELAY_PIN, False)# NOで接続した場合の回路が閉じた状態の処理
servo_angle(0)
time.sleep(0.5)
GPIO.output(RELAY_PIN, True) # NOで接続した場合回路が開いた状態の処理
GPIO.cleanup()

