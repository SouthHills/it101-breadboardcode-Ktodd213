from pathlib import Path
import sys
from gpiozero import LEDBarGraph
import time

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
    possible_values = (25.5, 51, 76, 102, 127.5, 153, 178.5, 204, 229.5)
    length_of_pv = len(possible_values)
    while True:
        value = ADC.analogRead(0)  # read the ADC value of channel 0
        #change possiable values between 255/10
        
        for i in range(length_of_pv):
            if value <  possible_values[i]:
                LEDS[i].off()

        for i in range(length_of_pv):
            if value >= possible_values[i]:
                LEDS[i].on()
      
        voltage = value / 255.0 * 3.3
        print (f'ADC Value: {value} \tVoltage: {voltage:.2f} ')
        time.sleep(0.01)

def destroy():
    global ADC, LEDS
    ADC.close()
    for led in LEDS:
        led.close()
    
if __name__ == '__main__':   # Program entrance
    print ('Program is starting... ')
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        destroy()
        