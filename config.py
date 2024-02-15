#!/usr/bin/python

#PIN 0-8 3v3 pull-up default, 9-27 pull-down default

# Raspberry Pi SPI Port and Device
spi_port = 0
spi_dev = 0


# Pin # for relay connected to heating element
he_pin = 26

brew_pin = 17
steam_pin = 22


#overriding the time config when wanting to heat up not during normal hours
overRide = 16

# Default goal temperature
set_temp = 103
set_steam_temp = 149.
# Default alarm time
snooze = '07:00'

#circuit breaker time in minutes convert to seconds
circuitBreakerTime = 20 * 60
TimerOnMo = '9:20'
TimerOffMo = '10:10'
TimerOnTu = '09:20'
TimerOffTu = '10:10'
TimerOnWe = '09:20'
TimerOffWe = '10:10'
TimerOnTh = '09:20'
TimerOffTh = '10:10'
TimerOnFr = '09:20'
TimerOffFr = '10:10'
TimerOnSa = '10:30'
TimerOffSa = '11:30'
TimerOnSu = '10:30'
TimerOffSu = '11:30'


#temp lowpoint and high point
low_temp_b = 85
high_temp_b = 110

low_temp_s = 130
high_temp_s = 155

# Main loop sample rate in seconds
sample_time = 0.1

# PID Proportional, Integral, and Derivative value
# we use Ziegler Nichols method to tune, from experiment Ts=130sec, Ku = 22. Therefore
Ku = 22
Ts = 130

Pc = 0.55 * Ku#22#8.2#5.6#3.4
Ic = 1.2 * Ku/Ts#0.6#1.2
Dc = 0.075 * Ku * Ts #40.0

Pw = Pc
Iw = Ic
Dw = Dc
# Pw = 22#8.4#6.4#5.6#2.9
# Iw = 0#0.6#1.2
# Dw = 0#40.0

#Web/REST Server Options
port = 8080
