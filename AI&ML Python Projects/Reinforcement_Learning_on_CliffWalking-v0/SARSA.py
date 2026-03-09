import gymnasium as gym
import random
import numpy as np
import time
from collections import deque
import pickle


from collections import defaultdict


EPISODES =  30000
LEARNING_RATE = .1
DISCOUNT_FACTOR = .99
EPSILON = 1
EPSILON_DECAY = .999


def default_Q_value():
    return 0

if __name__ == "__main__":
    env_name = "CliffWalking-v0"
    env = gym.envs.make(env_name)
    env.reset(seed=1)

    # You will need to update the Q_table in your iteration
    Q_table = defaultdict(default_Q_value) # starts with a pessimistic estimate of zero reward for each state.
    episode_reward_record = deque(maxlen=100)

    for i in range(EPISODES):
        episode_reward = 0
        done = False
        obs = env.reset()[0]

        ##########################################################
        # YOU DO NOT NEED TO CHANGE ANYTHING ABOVE THIS LINE
        # TODO: Replace the following with SARSA

        while (not done): #Adapted from HW10 coding session, selecting action using epsilon-greedy policy. 
            if random.uniform(0, 1) > EPSILON:
                v = max(Q_table[(obs, a)] for a in range(env.action_space.n)) #Getting max Q value for the current state. 
                pi = [a for a in range(env.action_space.n) if Q_table[obs, a] == v] #All actions that produce the max Q value. 
                action = random.sample(pi, 1)[0] #Randomly selecting one of the optimal actions. 
            else:
                action = env.action_space.sample() #only performs a random action.
            
            next_obs,reward,terminated,truncated,info = env.step(action)
            done = terminated or truncated

            if not done: #Selecting the next action using epsilon-greedy policy again. 
                if random.uniform(0, 1) > EPSILON:
                    v = max(Q_table[(next_obs, a)] for a in range(env.action_space.n))
                    pi = [a for a in range(env.action_space.n) if Q_table[(next_obs, a)] == v]
                    next_action = random.sample(pi, 1)[0]
                else:
                    next_action = env.action_space.sample()

                
                Q_table[(obs, action)] = (1 - LEARNING_RATE) * Q_table[(obs, action)] + LEARNING_RATE * (reward + DISCOUNT_FACTOR * Q_table[(next_obs, next_action)]) #Updating Q value for the current state using the provided SARSA formula. 

            else:
                Q_table[(obs, action)] = (1 - LEARNING_RATE) * Q_table[(obs, action)] + LEARNING_RATE * reward #If done, updating Q value multiplying by only reward. 

            obs = next_obs #updating current state. 

            if not done:
                action = next_action #If done, use the next action for the next iteration. 
            else:
                None
            
            episode_reward += reward #updating episode reward. 

        EPSILON *= EPSILON_DECAY #applying epsilon decay. 
                
        # END of TODO
        # YOU DO NOT NEED TO CHANGE ANYTHING BELOW THIS LINE
        ##########################################################

        # record the reward for this episode
        episode_reward_record.append(episode_reward) 
     
        if i % 100 == 0 and i > 0:
            print("LAST 100 EPISODE AVERAGE REWARD: " + str(sum(list(episode_reward_record))/100))
            print("EPSILON: " + str(EPSILON) )
    
    
    #### DO NOT MODIFY ######
    model_file = open(f'Q_TABLE_SARSA.pkl' ,'wb')
    pickle.dump([Q_table,EPSILON],model_file)
    model_file.close()
    #########################