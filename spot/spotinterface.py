from PIL import Image
import numpy as np
from datetime import datetime

from spot.spot_image_processing import rotate_image, detect_tags

from bosdyn.api import image_pb2
import bosdyn.client
import bosdyn.client.util
from bosdyn.client.robot_state import RobotStateClient
from bosdyn.client.image import ImageClient, build_image_request
from bosdyn.client.frame_helpers import (BODY_FRAME_NAME, ODOM_FRAME_NAME, VISION_FRAME_NAME,
                                         get_se2_a_tform_b)
from bosdyn.client import math_helpers


SPOT_IP = "192.168.80.3"

class SpotInterface:
    def __init__(self, spotIP=SPOT_IP) -> None:
        print("Attempting Spot Connection")

        # TODO get rid of this after testing 
        # address = input("Please enter Spot Robot IP: ")
        address = spotIP

        # Creating robot Object
        self.init_robot_connection(address)

        # Create detection storage
        # This allows us to ensure dectections are only displayed every 
        # certain delay
        self.detectionHistory = {}

    #Connects to the robot and creates necessary clients
    def init_robot_connection(self, address):
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
    def get_detections(self):
        ## Find a april tag within an image source
        ## Return the value of said tag

        detections = []
        for i in self.image_sources:
            # Get image
            try:
                img_req = build_image_request(i, quality_percent=100, image_format=image_pb2.Image.FORMAT_RAW)
                response = self.image_client.get_image([img_req])
            
            except Exception as e:
                print(e)
                continue

            # Extract image parameters and data
            width = response[0].shot.image.cols
            height = response[0].shot.image.rows
            data = response[0].shot.image.data

            # Transform image and detect april tags
            img_grey = np.array(Image.frombytes('P', (int(width), int(height)), data, decoder_name='raw'))
            img_grey = rotate_image(img_grey, i)
            tags = detect_tags(img_grey)

            # Make note of detected values
            if tags != []:
                detections += [x.tag_id for x in tags]

        return detections

    #Gets full robotic state
    def get_state(self):
        
        return self.robot_state_client.get_robot_state()
    
    #Returns robot odometry
    def get_odometry(self):
        state = self.get_state()
        
        transforms = state.kinematic_state.transforms_snapshot

        return transforms.child_to_parent_edge_map['vision'].parent_tform_child

    def get_pos(self):
        transforms = self.robot_state_client.get_robot_state().kinematic_state.transforms_snapshot

        out_tform_body = get_se2_a_tform_b(transforms, ODOM_FRAME_NAME, BODY_FRAME_NAME)

        return (out_tform_body.x, out_tform_body.y)

    #Checks if certain time has passed since last detection of a certain type
    #Updates detection history
    def get_alerts(self, delay):
        detections = [str(x) for x in self.get_detections()]

        new = []
        for id in detections:
            if id in self.detectionHistory:
                if datetime.now().timestamp() - self.detectionHistory[id] < delay:
                    continue
            self.detectionHistory[id] = datetime.now().timestamp()
            new.append(id)
        
        return new

def main():
    b = SpotInterface()
    #print(b.getOdom())

    while True:
        alerts = b.get_alerts(10)
        if alerts != []:
            print(alerts)

if __name__ == "__main__":
    main()
