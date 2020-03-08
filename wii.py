import cwiid
import time


class Wiimote:
    def __init__(self):
        self.acc = [0, 0, 0]

        '''Connect to Wiimote'''
        print("Press 1+2 on your Wiimote now...")

        i = 1
        self.wm = None

        while not self.wm:
            try:
                self.wm=cwiid.Wiimote()
            except RuntimeError:
                if (i>10):
                    quit()
                    break
                print("Error opening Wiimote connection")
                print("Attempt No: " + str(i))
                i += 1

        print("Successfully connected to Wiimote!")
        self.wm.led = 9  # Show successful connection on Wiimote 
        self.wm.rumble = False

        '''Configure Wiimote'''
        self.wm.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC
    
    def accel(self):
        return self.wm.state['acc']

    def buttons(self):
        raw_buttons = self.wm.state['buttons']
        buttons = {
                "trigger": bool(raw_buttons & 0b100),  # 4
                "a": bool(raw_buttons & 0b1000),  # 8
                "minus": bool(raw_buttons & 0b10000),  # 16
                "home": bool(raw_buttons & 0b10000000),  # 128
                "left": bool(raw_buttons & 0b100000000),  # 256
                "right": bool(raw_buttons & 0b1000000000),  # 512
                "down": bool(raw_buttons & 0b10000000000),  # 1024
                "up": bool(raw_buttons & 0b100000000000),  # 2048
                "plus": bool(raw_buttons & 0b1000000000000),  # 4096
                }
        return buttons
    
    def rumble(self, logical):
        self.wm.rumble = logical
    
    def led(self, number):
        self.wm.led = number
