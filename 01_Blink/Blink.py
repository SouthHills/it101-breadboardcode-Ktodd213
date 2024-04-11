from gpiozero import LED as LEDClass # Alias
import time

LED = LEDClass(17)  # define led
LED2 = LEDClass(27)

def loop():
    global LED,LED2
    while True:
        LED.on() 
        LED2.off()
        print ("led turned on >>>") # print information on terminal
        time.sleep(1)
        LED2.on()
        LED.off()
        print ("led turned off <<<")
        time.sleep(1)
        
def destroy():
    global LED,LED2
    # Release resources
    LED.close()
    LED2.close()

if __name__ == "__main__":    # Program start point
    print("Program is starting ... \n")
    print(f"Using pin {LED.pin} and {LED2.pin}")
    try:
        loop()
    except KeyboardInterrupt:   # Press ctrl-c to end the program.
        destroy()
