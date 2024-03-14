from time import sleep
import os
from haptics.bhaptics import haptic_player

class HapticVest:
    def __init__(self, patternDir="all_patterns"):
        self.patternDir = patternDir
        self.player = haptic_player.HapticPlayer()
        sleep(1) # Assure connection is made with vest
        print("Vest Connection Complete")
        
        for fil in os.listdir(self.patternDir):
            f = os.path.join(self.patternDir, fil)
            self.player.register(f"{fil}_n", f) # Add this pattern to the list of known patterns

        sleep(0.2)
        print("Pattern Registration Complete")
        sleep(1)

    # Plays all saved patterns
    def play_all_patterns(self, delay=3):

        dir = self.patternDir

        for fil in os.listdir(dir):
            f = os.path.join(dir, fil)

            print(f"PLAYING: {fil.replace('.tact', '')}")

            self.player.submit_registered(f"{fil}_n") # Plays the submitted pattern
            sleep(delay)

    def display_warning(self):
        self.player.submit_registered_with_option(f"Incoming!.tact_n", 'temp', 
                                                  scale_option={"intensity": 300, "duration": 0.6},
                                                  rotation_option={"offsetAngleX": 0, "offsetY": 0})
        sleep(0.8)

    def display_pattern(self, name, dur=0, intensity=150, angle=0, warn=True):

        if warn:
            self.display_warning(self)
        self.player.submit_registered_with_option(f"{name}.tact_n", 'temp', 
                                                  scale_option={"intensity": intensity, "duration": dur}, 
                                                  rotation_option={"offsetAngleX": angle, "offsetY": 0})

        sleep(dur+0.2)

    def display_dots(self, af, dots,intensity=100, dur=0.2):
        dot_data = [{"index": x, "intensity": intensity} for x in dots]
        for i in dots:
            self.player.submit_dot("backFrame" if af == "Back" else "frontFrame", 
                                   "VestBack"  if af == "Back" else "VestFront", 
                                   dot_data, int(dur* 1000))
        
    def display_walking(self, angle, intensity=100, gap=0.5, speed=0.15):
        WALKSPEED = speed
        GAP = WALKSPEED if gap < WALKSPEED else gap # Gap must be at least walkspeed
        VESTROW = 3
        
        # Maybe replace this with some kind of match?
        if 293 <= angle <= 338:
            af = bf = "Front"
            ai = 0
            bi = 1
        elif 338 <= angle or angle < 23:
            af = bf = "Front"
            ai = 1
            bi  = 2
        elif 23 <= angle < 68:
            af = bf = "Front"
            ai = 2
            bi  = 3
        elif 68 <= angle < 113:
            af = "Front" 
            bf = "Back"
            ai = bi = 3
        elif 113 <= angle < 158:
            af = bf = "Back"
            ai = 3
            bi  = 2
        elif 158 <= angle < 203:
            af = bf = "Back"
            ai = 2
            bi  = 1
        elif 203 <= angle < 248:
            af = bf = "Back"
            ai = 1
            bi = 0
        else:
            af = "Back"
            bf = "Front" 
            ai = bi = 0

        #Row
        ai += VESTROW * 4
        bi += VESTROW * 4

        # TODO use self.dots instead!
        self.player.submit_dot("backFrame" if af == "Back" else "frontFrame", 
                               "VestBack"  if af == "Back" else "VestFront", 
                               [{"index": ai, "intensity": intensity}], int(WALKSPEED* 1000))
        sleep(GAP)
        self.player.submit_dot("backFrame" if bf == "Back" else "frontFrame", 
                               "VestBack"  if bf == "Back" else "VestFront", 
                               [{"index": bi, "intensity": intensity}], int(WALKSPEED* 1000))
        sleep(GAP/2)

    def display_angle(self, angle, intensity, dur):
        VESTROW = 3

        # Maybe replace this with some kind of match?
        if 293 <= angle <= 338:
            af = bf = "Front"
            ai = 0
            bi = 1
        elif 338 <= angle or angle < 23:
            af = bf = "Front"
            ai = 1
            bi  = 2
        elif 23 <= angle < 68:
            af = bf = "Front"
            ai = 2
            bi  = 3
        elif 68 <= angle < 113:
            af = "Front" 
            bf = "Back"
            ai = bi = 3
        elif 113 <= angle < 158:
            af = bf = "Back"
            ai = 3
            bi  = 2
        elif 158 <= angle < 203:
            af = bf = "Back"
            ai = 2
            bi  = 1
        elif 203 <= angle < 248:
            af = bf = "Back"
            ai = 1
            bi = 0
        else:
            af = "Back"
            bf = "Front" 
            ai = bi = 0

        
        #Row
        ai += VESTROW * 4
        bi += VESTROW * 4

        # TODO use self.dots instead!
        if af == bf:
            self.player.submit_dot("backFrame" if af == "Back" else "frontFrame", 
                                   "VestBack"  if af == "Back" else "VestFront", 
                                  [{"index": ai, "intensity": intensity},{"index": bi, "intensity": intensity}], int(dur* 1000))
        else:
            self.player.submit_dot("backFrame" if af == "Back" else "frontFrame", 
                                   "VestBack"  if af == "Back" else "VestFront", 
                                  [{"index": ai, "intensity": intensity}], int(dur* 1000))
            
            self.player.submit_dot("backFrame" if bf == "Back" else "frontFrame", 
                               "VestBack"  if bf == "Back" else "VestFront", 
                               [{"index": bi, "intensity": intensity}], int(dur* 1000))
        
        sleep(dur-.1)

if __name__ == "__main__":
    vest = HapticVest(r"haptics/all_patterns")

    #vest.play_all_patterns()
    #vest.display_pattern("Right", dur=1.5, intensity=400, angle=90)

    # while True:    
    #     vest.dots("Front", [0,1], dur=0.2)
    #     sleep(0.2)

    #vest.playPattern("All")
    
    #vest.playPattern("Top_360", 1.5, intensity=20)
    #vest.playPattern("Top_360", 1.5, intensity=40)
    #vest.playPattern("Top_360", 1.5, intensity=60)
    
    #vest.playPattern("Top_360", 1.5, intensity=80)
    #vest.playPattern("Top_360", 1.5, angle=100)

    for i in range(0, 370, 20):
        print(i)
        vest.display_angle(i, 400, 0.3)
    for i in range(0, 370, 20):    
        vest.display_angle(i, 150, 0.2)
        sleep(0.2)

# interval = 0.5
# durationMillis = 1000

# for i in range(20):
#     print(i, "back")
#     player.submit_dot("backFrame", "VestBack", [{"index": i, "intensity": 100}], durationMillis)
#     sleep(interval)

#     print(i, "front")
#     player.submit_dot("frontFrame", "VestFront", [{"index": i, "intensity": 100}], durationMillis)
#     sleep(interval)
