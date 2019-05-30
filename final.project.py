import random
import arcade
import math
import os

SPRITE_SCALING_PLAYER = 0.4
SPRITE_SCALING_SHRIMPS = 0.2
SPRITE_SCALING_TRASH = 0.1

SHRIMPS_COUNT = 35
TRASH_COUNT = 15

SCREEN_WIDTH = 1250
SCREEN_HEIGHT = 800

class Shrimps(arcade.Sprite):

    def __init__(self, filename, sprite_scaling):
        """ Constructor. """
        # Call the parent class (Sprite) constructor
        super().__init__(filename, sprite_scaling)

        # Current angle in radians
        self.circle_angle = 0

        # How far away from the center to orbit, in pixels
        self.circle_radius = 0

        # How fast to orbit, in radians per frame
        self.circle_speed = 0.008

        # Set the center of the point we will orbit around
        self.circle_center_x = 0
        self.circle_center_y = 0

    def update(self):
        """ Update the ball's position. """
        # Calculate a new x, y
        self.center_x = self.circle_radius * math.sin(self.circle_angle) \
                        + self.circle_center_x
        self.center_y = self.circle_radius * math.cos(self.circle_angle) \
                        + self.circle_center_y

        # Increase the angle in prep for the next round.
        self.circle_angle += self.circle_speed

class MyGame(arcade.Window):
    """ Our custom Window Class"""

    def __init__(self):
        """ Initializer """
        # Call the parent class initializer
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Seals love shrimps ")

        # Variables that will hold sprite lists
        self.shrimps_list = None

        # set the background
        arcade.set_background_color(arcade.color.SKY_BLUE)

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.shrimps_list = arcade.SpriteList()

        # Create the shrimps
        for i in range(SHRIMPS_COUNT):
            # Create the shrimps instance
            # shrimp image
            shrimps = Shrimps("images/shrimps.png", SPRITE_SCALING_SHRIMPS)

            # Position the center of the circle the can will orbit
            shrimps.circle_center_x = random.randrange(SCREEN_WIDTH)
            shrimps.circle_center_y = random.randrange(SCREEN_HEIGHT)

            # Random radius from 10 to 200
            shrimps.circle_radius = random.randrange(10, 200)

            # Random start angle from 0 to 2pi
            shrimps.circle_angle = random.random() * 2 * math.pi

            # Add the can to the lists
            self.shrimps_list.append(shrimps)

    def on_draw(self):
        """ Draw everything """
        arcade.start_render()
        self.shrimps_list.draw()

    def update(self, delta_time):
        if len(self.shrimps_list) > 0:
            self.shrimps_list.update()

def main():
    """ Main method """
    window = MyGame()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()