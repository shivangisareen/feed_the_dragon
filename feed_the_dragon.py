import pygame, random

pygame.init()

# set the display surface
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 500
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Feed the Dragon!")

# Set FPS and clock 
FPS = 60
clock = pygame.time.Clock() 

# Set game values 
PLAYER_STARTING_LIVES = 3
PLAYER_VELOCITY = 10
COIN_STARTING_VELOCITY = 10
COIN_ACCELERATION = 1
BUFFER_DISTANCE = 100

score = 0
player_lives = PLAYER_STARTING_LIVES
coin_velocity = COIN_STARTING_VELOCITY

# Set colours 
GREEN = (0,255,0)
DARKGREEN = (10,50,10)
WHITE = (255,255,255)
BLACK = (0,0,0)

# Set fonts
font = pygame.font.Font("./feed_the_dragon/assets/AttackGraffiti.ttf", 32)

# Set text 
score_text = font.render("SCORE: " + str(score), True, GREEN)
score_rect = score_text.get_rect()
score_rect.topleft = (20,20)

title_text = font.render("FEED THE DRAGON", True, GREEN)
title_rect = title_text.get_rect()
title_rect.centerx = WINDOW_WIDTH//2
title_rect.y = 20

lives_text = font.render("LIVES: " + str(player_lives), True, GREEN)
lives_rect = lives_text.get_rect()
lives_rect.topright = (WINDOW_WIDTH - 20,20)

game_over_text = font.render("GAME OVER!", True, GREEN)
game_over_rect = game_over_text.get_rect()
game_over_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

continue_text = font.render("Press any key to play again", True, GREEN)
continue_rect = continue_text.get_rect()
continue_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 32)


# Set sounds and music 
coin_sound = pygame.mixer.Sound("./feed_the_dragon/assets/coin_sound.wav")
miss_sound = pygame.mixer.Sound("./feed_the_dragon/assets/miss_sound.wav")
miss_sound.set_volume(.1)
pygame.mixer.music.load("./feed_the_dragon/assets/ftd_background_music.wav")



# Set images
player_image = pygame.image.load("./feed_the_dragon/assets/dragon_right.png")
player_rect = player_image.get_rect()
player_rect.x = 32
player_rect.y = WINDOW_HEIGHT//2

coin_image = pygame.image.load("./feed_the_dragon/assets/coin.png")
coin_rect = coin_image.get_rect()
coin_rect.x = WINDOW_WIDTH + BUFFER_DISTANCE
coin_rect.y = random.randint(70, WINDOW_HEIGHT - 32)


pygame.mixer.music.play(-1, 0)

# main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # check to see if the user wants to move
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player_rect.top > 70:
        player_rect.y -= PLAYER_VELOCITY
    if keys[pygame.K_DOWN] and player_rect.bottom < WINDOW_HEIGHT:
        player_rect.y += PLAYER_VELOCITY

    # move the coin
    # check to see if the x-coordinate of the coin is off the screen - player missed the coin
    if coin_rect.x < 0:
        player_lives -= 1
        miss_sound.play()
        coin_rect.x = WINDOW_WIDTH + BUFFER_DISTANCE
        coin_rect.y = random.randint(70, WINDOW_HEIGHT - 32)
    else:
        # move the coin
        coin_rect.x -= coin_velocity

    # check for collision
    if player_rect.colliderect(coin_rect):
        score += 1
        coin_sound.play()
        coin_velocity += COIN_ACCELERATION
        coin_rect.x = WINDOW_WIDTH + BUFFER_DISTANCE
        coin_rect.y = random.randint(70, WINDOW_HEIGHT - 32)
         

    # update the HUD
    score_text = font.render("SCORE: " + str(score), True, GREEN)
    lives_text = font.render("LIVES: " + str(player_lives), True, GREEN)

    # check for game over
    if player_lives == 0:
        display_surface.blit(game_over_text, game_over_rect)
        display_surface.blit(continue_text, continue_rect)
        pygame.display.update()

        # pause the game until player presses a key to continue. we will then reset the game
        pygame.mixer.music.stop()
        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    score = 0
                    player_lives = PLAYER_STARTING_LIVES
                    player_rect.y = WINDOW_HEIGHT//2 
                    coin_velocity = COIN_STARTING_VELOCITY
                    pygame.mixer.music.play(-1, 0.0)
                    is_paused = False
                # the player wants to quit
                if event.type == pygame.QUIT:
                    is_paused = False
                    running = False


    # fill the display
    display_surface.fill(BLACK)

    # blit the HUD  
    display_surface.blit(score_text, score_rect)
    display_surface.blit(title_text, title_rect)
    display_surface.blit(lives_text, lives_rect) 

    pygame.draw.line(display_surface, GREEN, (0, 70),(WINDOW_WIDTH, 70), 1)

    # blit assets
    display_surface.blit(player_image, player_rect)
    display_surface.blit(coin_image, coin_rect) 

    # update the display
    pygame.display.update()

    # tick the clock
    clock.tick(FPS)

# end the game
pygame.quit()
