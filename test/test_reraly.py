#!/usr/bin/env python
# -*- coding: utf-8 -*-
# GPIO4を出力としてリレーに給電する
import RPi.GPIO as GPIO
import json
import sys
import wiringpi as WIR
import requests
import RPi.GPIO as GPIO
from time import sleep

# 0~180°の角度を指定
def servo_angle(set_degree):
    move_deg = int((9.5*set_degree/180 + 2.5)*(1024/100))
    WIR.pwmWrite(servo_pin, move_deg)
    sleep(0.8)  

RELAY_PIN = 4
servo_pin = 18             # サーボピンをGPIO18に設定

GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PIN, GPIO.OUT)

WIR.wiringPiSetupGpio()    # 上図 pin(BOARD) の番号でピン指定するモード
WIR.pinMode(servo_pin, 2)  # 出力ピンとして指定
WIR.pwmSetMode(0)          # 0Vに指定
WIR.pwmSetRange(1024)      # レンジを0～1024に指定
WIR.pwmSetClock(375)     



while True:
    GPIO.output(RELAY_PIN, True) # NOで接続した場合の回路が開いた状態の処理
    sleep(3.0)
    GPIO.output(RELAY_PIN, False)# NOで接続した場合の回路が閉じた状態の処理
    servo_angle(100)
    sleep(2.0)
    servo_angle(7)
    sleep(2.0)
