import tkinter as tk
import math
from SimWalker import Robot

SIMSPEED = 1  # ms time for each Tick
MAXTIME = 1500000
GRAIN = 25
CANVASSIZE = 900

def initialize(window):
    window.resizable(False, False)  # Window should not change
    canvas = tk.Canvas(window, width=CANVASSIZE, height=CANVASSIZE)
    
    canvas.create_text(50, 35, text="Theta θ  :", fill="white", font=('mono 15'))
    canvas.create_text(50, 15, text="isWalking:", fill="white", font=('mono 15'))
    canvas.pack()
    return canvas


def runTest(robot, canvas, time=0):
    robot.act()

    if time > MAXTIME:  # Simtime is up
        canvas.delete('all')
    else:
        canvas.after(SIMSPEED, runTest, robot, canvas, time + 1)
        
    canvas.delete("label")
    
    angle = robot.theta + math.pi/2 #if math.theta < 180 else robot.theta + math.pi
    
    if angle > 2 * math.pi:
        angle -= math.pi * 2
    elif angle < 0 :
        angle += math.pi * 2
    
    canvas.create_text(180, 15, text=f"{angle:.3f} = {math.degrees(angle):.3f}°", fill="red", font=('mono 15'), tags="label")
    canvas.create_text(130, 35, text=f"{robot.iswalking}", fill="red", font=('mono 15'), tags="label")
    canvas.pack()


def handle_key_press(event):
    keys.add(event.char)
    update_movement()

def handle_key_release(event):
    keys.remove(event.char)
    update_movement()


def update_movement():
    movement = [0, 0]

    if 'w' in keys:
        movement[1] += 3
    if 's' in keys:
        movement[1] -= 3
    if 'a' in keys:
        movement[0] -= math.pi/40
    if 'd' in keys:
        movement[0] += math.pi/40
    
    if movement[1] > 0:
        b.forward(movement[1])
        b.iswalking = "True"
    else:
        b.iswalking = "False"
         
    b.turn(movement[0])


def test(window):
    global b
    canvas = initialize(window)
    canvas.configure(background='gray')

    startpos = (CANVASSIZE / 2, CANVASSIZE / 2)

    randomAng = 0
    rx = math.sin(math.radians(randomAng)) * 40
    ry = math.cos(math.radians(randomAng)) * 40

    b = Robot(canvas, (startpos[0] + rx, startpos[1] + ry))

    window.bind('<KeyPress>', handle_key_press)
    window.bind('<KeyRelease>', handle_key_release)

    runTest(b, canvas)

    window.mainloop()


if __name__ == '__main__':
    keys = set()
    window = tk.Tk()
    test(window)
