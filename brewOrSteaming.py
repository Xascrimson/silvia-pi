#!/usr/bin/python

from time import sleep, time
import config as conf
import RPi.GPIO as GPIO

"""
Input:timeSinceLastSteal
output : steam, circuitbreaker, timeSinceLastSteaming
"""
def steaming(timeSinceLastSteaming,state):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(conf.steam_pin,GPIO.IN,GPIO.PUD_DOWN)
    steam_pin = GPIO.input(conf.steam_pin)

    if steam_pin == True:
        print("steaming")
        #resetted steam pin since new press
        if timeSinceLastSteaming == None:
            timeSinceLastSteaming = time()
        
        #steam working fine
        if time() - timeSinceLastSteaming < conf.circuitBreakerTime:
            return True,False,timeSinceLastSteaming
        #circuit protection
        return False, True, timeSinceLastSteaming
    #not steaming = espresso temp
    else:
        #if wakeup is true, and we last steamed then now you can set it as false
        if state['wakeup'] == True and timeSinceLastSteaming != None:
            state['wakeup'] = False
        return False,False,None
    