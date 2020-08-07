from pinball.pinball import Pinball

if __name__ == "__main__":

    standard = {
        'size': {'width': 480, 'height': 360},
        'player': {
            'radius': 10,
            'position': (10, 10),
        },
        'mu': .5,
        'obstacles': [
            {'from': (360, 240), 'to': (120, 360)},
            {'from': (60, 360), 'to': (60, 240)},
        ],
        'enemies': [
            {'position': (100, 100), 'radius': 30, 'color': (255, 255, 255), 'score': 10},
            {'position': (200, 100), 'radius': 30, 'color': (255, 255, 255), 'score': 10},
            {'position': (300, 100), 'radius': 30, 'color': (255, 255, 255), 'score': 10},
            {'position': (400, 200), 'radius': 30, 'color': (255, 255, 255), 'score': 10},
            {'position': (100, 300), 'radius': 30, 'color': (255, 255, 255), 'score': 10},
            {'position': (200, 300), 'radius': 30, 'color': (255, 255, 255), 'score': 10},
            {'position': (300, 300), 'radius': 30, 'color': (255, 255, 255), 'score': 10},
            {'position': (400, 300), 'radius': 30, 'color': (255, 255, 255), 'score': 10},
        ],
        'chance': 10
    }

    env = Pinball(standard,render=True)
    action = [500, 500]
    observation = env.reset()
    for i in range(10):
        observation, reward, done = env.step(action)
    
