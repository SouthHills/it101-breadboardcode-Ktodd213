from gpiozero import LED as LEDClass, Button
from signal import pause
import time

LED = LEDClass(17)  # define ledPin
BUTTON = Button(18)  # define buttonPin
strobing = False

def loop():
    global LED
    
    while True:
        if strobing == True:
            LED.on()
            time.sleep(0.2)
            LED.off()
            time.sleep(0.2)
            print('Strobing LED')
            
def changeLedState():
    global strobing
    strobing = not strobing

def destroy():
    global LED, BUTTON
    LED.close()
    BUTTON.close()
    
if __name__ == "__main__":
    print("Program is starting...")
    try:
        # If the button gets pressed call the function
        BUTTON.when_pressed = changeLedState
        loop()
    except KeyboardInterrupt: # Press ctrl-c to end the program.
        destroy()