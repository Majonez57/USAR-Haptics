from time import sleep
from bhaptics import haptic_player


player = haptic_player.HapticPlayer()
sleep(0.4) # Assure connection is made with vest

player.register("Right", "patterns/Right.tact") # Add this pattern to the list
player.submit_registered("Right") # Plays the submitted pattern
sleep(2)

player.submit_registered_with_option("Right", "alt",
                                     scale_option={"intensity": 1, "duration": 1},
                                     rotation_option={"offsetAngleX": 180, "offsetY": 0}) #Does not produce an error if thing is non-registered
sleep(1)


# interval = 0.5
# durationMillis = 1000

# for i in range(20):
#     print(i, "back")
#     player.submit_dot("backFrame", "VestBack", [{"index": i, "intensity": 100}], durationMillis)
#     sleep(interval)

#     print(i, "front")
#     player.submit_dot("frontFrame", "VestFront", [{"index": i, "intensity": 100}], durationMillis)
#     sleep(interval)

