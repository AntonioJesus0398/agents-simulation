from main import _percent_to_number, Enviroment
from robot_strategies import HibridRobot, ProActiveBot
import random

def generate_enviroment():
    rows, columns = random.randint(8, 15), random.randint(8, 15)
    total_cells = rows * columns
    dirty_percent = random.randint(2, 10)
    obstacle_percent = random.randint(5, 10)
    kids = random.randint(_percent_to_number(3, total_cells), _percent_to_number(5, total_cells))
    t = random.randint(80, 150)
    return Enviroment(rows, columns, dirty_percent, obstacle_percent, kids, 0, t)

def simulate(no_envs, sims_per_env):
    hibrid_results = []
    proactive_results = []
    for e in range(no_envs):
        results_h = {'total_dirt': 0, 'total_time': 0, 'fails': 0, 'success': 0}
        results_p = dict(results_h)
        env = generate_enviroment()
        hibrid = HibridRobot(env)
        proactive = ProActiveBot(env)
        for s in range(sims_per_env):
            print(f'enviroment #{e + 1}, simulation #{s + 1}, hibrid')
            perform_simulation(hibrid, results_h)
            print(f'enviroment #{e + 1}, simulation #{s + 1}, proactive')
            perform_simulation(proactive, results_p)
        results_h['mean_dirt_cells'] = results_h['total_dirt'] / results_h['total_time']
        results_p['mean_dirt_cells'] = results_p['total_dirt'] / results_p['total_time']
        hibrid_results.append(results_h)
        proactive_results.append(results_p)
    print('\n\n\nResults:\n')
    for e in range(no_envs):
        print(f'enviroment #{e + 1}:\nHibrid:{hibrid_results[e]}\nProactive:{proactive_results[e]}\n\n')
    
    hibrid_globals = {}
    hibrid_globals['fails'] = sum(map(lambda d: d['fails'], hibrid_results))
    hibrid_globals['success'] = sum(map(lambda d: d['success'], hibrid_results))

    proactive_globals = {}
    proactive_globals['fails'] = sum(map(lambda d: d['fails'], proactive_results))
    proactive_globals['success'] = sum(map(lambda d: d['success'], proactive_results))

    print(f'General results:\nHibrid: {hibrid_globals}\nProactive:{proactive_globals}\n')



def perform_simulation(robot, results):
    env = robot.enviroment
    env.time = 0
    env = env.variate()
    robot.enviroment = env
    robot.state = 'I'
    time_limit = 100 * env.t
    while robot.state not in ['FS', 'FF'] and env.time < time_limit:
        env.time += 1
        robot.execute()
        env.change()
        results['total_dirt'] += env.dirt_cells_percent
        results['total_time'] += 1
        if env.time % env.t == 0:
            env = env.variate()
            robot.enviroment = env
            robot.state = 'I'

    if robot.state == 'FS':
        results['success'] += 1
    elif robot.state == 'FF':
        results['fails'] += 1

simulate(10, 5)