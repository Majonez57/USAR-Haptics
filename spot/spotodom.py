import sys
import bosdyn.client
import bosdyn.client.util
from bosdyn.client.robot_state import RobotStateClient

class Bridge:
    def __init__(self) -> None:
        print("Attempting Spot Connection")
        self.robot_state_client = self.connectToSpot()

    def connectToSpot(self):
        
        address = input("Please enter Spot Robot IP: ")
        
        # Creating robot Object
        try:
            sdk = bosdyn.client.create_standard_sdk('RobotStateClient')
            robot = sdk.create_robot(address)    
            bosdyn.client.util.authenticate(robot)
            robot_state_client = robot.ensure_client(RobotStateClient.default_service_name)
        
            return robot_state_client
        except Exception as e:
            print("An error occured connecting to the robot: ")
            print(e)
        
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
    except Exception as e:
        print(":( adrian code sucks")
