
import pygame
import random
import numpy as np
from enum import Enum
from frame_calcs import FrameCalculator


###
# Module constants
###

# SPEED = 10  # for humans
SPEED = 150  # for robots

TIMEOUT = 300

FRAME_X = 800
FRAME_Y = 480
PADDING = 10
BOX1_X = 300
BOX1_Y = 100

WHITE = (255, 255, 255)
RED = (255, 000, 000)
GREEN = (000, 255, 000)
BLUE = (000, 000, 255)
BLACK = (000, 000, 000)


class Keypress(Enum):
    NONE = 0  # using it otherwise keypress doesn't change
    UP = 1  # buy
    DOWN = 2  # sell


###
# PyGame stuff
###
pygame.init()
font = pygame.font.SysFont('comicsans', 24, True)


class WalkGame(object):
    """
    A random walk to emulate buying and selling of assets
    """
    def __init__(self, starting_price, volatility, length):
        # price line properties
        self.starting_price = starting_price
        self.current_price = starting_price
        self.volatility = volatility
        self.length = length
        self.price_history = [starting_price]
        self.last_transaction_price = -1
        self.last_transaction = 0

        # set display
        self.display = pygame.display.set_mode((FRAME_X, FRAME_Y))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Random Walk')

        self.frame_info = FrameCalculator(
            frame_x=FRAME_X,
            frame_y=FRAME_Y,
            padding=PADDING,
            box1_x=BOX1_X,
            box1_y=BOX1_Y
        )

        # game properties
        self.keypress = Keypress.NONE
        self.iteration = 0
        self.starting_balance = 500
        self.balance = self.starting_balance
        self.asset_volume = 0
        self.game_over = False

        self.reward = 0

    def reset(self):
        self.keypress = Keypress.NONE
        self.iteration = 0
        self.balance = self.starting_balance
        self.asset_volume = 0
        self.game_over = False
        self.reward = 0

        self.starting_price = random.randint(100, 200)
        self.volatility = random.uniform(1, 10)
        self.current_price = self.starting_price
        self.price_history = [self.starting_price]
        self.last_transaction = 100  # HIST_LENGTH

    @property
    def total_value(self) -> float:
        return self.balance + (self.asset_volume * self.current_price)

    @property
    def buy_price(self) -> float:
        return self.current_price * 1.01

    @property
    def sell_price(self) -> float:
        return self.current_price / 1.01

    def play_step(self, action) -> (int, bool, float):
        self.iteration += 1

        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.keypress = Keypress.UP
                elif event.key == pygame.K_DOWN:
                    self.keypress = Keypress.DOWN

        # 2. update balances
        self._user_action(action)
        self.keypress = Keypress.NONE

        # 3. check if game over
        self.reward = 0
        self.game_over = False
        if self.iteration > self.length or self.last_transaction + TIMEOUT < self.iteration:
            # end of 'game' or transaction timeout (avoiding the hold and wait strategy)
            self.game_over = True
            if self.total_value < self.starting_balance or self.last_transaction + TIMEOUT < self.iteration:
                self.reward = -10
            return self.reward, self.game_over, self.total_value

        # 4. update price
        self._update_price()
        self.reward = self.total_value - self.starting_balance

        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)

        # 6. return game over and value
        return self.reward, self.game_over, self.total_value

    def _update_price(self):
        self.price_history.append(self.current_price)
        self.current_price = max(
            self.current_price + random.uniform(-self.volatility, self.volatility),
            0
        )

    def _user_action(self, action):
        # [buy, sell]
        if np.array_equal(action, [0, 0]):
            new_action = Keypress.NONE
        elif np.array_equal(action, [1, 0]):
            new_action = Keypress.UP
        elif np.array_equal(action, [0, 1]):
            new_action = Keypress.DOWN
        else:
            new_action = Keypress.NONE

        self.keypress = new_action

        # now do the thing
        if self.keypress == Keypress.UP:
            self._buy_asset()
        elif self.keypress == Keypress.DOWN:
            self._sell_asset()

    def _buy_asset(self):
        if self.balance > 0:
            if self.buy_price > 0:
                self.asset_volume = (self.balance / self.buy_price)
                self.balance = 0
                self.last_transaction_price = self.current_price
                self.last_transaction = self.iteration

    def _sell_asset(self):
        if self.asset_volume > 0:
            self.balance = (self.asset_volume * self.sell_price)
            self.asset_volume = 0
            self.last_transaction_price = self.current_price
            self.last_transaction = self.iteration

    def _update_ui(self):
        # set up display
        self.display.fill(WHITE)
        pygame.draw.rect(self.display, RED, pygame.Rect(*self.frame_info.box1), 2)
        pygame.draw.rect(self.display, RED, pygame.Rect(*self.frame_info.box2), 2)
        pygame.draw.rect(self.display, RED, pygame.Rect(*self.frame_info.box3), 2)

        # box3 graph
        if len(self.price_history) > 1:
            pygame.draw.lines(
                surface=self.display,
                color=BLUE,
                closed=False,
                points=[self._point_map(i, p) for i, p in enumerate(self.price_history, start=10)]  # [(0, p_1), ..., (n, p_n)]
            )

        # box1 text
        iter_text = font.render(f"Iteration: {str(self.iteration)}", True, BLACK)
        bal_text = font.render(f"Balance: {str(round(self.balance, 2))}", True, BLACK)
        asset_text = font.render(
            f"Asset: {str(round(self.asset_volume, 2))}", True, BLACK
        )
        value_text = self._font_render('Total Value', self.total_value)

        box1_x, box1_y = self.frame_info.box1[:2]

        self.display.blit(iter_text, [box1_x + 5, box1_y + 5])
        self.display.blit(bal_text, [box1_x + 5, box1_y + 30])
        self.display.blit(asset_text, [box1_x + 5, box1_y + 55])
        self.display.blit(value_text, [box1_x + 5, box1_y + 80])

        # box2 text
        price_text = font.render(
            f"Current Price: {str(round(self.current_price, 2))}", True, BLACK
        )
        # start_text = self._font_render('Start Price', self.starting_price)
        txn_p_text = self._font_render('Last Action Price', self.last_transaction_price)
        txn_t_text = self._font_render('Last Action', self.last_transaction)
        reward_text = self._font_render('Reward', self.reward)

        box2_x, box2_y = self.frame_info.box2[:2]

        self.display.blit(price_text, [box2_x + 5, box2_y + 5])
        self.display.blit(txn_p_text, [box2_x + 5, box2_y + 30])
        self.display.blit(txn_t_text, [box2_x + 5, box2_y + 55])
        self.display.blit(reward_text, [box2_x + 5, box2_y + 80])

        # update
        pygame.display.flip()  # updates entire display
        # pygame.display.update()  # updates the portion of the screen passed as arg

    @staticmethod
    def _font_render(key_text, key):
        return font.render(f'{key_text}: {str(key)}', True, BLACK)

    def _point_map(self, xpoint, ypoint):
        """
        Take in an (x, y) coord and return the (x, y) coord for the box3 pygame frame
        """
        x = 3 * PADDING + FRAME_X*(xpoint - 2 * PADDING)/(self.length + 6*PADDING)
        y = FRAME_Y - 2 * PADDING - ypoint
        return x, y


if __name__ == '__main__':
    game = WalkGame(starting_price=100, volatility=3, length=1000)

    # game loop
    while True:
        game_over, value = game.play_step()

        if game_over:
            break

    print('Final Value', value)
    pygame.quit()
