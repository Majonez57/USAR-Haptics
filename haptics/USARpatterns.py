from haptics.hapticVest import HapticVest
from time import sleep
# File contains some shared Haptic Patterns


def display_dead(vest, style):
    if "A" in style:
        vest.display_pattern('Heartx2',intensity=200, dur=1)
        vest.display_pattern('Quad_X_Outwards',intensity=200, dur=1.5, warn=False)
    else: 
        vest.display_pattern('Small_Square_BL',intensity=200, dur=1)
    
def display_injured(vest, style):
    if "A" in style:
        vest.display_pattern('Heartx2',intensity=200, dur=1)
        vest.display_pattern('Zig_Zag_Col',intensity=200, dur=1.5, warn=False)
    else:
        vest.display_pattern('Small_Square_TL',intensity=200, dur=1)

def display_uninjured(vest, style):
    if "A" in style:
        vest.display_pattern('Heartx4',intensity=200, dur=1.5)
    else:
        vest.display_pattern('Small_Square_TR',intensity=200, dur=1)

def display_fire(vest, style):
    if "A" in style:
        vest.display_pattern('Right', dur=1.5, intensity=80, angle=90)
    else:
        vest.display_pattern('Small_Square_BR',intensity=200, dur=1)

def display_lowO(vest, style):
    if "A" in style:
        vest.display_pattern('Inward_heart_Spiral', dur=1)
        vest.display_pattern('Inward_heart_Spiral', dur=1 ,warn=False)
    else:
        vest.display_warning()
        vest.display_dots("Back", [0, 1, 4, 5], intensity=200, dur=1)
        sleep(1)

def display_bio(vest, style):
    if "A" in style:
        vest.display_pattern('Chevrons', dur=1.5)
    else:
        vest.display_warning()
        vest.display_dots("Back", [2, 3, 6, 7], intensity=200, dur=1)
        sleep(1)

def display_connection(vest, style):
    if "A" in style:
        vest.display_pattern('Top_360',intensity=200, dur=2)
    else:
        vest.display_warning()
        vest.display_dots("Back", [12, 13, 16, 17], intensity=200, dur=1)
        sleep(1)

def display_error(vest, style):
    if "A" in style:
        vest.display_pattern('Triple_Flip',intensity=200, dur=2)
    else:
        vest.display_warning()
        vest.display_dots("Back", [14, 15, 18, 19], intensity=200, dur=1)
        sleep(1)