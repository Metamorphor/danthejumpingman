import pygame
pygame.init()
pygame.font.init()

# Create the viewing window
screen_width = 800
screen_height = 600
score = 0
win = pygame.display.set_mode((screen_width, screen_height))
# Create a title
pygame.display.set_caption("Dan The Jumping Man")

# This is copied code that imports all of the numerous sprite images into the program
walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
bg = pygame.image.load('mario.jpg')
char = pygame.image.load('standing.png')

# Setting the framerate fps
clock = pygame.time.Clock()

class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 10
        self.isjumping = False
        self.jumpcount = 10
        self.left = False
        self.right = False
        self.walkCount = 0
        self.stand = True
        self.hitbox = (self.x + 17, self.y + 13, 30, 50) # Rectangle around player

    def draw(self, win):
        #pygame.draw.rect(win, (0, 255, 255, 255), (x, y, width, height))
        if self.walkCount + 1 > 27: # There are 9 sprites, each will display for 3 frames. Thus anything over 27 will lead to an index error from the walkLeft or walkRight lists
            self.walkCount = 0

        if not self.stand: # if hes not standing still, show his direction of movement
            if self.left:
                win.blit(walkLeft[self.walkCount//3], (self.x, self.y)) # integer division. (x, y) keeps track of our position.
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount//3], (self.x, self.y)) # Each sprite is going to display for 3 frames
                self.walkCount += 1
        else:  # if he is standing, keep him facing in his last direction
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))
        self.hitbox = (self.x + 17, self.y + 13, 30, 50)
        #pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def collides(self, collisions):
        pass

class projectile(object):
    def __init__(self, x, y, radius, colour, facing):
        self.x = x
        self.y = y    
        self.radius = radius
        self.colour = colour
        self.facing = facing # will be 1 or -1 to determine direction
        self.vel = 8 * facing


    def draw(self, win):
        pygame.draw.circle(win, self.colour, (self.x, self.y), self.radius)


class enemy(object):
    walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'), pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'), pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'), pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
    walkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'), pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'), pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'), pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = (self.x, self.end)
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x + 20, self.y + 2, 35, 55)
        self.health = 100
        self.visible = True

    def draw(self, win):
        self.move() #Everytime we draw the character we are going to move first.
        if self.visible:
            if self.walkCount + 1 >= 33:
                self.walkCount = 0

            if self.vel > 0: # Moving right
                win.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            else:
                win.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(win, (0, 255, 0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - (self.health // 10))), 10))
            self.hitbox = (self.x + 20, self.y + 2, 35, 55)
            #pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)


    def move(self):
        if self.vel > 0: # moving right
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1  # Change direction
                self.walkCount = 0        # Reset the sprite img
        else:             #moving left
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
    def hit(self):
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False




# Create a function for any drawing that need to be done (outside of the loop)

def draw_game_window():
    #win.fill((238, 122, 233, 255)) This would just fill the screen with a specified colour
    win.blit(bg, (0,0)) # Upload the background image
    text = font.render(' Your Score: ' + str(score - collisions), 1, (0,0,0))
    win.blit(text, (580, 10))
    dan.draw(win)  # Calling the new draw function
    foe.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    pygame.display.update()



# Main loop
font = pygame.font.SysFont("comicsans", 35, True, True)
dan = player(300, 455, 64, 64)
foe = enemy(100, 465, 64, 64, 550)
run = True
bullets = []
shoot_limiter = 0   # Creates a space between bullets
collisions = 0
while run:
    clock.tick(27) #fps

    if shoot_limiter > 0:
        shoot_limiter += 1
    if shoot_limiter > 5:
        shoot_limiter = 0

    for event in pygame.event.get(): # Check for an event. event = user input
        if event.type == pygame.QUIT:
            run = False

    for bullet in bullets:
        # Check if bullet is within height(y) limits of the enemy
        if bullet.y - bullet.radius < foe.hitbox[1] + foe.hitbox[3] and bullet.y + bullet.radius > foe.hitbox[1]:
            # Check if bullet is within height(y) limits of the enemy
            if bullet.x + bullet.radius > foe.hitbox[0] and bullet.x - bullet.radius < foe.hitbox[0] + foe.hitbox[2]:
                # Then bullet has hit our enemy
                score += 1
                foe.hit()
                #Remove the bullet once it collides
                bullets.pop(bullets.index(bullet))

        if bullet.x < screen_width and bullet.x > 0:
            bullet.x += bullet.vel
        else: #Bullet is off the screen so delete it
            bullets.pop(bullets.index(bullet))

    # Check if the player has come into contact with the foe
    # Are the y coordinates overlapping?
    if dan.hitbox[1] + dan.hitbox[3] >= foe.hitbox[1]:
        # Are the x coordinates overlapping
        if (dan.hitbox[0] + dan.hitbox[2] >= foe.hitbox[0] and dan.hitbox[0] < foe.hitbox[0]) or (dan.hitbox[0] + dan.hitbox[2] >= foe.hitbox[0] + foe.hitbox[2] and dan.hitbox[0] < foe.hitbox[0] + foe.hitbox[2]):
            collisions += 1
            dan.collides(collisions)

    # Set up the keys for the user input
    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and shoot_limiter == 0:
        if dan.left:
            facing = -1
        else:
            facing = 1
        if len(bullets) < 20:
            bullets.append(projectile(round(dan.x + dan.width // 2), round(dan.y + dan.height // 2), 6, (255, 215, 0), facing)) #projectile originates at the centre of the current position of dan, and facing the same direction
        shoot_limiter = 1

    if keys[pygame.K_LEFT] and dan.x > dan.vel: # Creates boundary
        dan.x -= dan.vel
        dan.left = True
        dan.right = False
        dan.stand = False
    elif keys[pygame.K_RIGHT] and dan.x < screen_width - dan.width - dan.vel:
        dan.x += dan.vel # Move if not at boundary
        dan.right = True
        dan.left = False
        dan.stand = False
    else:     # If we are standing
        dan.stand = True
        dan.walkCount = 0
    if not dan.isjumping: #We dont want the user to be able to jump again while jumping
        if keys[pygame.K_UP]: # If spacebar is pressed, activate the jump
            dan.isjumping = True
            dan.right = False
            dan.left = False
            dan.walkCount = 0
    else: # Create the jump
        if dan.jumpcount >= -10:   #initially 10
            neg = 1
            if dan.jumpcount < 0:
                neg = -1
            dan.y -= (dan.jumpcount ** 2) * 0.5 * neg  #reduce the y coordinate in increments to produce the jump
            dan.jumpcount -= 1
        else:
            dan.isjumping = False
            dan.jumpcount = 10

    draw_game_window() # Call the drawing function

pygame.quit()
