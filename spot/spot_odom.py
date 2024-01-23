import sys
import bosdyn.client
import bosdyn.client.util
from bosdyn.client.robot_state import RobotStateClient

class bridge:
    def __init__(self) -> None:
        print("Attempting Spot Connection")
        self.robot_state_client = self.connectToSpot()

    def connectToSpot(self):
        
        bosdyn.client.util.add_base_arguements()
        
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
        return pass
