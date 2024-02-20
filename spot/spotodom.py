from PIL import Image
import numpy as np
import cv2
from spot_image_processing import rotate_image, detectTagValue
from bosdyn.api import image_pb2
import bosdyn.client
import bosdyn.client.util
from bosdyn.client.robot_state import RobotStateClient
from bosdyn.client.image import ImageClient, build_image_request

class Bridge:
    def __init__(self) -> None:
        print("Attempting Spot Connection")
        address = input("Please enter Spot Robot IP: ")

        # Creating robot Object
        try:
            sdk = bosdyn.client.create_standard_sdk('RobotStateClient')
            robot = sdk.create_robot(address)    
            bosdyn.client.util.authenticate(robot)
            self.robot_state_client = robot.ensure_client(RobotStateClient.default_service_name)
            self.image_client = robot.ensure_client(ImageClient.default_service_name)
            # Get regular camera sources
            self.image_sources = [src.name for src in self.image_client.list_image_sources() if 
                                  src.image_type == image_pb2.ImageSource.IMAGE_TYPE_VISUAL and 'depth' not in src.name]




        except Exception as e:
            print("An error occured connecting to the robot: ")
            print(e)

    def detectedValues(self):
        ## Find a april tag within an image source
        ## Return the value of said tag

        for i in self.image_sources:
            # Get image
            img_req = build_image_request(i, quality_percent=100,
                                          image_format=image_pb2.Image.FORMAT_RAW)
            response = self.image_client.get_image([img_req])

            width = response[0].shot.image.cols
            height = response[0].shot.image.rows

            data = response[0].shot.image 

            img_grey = np.array(Image.frombytes('P', (int(width), int(height)), data, i))

            img_grey = rotate_image(img_grey, i)

            value = detectTagValue(img_grey)

            print(value)



    def getState(self):
        return self.robot_state_client.get_robot_state()
    
    def getOdom(self):
        state = self.getState()
        
        # TODO 
        transforms = state.kinematic_state.transforms_snapshot
        
        return transforms.child_to_parent_edge_map['odom'].parent_tform_child
    


if __name__ == "__main__":
    b = Bridge()
    
    try:
        print(b.getOdom())
        b.detectedValues()
    except Exception as e:
        print(":( adrian code sucks")
        print(e)
