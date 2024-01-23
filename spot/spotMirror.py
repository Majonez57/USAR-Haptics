import tkinter as tk
import threading
import math
from time import sleep
from haptics.hapticVest import HapticVest
from spot_odom import Bridge


def quaternion_to_euler(x, y, z, w):
    # Normalize the quaternion
    norm = math.sqrt(x**2 + y**2 + z**2 + w**2)
    x /= norm
    y /= norm
    z /= norm
    w /= norm

    # Calculate angles
    roll = math.atan2(2 * (w * x + y * z), 1 - 2 * (x**2 + y**2))
    pitch = math.asin(2 * (w * y - z * x))
    yaw = math.atan2(2 * (w * z + x * y), 1 - 2 * (y**2 + z**2))

    # Convert angles to degrees if needed
    roll = math.degrees(roll)
    pitch = math.degrees(pitch)
    yaw = math.degrees(yaw)

    return roll, pitch, yaw

def extractRotation(odometryInfo):
    rotation = odometryInfo.rotation
    
    return rotation.x, rotation.y, rotation.z, rotation.w 


# Attempt connection to Robot
b = Bridge()

# Attempt connection to Vest
vest = HapticVest(r"haptics/patterns")

# Begin Feedback Loop

POLLRATE = 2 # Polls /s

#Initial Rotation
ax, ay, az = quaternion_to_euler(extractRotation(b.getOdom()))

while True: #Maybe make this not infinite at some point?

    # Get current rotation
    nx, ny, nz = quaternion_to_euler(extractRotation(b.getOdom()))

    # Insert Angle Fixing code if needed here!

    # Play Correct Direction
    gap = 0.5
    vest.walk(math.degrees(nz), gap = gap, speed= 0.15)

    totalw = gap + gap/2 # Wait from the vest actions
    
    if totalw < 1/POLLRATE:
        sleep((1/POLLRATE) - totalw) # Wait longer if required.

