import tkinter as tk
from PIL import ImageTk, Image
from haptics.hapticVest import HapticVest
import haptics.USARpatterns as USAR
from time import time, sleep
from random import shuffle, randint, random
import threading

def button_clicked(button_text):
    text = f"[{time()}]: USER: {button_text} \n"
    file.write(text)
    print(text)

def pattern_played(category):
    text = f"[{time()}]: VEST: {category} \n"
    file.write(text)
    print(text)

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

participant = input("Enter Participant ID: ")
testn = input("Enter test number: ")

file = open(f"{participant}_{testn}.txt", "x")

w = Window()

vest = connect_to_vest()

# A participants will have full patterns
# B participats will have simple patterns

def register_incapacitated():
    pattern_played("Incapacitated")
    USAR.display_dead(vest, participant)
    
def register_injured():
    pattern_played("Injured Person")
    USAR.display_injured(vest, participant)
    
def register_uninjured():
    pattern_played("Uninjured Person")
    USAR.display_uninjured(vest, participant)
    
def register_fire():
    pattern_played("Fire")
    USAR.display_fire(vest, participant)
    
def register_lowO():
    pattern_played("Low Oxygen")
    USAR.display_lowO(vest, participant)

def register_bio():
    pattern_played("Biohazard")
    USAR.display_bio(vest, participant)

def register_connection():
    pattern_played("Connection Lost")
    USAR.display_connection(vest, participant)

def register_error():
    pattern_played("Robot Error")
    USAR.display_error(vest, participant)


pat = [lambda: register_incapacitated(),
       lambda: register_uninjured(),
       lambda: register_injured(),
       lambda: register_fire(),
       lambda: register_lowO(),
       lambda: register_bio(),
       lambda: register_connection(),
       lambda: register_error()]

sleep(5)

print("Test Begin")
start = time()
TESTDURATION = 60

while time() - start < 60:
    pat[randint(0, len(pat)-1)]()

    sleep(random() * 8)

print("---- Test Complete ----")
exit(0)