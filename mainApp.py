import tkinter as tk
import UltrasonicManager
import PIL

from PIL import Image, ImageTk
from neopixel import *
import threading
from LEDVisualizer import *
from SoundManager import *


class PiReminGUI(object):
    def __init__(self, master, **kwargs):
        self.master = master
        self.state = False
        master.resizable(width=False, height=False)
        # master.geometry("{0}x{1}+0+0".format(master.winfo_screenwidth() - pad, master.winfo_screenheight() - pad))
        master.geometry('{}x{}'.format(1024, 600))  # Set window size to fit lcd touch screen

        master.bind("<F11>", self.toggle_fullscreen)
        master.bind("<Escape>", self.end_fullscreen)
        master.protocol("WM_DELETE_WINDOW", self.on_closing)

        # master.wm_attributes('-transparentcolor', 'black')

        self.init_element(master)

        self.ledVisual = LEDVisualizer()
        self.ledVisual.setDaemon(True)
        self.ledVisual.start()          # Start LED Visualizer thread

        self.ultrasonic1 = UltrasonicManager.Ultrasonic(23, 24)
        self.ultrasonic1.start()

        self.soundManager = SoundManager()
        self.soundManager.start()  # Start sound manager

    def on_closing(self):
        self.ledVisual.end()
        self.ultrasonic1.end()
        self.soundManager.shutDownSystem()
        self.master.destroy()


    def toggle_fullscreen(self, event=None):
        self.state = not self.state  # Just toggling the boolean000

        self.master.attributes("-fullscreen", self.state)
        return "break"


    def end_fullscreen(self, event=None):
        self.state = False
        self.master.attributes("-fullscreen", False)
        return "break"


    def change_screen_mode(self):
        if (self.state):
            self.end_fullscreen()
        else:
            self.toggle_fullscreen()


    def init_element(self, master):
        print("initing GUI")
        self.pitch_slider = tk.Scale(master, from_=0, to=200, orient=tk.VERTICAL)
        photo = ImageTk.PhotoImage(file="/home/pi/max/project/Piremin_main_gui_bg.jpg")
        label = tk.Label(master, image=photo)
        label.image = photo  # keep a reference!
        label.place(x=0, y=0, relwidth=1, relheight=1)

        self.pitch_slider = tk.Scale(master, sliderlength=50, length=400, from_=0, to=100,
                                     width=70, repeatdelay=1, orient=tk.VERTICAL,
                                     command=self.on_pitch_slder_change,
                                     bg="#834C38",
                                     highlightbackground="black",
                                     troughcolor="#663429",
                                     activebackground="#9A746B")
        self.pitch_slider.place(x=552, y=183)

        self.freq_slider = tk.Scale(master, sliderlength=50, length=400, from_=200, to=1000,
                                    width=70, repeatdelay=1, orient=tk.VERTICAL,
                                    command=self.on_pitch_slder_change,
                                    bg="#834C38",
                                    highlightbackground="black",
                                    troughcolor="#663429",
                                    activebackground="#9A746B"
                                    )
        self.freq_slider.place(x=701, y=183)

        self.vol_slider = tk.Scale(master, sliderlength=50, length=400, from_=0, to=100,
                                   width=70, repeatdelay=1, orient=tk.VERTICAL,
                                   command=self.on_pitch_slder_change,
                                   bg="#834C38",
                                   highlightbackground="black",
                                   troughcolor="#663429",
                                   activebackground="#9A746B"
                                   )
        self.vol_slider.place(x=850, y=183)

        self.pitch_label = tk.Label(master, text="Pitch", bg="brown")
        # self.pitch_label.place(x=120,y=135)

        self.screenMode_button = tk.Button(master, text="Change screen mode", command=self.change_screen_mode)
        self.screenMode_button.place(x=850, y=50)

        self.val = tk.StringVar()
        self.ultrasonicVal = tk.Label(master, textvariable=self.val, font=("Courier", 44))
        self.ultrasonicVal.place(x=30, y=150)

        self.screenMode_button = tk.Button(master, text="LED", command=self.setLight, font=("Courier", 44))
        self.screenMode_button.place(x=30, y=250)

        self.ultrasonicVal.after(33, self.updateVal)
        print("Done init GUI")


    def setLight(self):
        self.ledVisual.changeMode()


    def updateVal(self):
        ultrasonicRange = self.ultrasonic1.getValue()

        if (ultrasonicRange > 40):
            ultrasonicRange = 0

        #print("Ultrasonic = ", ultrasonicRange)
        #update value on GUI
        self.val.set(format(format(ultrasonicRange, '.2f'),">6s"))

        #if ultrasonicRange > 255:
        #  ultrasonicRange = 0

        # print("VOL Slider = ", self.vol_slider.get())

        self.ledVisual.receiveUltrasonicValue(ultrasonicRange)
        self.ledVisual.updateBrightness()

        freq = ultrasonicRange * 100 + self.freq_slider.get()
        vol = self.vol_slider.get() / 100.0
        if(ultrasonicRange == 0):
            vol = 0

        self.soundManager.updateSound(freq, vol)
        self.ultrasonicVal.after(33, self.updateVal)


    def on_pitch_slder_change(self, value):
        print(value)


def main():
    window = tk.Tk()  # Create new main window
    app = PiReminGUI(window)  # Create GUI App
    window.mainloop()


main()
