from pathlib import Path
import sys
import time
import math
from gpiozero import LEDBarGraph

HERE = Path(__file__).parent.parent
sys.path.append(str(HERE / 'Common'))
from ADCDevice import * 

USING_GRAVITECH_ADC = False # Only modify this if you are using a Gravitech ADC

LED_PINS : list[int] = [18, 23, 24, 25, 12, 16, 20, 21, 26, 19] #change numbers
LEDS = LEDBarGraph(*LED_PINS, active_high=False)
ADC = ADCDevice() # Define an ADCDevice class object

def setup():
    global ADC
    if(ADC.detectI2C(0x48) and USING_GRAVITECH_ADC): 
        ADC = GravitechADC()
    elif(ADC.detectI2C(0x48)): # Detect the pcf8591.
        ADC = PCF8591()
    elif(ADC.detectI2C(0x4b)): # Detect the ads7830
        ADC = ADS7830()
    else:
        print("No correct I2C address found, \n"
            "Please use command 'i2cdetect -y 1' to check the I2C address! \n"
            "Program Exit. \n")
        exit(-1)
        

def loop():
    global ADC, LEDS
    possible_values = (10, 20, 30, 40, 50, 60, 70, 80, 90, 100)
    length_of_pv = len(possible_values)
    while True:
        value = ADC.analogRead(0)        # read ADC value A0 pin
        voltage = value / 255.0 * 3.3        # calculate voltage
        Rt = 10 * voltage / (3.3 - voltage)    # calculate resistance value of thermistor
        tempK = 1/(1/(273.15 + 25) + math.log(Rt/10)/3950.0) # calculate temperature (Kelvin)
        tempC = tempK - 273.15        # calculate temperature (Celsius)
        tempF = tempC * 1.8 + 32
        print (f'ADC Value: {value} \tVoltage: {voltage:.2f} \tTemperature(C): {tempC:.2f} \tTemperature(F): {tempF:.2f}')
        time.sleep(0.01)
        
        for i in range(length_of_pv):
            if tempF <  possible_values[i]:
                LEDS[i].off()

        for i in range(length_of_pv):
            if tempF >= possible_values[i]:
                LEDS[i].on()
      
        voltage = value / 255.0 * 3.3
        print (f'ADC Value: {value} \tVoltage: {voltage:.2f} ')
        time.sleep(0.01)
        
def destroy():
    global LEDS
    ADC.close()
    for led in LEDS:
        led.off()

    
if __name__ == '__main__':  # Program entrance
    print ('Program is starting... ')
    setup()
    try:
        loop()
    except KeyboardInterrupt: # Press ctrl-c to end the program.
        destroy()
