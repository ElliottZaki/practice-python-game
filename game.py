# Import the pygame module
import pygame

# Import random for random numbers
import random

# Initialize pygame
pygame.init()

# Import pygame.locals for easier access to key coordinates
from pygame.locals import (
  RLEACCEL, # does something to allow uploaded images to render on the screen
  K_UP, # recognises the up key
  K_DOWN, # recognises the down key
  K_LEFT, # recognises the left key
  K_RIGHT, # recognises the right key
  K_ESCAPE, # recognises the esc key
  KEYDOWN, # listens for when any key is pressed
  QUIT, # recognises the wondow's quit button
)

# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HIGHT = 600

# Define a Player object using pygame.sprite.Sprite
# Sprite is a library that helps is class diff objects in the game
# and perform methods on them
class Player(pygame.sprite.Sprite):
  def __init__(self):
    super(Player, self).__init__()
    # we would have used the below line if there wasnt an image being uploaded, to set teh surface area of the player
    # self.surf = pygame.Surface((75, 25)) 
    self.surf = pygame.image.load("hacker.jpeg").convert() # loads the image
    self.surf = pygame.transform.scale(self.surf, (75, 75)) # resizes the image
    self.surf.set_colorkey((255, 255, 255), RLEACCEL) # something magic with the colour?
    self.rect = self.surf.get_rect() # I don't fully understand but I believe this represents the location
  
  # update is called at the end of every frame
  # if a key has been pressed that is apssed into the method
  # the player moves according to whish key is pressed
  def update(self, pressed_keys):
    if pressed_keys[K_UP]:
      self.rect.move_ip(0, -5)
    if pressed_keys[K_DOWN]:
      self.rect.move_ip(0, 5)
    if pressed_keys[K_LEFT]:
      self.rect.move_ip(-5, 0)
    if pressed_keys[K_RIGHT]:
      self.rect.move_ip(5, 0)

    # this code keeps player on the screen
    # if they try to move off they are reset to the edge of the screen
    if self.rect.left < 0:
        self.rect.left = 0
    if self.rect.right > SCREEN_WIDTH:
        self.rect.right = SCREEN_WIDTH
    if self.rect.top <= 0:
        self.rect.top = 0
    if self.rect.bottom >= SCREEN_HIGHT:
        self.rect.bottom = SCREEN_HIGHT

# Defines the enemy(laptop) object with pygame.sprite.Sprite
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("laptop.jpeg").convert()
        self.surf = pygame.transform.scale(self.surf, (30, 30))
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        # this assigns the enemy to a random location
        # between 20 - 100 px to the right of the screen
        # and at a random hight within the screens limit
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HIGHT),
            )
        )
        # this assigns a random speed to the object within a range
        self.speed = random.randint(5, 15)

    # Moves the enemy horizontally based on their speed
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
          # Removes the enemy when it passes the left edge of the screen
            self.kill()


# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HIGHT))

# Create a custom event for adding a new enemy
# custom events are stored as unique integers
# e.g. USEREVENT + 1
# call the event every .5 second
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 500)

# Instantiate the player
player = Player()

# Create groups to hold all enemy sprites
# and a group to hold all sprites
# - enemies will be used for collision detection and position updates
# - all_sprites will be used for rendering
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Setup the clock so we can create a framerate
# This should increase playability for the game
# by allowing us to pick an appropriate pace
clock = pygame.time.Clock()

# Variable to keep the main loop (game) running
running = True

# Main loop
while running:
    # for loop through the event queue
    for event in pygame.event.get():
        # Check if a key has been pressed
        if event.type == KEYDOWN:
            # If the Esc key is pressed, then exit the main loop
            if event.key == K_ESCAPE:
                running = False
        # Check for the window quit button to be pressed.
        elif event.type == QUIT:
            running = False
        # check if a new enemy needs to be added this frame
        elif event.type == ADDENEMY:
          # Create new enemy and add them to the groups
          new_enemy = Enemy()
          enemies.add(new_enemy)
          all_sprites.add(new_enemy)

    # Get the set of keys pressed and check for user input
    pressed_keys = pygame.key.get_pressed()

    # Update the player sprite based on user keypresses
    player.update(pressed_keys)

    # Update enemy position
    enemies.update()

    # Fill the screen with black (background)
    screen.fill((0,0,0))

    # Draw all current sprites on the screen
    # this loops through all current enemies and the player
    # and draws them on the screen at their current locations
    for entity in all_sprites:
      screen.blit(entity.surf, entity.rect)

    # Check if any enemies have collided with the player
    if pygame.sprite.spritecollideany(player, enemies):
      # If so, then remove the player and stop the loop
      player.kill()
      running = False

    # update the display
    pygame.display.flip()

    # Ensure program maintains a rate of 30 frames per second
    # we can do this because we set up the clock earlier
    clock.tick(30)

