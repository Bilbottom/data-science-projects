
import pygame
import random
from enum import Enum
from frame_calcs import FrameCalculator


###
# Module constants
###

SPEED = 10  # for humans
# SPEED = 100  # for humans

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
    UP = 1
    DOWN = 2


###
# PyGame stuff
###
pygame.init()
font = pygame.font.SysFont('comicsans', 30, True)


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
        self.price_iteration = 0
        self.balance = 500
        self.asset_volume = 0
        self.game_over = False

        self.reward = 0

    def reset(self):
        self.keypress = Keypress.NONE
        self.price_iteration = 0
        self.balance = 500
        self.asset_volume = 0
        self.game_over = False
        self.reward = 0

    @property
    def total_value(self) -> float:
        return self.balance + (self.asset_volume * self.current_price)

    @property
    def buy_price(self) -> float:
        return self.current_price * 1.01

    @property
    def sell_price(self) -> float:
        return self.current_price / 1.01

    def play_step(self) -> (int, bool, float):
        self.price_iteration += 1

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
        self._user_action()
        self.keypress = Keypress.NONE

        # 3. check if game over
        self.reward = 0
        self.game_over = False
        if self.price_iteration > self.length:
            self.game_over = True
            self.reward = -10
            return self.game_over, self.total_value

        # 4. update price
        self._update_price()
        if self.total_value > self.starting_price:
            self.reward = self.total_value / self.starting_price

        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)

        # 6. return game over and value
        return self.game_over, self.total_value

    def _update_price(self):
        self.price_history.append(self.current_price)
        self.current_price = max(
            self.current_price + random.uniform(-self.volatility, self.volatility),
            0
        )

    def _user_action(self):
        if self.keypress == Keypress.UP:
            self._buy_asset()
        elif self.keypress == Keypress.DOWN:
            self._sell_asset()

    def _buy_asset(self):
        if self.balance > 0:
            self.asset_volume = (self.balance / self.buy_price)
            self.balance = 0

    def _sell_asset(self):
        if self.asset_volume > 0:
            self.balance = (self.asset_volume * self.sell_price)
            self.asset_volume = 0

    def _update_ui(self):
        self.display.fill(WHITE)
        if len(self.price_history) > 1:
            pygame.draw.lines(
                surface=self.display,
                color=BLUE,
                closed=False,
                points=[self._point_map(i, p) for i, p in enumerate(self.price_history, start=10)]  # [(0, p_1), ..., (n, p_n)]
            )
        # pygame.draw.rect(self.display, RED, pygame.Rect(10, 10, 90, 90), 2)
        pygame.draw.rect(self.display, RED, pygame.Rect(*self.frame_info.box1), 2)
        pygame.draw.rect(self.display, RED, pygame.Rect(*self.frame_info.box2), 2)
        pygame.draw.rect(self.display, RED, pygame.Rect(*self.frame_info.box3), 2)

        iter_text = font.render(f"Iteration: {str(self.price_iteration)}", True, BLACK)
        price_text = font.render(
            f"Current Price: {str(round(self.current_price, 2))}", True, BLACK
        )
        bal_text = font.render(f"Balance: {str(self.balance)}", True, BLACK)
        asset_text = font.render(f"Asset: {str(self.asset_volume)}", True, BLACK)
        self.display.blit(iter_text, [0, 0])
        self.display.blit(price_text, [0, 25])
        self.display.blit(bal_text, [0, 50])
        self.display.blit(asset_text, [0, 75])
        pygame.display.flip()  # updates entire display
        # pygame.display.update()  # updates the portion of the screen passed as arg

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
