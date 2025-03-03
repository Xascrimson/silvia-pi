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
set_temp = 101
set_steam_temp = 150.
# Default alarm time
snooze = '07:00'

#circuit breaker time in minutes convert to seconds
circuitBreakerTime = 20 * 60
TimerOnMo = '8:30'
TimerOffMo = '9:45'
TimerOnTu = '8:30'
TimerOffTu = '9:45'
TimerOnWe = '8:30'
TimerOffWe = '9:45'
TimerOnTh = '8:30'
TimerOffTh = '9:45'
TimerOnFr = '8:30'
TimerOffFr = '9:45'
TimerOnSa = '10:00'
TimerOffSa = '14:00'
TimerOnSu = '10:00'
TimerOffSu = '14:00'


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
