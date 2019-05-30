import random
import arcade
import math
import os

SPRITE_SCALING_SEAL = 0.2
SPRITE_SCALING_SHRIMPS = 0.2
SPRITE_SCALING_TRASH = 0.1

SHRIMPS_COUNT = 30
TRASH_COUNT = 15

SCREEN_WIDTH = 1250
SCREEN_HEIGHT = 800

class Seal(arcade.Sprite):
    def __init__(self, filename, sprite_scaling):
        super().__init__(filename, sprite_scaling)

        self.change_x = 0
        self.change_y = 0

    def update(self):
        # Move the seal
        self.center_x += self.change_x
        self.center_y += self.change_y

        # If we are out-of-bounds, then 'bounce'
        if self.left < 0:
            self.change_x *= -1

        if self.right > SCREEN_WIDTH:
            self.change_x *= -1

        if self.bottom < 0:
            self.change_y *= -1

        if self.top > SCREEN_HEIGHT:
            self.change_y *= -1

class MyGame(arcade.Window):
    """ Our custom Window Class"""

    def __init__(self):
        """ Initializer """
        # Call the parent class initializer
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Seal and Shrimps")

        # Variables that will hold sprite lists
        self.shrimps_list = None
        self.seal_list = None

        # Set up the player info
        self.player_sprite = None
        self.score = 0

        # Don't show the mouse cursor
        self.set_mouse_visible(False)

        arcade.set_background_color(arcade.color.SKY_BLUE)

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.shrimps_list = arcade.SpriteList()
        self.seal_list = arcade.SpriteList()

        # Score
        self.score = 0

        # Set up the player
        # Character images
        self.player_sprite = arcade.Sprite("images/seal.png", SPRITE_SCALING_SEAL)
        self.player_sprite.center_x = 120
        self.player_sprite.center_y = 120
        self.seal_list.append(self.player_sprite)


    def on_draw(self):
        """ Draw everything """
        arcade.start_render()
        self.seal_list.draw()


    def on_key_press(self, key, modifiers):
        # Pull down the apple to the ground
        if key == arcade.key.UP:
            self.player_sprite.center_y += 10

        if key == arcade.key.LEFT:
            self.player_sprite.center_x -= 10

        if key == arcade.key.RIGHT:
            self.player_sprite.center_x += 10

        if key == arcade.key.DOWN:
            self.player_sprite.center_y -= 10


def main():
    """ Main method """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
