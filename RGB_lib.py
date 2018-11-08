#!/usr/bin/env python
# encoding: utf-8
 
import RPi.GPIO as GPIO


class RGBResult:
    'RGB sensor ,set R G B colours'
    
class RGB:
    'RGB sensor set class for Raspberry'
    __r_pin =0
    __g_pin =0
    __b_pin =0
    
    def __init__(self,r_pin,g_pin,b_pin):
        self.__r_pin =r_pin
        self.__g_pin =g_pin
        self.__b_pin =b_pin
        
        
    def setOut(self):
        GPIO.setup(self.__r_pin,GPIO.OUT)
        GPIO.setup(self.__g_pin,GPIO.OUT)
        GPIO.setup(self.__b_pin,GPIO.OUT)

    def setRedOn(self):
        GPIO.output(self.__r_pin,GPIO.HIGH)
        GPIO.output(self.__g_pin,GPIO.LOW)
        GPIO.output(self.__b_pin,GPIO.LOW)
    def setRedOff(self):
        GPIO.output(self.__r_pin,GPIO.LOW)
        GPIO.output(self.__g_pin,GPIO.LOW)
        GPIO.output(self.__b_pin,GPIO.LOW)
        
    def setGreenOn(self):
        GPIO.output(self.__r_pin,GPIO.LOW)
        GPIO.output(self.__g_pin,GPIO.HIGH)
        GPIO.output(self.__b_pin,GPIO.LOW)
        
    def setGreenOff(self):
        GPIO.output(self.__r_pin,GPIO.LOW)
        GPIO.output(self.__g_pin,GPIO.LOW)
        GPIO.output(self.__b_pin,GPIO.LOW)
        
    def setBlueOn(self):
        GPIO.output(self.__r_pin,GPIO.LOW)
        GPIO.output(self.__g_pin,GPIO.LOW)
        GPIO.output(self.__b_pin,GPIO.HIGH)
        
    def setBlueOff(self):
        GPIO.output(self.__r_pin,GPIO.LOW)
        GPIO.output(self.__g_pin,GPIO.LOW)
        GPIO.output(self.__b_pin,GPIO.LOW)
        
    def setGPIOclean(self):
        GPIO.cleanup()
       
         
     
         
     
  

