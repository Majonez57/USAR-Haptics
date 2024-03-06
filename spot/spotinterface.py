from PIL import Image
import numpy as np
from datetime import datetime

from spot.spot_image_processing import rotate_image, detectTagValue

from bosdyn.api import image_pb2
import bosdyn.client
import bosdyn.client.util
from bosdyn.client.robot_state import RobotStateClient
from bosdyn.client.image import ImageClient, build_image_request


SPOT_IP = "192.168.80.3"

class SpotInterface:
    def __init__(self, spotIP=SPOT_IP) -> None:
        print("Attempting Spot Connection")

        # TODO get rid of this after testing 
        # address = input("Please enter Spot Robot IP: ")
        address = spotIP

        # Creating robot Object
        self.createConnection(address)

        # Create detection storage
        # This allows us to ensure dectections are only displayed every 
        # certain delay
        self.detectionHistory = {}

    #Connects to the robot and creates necessary clients
    def createConnection(self, address):
        try:
            sdk = bosdyn.client.create_standard_sdk('RobotStateClient')
            robot = sdk.create_robot(address)    
            bosdyn.client.util.authenticate(robot)
            self.robot_state_client = robot.ensure_client(RobotStateClient.default_service_name)
            self.image_client = robot.ensure_client(ImageClient.default_service_name)
            # Get regular camera sources
            self.image_sources = [src.name for src in self.image_client.list_image_sources() if 
                                  src.image_type == image_pb2.ImageSource.IMAGE_TYPE_VISUAL and 'depth' not in src.name]

            print(self.image_sources)
        except Exception as e:
            print("An error occured connecting to the robot: ")
            print(e)

    #Returns all visible detections
    def getDetections(self):
        ## Find a april tag within an image source
        ## Return the value of said tag

        detections = []

        for i in self.image_sources:
            # Get image
            try:
                img_req = build_image_request(i, quality_percent=100,
                                          image_format=image_pb2.Image.FORMAT_RAW)
                response = self.image_client.get_image([img_req])
            
            except Exception as e:
                print(e)
                continue

            width = response[0].shot.image.cols
            height = response[0].shot.image.rows

            data = response[0].shot.image.data

            img_grey = np.array(Image.frombytes('P', (int(width), int(height)), data, decoder_name='raw'))

            img_grey = rotate_image(img_grey, i)

            tags = detectTagValue(img_grey)

            if tags != []:
                detections += [x.tag_id for x in tags]

        return detections

    #Gets full robotic state
    def getState(self):
        return self.robot_state_client.get_robot_state()
    
    #Returns robot odometry
    def getOdom(self):
        state = self.getState()
        
        # TODO 
        transforms = state.kinematic_state.transforms_snapshot
        
        return transforms.child_to_parent_edge_map['odom'].parent_tform_child
    
    #Checks if certain time has passed since last detection of a certain type
    #Updates detection history
    def getAlerts(self, delay):
        detections = [str(x) for x in self.getDetections()]

        new = []
        for id in detections:
            if id in self.detectionHistory:
                if datetime.now().timestamp() - self.detectionHistory[id] < delay:
                    continue
            self.detectionHistory[id] = datetime.now().timestamp()
            new.append(id)
        
        return new

if __name__ == "__main__":
    b = SpotInterface()
    #print(b.getOdom())

    while True:
        alerts = b.getAlerts(10)
        if alerts != []:
            print(alerts)
