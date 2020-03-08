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
    
    def rumble(self, logical):
        self.wm.rumble = logical

