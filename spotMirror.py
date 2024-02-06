import math
from time import sleep
from haptics.hapticVest import HapticVest
from spot.spot_odom import Bridge


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

def extractPosition(odometryInfo):
    pos = odometryInfo.position 

    return pos.x, pos.y, pos.z


# Attempt connection to Robot
b = Bridge()

# Attempt connection to Vest
vest = HapticVest(r"haptics/patterns")

# Begin Feedback Loop

POLLRATE = 2 # Polls /s


odom = b.getOdom()
#Initial Rotation + Position
rx, ry, rz, rw = extractRotation(odom)
_, _, atheta = quaternion_to_euler(rx, ry, rz, rw)
ax, ay, az = extractPosition(odom)
print(f"INITIAL ANGLE: {atheta + 180}")
stopped = 5
atheta += 180
while True: #Maybe make this not infinite at some point?

    odom = b.getOdom()
    # Get current rotation
    rx, ry, rz, rw = extractRotation(odom)
    _, _, ntheta = quaternion_to_euler(rx, ry, rz, rw)

    ntheta += 180

    walkAngle = ntheta - atheta
    print(f"~{walkAngle}")
    walkAngle = walkAngle if walkAngle > 0 else 360+walkAngle

    print(atheta, ntheta)
    print(f"CURRENT ANGLE: {walkAngle}")

    # Is robot moving?
    x, y, z = extractPosition(odom)
    
    vdis = ((ax-x)**2 + (ay-y)**2 + (az-z)**2)**0.5

    #print(f"DELTA POSITION: {vdis}")

    if vdis > 3:
        stopped = 0
    else:
        stopped += 1

    if stopped < 5:
        # Play Correct Direction
        gap = 0.25
        vest.walk(walkAngle,intensity=200 ,gap = gap, speed= 0.1)

        totalw = gap + gap/2 # Wait from the vest actions
        
        if totalw < 1/POLLRATE:
            sleep((1/POLLRATE) - totalw) # Wait longer if required.
    else:
        # Static
        vest.angle(walkAngle, intensity=50, dur=1/POLLRATE)
    
    ax, ay, az = x, y, z

