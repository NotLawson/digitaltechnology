import pygame # Game engine
from pygame.math import Vector2

import os, sys                        #
from os import listdir                #  Import system libraries
from sys import exit                  #
from os.path import isfile, join      #

import json # JSON interpretation

import maps.tilemaps as tilemap # Import tile map loader

import subprocess  # unused, was to start multiplayer server
import socket # unused, was to connect to multiplayer server

username = None  # unused, was for multiplayer
password = None  # unused, was for multiplayer
map = None  # used to load map


# development purposes only
try:
    if sys.argv[1] == "py":
        print("running in py mode")
        exe = False
    else:
        exe = True
except:
    exe = True
### FUNCTIONS ###

# Quit the game
def quit():
    pygame.quit()
    print("Exiting...")
    exit()

# display tilemap
def create_tilemap(window):
    global solids
    global scaffold
    global air
    global Tile

    window.fill((0, 0, 0))
    currentmap = load_map(map)
    x = y = 0
    for row in currentmap.map:
        for col in row:
            tile_texture = currentmap.textures[col]
            t = Tile(x, y, tile_texture)
            tiles.add(t)
            if currentmap.tile_types[col] == tilemap.TileTypes.solid:
                solids.add(t)
            elif currentmap.tile_types[col] == tilemap.TileTypes.air:
                air.add(t)
            elif currentmap.tile_types[col] == tilemap.TileTypes.scaffold:
                scaffold.add(t)
            x += currentmap.tilesize
        y += currentmap.tilesize
        x = 0

    return currentmap.width, currentmap.height, currentmap.bg_colour
    
# display the window
def draw(window, all_sprites, tiles, cam, bg_colour):
    window.fill(bg_colour)
    for e in tiles:
        e.draw(window, cam)
    for e in all_sprites:
        e.draw(window, cam)                                           # Draw the entity
    pygame.display.update()                                      # Update Display

# camera function
def simple_camera(camera, target_rect):
    l, t, _, _ = target_rect # l = left,  t = top
    _, _, w, h = camera      # w = width, h = height
    return pygame.Rect(-l+(WIDTH/2), -t+(HEIGHT/2), w, h)

# import the tilemap
def load_map(map):
    map = tilemap.Map(map)
    return map

# file loader
def load(relative_path):
    try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# handle username, password and map from data.json
def handle_data():
    global username
    global password
    global map
    data = json.load(open(load("data.json")))
    try:
        username = data["username"]
    except KeyError:
        data["username"] = "please put username here"
    
    try:
        password = data["password"]
    except KeyError:
        data["password"] = "please put password here"

    try:
        map = data["map"]
    except KeyError:
        data["map"] = "default"
        map = "default"

# unused, ran out of time to do animations
def get_character_image():
    class player_image:
        left = pygame.image.load(load("player/left.png"))
        right = pygame.image.load(load("player/right.png"))
        fall = pygame.image.load(load("player/fall.png"))
        jump = {
            1 : pygame.image.load(load("player/jump_1.png")),
            2 : pygame.image.load(load("player/jump_2.png")),
            3 : pygame.image.load(load("player/jump_3.png")),
            4 : pygame.image.load(load("player/jump_4.png")),
            5 : pygame.image.load(load("player/jump_5.png")),
            6 : pygame.image.load(load("player/jump_6.png"))
        }
        run_left = {
            1 : pygame.image.load(load("player/left_1.png")),
            2 : pygame.image.load(load("player/left_2.png")),
            3 : pygame.image.load(load("player/left_3.png")),
            4 : pygame.image.load(load("player/left_4.png")),
            5 : pygame.image.load(load("player/left_5.png")),
            6 : pygame.image.load(load("player/left_6.png"))
        }
        run_right = {
            1 : pygame.image.load(load("player/right_1.png")),
            2 : pygame.image.load(load("player/right_2.png")),
            3 : pygame.image.load(load("player/right_3.png")),
            4 : pygame.image.load(load("player/right_4.png")),
            5 : pygame.image.load(load("player/right_5.png")),
            6 : pygame.image.load(load("player/right_6.png"))
        }
        '''pickup = {
            1 : pygame.image.load(load("player/pickup_1.png")),
            2 : pygame.image.load(load("player/pickup_2.png")),
            3 : pygame.image.load(load("player/pickup_3.png")),
            4 : pygame.image.load(load("player/pickup_4.png")),
            5 : pygame.image.load(load("player/pickup_5.png")),
            6 : pygame.image.load(load("player/pickup_6.png"))
        }'''
        '''tag_win = {
            1 : pygame.image.load(load("player/tagwin_1.png")),
            2 : pygame.image.load(load("player/tagwin_2.png")),
            3 : pygame.image.load(load("player/tagwin_3.png")),
            4 : pygame.image.load(load("player/tagwin_4.png")),
            5 : pygame.image.load(load("player/tagwin_5.png")),
            6 : pygame.image.load(load("player/tagwin_6.png"))
        }'''
        '''tag_loss = {
            1 : pygame.image.load(load("player/tagloss_1.png")),
            2 : pygame.image.load(load("player/tagloss_2.png")),
            3 : pygame.image.load(load("player/tagloss_3.png")),
            4 : pygame.image.load(load("player/tagloss_4.png")),
            5 : pygame.image.load(load("player/tagloss_5.png")),
            6 : pygame.image.load(load("player/tagloss_6.png"))
        }'''
    return player_image

# unused, was to get multiplayer skins
def get_player_image(username):
    pass

### PYGAME INIT ###
pygame.init()  # To start pygame
pygame.display.set_caption("Tag Game")   # Set the title of the window
window = pygame.display.set_mode((700,500), pygame.RESIZABLE)  # Set window
### VARIABLES ###
WIDTH, HEIGHT = 700, 500  # Window Width and Height
FPS = 60     # Frames Per Second limit


### SPRITE SETUP ###

# player class
class Player(pygame.sprite.Sprite):
    COLOUR = (255, 0, 0)
    GRAVITY = 1

    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)        # Create a rect with the details
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)      # Create a surface with the details
        self.x_vel = 0   # Defining X velocity
        self.y_vel = 0   # Defining Y velocity
        self.onground = True  # Is the player on the ground?
        self.width = width   # width of the player image
        self.height = height # height of the player image
        self.jump_strength = 20  # how high the player jumps
        self.direction = "left"   # Direction of the player
        self.animation_count = 0  # unused, ran out of time for animations
        self.state = "idle" # unused, ran out of time for animations
    
    def draw(self, win, _):
        self.image.fill((0,0,0,0)) # clear animations
        if self.direction == "left":
            self.image.blit(pygame.image.load(load("player/left_4.png")), (0,0))  # load left image
        elif self.direction == "right":
            self.image.blit(pygame.image.load(load("player/right_4.png")), (0,0)) # load right image
        else:
            self.image.blit(pygame.image.load(load("player/left_4.png")), (0,0)) # if broken, load left
            self.direction = "left"
        win.blit(self.image, ((WIDTH/2), (HEIGHT/2)))  # display player in the middle of the screen

    def update(self, solids, scaffold, enemies):
        dx = 0  # delta x, or how far the player will move in an x direction
        dy = 0  # delta y, or how far the player will move in a y direction
        # HANDLE KEYS #
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]: # A key pressed
            dx = -7   # move the player 7 pixels to the left
            self.direction = "left"
        if keys[pygame.K_d]: # D key pressed
            dx = 7    # move the player 7 pixels to the right
            self.direction = "right"
        if keys[pygame.K_SPACE] and self.onground: # space key pressed and on the ground
            self.y_vel = -20  # move 20 pixels upwards
            self.onground = False  # not on the ground
        
        # GRAVITY #
        self.y_vel += 1           # Gravity mechanics
        if self.y_vel > 20:       # ^^^
            self.y_vel = 20       # ^^^
        dy += self.y_vel          # ^^^

        # COLLISIONS #
        if pygame.sprite.spritecollideany(self, enemies): # if the player touches the enemies
            return True # return game over

        for t in solids:  # for every tile in the tile map that is a solid
            # X COLLIONS #
            if t.rect.colliderect(pygame.Rect(self.rect.x + dx, self.rect.y, self.width, self.height)):   # make a new rect where the player would go to check if it would collide
                dx = 0   # if it does, don't move player


            # Y COLLISIONS #
            if t.rect.colliderect(pygame.Rect(self.rect.x, self.rect.y + dy, self.width, self.height)):   # same as x, but on the y axis
                # check if below ground
                if self.y_vel < 0:
                    dy = t.rect.bottom - self.rect.top  # define how far the player can go before it touches the ceiling
                    self.y_vel = 0  # set the y velocity to 0
                # check if above ground
                elif self.y_vel > 0:
                    dy = t.rect.top - self.rect.bottom  # same, but before it touches the ground
                    self.y_vel = 0
                    self.onground = True  # on the ground
        
        # MOVE THE PLAYER #
        self.rect.move_ip((dx, dy))  # apply the delta x and delta y
        self.x_vel = dx # set x veloctity

        return False # game not over
    
# generic object definition
class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, name = None):
        super().__init__()
        self.rect = pygame.Rect(x, y, w, h)  # creat a rect with data
        self.image = pygame.Surface((w, h), pygame.SRCALPHA) # create a surface
        self.image.fill((255, 0, 0))  # fill the surface (for now)
        self.width = w # set width
        self.height = h # set height
        self.name = name # set name (if one)

    def draw(self, window, cam):
        window.blit(self.image, cam.apply(self))  # draw the object

# tile class
class Tile(Object):
    def __init__(self, x, y, image):
        super().__init__(x, y, 32, 32) # do what Object.__init__() does and pass on information
        self.image.blit(image, (0,0)) # draw the tile texture onto the tile

# enemy class
class Enemy(Object):
    def __init__(self, x, y, speed):
        super().__init__(x, y, 32, 32) # do what Object.__init__() does and pass on data
        self.speed = speed   # set the speed

    def update(self, player):

        target_vector = Vector2(player.rect.x, player.rect.y)  # player vect
        follower_vector = Vector2(self.rect.x, self.rect.y)    # enemy vect

        ## BIG BRAIN MATHS STUFF THATS HARD TO EXPLAIN ##

        distance = follower_vector.distance_to(target_vector)

        minimum_distance = -100
        maximum_distance = 10000
        min_step = max(0, distance - maximum_distance)
        max_step = distance - minimum_distance
        VELOCITY = self.speed
    
        direction_vector = target_vector - follower_vector
        distance = follower_vector.distance_to(target_vector)
        if distance > minimum_distance:
            direction_vector    = (target_vector - follower_vector) / distance
            min_step            = max(0, distance - maximum_distance)
            max_step            = distance - minimum_distance
            step_distance       = min(max_step, max(min_step, VELOCITY))
            #step_distance       = min_step + (max_step - min_step) * LERP_FACTOR

        dx = (direction_vector * step_distance).x  # set delta x
        dy = (direction_vector * step_distance).y  # set delta y

        

        for t in solids:
            # X COLLIONS #
            if t.rect.colliderect(pygame.Rect(self.rect.x + dx, self.rect.y, self.width, self.height)): # create a temporary new rect to see if the enemy collides with a platform
                dx = 0 # if it does, set delta x to 0 (don't move)
            # Y COLLISIONS #
            if t.rect.colliderect(pygame.Rect(self.rect.x, self.rect.y + dy, self.width, self.height)): # same thing with y axis
                dy = 0
        
        self.rect.move_ip(dx, dy)  # apply delta x and delta y

# camera class
class Camera:
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func  # set the camera function (simple camera)
        self.state = pygame.Rect(0, 0, width, height)  # set the position of the camera
        
    def apply(self, target):
        return target.rect.move(self.state.topleft) # move the target to where it is supposed to be
        
    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)  # set the focus for the camera (player)

## GROUPS ##
all_sprites = pygame.sprite.Group()   # all the sprites
players = pygame.sprite.Group() # just player, not really used, was for multiplayer
tiles = pygame.sprite.Group()  # all the tiles

solids = pygame.sprite.Group()  # solid tile types
air = pygame.sprite.Group()  # air tile types
scaffold = pygame.sprite.Group()  # scaffold tile types

### MAIN ###
def menu(window):  # menu window
    global WIDTH  # import the width
    global HEIGHT # import the height
    global scaffold

    screen = "mainmenu" # set the screen
    while 1: # menu loop
        window.fill((255,255,255,0))  # fill the screen with white

        # MOUSE #
        surf = pygame.Surface((10,10))    # set the cursor
        surf.fill((0, 0, 0))
        pos = pygame.mouse.get_pos()
        rect_pos = (pos[0]-5, pos[1]-5)
        window.blit(surf, rect_pos)
        pygame.mouse.set_visible(False)

        if screen == "mainmenu": # main menu
            # TITLE #
            text = pygame.font.SysFont("arialblack", 40).render("Tag!", True, (0,0,0))  # display the title
            text_rect = text.get_rect(center=(WIDTH/2, HEIGHT-(HEIGHT/4)*3))
            coords = (text_rect.x, text_rect.y)
            window.blit(text, coords)

            pos = pygame.mouse.get_pos()  # set the mouse position
            # JOIN BUTTON #
            def join_button(window, pos, screen, click = False): # code for the join button
                text = pygame.font.SysFont("arialblack", 30).render("Join (broken)", True, (0,0,0))
                button_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2 + 70))

                coords = (button_rect.x, button_rect.y)
                
                button_rect = pygame.Rect(button_rect.x-5,button_rect.y,button_rect.width+10, button_rect.height)
                
                if button_rect.collidepoint(pos): # if mouse is hovering over
                    text = pygame.font.SysFont("arialblack", 30).render("Join (broken)", True, (255,255,255))  # set the text to white and the box to black
                    pygame.draw.rect(window, (0,0,0), button_rect)  # draw the button
                else: # otherwise
                    text = pygame.font.SysFont("arialblack", 30).render("Join (broken)", True, (0,0,0)) # set the text to black and the box to white
                    pygame.draw.rect(window, (0,0,0), button_rect, 2)
                window.blit(text, coords) # draw the text for the button

                if click and button_rect.collidepoint(pos):  # if clicked on
                    screen = "join"  # open the join screen
                
                return screen  # return the screen variable


            def host_button(window, pos, screen, click=False): # code for the host button (the same as the join button, which has documentation)
                text = pygame.font.SysFont("arialblack", 30).render("Host (broken)", True, (0,0,0))
                button_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))

                coords = (button_rect.x, button_rect.y)
                
                button_rect = pygame.Rect(button_rect.x-5,button_rect.y,button_rect.width+10, button_rect.height)
                
                if button_rect.collidepoint(pos):
                    text = pygame.font.SysFont("arialblack", 30).render("Host (broken)", True, (255,255,255))
                    pygame.draw.rect(window, (0,0,0), button_rect)
                else:
                    text = pygame.font.SysFont("arialblack", 30).render("Host (broken)", True, (0,0,0))
                    pygame.draw.rect(window, (0,0,0), button_rect, 2)
                window.blit(text, coords)
                if click and button_rect.collidepoint(pos): screen = "host"
                return screen
            
            def freeplay_button(window, pos, screen, click=False): # code for the freeplay button (same as the host and join buttons, see the join button for documentation)
                text = pygame.font.SysFont("arialblack", 30).render("Freeplay", True, (0,0,0))
                button_rect = text.get_rect(center=(WIDTH/2, HEIGHT-120))

                coords = (button_rect.x, button_rect.y)
                
                button_rect = pygame.Rect(button_rect.x-5,button_rect.y,button_rect.width+10, button_rect.height)
                
                if button_rect.collidepoint(pos):
                    text = pygame.font.SysFont("arialblack", 30).render("Freeplay", True, (255,255,255))
                    pygame.draw.rect(window, (0,0,0), button_rect)
                else:
                    text = pygame.font.SysFont("arialblack", 30).render("Freeplay", True, (0,0,0))
                    pygame.draw.rect(window, (0,0,0), button_rect, 2)
                window.blit(text, coords)
                if click and button_rect.collidepoint(pos): screen = "freeplay"
                return screen
            
            # Call all of the buttons
            join_button(window, pos, screen)
            host_button(window, pos, screen)
            freeplay_button(window, pos, screen)

            # events =D
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:  # If the "X" button is pressed
                        quit()

                    if event.type == pygame.VIDEORESIZE:  # if you resize the window
                        WIDTH = event.w  #  set the width
                        HEIGHT = event.h #  set the height

                    if event.type == pygame.KEYDOWN:   # If a key is pressed

                        if event.key == pygame.K_ESCAPE:   # If the key was escape
                            quit()
                        
                    if event.type == pygame.MOUSEBUTTONDOWN: # if the mouse button was clicked
                        # check the buttons to see if it was clicked on
                        screen = join_button(window, event.pos, screen, click = True)
                        screen = host_button(window, event.pos, screen, click = True)
                        screen = freeplay_button(window, event.pos, screen, click = True)
                        
        elif screen == "join":  # join screen wasn't finished, so there is no documentation available

            # !
            # !
            # !   UNFINISHED CODE, NO DOCUMENTATION !!!
            # !
            # !

            for event in pygame.event.get():
                    if event.type == pygame.QUIT:                        # If the "X" button is pressed
                        quit()
                    if event.type == pygame.VIDEORESIZE:
                        WIDTH = event.w
                        HEIGHT = event.h
                    if event.type == pygame.KEYDOWN:                     # If a button is pressed
                        if event.key == pygame.K_ESCAPE:                 # If the button was escape
                            quit()
            host = False
            break
        
        elif screen == "host":
            host = True
            break

        elif screen == "freeplay":
            skip = True
            host = False
            break

        pygame.display.update()

    return host, "127.0.0.0", skip # whether to host, the address, and whether to skip the joining theatrics

# main game
def main(window, host, address, skip):
    global WIDTH   # import width
    global HEIGHT  # import height

    if skip == False: # if not free play

            # !
            # !
            # !   UNFINISHED CODE/UNUSED CODE, HOWEVER SOME DOCUMENTATION !!!
            # !
            # !

        if host: # if hosting
            serverprocess = subprocess.Popen("server.exe") # open the server file
            address = "localhost"  # use the address localhost
            pygame.time.delay(100)   # wait 100ms
        try:
            server = socket.socket()  # try to connect to the server
            print("attemping to connect...")
            server.connect((address, 8080))
        except socket.error as err:  # if cant connect
            print("Cant connect! Reason: ", err) # report
            if host:
                serverprocess.kill()  # kill the server
            quit()
        
        server.setblocking(False) # allows code to run afterwards if no repsonse
        while 1: # wating in lobby
            try: # try to read data from server
                data = ""
                print("try read")
                data = server.recv(1024).decode()
                print(data)
            except: # if no data
                print("fail")
                data = "none"
            if data == "match.begin": # if begin match
                break # exit waiting lobby

            # no documentation needed
            window.fill((255,255,255))
            text = pygame.font.SysFont("arialblack", 40).render("Waiting for other player...", True, (0,0,0))
            text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
            coords = (text_rect.x, text_rect.y)
            window.blit(text, coords)
            pygame.display.update()
            print("loop finish")

    # The actual game !!!

    clock = pygame.time.Clock()     # Set the clock
    player = Player(100, 100, 64, 64)  # Define Player
    enemy1 = Enemy(200, 850, 4) # set the enemys
    enemy2 = Enemy(200, 500, 5) # 
    enemy3 = Enemy(200, 700, 6) #

    levelwidth, levelheight, bg_colour = create_tilemap(window) # create tilemap and extract vars

    cam = Camera(simple_camera, levelwidth, levelheight)  # start camera

    all_sprites.add(player)  # Adds player to all_sprites

    all_sprites.add(enemy1)  # Adds enemy to all_sprites
    all_sprites.add(enemy2)  # ^^^
    all_sprites.add(enemy3)  # ^^^

    enemies = pygame.sprite.Group() # enemy group
    enemies.add(enemy1) # Add enemies
    enemies.add(enemy2) # ^^^
    enemies.add(enemy3) # ^^^

    players.add(player)  # Adds player to all_players
    
    
    run = True  # If the game is running
    while run:
        clock.tick(FPS)   # Tick 60 times per second

        ## EVENTS ##
        #
        # Pretty much the same as the last one, but with a few changes:
        # - no mouse click detection (not needed)
        # - recreates tilemap on resize
        #
        for event in pygame.event.get():
            if event.type == pygame.QUIT:                        # If the "X" button is pressed
                serverprocess.kill()
                quit()
            if event.type == pygame.VIDEORESIZE:
                WIDTH = event.w
                HEIGHT = event.h
                create_tilemap(window)
            if event.type == pygame.KEYDOWN:                     # If a button is pressed
                if event.key == pygame.K_ESCAPE:                 # If the button was escape
                    if host:
                        serverprocess.kill()
                    quit()
        
        ## UPDATE ##
        cam.update(player)  # update the camera
        gameover = player.update(solids, scaffold, enemies)  # update the player and check if gameover
        for e in enemies:  # run through enemies
            e.update(player) # update enemies
        if gameover: # if game over escape loop
            break
        
        draw(window, all_sprites, tiles, cam, bg_colour) # Draw the game
    
    r = False # is r pressed?
    while r == False:
            
            # game over text
            text = pygame.font.SysFont("arialblack", 60).render("Game over", True, (0,0,0))
            text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
            coords = (text_rect.x, text_rect.y)
            window.blit(text, coords)

            # press r to restart
            text = pygame.font.SysFont("arialblack", 20).render("Press R to restart", True, (0,0,0))
            text_rect = text.get_rect(center=(WIDTH/2, (HEIGHT/2)+35))
            coords = (text_rect.x, text_rect.y)
            window.blit(text, coords)

            #
            # Again the same as the last one, with a few changes:
            # - will still recreate tile map on resize
            # - now detects "r" press
            #
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:                        # If the "X" button is pressed
                        quit()
                    if event.type == pygame.VIDEORESIZE:
                        WIDTH = event.w
                        HEIGHT = event.h
                        create_tilemap(window)
                    if event.type == pygame.KEYDOWN:                     # If a button is pressed
                        if event.key == pygame.K_ESCAPE:                 # If the button was escape
                            quit()
                        if event.key == pygame.K_r:
                            r = True
            pygame.display.update()


# clear the window
def clear(window, tiles, all_sprites):
    window.fill((255, 255, 255))
    for e in all_sprites:
        e.kill()
    for t in tiles:
        t.kill()


handle_data()  # handle data
hosting, address, skip = menu(window)  # call menu
while 1: # keep the game running
    main(window, hosting, address, skip)  # run game
    clear(window, tiles, all_sprites)  # clear window
