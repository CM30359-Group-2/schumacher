import os
import gym
import json
import time

from agents.q_learning import QLearning

script_dir = os.path.dirname(__file__)
transitions = []
filename = os.path.join(script_dir, "demos", "epNo" + str(time.time()) + ".json")


def game_callback(obs_t, obs_tp1, action, rew, done, info):
    global filename
    global transitions

    stateData = {
        "obs_t": obs_t.tolist(),
        "obs_tp1": obs_tp1.tolist(),
        "action": action.tolist(),
        "rew": rew,
        "done": done,
        "info": info
    }

    transitions.append(stateData)
    episode_reward = sum([x["rew"] for x in transitions])

    if done and len(transitions) > 0 and episode_reward > 200:
        with open(filename, "w") as file:
            dumped_transitions = json.dumps({
                "strategy": "example",  # Fill in whatever the chosen strategy is, if none, put 'N/A'
                "user": "Q",  # Fill in the user who is controlling this demonstration episode
                "data": transitions
            }, indent=4)
            file.write(dumped_transitions)
        transitions = []
        filename = os.path.join(script_dir, "demos", "epNo" + str(time.time()) + ".json")

if __name__ == '__main__':
    env = gym.make('LunarLander-v2')
    agent = QLearning(action_space=env.action_space.n, state_space=env.observation_space.shape[0])
    agent.play(env, episodes=100, step_callback=game_callback)

