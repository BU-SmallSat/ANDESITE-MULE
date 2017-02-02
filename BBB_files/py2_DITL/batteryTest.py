from battery_driver import EPS_driver
import time


EPS = EPS_driver()
print("***Perfroming status check of all ADC channels on EPS***")
while(1):
    EPS.adc__battery__current__direction()
    time.sleep(.5)
    EPS.adc__battery__current()
    time.sleep(.5)
    EPS.adc__cell__voltage()
    time.sleep(.5)
    EPS.adc_battery_voltage()
    time.sleep(.5)
    EPS.adc__battery__temperature()
    time.sleep(.5)
    EPS.adc__battery1__current__direction()
    time.sleep(.5)
    EPS.adc__battery1__current()
    time.sleep(.5)
    EPS.adc__cell1__voltage()
    time.sleep(.5)
    #EPS.adc__battery1__voltage()
    #time.sleep(.5)
    #EPS.adc__battery1__temperature()
    #time.sleep(.5)
    #EPS.adc__battery2__current__direction()
    #time.sleep(.5)
    #EPS.adc__battery2__current()
    #time.sleep(.5)
    #EPS.adc__cell2__voltage()
    #time.sleep(.5)
    #EPS.adc__battery2__voltage()
    #time.sleep(.5)
    #EPS.adc__battery2__temperature()
    #time.sleep(.5)

'''
#additional commands
EPS.status()
time.sleep(2)
EPS.heater_on()
time.sleep(2)
EPS.heater_off()
time.sleep(2)
EPS.heater_status()
time.sleep(2)
EPS.watchdog()
'''

