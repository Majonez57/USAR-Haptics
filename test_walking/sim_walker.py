import random
import math

# Simplest Robot with movement capabilities
class Robot:
    def __init__(self, canvas, startpos):
        self.canvas = canvas
        self.id = "bot"
        
        # Positional Variables
        self.x = startpos[0]
        self.y = startpos[1]
        self.theta = -math.pi/2

        #Constants
        self.SIZE = 20 #Robot Size
        self.LSPEED = 1.5 #Robot Linear Speed

    def draw(self):
        size = self.SIZE
        
        points = [ (self.x + size*math.sin(self.theta)) - size*math.sin((math.pi/2.0)-self.theta), \
                   (self.y - size*math.cos(self.theta)) - size*math.cos((math.pi/2.0)-self.theta), \
                   (self.x - size*math.sin(self.theta)) - size*math.sin((math.pi/2.0)-self.theta), \
                   (self.y + size*math.cos(self.theta)) - size*math.cos((math.pi/2.0)-self.theta), \
                   (self.x - size*math.sin(self.theta)) + size*math.sin((math.pi/2.0)-self.theta), \
                   (self.y + size*math.cos(self.theta)) + size*math.cos((math.pi/2.0)-self.theta), \
                   (self.x + size*math.sin(self.theta)) + size*math.sin((math.pi/2.0)-self.theta), \
                   (self.y - size*math.cos(self.theta)) + size*math.cos((math.pi/2.0)-self.theta)  \
                ]
        self.canvas.create_polygon(points, fill="#403A38", tags=self.id)
    
        #Front indicator
        fx = self.x + math.cos(self.theta)*size
        fy = self.y + math.sin(self.theta)*size
        self.canvas.create_oval(fx+5, fy+5, fx-5, fy-5, tags=self.id, fill='yellow')
    
    # Turns a certain amount
    def turn(self, angle):
        self.theta += angle
        if self.theta > math.pi *2:
            self.theta -= math.pi*2
        elif self.theta < 0:
            self.theta += math.pi*2
    
    # Moves a certain amount in the current direction
    def forward(self, magnitude):
        self.x = self.x + math.cos(self.theta)*magnitude
        self.y = self.y + math.sin(self.theta)*magnitude
    
    # Make sure robot stays on screen
    def checkWrapping(self):
        #Wrapping around sides
        if not (0 < self.x < 900) or not (0 < self.y < 900):
            self.theta = (self.theta + math.pi/2) % 2*math.pi
            self.forward(self.LSPEED/2)
            #If somehow the robot has found itself outside the enviroment
            #Just teleport it back to the HQ
            if self.x > 1100:
                self.x = 950
            if self.x < -50:
                self.x = 50
            if self.y > 1100:
                self.y = 950
            if self.y < -50:
                self.y = 50

    # Robot Behaviours
    def act(self):
        
        self.checkWrapping()
        self.canvas.delete("bot")
        self.draw()
