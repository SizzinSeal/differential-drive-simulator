import graphics
import asyncio
import time
import math
import screeninfo

## Get the primary monitor's resolution
monitor = screeninfo.get_monitors()[0]
win = graphics.GraphWin("Differential Drive Simulator", monitor.height/2, monitor.height/2)
win.setCoords(-72, -72, 72, 72)


## Clamp a value in a range
##
## {number} value - The value to clamp
## {number} min - The minimum value
## {number} max - The maximum value
##
## returns {number} - The clamped value
def clamp(value, min, max):
    if value < min:
        return min
    elif value > max:
        return max
    else:
        return value


## Robot class
class Robot:
    ## Robot constructor
    ##
    ## {number} trackWidth - Robot's track width in inches
    ## {number} maxSpeed - Robot's maximum speed in inches per second
    ## {number} x - Robot's initial x position in inches
    ## {number} y - Robot's initial y position in inches
    ## {number} theta - Robot's initial angle in radians
    ##
    ## returns {Robot} - the robot object
    def __init__(self, trackWidth, maxSpeed, x = 0, y = 0, theta = 0):
        self.trackWidth = trackWidth
        self.x = x
        self.y = y
        self.theta = theta
        self.leftSpeed = 0
        self.rightSpeed = 0
        self.lastTime = time.time()
        self.maxSpeed = maxSpeed
        self.body = graphics.Circle(graphics.Point(self.x, self.y), trackWidth/2)
        self.body.draw(win)

    async def initialize(self):
        task = asyncio.create_task(self.updater())
        await task
    
    ## Update the robot's position
    async def updater(self):
        while True:
            # update simulation position
            deltaTime = time.time() - self.lastTime
            deltaL = deltaTime * self.leftSpeed
            deltaR = deltaTime * self.rightSpeed
            self.lastTime = time.time()
            ## Calculate the robot's new position
            ## This is using inverse differential drive kinematics
            deltaTheta = (deltaR - deltaL) / self.trackWidth
            if deltaTheta == 0:
                chord = deltaR
            else:
                chord = 2 * math.sin(deltaTheta / 2) * (deltaR / deltaTheta - self.trackWidth / 2)
            averageTheta = (deltaTheta / 2) + self.theta
            # update robot position
            self.x += chord * -math.sin(averageTheta)
            self.y += chord * math.cos(averageTheta)
            self.theta += deltaTheta
            # update robot position on screen
            self.body.move(self.x - self.body.getCenter().getX(), self.y - self.body.getCenter().getY())
            # draw the wheels
            await asyncio.sleep(0.01)
    
    ## Set the speed of the robot
    ##
    ## {number} leftSpeed - The speed of the left wheel in inches per second
    ## {number} rightSpeed - The speed of the right wheel in inches per second
    def setSpeed(self, leftSpeed, rightSpeed):
        self.leftSpeed = clamp(leftSpeed, -self.maxSpeed, self.maxSpeed)
        self.rightSpeed = clamp(rightSpeed, -self.maxSpeed, self.maxSpeed)

