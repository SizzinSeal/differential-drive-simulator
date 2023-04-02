import asyncio
import robot

robor = robot.Robot(10, 10)
robor.leftSpeed = 10
robor.rightSpeed = -2

async def main():
    await robor.initialize()

if __name__ == '__main__':
    asyncio.run(main())
