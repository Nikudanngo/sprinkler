#!/usr/bin/env python3
# -- coding: utf-8 --
import RPi.GPIO as GPIO
import time
import json
import sys
import wiringpi as WIR
import requests
from setting import Water_Ctrl,WeatherCheck,notify

result = WeatherCheck()

print("今日の天気は"+str(result[0])+"なので"+str(Water_Ctrl(result[1])*1.0/60)+"分間散水しました。")
GPIO.cleanup()