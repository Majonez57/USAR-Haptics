import tkinter as tk
from PIL import ImageTk, Image
from haptics.hapticVest import HapticVest
import haptics.USARpatterns as USAR
from random import shuffle


def create_button(root, pos, image_path, text, on_press):
    row, col = pos
    # Open and resize the image to fit the button
    image = Image.open(image_path)
    image = image.resize((130, 130), Image.ANTIALIAS) 
    image = ImageTk.PhotoImage(image)
    
    # Create the button with image and text
    button = tk.Button(root, text=text, image=image, compound=tk.TOP, command=on_press, font=("Helvetica", 14, "bold"), bg="white")
    button.image = image  # Jank to prevent image from being garbage collected
    button.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")

def connect_to_vest():
    try:
        vest = HapticVest(r"haptics/all_patterns")
        return vest
    except Exception as e:
        print("An error occured connecting to the haptic vest:")
        print(e)
        exit(0)

def main():
    
    participant = input("Enter Participant ID: ")
    vest = connect_to_vest()

    root = tk.Tk()
    root.title("USAR-Haptics-Training")

    # Get screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Set window size
    window_width  = screen_width // 2
    window_height = 2*screen_height // 3
    root.geometry(f"{window_width}x{window_height}")

    # Configure row and column weights to make buttons fill the space
    for i in range(1, 3):  # 2 rows
        root.grid_rowconfigure(i, weight=1)
    for i in range(4):  # 4 columns
        root.grid_columnconfigure(i, weight=1)

    # Shuffle Button Positions
    pos = [(1,0),(1,1),(1,2),(1,3),(2,0),(2,1),(2,2), (2,3)]
    
    #shuffle(pos)

    # Create buttons with images and text
    # Enviroment State
    create_button(root, pos[4], "resources/images/fire.jpg", "Fire", lambda: USAR.display_fire(vest, participant))
    create_button(root, pos[5], "resources/images/biohaz.jpg", "Biohazard", lambda: USAR.display_bio(vest, participant))
    create_button(root, pos[6], "resources/images/oxygen.jpg", "Low Oxygen", lambda: USAR.display_lowO(vest, participant))
    # User Detections
    create_button(root, pos[0], "resources/images/alive.png", "Uninjured Person", lambda: USAR.display_uninjured(vest, participant))
    create_button(root, pos[1], "resources/images/injured.png", "Injured Person", lambda: USAR.display_injured(vest, participant))
    create_button(root, pos[2], "resources/images/dead.jpg", "Unconscious Person", lambda: USAR.display_dead(vest, participant))
    # Robotic State
    create_button(root, pos[3], "resources/images/lost.png", "Connection Lost", lambda: USAR.display_connection(vest, participant))
    create_button(root, pos[7], "resources/images/robotIssue.jpg", "Robot Error", lambda: USAR.display_error(vest, participant))


    example_label = tk.Label(root, text="Press a Category to recieve message:", font=("Arial", 20, "bold"))
    example_label.grid(row=0, column=0, columnspan=4, pady=10)

    root.mainloop()

main()