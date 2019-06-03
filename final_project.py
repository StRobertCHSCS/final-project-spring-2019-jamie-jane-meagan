import random
import arcade
import math
import os

SPRITE_SCALING_ROCK = 0.5
SPRITE_SCALING_SEAL = 0.3
SPRITE_SCALING_SHRIMPS = 0.2
SPRITE_SCALING_TRASH = 0.08
SPRITE_SCALING_FISH = 0.1
SPRITE_SCALING_SHOOTER = 0.01

SHRIMPS_COUNT = 30
TRASH_COUNT = 15
FISH_COUNT = 2

SCREEN_WIDTH = 1250
SCREEN_HEIGHT = 800

SHOOT_SPEED = 5

INSTRUCTION_PAGE = 0
GAMEPLAY = 1
GAMEOVER = 2


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
        self.circle_speed = 0.01

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


class Trash(arcade.Sprite):

    def __init__(self, filename, sprite_scaling):

        super().__init__(filename, sprite_scaling)

        self.change_x = 0
        self.change_y = 0

    def update(self):

        # Move the fish
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


class Fish(arcade.Sprite):

    def __init__(self, filename, sprite_scaling):
        super().__init__(filename, sprite_scaling)

    def update(self):
        # move the fish
        self.center_y -= 1

        # see if the fish have fallen off the bottom of the screen
        # if so, reset it
        if self.top < 0:
            self.reset_pos()

    def reset_pos(self):
        # reset the fish to a random spot above the screen
        self.center_y = random.randrange(SCREEN_HEIGHT + 20, SCREEN_HEIGHT + 100)
        self.center_x = random.randrange(SCREEN_WIDTH)


class MyGame(arcade.Window):
    """ Our custom Window Class"""

    def __init__(self):
        """ Initializer """
        # Call the parent class initializer
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Seal and Shrimps")

        # background
        self.background = None

        # Open game with introduction page
        self.current_state = INSTRUCTION_PAGE

        # Timer
        self.total_time = 30.0

        # Variables that will hold sprite lists
        self.wall_list = None
        self.shrimps_list = None
        self.seal_list = None
        self.trash_list = None
        self.fish_list = None
        self.shooting_list = None

        # Set up the player info
        self.player_sprite = None
        self.score = 0
        self.lives = 3

        # Don't show the mouse cursor
        self.set_mouse_visible(True)

        self.background = arcade.load_texture("images/background.jpg")

        texture = arcade.load_texture("images/introscreen.png")
        self.instructions = texture

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.wall_list = arcade.SpriteList()
        self.shrimps_list = arcade.SpriteList()
        self.seal_list = arcade.SpriteList()
        self.trash_list = arcade.SpriteList()
        self.fish_list = arcade.SpriteList()
        self.shooting_list = arcade.SpriteList()

        # Score
        self.score = 0

        # Timer
        self.total_time = 45.0

        # Set up the player
        # Character images
        self.player_sprite = arcade.Sprite("images/seal.png", SPRITE_SCALING_SEAL)
        self.player_sprite.center_x = 1150
        self.player_sprite.center_y = 100
        self.seal_list.append(self.player_sprite)

        # Manually create and position a rock at 180, 85
        wall = arcade.Sprite("images/rock.png", SPRITE_SCALING_ROCK)
        wall.center_x = 180
        wall.center_y = 85
        self.wall_list.append(wall)

        # Manually creat and position a box at 1100, 240
        wall = arcade.Sprite("images/rock.png", SPRITE_SCALING_ROCK)
        wall.center_x = 1100
        wall.center_y = 220
        self.wall_list.append(wall)

        # Manually create and position a rock at
        wall = arcade.Sprite("images/rock.png", SPRITE_SCALING_ROCK)
        wall.center_x = 243
        wall.center_y = 38
        self.wall_list.append(wall)

        # lives
        self.lives = 3
        cur_pos = 10
        for i in range(self.lives):
            life = arcade.Sprite("images/lives.png", 0.5)
            life.center_x = cur_pos + life.width
            life.center_y = 765
            cur_pos += life.width
            self.wall_list.append(life)

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

            # Add the shrimps to the lists
            self.shrimps_list.append(shrimps)

        for i in range(TRASH_COUNT):
            # Create the trash instance
            # trash image
            trash = Trash("images/trash.png", SPRITE_SCALING_TRASH)

            # Position the trash
            trash.center_x = random.randrange(SCREEN_WIDTH)
            trash.center_y = random.randrange(SCREEN_HEIGHT)
            trash.change_x = random.randrange(-3, 4)
            trash.change_y = random.randrange(-3, 4)

            # Add the trash to the lists
            self.trash_list.append(trash)

        for i in range(FISH_COUNT):
            # Create the fish instance
            # Fish image
            fish = Fish("images/fish.png", SPRITE_SCALING_FISH)

            # position the fish
            fish.center_x = random.randrange(SCREEN_WIDTH)
            fish.center_y = random.randrange(SCREEN_HEIGHT)

            # add the fish to the lists
            self.fish_list.append(fish)

    def draw_instructions_page(self):
        """
        Draw an instruction page. Load the page as an image.
        """
        # page_texture = self.instructions()
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH,
                                      SCREEN_HEIGHT, self.instructions, 0)

    def draw(self):
        """ Draw everything """
        arcade.start_render()
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        self.wall_list.draw()
        self.seal_list.draw()
        self.shrimps_list.draw()
        self.trash_list.draw()
        self.fish_list.draw()
        self.shooting_list.draw()

        # Timer
        minutes = int(self.total_time) // 60
        seconds = int(self.total_time) % 60
        output = f"Time: {minutes:02d}:{seconds:02d}"
        arcade.draw_text(output, 10, 70, arcade.color.BLACK, 17)

        # put the text on the screen
        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 17)

        if len(self.shrimps_list) == 0 or self.score >= 50:
            arcade.draw_text("CONGRATULATIONS, YOU WON!", 340, 400, arcade.color.BLUE, 30)

        if len(self.trash_list) == 0 or self.score <= -3 or self.lives == 0:
            arcade.draw_text("GAME OVER!", 300, 400, arcade.color.RED, 75)

        if self.total_time == 0:
            arcade.draw_text("GAME OVER!", 300, 400, arcade.color.RED, 75)

    def on_key_press(self, key, modifiers):
        # Pull down the apple to the ground
        if key == arcade.key.UP:
            self.player_sprite.center_y += 45

        if key == arcade.key.LEFT:
            self.player_sprite.center_x -= 45

        if key == arcade.key.RIGHT:
            self.player_sprite.center_x += 45

        if key == arcade.key.DOWN:
            self.player_sprite.center_y -= 45

        if key == arcade.key.SPACE:
            if self.current_state == INSTRUCTION_PAGE:
                # Next page of instructions.
                self.current_state = GAMEPLAY


    def update(self, delta_time):
        if len(self.shrimps_list) > 0 and len(self.trash_list) > 0 and self.score > -3 and self.score < 50 and self.total_time > 0.0:
            self.shrimps_list.update()
            self.trash_list.update()
            self.fish_list.update()
            self.total_time -= delta_time

            # generate a list of all sprites that collided with the player
            shrimps_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.shrimps_list)
            trash_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.trash_list)
            fish_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.fish_list)

            # Loop through each colliding sprite, remove it, and add to the score.
            for shrimp in shrimps_hit_list:
                shrimp.kill()
                self.score += 1
                os.system("afplay shrimps.mp3&")

            for trash in trash_hit_list:
                trash.kill()
                self.score -= 1
                os.system("afplay trash.mp3&")

            for fish in fish_hit_list:
                fish.kill()
                self.score += 10
                os.system("afplay fish.mp3&")

        self.shooting_list.update()

        # Loop through each shot
        for shoot in self.shooting_list:

            # Check if trash is hit
            hit_list = arcade.check_for_collision_with_list(shoot, self.trash_list)

            # Remove pieces of trash that are hit
            if len(hit_list) > 0:
                shoot.kill()

            # Adjust score
            for trash in hit_list:
                trash.kill()
                self.score += 5
                os.system("afplay shoot.mp3&")

            # If the shot flies off-screen, remove it.
            if shoot.bottom > SCREEN_HEIGHT:
                shoot.kill()

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):

        # Create shooter
        shooter = arcade.Sprite("images/shooter.png", SPRITE_SCALING_SHOOTER)

        # Adjust position to match seal
        shooter.center_x = self.player_sprite.center_x
        shooter.center_y = self.player_sprite.center_y
        shooter.change_y = SHOOT_SPEED
        shooter.angle = 90

        self.shooting_list.append(shooter)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()

        if self.current_state == INSTRUCTION_PAGE:
            self.draw_instructions_page()

        elif self.current_state == GAMEPLAY:
            self.draw()

        else:
            self.draw()


def main():
    """ Main method """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
