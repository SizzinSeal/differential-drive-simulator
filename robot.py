import graphics
import threading
import time
import math

win = graphics.GraphWin("Robot", 500, 500)



class Robot:
    def __init__ (self, trackWidth):
        self.x = 200
        self.y = 200
        self.angularVelocity = 0.01
        self.lateralVelocity = 1
        self.heading = 0
        self.body = graphics.Circle(graphics.Point(self.x, self.y), trackWidth)
        self.body.draw(win)
        self.updateThread = threading.Thread(self.update())
    def update(self):
        while True:
            dx = self.lateralVelocity * math.cos(self.heading)
            dy = self.lateralVelocity * math.sin(self.heading)
            self.x += dx
            self.y += dy
            self.lateralVelocity += 0.001
            self.heading += self.angularVelocity
            self.body.move(dx, dy)
            time.sleep(0.01)
    def move(self, angularVelocity, lateralVelocity):
        self.angularVelocity = angularVelocity
        self.lateralVelocity = lateralVelocity





# main function
def main():
    robot = Robot(10)
    input("Press any key to exit ...")


if __name__ == "__main__":
    main()