import tkinter as tk
import threading
import math
from time import sleep
from test_walking.SimWalker import Robot
from haptics.hapticVest import HapticVest

SIMSPEED = 50  # ms time for each Tick
MAXTIME = 1500000
CANVASSIZE = 900

class Sim:
    def __init__(self):
        self.root = tk.Tk()
        self.root.resizable(False, False)
        self.canvas = tk.Canvas(self.root, width=CANVASSIZE, height=CANVASSIZE)

        self.canvas.configure(background='gray')
        self.canvas.create_text(50, 35, text="Theta θ  :", fill="white", font=('mono 15'))
        #self.canvas.create_text(50, 15, text="isWalking:", fill="white", font=('mono 15'))
        self.canvas.pack()
        
        self.angle = 0
        startpos = (CANVASSIZE / 2, CANVASSIZE / 2)
        
        self.robot = Robot(self.canvas, (startpos[0], startpos[1]))

        self.vest = HapticVest(r"haptics/patterns")
        
        self.root.bind('<KeyPress-w>', self.movef)
        self.root.bind('<KeyPress-a>', self.turnl)
        self.root.bind('<KeyPress-d>', self.turnr)



        self.canvas.after(SIMSPEED, self.runSim)
        self.canvas.after(SIMSPEED, self.startVest)

        self.root.mainloop()

    def runSim(self):

        self.robot.act()
            
        self.canvas.delete("label")
        
        angle = self.robot.theta + math.pi/2 #if math.theta < 180 else robot.theta + math.pi
        
        #could use mod
        if angle > 2 * math.pi:
            angle -= math.pi * 2
        elif angle < 0 :
            angle += math.pi * 2
        
        self.angle = math.degrees(angle)

        self.canvas.create_text(180, 15, text=f"{angle:.3f} = {math.degrees(angle):.3f}°", fill="red", font=('mono 15'), tags="label")
        #self.canvas.create_text(130, 35, text=f"{self.iswalking}", fill="red", font=('mono 15'), tags="label")
        self.canvas.pack()

        self.canvas.after(SIMSPEED, self.runSim)

    def movef(self, event):
        self.vest.dots("Front", [9,10], dur=0.3)
        self.robot.forward(5)
    
    def turnl(self, event):
        self.robot.turn(-math.pi/50) 

    def turnr(self, event):
        self.robot.turn(+math.pi/50)

    def startVest(self):
        self.vest.walk(self.angle, 50)
        self.canvas.after(100, self.startVest)


if __name__ == '__main__':
    S = Sim()
