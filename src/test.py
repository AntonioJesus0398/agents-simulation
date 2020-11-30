from main import *
from robot_strategies import HibridRobot

env = Enviroment(10, 10, 0, 5, 5)
r = HibridRobot(env)

while r.state not in ['FS', 'FF']:
    r.execute()
    env.change()
    env.time += 1

print(r.state)