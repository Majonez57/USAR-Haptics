import tkinter as tk
from PIL import ImageTk, Image

def button_clicked(button_text):
    print("Button Clicked:", button_text)

root = tk.Tk()
root.title("USAR-Haptics-Training")

# Get screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set window size to half the screen width and height
window_width = screen_width // 2
window_height = screen_height // 2
root.geometry(f"{window_width}x{window_height}")

# Function to create buttons with images and text
def create_button(row, col, image_path, text):
    # Open and resize the image to fit the button
    image = Image.open(image_path)
    image = image.resize((170, 170), Image.ANTIALIAS) 
    image = ImageTk.PhotoImage(image)
    
    # Create the button with image and text
    button = tk.Button(root, text=text, image=image, compound=tk.TOP, command=lambda: button_clicked(text), font=("Helvetica", 14, "bold"), bg="white")
    button.image = image  # To prevent image from being garbage collected
    button.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

# Configure row and column weights to make buttons fill the space
for i in range(1, 3):  # 2 rows
    root.grid_rowconfigure(i, weight=1)
for i in range(3):  # 3 columns
    root.grid_columnconfigure(i, weight=1)

# Create buttons with images and text
create_button(1, 0, "resources/images/fire.jpg", "Fire")
create_button(1, 1, "resources/images/biohaz.jpg", "Biohazard")
create_button(1, 2, "resources/images/oxygen.jpg", "Low Oxygen")
create_button(2, 0, "resources/images/alive.png", "Uninjured Person")
create_button(2, 1, "resources/images/injured.png", "Injured Person")
create_button(2, 2, "resources/images/dead.jpg", "Dead Person")

example_label = tk.Label(root, text="< Label >", font=("Arial", 20, "bold"))
example_label.grid(row=0, column=0, columnspan=3, pady=10)

root.mainloop()
