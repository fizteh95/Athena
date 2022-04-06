import math
import random

import pygame

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BALL_SIZE = 10

NUMBER_OF_BALLS = 10


class Ball:
    """
    Class to keep track of a ball's location and vector.
    """

    def __init__(self, i, speed=0.02, change_speed=0.0):
        self.number = i
        self.x = 0
        self.y = 0
        self.alpha = -math.pi / 2
        self.speed = speed
        self.change_speed = change_speed
        self.now_speed = 0
        self.rand = random.randint(1, 100) / 100


def main():
    """
    This is our main program.
    """
    pygame.init()

    # Set the height and width of the screen
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Bouncing Balls")

    # Loop until the user clicks the close button.
    done = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    ball_list = [
        Ball(i, speed=random.randint(1, 100) / 1500, change_speed=(i / 3))
        for i in range(NUMBER_OF_BALLS)
    ]
    for i in range(NUMBER_OF_BALLS):
        pygame.draw.circle(screen, WHITE, [0, 0], make_radius(i), 2)

    # -------- Main Program Loop -----------
    while not done:
        # --- Event Processing
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            # elif event.type == pygame.KEYDOWN:
            #     # Space bar! Spawn a new ball.
            #     if event.key == pygame.K_SPACE:
            #         ball = make_ball()
            #         ball_list.append(ball)

        # --- Logic
        for ball in ball_list:
            # Move the ball's center
            move_ball(ball, make_radius(ball.number + 1))

        # --- Drawing
        # Set the screen background
        screen.fill(BLACK)

        # Draw the balls
        for ball in ball_list:
            pygame.draw.circle(screen, WHITE, [ball.x, ball.y], BALL_SIZE)
            pygame.draw.line(screen, WHITE, (400, 300), (ball.x, ball.y))
            pygame.draw.circle(
                screen, WHITE, [400, 300], make_radius(ball.number + 1), 2
            )

        # --- Wrap-up
        # Limit to 60 frames per second
        clock.tick(60)

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

    # Close everything down
    pygame.quit()


def move_ball(ball, radius):
    ball.x = 400 + radius * math.cos(ball.alpha + ball.rand)
    ball.y = 300 + radius * math.sin(ball.alpha + ball.rand)
    ball.alpha += ball.now_speed
    ball.now_speed = (
        ball.speed * math.cos(ball.change_speed) * math.sin(ball.change_speed / 3) * 5
    )
    ball.change_speed += 0.03 * ball.rand
    return ball


def make_radius(i):
    return ((i + 1) / NUMBER_OF_BALLS) * 250


if __name__ == "__main__":
    main()
