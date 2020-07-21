from robot import ArmEnv
from ddpg import DDPG
from memory import Memory, Transition

import torch

EPISODES = 1000
STEPS  = 200
BATCH_SIZE = 32

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Set env
env = ArmEnv()

s_dim = env.state_dim
a_dim = env.action_dim
a_bound = env.action_bound

model = DDPG(a_dim, s_dim, a_bound, 0.9, 0.01)
memory = Memory(30000)

def train():
    for i in range(EPISODES):
        score = 0
        value_loss, policy_loss = 0, 0
        state = torch.Tensor([env.reset()]).to(device)
        for j in range(STEPS):
            action = model.predict(state)
            next_state, reward, done = env.step(action.cpu().numpy()[0])
            score += reward
            mask = torch.Tensor([done]).to(device)
            reward = torch.Tensor([reward]).to(device)
            next_state = torch.Tensor([next_state]).to(device)
            memory.push(state, action, mask, next_state, reward)
            state = next_state
            if len(memory) > BATCH_SIZE:
                transitions = memory.sample(BATCH_SIZE)
                batch = Transition(*zip(*transitions))
                value_loss, policy_loss = model.train(batch)
            if done:
                break
        if done:
            model.save('./robot-model')
        print('Episode %d:%s Critic Loss %.2f, Action Loss %.2f' % (i+1, ' Finished Step %d,' % (j+1) if done else '', value_loss, policy_loss))

def test():
    model.load('./robot-model')
    state = torch.Tensor([env.reset()]).to(device)
    while True:
        env.render()
        action = model.predict(state)
        next_state, reward, done = env.step(action.cpu().numpy()[0])
        state = torch.Tensor([next_state]).to(device)

test()