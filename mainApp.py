import tkinter as tk
import UltrasonicManager
import PIL
import subprocess

from PIL import Image, ImageTk
from neopixel import *
import threading
from LEDVisualizer import *
from SoundManager import *

# Set ultrasonic sensor pin for frequency control
FREQ_TRIG = 23
FREQ_ECHO = 24

# Set ultrasonic sensor pin for amplitude control
AMP_TRIG = 17
AMP_ECHO = 27

# Main program update interval (ms)
UPDATE_INTERVAL = 33

# LED Mode text for button
LED_MODE = ["OFF","Rainbow","VU Meter"]

# Main class for GUI
class PiReminGUI(object):
    def __init__(self, master, **kwargs):
        self.master = master
        self.fullScreen = False
        self.master.title("PiRemin")
        master.resizable(width=False, height=False)
        master.geometry('{}x{}'.format(1024, 600))  # Set window size to fit lcd touch screen

        master.bind("<F11>", self.toggle_fullscreen)
        master.bind("<Escape>", self.end_fullscreen)
        master.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.currentLEDmode = LED_MODE[0]
        self.lastLEDstate = False

        self.init_element(master)


        self.ultrasonicFreq = UltrasonicManager.Ultrasonic(FREQ_TRIG, FREQ_ECHO)
        self.ultrasonicFreq.start()
        self.ultrasonicAmp = UltrasonicManager.Ultrasonic(AMP_TRIG, AMP_ECHO)
        self.ultrasonicAmp.start()

        self.soundManager = SoundManager()
        self.soundManager.start()

        self.ledVisual = LEDVisualizer()
        self.ledVisual.start()
        self.toggle_fullscreen()
        self.setLight()

    def on_closing(self):
        # Turn off ultrasonic Status LED
        try:
            subprocess.call(['./home/pi/max/project/asm/light_off'])
        except Exception:
            pass
        try:
            subprocess.call(['./max/project/asm/light_off'])
        except Exception:
            pass

        # Turn off LED Visualizer / SoundManager / UltrasonicSensor
        self.ledVisual.end()
        self.soundManager.shutDownSystem()
        self.ultrasonicAmp.end()
        self.ultrasonicFreq.end()

        # Destroy Main GUI Window
        self.master.destroy()

    # Toggle fullscreen / windowed mode
    def toggle_fullscreen(self, event=None):
        self.fullScreen = not self.fullScreen
        self.master.attributes("-fullscreen", self.fullScreen)
        return "break"

    # Exit fullscreen mode
    def end_fullscreen(self, event=None):
        self.fullScreen = False
        self.master.attributes("-fullscreen", False)
        return "break"

    # Change the current screen mode
    def change_screen_mode(self):
        if (self.fullScreen):
            self.end_fullscreen()
        else:
            self.toggle_fullscreen()

    # Inintialize all GUI elements and then start the update loop
    def init_element(self, master):
        print("initing GUI")
        self.pitch_slider = tk.Scale(master, from_=0, to=200, orient=tk.VERTICAL)
        photo = ImageTk.PhotoImage(file="/home/pi/max/project/Piremin_main_gui_bg.jpg")
        label = tk.Label(master, image=photo)
        label.image = photo  # keep a reference!
        label.place(x=0, y=0, relwidth=1, relheight=1)

        self.freq_slider = tk.Scale(master, sliderlength=50, length=400, from_=200, to=1000,
                                    width=70, repeatdelay=1, orient=tk.VERTICAL,
                                    bg="#834C38",
                                    highlightbackground="black",
                                    troughcolor="#663429",
                                    activebackground="#9A746B"
                                    )
        self.freq_slider.place(x=701, y=183)

        self.amp_slider = tk.Scale(master, sliderlength=50, length=400, from_=0, to=100,
                                   width=70, repeatdelay=1, orient=tk.VERTICAL,
                                   bg="#834C38",
                                   highlightbackground="black",
                                   troughcolor="#663429",
                                   activebackground="#9A746B"
                                   )
        self.amp_slider.place(x=850, y=183)

        self.screenMode_button = tk.Button(master, text="Change screen mode", command=self.change_screen_mode)
        self.screenMode_button.place(x=850, y=50)

        self.FreqVal = tk.StringVar()
        self.AmpVal = tk.StringVar()
        self.ultrasonicFreqVal = tk.Label(master, textvariable=self.FreqVal, font=("Courier", 32))
        self.ultrasonicFreqVal.place(x=420, y=150)
        self.ultrasonicAmpVal = tk.Label(master, textvariable=self.AmpVal, font=("Courier", 32))
        self.ultrasonicAmpVal.place(x=420, y=210)

        self.ledMode_button = tk.Button(master, text="OFF", command=self.setLight, font=("Courier", 32))
        self.ledMode_button.place(x=28, y=375)

        # Begin the update loop
        self.master.after(UPDATE_INTERVAL, self.update)
        print("Done init GUI")


    # Cycle LED Visualizer mode
    def setLight(self):
        print(self.currentLEDmode)
        self.ledVisual.changeMode()
        self.ledMode_button["text"] = LED_MODE[self.ledVisual.mode]

    # Change ultrasonic status LED according to state
    def statusLED(self,state):
        if (state == self.lastLEDstate):
            return
        else:
            if(state):
                try:
                    subprocess.call(['./max/project/asm/light_on'])
                except Exception:
                    subprocess.call(['./asm/light_on'])

            else:
                try:
                    subprocess.call(['./max/project/asm/light_off'])
                except Exception:
                    subprocess.call(['./asm/light_off'])
            self.lastLEDstate = state

    # Update loop
    def update(self):
        # Get the sensor distances
        ultrasonicFreqRange = self.ultrasonicFreq.getValue()
        ultrasonicAmpRange = self.ultrasonicAmp.getValue()

        # Cap the sensor inputs at 50 cm
        if (ultrasonicFreqRange > 50):
            ultrasonicFreqRange = 0

        if (ultrasonicAmpRange > 50):
            ultrasonicAmpRange = 0

        # Update ultrasonic status LED
        if(ultrasonicFreqRange + ultrasonicAmpRange != 0):
            self.statusLED(True)
        else:
            self.statusLED(False)

        # Update GUI
        self.FreqVal.set(format(format(ultrasonicFreqRange, '.2f'),">6s"))
        self.AmpVal.set(format(format(ultrasonicAmpRange, '.2f'), ">6s"))

        self.ledVisual.receiveUltrasonicValue(ultrasonicFreqRange)
        self.ledVisual.updateBrightness()

        freq = ultrasonicFreqRange * 100 + self.freq_slider.get()
        if self.amp_slider.get() > 0:
            vol = self.amp_slider.get() / 100
        else:
            vol = ultrasonicAmpRange / 50.0

        # Adjust the sound manager
        self.soundManager.updateSound(freq, vol)
        self.master.after(UPDATE_INTERVAL, self.update)

# main program
def main():
    print("PiRemin is starting...")
    time.sleep(5)
    window = tk.Tk()  # Create new main window
    app = PiReminGUI(window)  # Create GUI App
    window.mainloop()

main()
