from haptics.hapticVest import HapticVest
import haptics.USARpatterns as USAR 

import tkinter as tk
from PIL import Image, ImageTk
import math

class RobotSim:
    def __init__(self, master):
        self.master = master
        self.master.title("RobotSim2D")
        self.master.configure(bg="#1E1E1E")

        self.canvas = tk.Canvas(self.master, width=400, height=400, bg="#2C2C2C")
        self.canvas.pack(pady=20)

        self.square_size = 20
        self.line_size = 30
        self.x = 200
        self.y = 200
        self.angle = 0
        self.speed = 5

        self.square = self.canvas.create_oval(
            self.x - self.square_size/2,
            self.y - self.square_size/2,
            self.x + self.square_size/2,
            self.y + self.square_size/2,
            fill="red"
        )
        
        self.arrow = self.canvas.create_line(
            self.x, self.y,
            self.x + self.line_size * math.cos(math.radians(self.angle)),
            self.y - self.line_size * math.sin(math.radians(self.angle)),
            fill="white", width=3, arrow=tk.LAST)
        
        self.angle_label = tk.Label(self.master, text=f"Angle: {self.angle}°", 
                                    font=("Arial", 16), bg="#1E1E1E", fg="white")
        self.angle_label.pack(pady=10)
        
        self.master.bind("<KeyPress>", self.move_square)

    def move_square(self, event):
        if event.keysym == "Up":
            self.x += self.speed * math.cos(math.radians(self.angle))
            self.y -= self.speed * math.sin(math.radians(self.angle))
        elif event.keysym == "Down":
            self.x -= self.speed * math.cos(math.radians(self.angle))
            self.y += self.speed * math.sin(math.radians(self.angle))
        elif event.keysym == "Left":
            self.angle = (self.angle + 15) % 360
        elif event.keysym == "Right":
            self.angle = (self.angle - 15) % 360
        
        # Ensure the square stays within the canvas boundaries
        self.x = max(self.square_size/2, min(self.x, 400 - self.square_size/2))
        self.y = max(self.square_size/2, min(self.y, 400 - self.square_size/2))
        
        self.update_square()

    def update_square(self):
        self.canvas.coords(self.square,
            self.x - self.square_size/2, self.y - self.square_size/2,
            self.x + self.square_size/2, self.y + self.square_size/2)
        self.canvas.coords(self.arrow,
            self.x, self.y,
            self.x + self.line_size * math.cos(math.radians(self.angle)),
            self.y - self.line_size * math.sin(math.radians(self.angle)))
        self.angle_label.config(text=f"Angle: {self.angle}°")

def connect_to_vest():
    try:
        vest = HapticVest(r"haptics/all_patterns")
        return vest
    except Exception as e:
        print("An error occured connecting to the haptic vest:")
        print(e)
        exit(0)


def create_button(parent, image_path, text, command, width=None, height=None):
    img = Image.open(image_path).resize((100, 100) if width is None else (width, height))
    photo = ImageTk.PhotoImage(img)
    
    button = tk.Button(parent, text=text, image=photo, compound=tk.TOP,
                       command=command, bg="#2C2C2C", fg="white",
                       activebackground="#3C3C3C", activeforeground="white",
                       relief=tk.FLAT, pady=20, padx=20,  # Increased padding
                       font=("Arial", 14),
                       width=140 if width is None else width+10, height=140 if width is None else height+10)
    
    button.image = photo
    return button

class mainUI:

    def __init__(self, master):
        self.master = master
        self.master.title("VibroHaptic Demo")
        self.master.configure(bg="#1E1E1E")

        self.sim = None

        semantic = True
        self.vest = connect_to_vest()

        top_bar = tk.Frame(master, bg="#2C2C2C")
        top_bar.pack(fill=tk.X, padx=20, pady=10)

        # Create title
        title_label = tk.Label(top_bar, text="Press to send Message", font=("Arial", 24), bg="#1E1E1E", fg="white")
        title_label.pack(side=tk.LEFT, pady=10)

        small_button = create_button(top_bar, "resources/images/move.png", "Move", self.open_sim, width=50, height=50)
        small_button.pack(side=tk.RIGHT, padx=10)

        # Create frame for buttons
        button_frame = tk.Frame(master, bg="#1E1E1E")
        button_frame.pack(padx=20, pady=20)

        images = ["alive.png", "injured.png", "dead.jpg", "biohaz.jpg", "fire.jpg", "lost.png", "oxygen.jpg", "robotIssue.jpg"]
        names = ["Person", "Injured Person", "Unconsious Person", "Biohazard", "Fire", "Robot Signal Lost", "Breathing Hazard","Robot Error"] 
        style = "A" if semantic else "B"
        messages = [lambda: USAR.display_uninjured(self.vest, style),
                    lambda: USAR.display_injured(self.vest, style),
                    lambda: USAR.display_dead(self.vest, style),
                    lambda: USAR.display_bio(self.vest, style),
                    lambda: USAR.display_fire(self.vest, style),
                    lambda: USAR.display_connection(self.vest, style),
                    lambda: USAR.display_lowO(self.vest, style),
                    lambda: USAR.display_error(self.vest, style)]
    
        # Create 8 buttons
        for i in range(8):
            row = i // 4
            col = i % 4
            button = create_button(button_frame, f"resources/images/{images[i]}", f"{names[i]}", messages[i])
            button.grid(row=row, column=col, padx=10, pady=10)

        self.checkDir()

    def open_sim(self):
        if self.sim is None or not self.sim.winfo_exists():
            self.sim = tk.Toplevel(self.master)
            RobotSim(self.sim)
            self.sim.protocol("WM_DELETE_WINDOW", self.on_sim_close)

    def on_sim_close(self):
        self.sim.destroy()
        self.sim = None
    
    def checkDir(self):
        if self.sim is not None and self.sim.winfo_exists():
            print("test")
        self.master.after(1000, self.checkDir)

    
    
# Run the application
root = tk.Tk()
main = mainUI(root)
root.mainloop()