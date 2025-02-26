#!/usr/bin/python

def he_control_loop(dummy, state,timeState):
    from time import sleep
    from datetime import datetime, timedelta
    import RPi.GPIO as GPIO
    import config as conf

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(conf.he_pin, GPIO.OUT)
    GPIO.setup(conf.steam_pin,GPIO.IN)
    GPIO.output(conf.he_pin, 0)
    GPIO.input(conf.steam_pin)
    heating = False

    try:
        while True:
            pidstate['awake'] = timer.timer(timeState)


            # if state['snoozeon'] == True:
            #     now = datetime.now()
            #     dt = datetime.strptime(state['snooze'], '%H:%M')
            #     if dt.hour == now.hour and dt.minute == now.minute:
            #         state['snoozeon'] = False

            avgpid = state['avgpid']
            
            if not state['awake'] or state['circuitBreaker']:
                state['heating'] = False
                GPIO.output(conf.he_pin, 0)
                sleep(1)
            else:
                if avgpid >= 100:
                    state['heating'] = True
                    GPIO.output(conf.he_pin, 1)
                    sleep(1)
                elif avgpid > 0 and avgpid < 100:
                    state['heating'] = True
                    GPIO.output(conf.he_pin, 1)
                    sleep(avgpid/100.)
                    GPIO.output(conf.he_pin, 0)
                    sleep(1-(avgpid/100.))
                    state['heating'] = False
                else:
                    GPIO.output(conf.he_pin, 0)
                    state['heating'] = False
                    sleep(1)

    finally:
        GPIO.output(conf.he_pin, 0)
        GPIO.cleanup()


def pid_loop(dummy, state):
    import sys
    from time import sleep, time
    from math import isnan
    # import Adafruit_GPIO.SPI as SPI
    import adafruit_max31855
    import PID as PID
    import config as conf
    from datetime import datetime
    from brewOrSteaming import steaming
    import RPi.GPIO as GPIO
    from digitalio import DigitalInOut
    import board


    def c_to_f(c):
        return c * 9.0 / 5.0 + 32.0
    spi = board.SPI()
    cs = DigitalInOut(board.D5)
    sensor = adafruit_max31855.MAX31855(spi,cs)
    # sensor = adafruit_max31855.MAX31855(spi=SPI.SpiDev(conf.spi_port, conf.spi_dev))
    pid = PID.PID(conf.Pc, conf.Ic, conf.Dc)
    pid.SetPoint = state['settemp']
    pid.setSampleTime(conf.sample_time*5)

    nanct = 0
    i = 0
    j = 0
    pidhist = [0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]
    avgpid = 0.
    temphist = [0., 0., 0., 0., 0.]
    avgtemp = 0.
    lastsettemp = state['settemp']
    lasttime = time()
    sleeptime = 0
    iscold = True
    iswarm = False
    lastcold = 0
    lastwarm = 0
    circuitBreaker = False
    timeSinceLastSteam = None

    try:
        while True:  # Loops 10x/second
            try:
                tempc = sensor.temperature
            except:
                continue
            steam,circuitBreaker,timeSinceLastSteam = steaming(timeSinceLastSteam)
            state['circuitBreaker'] = circuitBreaker
            state['steam'] = steam
            # if isnan(tempc):
            #     nanct += 1
            #     if nanct > 100000:
            #         print("ERROR IN READING TEMPERATURE LINE 98")
            #         with open("Failedcsv.csv","a+") as tempFile:
            #             fieldNames = ["time","avgtemp","settemp","steamtemp"]
            #             writer = csv.DictWriter(tempFile,fieldnames=fieldNames)
            #             writer.writerow({"time": datetime.now(), "avgtemp":state["avgtemp"],"settemp":state["settemp"],"steamtemp":state["steamtemp"]})
        
            #         sys.exit
            #     continue
            # else:
            #     nanct = 0

            # tempf = c_to_f(tempc)
            temphist[i % 5] = tempc
            avgtemp = sum(temphist)/len(temphist)
            
            #circuitbreaker is on
            if circuitBreaker:
                continue

            if state['steam'] :
                print("line 118 steam on hit")
                if avgtemp < 90:
                    lastcold = i

                if avgtemp > 130:
                    lastwarm = i

                if iscold and (i-lastcold)*conf.sample_time > 60*15:
                    pid = PID.PID(conf.Pw, conf.Iw, conf.Dw)
                    pid.SetPoint = state['steamtemp']
                    pid.setSampleTime(conf.sample_time*5)
                    iscold = False

                if iswarm and (i-lastwarm)*conf.sample_time > 60*15:
                    pid = PID.PID(conf.Pc, conf.Ic, conf.Dc)
                    pid.SetPoint = state['steamtemp']
                    pid.setSampleTime(conf.sample_time*5)
                    iscold = True

                if state['steamtemp'] != lastsettemp:
                    pid.SetPoint = state['steamtemp']
                    lastsettemp = state['steamtemp']
                
                print("pid.setpoint",pid.SetPoint)
                print("avg temp",avgtemp)

            else:
                print("line 142 brew hit")
                if avgtemp < 30:
                    lastcold = i

                if avgtemp > 90:
                    lastwarm = i

                if iscold and (i-lastcold)*conf.sample_time > 60*15:
                    pid = PID.PID(conf.Pw, conf.Iw, conf.Dw)
                    pid.SetPoint = state['settemp']
                    pid.setSampleTime(conf.sample_time*5)
                    iscold = False

                if iswarm and (i-lastwarm)*conf.sample_time > 60*15:
                    pid = PID.PID(conf.Pc, conf.Ic, conf.Dc)
                    pid.SetPoint = state['settemp']
                    pid.setSampleTime(conf.sample_time*5)
                    iscold = True

                if state['settemp'] != lastsettemp:
                    pid.SetPoint = state['settemp']
                    lastsettemp = state['settemp']


            if i % 10 == 0:
                pid.update(avgtemp)
                pidout = pid.output
                pidhist[int(i/10 % 10)] = pidout
                avgpid = sum(pidhist)/len(pidhist)

                # print("pidout",pidout)
                # print("pidHist",pidhist)
                # print("avgpid",avgpid)

            state['i'] = i
            state['tempc'] = round(tempc, 2)
            state['avgtemp'] = round(avgtemp, 2)
            state['pidval'] = round(pidout, 2)
            state['avgpid'] = round(avgpid, 2)
            state['pterm'] = round(pid.PTerm, 2)
            if iscold:
                state['iterm'] = round(pid.ITerm * conf.Ic, 2)
                state['dterm'] = round(pid.DTerm * conf.Dc, 2)
            else:
                state['iterm'] = round(pid.ITerm * conf.Iw, 2)
                state['dterm'] = round(pid.DTerm * conf.Dw, 2)
            state['iscold'] = iscold

            print (datetime.now())
            print(state)
            print("time since last steam", timeSinceLastSteam)

            sleeptime = lasttime+conf.sample_time-time()
            if sleeptime < 0:
                sleeptime = 0
            sleep(sleeptime)
            i += 1
            lasttime = time()

    except Exception as e:
        print(e)
    finally:
        GPIO.cleanup()
        pid.clear



if __name__ == '__main__':
    from multiprocessing import Process, Manager
    from time import sleep
    from urllib.request import urlopen
    import config as conf
    import timer
    from restServer import rest_server
    from datetime import datetime, timedelta
    import csv

    manager = Manager()
    pidstate = manager.dict()
    pidstate['snooze'] = conf.snooze
    pidstate['snoozeon'] = False
    pidstate['i'] = 0
    pidstate['settemp'] = conf.set_temp
    pidstate['steamtemp'] = conf.set_steam_temp
    pidstate['circuitBreaker'] = None
    pidstate['steam'] = False
    pidstate['avgpid'] = 0.

    timeState = manager.dict()    
    timeState['TimerOnMo'] = conf.TimerOnMo
    timeState['TimerOffMo'] = conf.TimerOffMo
    timeState['TimerOnTu'] = conf.TimerOnTu
    timeState['TimerOffTu'] = conf.TimerOffTu
    timeState['TimerOnWe'] = conf.TimerOnWe
    timeState['TimerOffWe'] = conf.TimerOffWe
    timeState['TimerOnTh'] = conf.TimerOnTh
    timeState['TimerOffTh'] = conf.TimerOffTh
    timeState['TimerOnFr'] = conf.TimerOnFr
    timeState['TimerOffFr'] = conf.TimerOffFr
    timeState['TimerOnSa'] = conf.TimerOnSa
    timeState['TimerOffSa'] = conf.TimerOffSa
    timeState['TimerOnSu'] = conf.TimerOnSu
    timeState['TimerOffSu'] = conf.TimerOffSu

    # timeState['overRide'] = conf.overRide

    pidstate['awake'] = timer.timer(timeState)

    p = Process(target=pid_loop, args=(1, pidstate))
    p.daemon = True
    p.start()

    h = Process(target=he_control_loop, args=(1, pidstate,timeState))
    h.daemon = True
    h.start()

    r = Process(target=rest_server, args=(1, pidstate,timeState))
    r.daemon = True
    r.start()

    # Start Watchdog loop
    piderr = 0
    weberr = 0
    weberrflag = 0
    urlhc = 'http://localhost:'+str(conf.port)+'/healthcheck'

    lasti = pidstate['i']
    sleep(1)

    while p.is_alive() and h.is_alive() and r.is_alive():
        curi = pidstate['i']
        if curi == lasti:
            piderr = piderr + 1
        else:
            piderr = 0

        lasti = curi

        if piderr > 9:
            print ('ERROR IN PID THREAD, RESTARTING')
            with open("FailedPIDcsv.csv","a+") as tempFile:
                fieldNames = ["time"]
                writer = csv.DictWriter(tempFile,fieldnames=fieldNames)
                writer.writerow({"time": datetime.now()})
        
            # p.terminate()

        try:
            hc = urlopen(urlhc, timeout=10)
        except:
            weberrflag = 1
        else:
            if hc.getcode() != 200:
                weberrflag = 1

        if weberrflag != 0:
            weberr = weberr + 1

        if weberr > 9:
            print ('ERROR IN WEB SERVER THREAD, RESTARTING')
            with open("FailedWEBcsv.csv","a+") as tempFile:
                fieldNames = ["time"]
                writer = csv.DictWriter(tempFile,fieldnames=fieldNames)
                writer.writerow({"time": datetime.now()})
            # r.terminate()

        weberrflag = 0

        sleep(1)
