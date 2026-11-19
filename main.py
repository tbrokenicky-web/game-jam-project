import pygame
import time
import math

WIDTH = 1280
HIGHT = 720

TILE = 40 

COL = WIDTH // TILE
ROW = HIGHT // TILE
print(COL, ROW)
# 32X18

walls = []

level = [
    "################################",
    "#..............................#",
    "#..............................#",
    "#................##............#",
    "#..............................#",
    "#..............................#",
    "#..............................#",
    "#..............................#",
    "#.######.......................#",
    "#......#.......................#",
    "#......#.......................#",
    "#......#.......................#",
    "#......#####...................#",
    "#..........#...................#",
    "#..............................#",
    "#..............................#",
    "#..............................#",
    "################################",
]



screen = pygame.display.set_mode((WIDTH, HIGHT))
pygame.display.set_caption("code app")
# this check the row in the level
for row_number, row in enumerate(level):
    # this checks if a character in that level is something
    for col_number, char in enumerate(row):
        if char == "#":
            wall = pygame.Rect(col_number * TILE, row_number * TILE, TILE, TILE) # takes cordinets and give them form
            walls.append(wall)

# makes a variable of the key you press kinda

class Player_model():
    def __init__(self, x, y):
        self.hitbox =  pygame.Rect(x, y, 24, 24)
        self.speed = 4
        self.health = 100
    

# creats a player and sets starign postion
player = Player_model(80, 80)
class Weapon():
    def __init__(self, damage, reach, cooldown, x, y):
        self.damage = damage
        self.reach = reach
        self.cooldown = cooldown
        self.timer = 0 # 0 mean ready to attack
        self.weapon_body = pygame.Rect(x, y, 10, 50)
        # sets the radius from the player to 30
        self.radius = 30
        # capital normaly mena class
        # the staring postion every time you open the game
        self.original = pygame.Surface((10, 50), pygame.SRCALPHA ) # adds a 4the valuse so that 0 = transparent
        # fills that specific space
        self.original.fill((0, 0, 0))

        self.image = self.original
        # need both image and rect bc Surface dosent have cordinest
        self.rect = self.image.get_rect()
    def follow(self, player):
        
        mouse_x, mouse_y = pygame.mouse.get_pos()
        center_x, center_y = player.hitbox.center
                            # goes y and then x very specific
        angle = math.atan2(mouse_y - center_y, mouse_x - center_x)
        # get the center of the players hitbox the take that 
        x = center_x + math.cos(angle) * self.radius
        y = center_y + math.sin(angle) * self.radius
                                                            # convers angle from radians to an angle
        self.image = pygame.transform.rotate(self.original, -math.degrees(angle) ) # negitive becasue pygame y is fliped
        self.rect = self.image.get_rect(center= (x, y))
        
    def update(self):
        if self.timer > 0:
            self.timer -= 1

    def attack(self):
        if self.timer > 0: # if the timer is less than 0 do nothing
            return
        self.timer = self.cooldown
    
weapon1 = Weapon(10, 30, 10, (player.hitbox.x) + 40, (player.hitbox.y - 10))     
       
def move(player, distance_x, distance_y):
    """
    this is what makes collision
    first the hit box is set  plus equal to watever distane_x is 
    then it look though the walls list for the wlal cords
    then checks for collision between the palyer hit box and any wall in the list
    then it checks where you hit the wall
    then depending on where you hit the wall it sets your positon to that walls edge
    this is so you cannot pass right though the wall
    """
    # gets player postion and then add the disance it has moved each time it moves 
    player.hitbox.x += distance_x
    for wall in walls:
        if player.hitbox.colliderect(wall):
            # this just cheks which wall you hit if its greater it was the right side of the player and the lef tside of the wall
            if distance_x > 0:
                # sets the players right edge to the walls left edge so you cant go through it
                player.hitbox.right = wall.left
            
            if distance_x < 0:
                player.hitbox.left = wall.right
    
    player.hitbox.y += distance_y
    for wall in walls:
        if player.hitbox.colliderect(wall):
            if distance_y > 0:
                player.hitbox.bottom = wall.top

            if distance_y < 0:
                player.hitbox.top = wall.bottom

clock = pygame.time.Clock()

clicked = False

running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                clicked = True
    
    # this is the player movent and 
    keys = pygame.key.get_pressed()
    # jsut tell me how much my player is moving
    distance_x = 0
    distance_y = 0
    if keys[pygame.K_a]:
        distance_x = -player.speed
    if keys[pygame.K_d]:
        distance_x = player.speed

    if keys[pygame.K_w]:
        distance_y = -player.speed

    if keys[pygame.K_s]:
        distance_y = player.speed

    # gets called every frame to check if youve moved and then update position
    move(player, distance_x, distance_y)
    weapon1.follow(player)
    screen.fill((211, 211, 211))
    for wall in walls:
         # where to dispaly, what color, where and how big
        # rect means draw a retangle
        pygame.draw.rect(screen, (255, 255, 255), wall) 
    # uses pixels and cant be rotated
    pygame.draw.rect(screen, (240, 200, 60), player.hitbox)
    screen.blit(weapon1.image, weapon1.rect)
    
    pygame.display.flip()
    
    clock.tick(60)

    





