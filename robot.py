import graphics
import asyncio
import time
import math
import screeninfo
import colorsys

## Get the primary monitor's resolution
monitor = screeninfo.get_monitors()[0]
win = graphics.GraphWin("Differential Drive Simulator", monitor.height/2, monitor.height/2)
win.setCoords(-72, -72, 72, 72)

def hsv2rgb(h,s,v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))


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
        # robot properties
        self.trackWidth = trackWidth
        self.x = x
        self.y = y
        self.theta = theta
        self.leftSpeed = 0
        self.rightSpeed = 0
        self.lastTime = time.time()
        self.maxSpeed = maxSpeed
        # draw robot
        self.body = graphics.Circle(graphics.Point(self.x, self.y), trackWidth/2)
        self.leftWheel = graphics.Line(graphics.Point(0, 0), graphics.Point(0, 0))
        self.rightWheel = graphics.Line(graphics.Point(0, 0), graphics.Point(0, 0))
        self.body.setWidth(3)
        self.body.draw(win)
        self.leftWheel.draw(win)
        self.rightWheel.draw(win)

    ## Initialize the robot
    ##
    ## This function must be called for the robot to update its position
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
            # update position
            self.x += chord * -math.sin(averageTheta)
            self.y += chord * math.cos(averageTheta)
            self.theta += deltaTheta

            # calculate the location of the left wheel
            leftWheelX1 = self.x - self.trackWidth/2 * math.cos(self.theta)
            leftWheelY1 = self.y - self.trackWidth/2 * math.sin(self.theta)
            leftWheelX2 = leftWheelX1 + self.leftSpeed * math.cos(self.theta + math.pi/2)
            leftWheelY2 = leftWheelY1 + self.leftSpeed * math.sin(self.theta + math.pi/2)
            leftWheelP1 = graphics.Point(leftWheelX1, leftWheelY1)
            leftWheelP2 = graphics.Point(leftWheelX2, leftWheelY2)
            # calculate color of the left wheel
            leftWheelColor = hsv2rgb(math.fabs(self.leftSpeed / self.maxSpeed / 2), 0.5, 1)
            # calculate the location of the right wheel
            rightWheelX1 = self.x + self.trackWidth/2 * math.cos(self.theta)
            rightWheelY1 = self.y + self.trackWidth/2 * math.sin(self.theta)
            rightWheelX2 = rightWheelX1 + self.rightSpeed * math.cos(self.theta + math.pi/2)
            rightWheelY2 = rightWheelY1 + self.rightSpeed * math.sin(self.theta + math.pi/2)
            rightWheelP1 = graphics.Point(rightWheelX1, rightWheelY1)
            rightWheelP2 = graphics.Point(rightWheelX2, rightWheelY2)
            # calculate color of the right wheel
            rightWheelColor = hsv2rgb(math.fabs(self.rightSpeed / self.maxSpeed / 2), 0.5, 1)
            # update the robot's graphics
            self.body.move(self.x - self.body.getCenter().getX(), self.y - self.body.getCenter().getY())
            self.leftWheel.undraw()
            self.rightWheel.undraw()
            self.leftWheel = graphics.Line(leftWheelP1, leftWheelP2)
            self.rightWheel = graphics.Line(rightWheelP1, rightWheelP2)
            self.leftWheel.setFill(graphics.color_rgb(leftWheelColor[0], leftWheelColor[1], leftWheelColor[2]))
            self.rightWheel.setFill(graphics.color_rgb(rightWheelColor[0], rightWheelColor[1], rightWheelColor[2]))
            self.leftWheel.setWidth(5)
            self.rightWheel.setWidth(5)
            self.leftWheel.draw(win)
            self.rightWheel.draw(win)
            await asyncio.sleep(0.01)
    
    ## Set the speed of the robot
    ##
    ## {number} leftSpeed - The speed of the left wheel in inches per second
    ## {number} rightSpeed - The speed of the right wheel in inches per second
    def setSpeed(self, leftSpeed, rightSpeed):
        self.leftSpeed = clamp(leftSpeed, -self.maxSpeed, self.maxSpeed)
        self.rightSpeed = clamp(rightSpeed, -self.maxSpeed, self.maxSpeed)

