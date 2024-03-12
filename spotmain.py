import math
from time import sleep, time
from haptics.hapticVest import HapticVest
from spot.spotinterface import SpotInterface
import matplotlib.pyplot as plt

ALERTGAP = 12

SHOW_DIRECTION = True
SHOW_MOTION = True
SHOW_DETECTIONS = True
RECORD_PATH = True

# Simulated detections via april tags
APRIL_TO_DETECTION = {
    3: "EXAMPLE_1",
    4: "EXAMPLE_2",
    10: "EXAMPLE_3",
    9: "EXAMPLE_4"
}

DETECTION_PATTERNS = {
    "EXAMPLE_1": "CenterX",
    "EXAMPLE_2": "Top_360",
    "EXAMPLE_3": "Circle",
    "EXAMPLE_4": "Right"
}

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

def extract_rotation(odometryInfo):
    rotation = odometryInfo.rotation
    
    return rotation.x, rotation.y, rotation.z, rotation.w 

def extract_position(odometryInfo):
    pos = odometryInfo.position 

    return pos.x, pos.y, pos.z

POLLRATE = 2 # Polls /s

class spotVestDisplay:
    def __init__(self):
        try:
            # Attempt connection to robot
            self.robot = SpotInterface()
        except Exception as e:
            print("An Exception occured whilst connecting to the rorobot.t:")
            print(e)
            exit(0)

        try:
            # Attempt connection to Vest
            self.vest = HapticVest(r"haptics/all_patterns")
        except Exception as e:
            print("An Exception occured whilst connecting to haptic vest:")
            print(e)
            exit(0)

        if SHOW_MOTION and not SHOW_DIRECTION:
            print("WARNING: Motion cannot be shown without direction")
        if SHOW_DIRECTION:
            self.init_angle()
        if RECORD_PATH:
            self.path = []
        
    def init_angle(self):
        self.odom = self.robot.get_odometry()
        self.robot_init_theta = quaternion_to_euler(*extract_rotation(self.odom))[2] + 180 #Get rotation info
        self.robot_theta = self.robot_init_theta
        self.robot_pos = self.robot.get_pos() # Get position info
        print(f"LOG: Initial Robot Angle {self.robot_init_theta}")
        print(f"LOG: Initial Robot Position {self.robot_pos}")        

        self.loops_since_motion = 5
    
    # Displays the current walking angle of the robot
    def display_angle_to_vest(self):
        self.odom = self.robot.get_odometry()
        robot_new_theta = quaternion_to_euler(*extract_rotation(self.odom))[2] + 180 #Get rotation info

        # Change in angle since beggining
        robot_facing = robot_new_theta - self.robot_init_theta 
        robot_facing += 0 if robot_facing > 0 else 1 if robot_facing > -1 else 360 

        # Change in angle since last reading
        delta_theta = self.robot_theta - robot_new_theta
        #Map to correct range, deal with edges
        delta_theta -= 0 if delta_theta < 360 else 360 

        if SHOW_MOTION:
            robot_new_pos = self.robot.get_pos() # Get position info
            delta_pos = sum(map(lambda x,y: (x-y)**2, self.robot_pos, robot_new_pos))**0.5 #Mapping magic to get euclidian distance

            #print(delta_pos, delta_theta)

            if delta_pos > 0.15 or abs(delta_theta) > 15: #If amount moved is more than 2m, or turn more than 5 degrees
                self.loops_since_motion = 0 
            else:
                self.loops_since_motion += 1
        
        if self.loops_since_motion < 1: # Currently in motion
            gap = 0.25
            self.vest.display_walking(robot_facing, intensity=300 ,gap = gap, speed= 0.1)

            totalw = gap + gap/2 # Wait from the vest actions
            
            if totalw < 1/POLLRATE:
                sleep((1/POLLRATE) - totalw) # Wait longer if required.

        else: # No longer in motion 
            self.vest.display_angle(robot_facing, intensity=200, dur = 1/POLLRATE)

        self.robot_pos = robot_new_pos
        self.robot_theta = robot_new_theta


    # Displays any detected alerts
    def display_alerts_to_vest(self):
        alerts = self.robot.get_alerts(ALERTGAP)
        if alerts == []:
            return 0
        else:
            patterns = [DETECTION_PATTERNS[APRIL_TO_DETECTION[int(a)]] for a in alerts]
            # TODO Play all for now
            for p in patterns:
                self.vest.display_pattern(p) #Will block
                sleep(1.2) # Wait before playing next parttern to make them easier to distinguish
        return 1
    
    def take_paths(self):

        x, y, = self.robot.get_pos()
        
        self.path.append((round(x, 4), round(y, 4)))

EXPERIMENT_DUR = 20

def main():
    disp = spotVestDisplay()
    start = time()
    
    while time() - start < EXPERIMENT_DUR:
        if SHOW_DETECTIONS:
            disp.display_alerts_to_vest()
        if SHOW_DIRECTION:
            disp.display_angle_to_vest()
        if RECORD_PATH:
            disp.take_paths()
    
    x, y = zip(*disp.path)
    plt.figure()
    
    plt.plot(x, y, marker='o', linestyle='-', color='r')
    
    plt.xlabel('X')
    #plt.xlim(-8, 8)
    plt.ylabel('Y')
    #plt.ylim(-8, 8)
    plt.title('Path')
    
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()

