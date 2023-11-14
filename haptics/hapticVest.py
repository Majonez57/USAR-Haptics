from time import sleep
import os
from bhaptics import haptic_player

class HapticVest:
    def __init__(self, patternDir="patterns"):
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
    def playAll(self, delay=3):

        dir = self.patternDir

        for fil in os.listdir(dir):
            f = os.path.join(dir, fil)

            print(f"PLAYING: {fil.replace('.tact', '')}")

            self.player.submit_registered(f"{fil}_n") # Plays the submitted pattern
            sleep(delay)

    def playPattern(self, name, dur=3, intensity=100, angle=0):
        self.player.submit_registered(f"{name}.tact_n")
        self.player.submit_registered_with_option(name, 'temp', 
                                                  scale_option={"intensity": intensity, "duration": dur}, 
                                                  rotation_option={"offsetAngleX": angle, "offsetY": 0})

        sleep(dur)

    def walk(self, angle, intensity=100, gap=0.5, speed=0.25):
        WALKSPEED = speed
        GAP = WALKSPEED if gap < WALKSPEED else gap # Gap must be at least walkspeed
        
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

        self.player.submit_dot("backFrame" if af == "Back" else "frontFrame", 
                               "VestBack"  if af == "Back" else "VestFront", 
                               [{"index": ai, "intensity": intensity}], int(WALKSPEED* 1000))
        sleep(GAP)
        self.player.submit_dot("backFrame" if bf == "Back" else "frontFrame", 
                               "VestBack"  if bf == "Back" else "VestFront", 
                               [{"index": bi, "intensity": intensity}], int(WALKSPEED* 1000))
        sleep(GAP)


if __name__ == "__main__":
    vest = HapticVest(r"haptics/patterns")

    
    vest.playPattern("Top_360", 1.5)
    vest.playPattern("Top_360", 1.5, angle=180)

    for i in range(0, 370, 45):
        print(i)
        for j in range(0, 4):
            vest.walk(i, 200)
        sleep(0.1)

# interval = 0.5
# durationMillis = 1000

# for i in range(20):
#     print(i, "back")
#     player.submit_dot("backFrame", "VestBack", [{"index": i, "intensity": 100}], durationMillis)
#     sleep(interval)

#     print(i, "front")
#     player.submit_dot("frontFrame", "VestFront", [{"index": i, "intensity": 100}], durationMillis)
#     sleep(interval)
