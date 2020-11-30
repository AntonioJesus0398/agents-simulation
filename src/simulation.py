from main import *
from robot_strategies import HibridRobot, ProActiveBot

env = Enviroment(10, 10, 0, 5, 5, 0, 100)
hibrid = HibridRobot(env)
proactive = ProActiveBot(env)

# time_limit = 100 * env.t

# while r.state not in ['FS', 'FF'] and env.time < time_limit:
#     env.time += 1
#     r.execute()
#     env.change()
#     if env.time % env.t == 0:
#         env = env.variate()
#         r.enviroment = env
#         r.state = 'I'
