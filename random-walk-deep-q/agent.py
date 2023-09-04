
import torch
import random
import numpy as np
import matplotlib.pyplot as plt
from collections import deque
from walk_game import WalkGame
from model import Linear_QNet, QTrainer
from IPython import display

###
# TODO: include option to load the model
#   https://stackoverflow.com/questions/42703500/best-way-to-save-a-trained-model-in-pytorch
###


MAX_MEMORY = 100000
BATCH_SIZE = 1000
LR = 0.001  # learning rate

HIST_LENGTH = 150  # number of prices in history to make decision from


plt.ion()


class Agent(object):
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0  # randomness
        self.gamma = 0.9  # discount rate
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = Linear_QNet(HIST_LENGTH + 4, 512, 2)
        self.trainer = QTrainer(self.model, LR, self.gamma)

    @staticmethod
    def adjust_list(list_to_adjust, length):
        diff = max(length - len(list_to_adjust), 0)
        return (
            list_to_adjust[-HIST_LENGTH:]
            if diff == 0
            else [-1] * diff + list_to_adjust
        )

    def get_state(self, game):
        value = max(game.total_value, 0)
        assets = max(game.asset_volume, 0)
        # start = max(game.starting_price, 0)
        last_txn_price = max(game.last_transaction_price, 0)
        price = max(game.current_price, 0)
        price_history = self.adjust_list(game.price_history, HIST_LENGTH)

        state = [
            *price_history,  # the last HIST_LENGTH prices
            value,  # current value (balance + asset value)
            assets,  # asset volume
            # start,  # starting prices
            last_txn_price,  # last transaction price => sell higher, buy lower
            price  # current price
        ]
        # print(state)

        return np.array(state, dtype=float)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)  # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state) -> list:
        # random moves: tradeoff exploration / exploitation
        self.epsilon = 80 - self.n_games
        final_move = [0, 0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 1)  # 0 or 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
        final_move[move] = 1
        return final_move


def train():
    plot_scores = []
    plot_mean_scores = []
    plot_ma_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = WalkGame(starting_price=100, volatility=3, length=2000)

    while True:
        done = False
        score = 0

        # only train once enough data
        if game.iteration < HIST_LENGTH:
            game.play_step([0, 0])
        else:
            state_old = agent.get_state(game)
            final_move = agent.get_action(state_old)

            # perform move and get new state
            reward, done, score = game.play_step(final_move)
            state_new = agent.get_state(game)

            # train short memory
            agent.train_short_memory(state_old, final_move, reward, state_new, done)

            # remember
            agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            # train the long memory (experience) and plot result
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()

            print('Game', agent.n_games, 'Score', score, 'Record', record)

            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            ma_score = get_ma(plot_scores, 30)
            plot_mean_scores.append(mean_score)
            plot_ma_scores.append(ma_score)
            plot(plot_scores, plot_mean_scores, plot_ma_scores)


def get_ma(a_list, n):
    calc_list = a_list[-n:]
    return sum(calc_list)/len(calc_list)


def plot(scores, mean_scores, ma_scores):
    display.clear_output(wait=True)
    display.display(plt.gcf())
    plt.clf()
    plt.title('Training...')
    plt.xlabel('Number of Games')
    plt.ylabel('Final Value')
    plt.plot(scores, linestyle='-', color='blue')
    plt.plot(mean_scores, linestyle='-', color='red')
    plt.plot(ma_scores, linestyle='--', color='green')
    plt.ylim(ymin=0)
    plt.text(len(scores)-1, scores[-1], str(round(scores[-1])))
    plt.text(len(mean_scores)-1, mean_scores[-1], str(round(mean_scores[-1])))
    plt.text(len(ma_scores)-1, ma_scores[-1], str(round(ma_scores[-1])))
    plt.show(block=False)
    plt.pause(.1)


if __name__ == '__main__':
    train()
