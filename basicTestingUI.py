import tkinter as tk
from PIL import ImageTk, Image
from haptics.hapticVest import HapticVest
from time import time, sleep
from random import shuffle, randint, random
import threading

def button_clicked(button_text):
    print(f"[{time()}]: USER: {button_text}")

def pattern_played(category):
    print(f"[{time()}]: VEST: {category}")

def create_button(root, pos, image_path, text, on_press):
    row, col = pos
    # Open and resize the image to fit the button
    image = Image.open(image_path)
    image = image.resize((130, 130), Image.ANTIALIAS) 
    image = ImageTk.PhotoImage(image)
    
    # Create the button with image and text
    button = tk.Button(root, text=text, image=image, compound=tk.TOP, command=on_press, font=("Helvetica", 14, "bold"), bg="white")
    button.image = image  # Jank to prevent image from being garbage collected
    button.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

def connect_to_vest():
    try:
        vest = HapticVest(r"haptics/all_patterns")
        return vest
    except Exception as e:
        print("An error occured connecting to the haptic vest:")
        print(e)
        exit(0)

class Window(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.start()
    
    def run(self):
        self.root = tk.Tk()
        self.root.title("USAR-Haptics-Training")

        # Get screen width and height
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Set window size
        window_width  = int(1.5*screen_width // 2)
        window_height = int(2.5*screen_height // 3)
        self.root.geometry(f"{window_width}x{window_height}")

        # Configure row and column weights to make buttons fill the space
        for i in range(1, 3):  # 2 rows
            self.root.grid_rowconfigure(i, weight=1)
        for i in range(4):  # 3 columns
            self.root.grid_columnconfigure(i, weight=1)

        # Shuffle Button Positions
        pos = [(1,0),(1,1),(1,2),(1,3),(2,0),(2,1),(2,2),(2,3)]
        shuffle(pos)

        # Enviroment State
        create_button(self.root, pos[0], "resources/images/fire.jpg", "Fire", lambda: button_clicked("Fire"))
        create_button(self.root, pos[1], "resources/images/biohaz.jpg", "Biohazard", lambda: button_clicked("Biohazard"))
        create_button(self.root, pos[2], "resources/images/oxygen.jpg", "Low Oxygen", lambda: button_clicked("Low Oxygen"))
        # User Detections
        create_button(self.root, pos[3], "resources/images/alive.png", "Uninjured Person", lambda: button_clicked("Uninjured Person"))
        create_button(self.root, pos[4], "resources/images/injured.png", "Injured Person", lambda: button_clicked("Injured Person"))
        create_button(self.root, pos[5], "resources/images/dead.jpg", "Dead Person", lambda: button_clicked("Dead Person"))
        # Robotic State
        create_button(self.root, pos[6], "resources/images/lost.png", "Connection Lost", lambda: button_clicked("Lost Robot Connection"))
        create_button(self.root, pos[7], "resources/images/robotIssue.jpg", "Robot Error", lambda: button_clicked("Robot Error"))

        title = tk.Label(self.root, text="When you feel an alert, press the corresponding button", font=("Arial", 20, "bold"))
        title.grid(row=0, column=0, columnspan=4, pady=10)

        self.root.mainloop()

w = Window()


vest = connect_to_vest()

def display_dead():
    pattern_played("Dead")
    vest.display_pattern('Heartx2',intensity=200, dur=1)
    vest.display_pattern('Quad_X_Outwards',intensity=200, dur=1.5)
    
def display_injured():
    pattern_played("Injured Person")
    vest.display_pattern('Heartx2',intensity=200, dur=1)
    vest.display_pattern('Zig_Zag_Col',intensity=200, dur=1.5)

def display_uninjured():
    pattern_played("Uninjured Person")
    vest.display_pattern('Heartx4',intensity=200, dur=1.8)

def display_fire():
    pattern_played("Fire")
    vest.display_pattern('Right', dur=1.5, intensity=80, angle=90)

def display_lowO():
    pattern_played("Low Oxygen")
    vest.display_pattern('Inward_heart_Spiral', dur=1.5)

def display_bio():
    pattern_played("Biohazard")
    vest.display_pattern('Chevrons', dur=1.5)

def display_connection():
    pattern_played("Connection Lost")
    vest.display_pattern('Top_360',intensity=200, dur=2)

def display_error():
    pattern_played("Robot Error")
    vest.display_pattern('Triple_Flip',intensity=200, dur=2)

pat = [lambda: display_dead(),
       lambda: display_uninjured(),
       lambda: display_injured(),
       lambda: display_fire(),
       lambda: display_lowO(),
       lambda: display_bio(),
       lambda: display_connection(),
       lambda: display_error()]

sleep(5)

print("Test Begin")
start = time()
TESTDURATION = 60

while time() - start < 60:
    pat[randint(0, len(pat)-1)]()

    sleep(random() * 8)

print("---- Test Complete ----")
exit(0)