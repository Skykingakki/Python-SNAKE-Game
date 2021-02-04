import pygame
import random
import os
pygame.init()
pygame.mixer.init()
bgimg = pygame.image.load(os.path.join('snake_image.jpg'))
splay = pygame.image.load(os.path.join('snake_play.png'))
gplay = pygame.image.load(os.path.join('gameplay.jpg'))


#colors
white = (255,255,255)
red = (255,0,0)
lime = (50,50,0)
blue = (0,0,255)
black = (0,0,0)
yellow = (255,255,0)


screen_width = 800
screen_height = 500

#background image
bgimg = pygame.transform.scale(bgimg,(screen_width,screen_height))
splay = pygame.transform.scale(splay,(screen_width,screen_height))
gplay = pygame.transform.scale(gplay,(screen_width,screen_height))

#game window and title
gameWindow = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("My Python Game Learning")
pygame.display.update()


clock = pygame.time.Clock()
font = pygame.font.SysFont(None,50)



#function to grow snake
def plot_snake(gameWindow, color, snake_list, snake_size):
    for x,y in snake_list:
        pygame.draw.rect(gameWindow,blue,[x,y, snake_size, snake_size])
    


#score funtion
def text_screen(text,color,x,y):
    screen_text = font.render(text,True, color)
    gameWindow.blit(screen_text,[x,y])
    
# snake game home welcome page
def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.fill(black)
        gameWindow.blit(splay,(0,0))
        text_screen("Welcome to SNAKE GAME",white,200,150)
        text_screen("Press SPACEBAR to Play",white,210,200)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.load('welcome.mp3')
                    pygame.mixer.music.play()
                    gameloop()

        pygame.display.update()
        clock.tick(60)
        


# movement and food
def gameloop():
    
    #game variables
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    velocity_x = 0
    velocity_y = 0

    food_x = random.randint(20, screen_width-50)
    food_y = random.randint(20, screen_height-50)
    init_velocity = 4
    score = 0
    fps = 60
    snake_size = 10

    snake_list = []
    snake_length = 1

    if(not os.path.exists("hiscore.txt")):
        with open("hiscore.txt","w") as f:
            f.write("0")

    with open("hiscore.txt","r") as f:
        hiscore = f.read()


    while not exit_game:
        if game_over:
            with open("hiscore.txt","w") as w:
                w.write(str(hiscore))
            gameWindow.fill(black)
            gameWindow.blit(bgimg,(0,0))
            text_screen("Game Over !!",red,280,50)
            text_screen("Your Score: " + str(score),red,280,80)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        welcome()

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:  
                        velocity_x = init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_LEFT:
                        velocity_x = - init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_UP:
                        velocity_y = - init_velocity
                        velocity_x = 0
                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0
                    if event.key == pygame.K_SPACE:
                        velocity_x = 0
                        velocity_y = 0
            
            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y

            if abs(snake_x - food_x)<8 and abs(snake_y - food_y)<8:
                score = score + 10
                food_x = random.randint(20, screen_width-50)
                food_y = random.randint(20, screen_height-50)
                snake_length = snake_length + 3
                if score>int(hiscore):
                    hiscore = score

            gameWindow.fill(lime)
            gameWindow.blit(gplay,(0,0))
            text_screen("Score: "+ str(score) + " HighScore: "+str(hiscore),yellow, 5,5)
            pygame.draw.rect(gameWindow, red, [food_x,food_y, snake_size, snake_size])
            
            head = []
            head.append(snake_x)
            head.append(snake_y)
            snake_list.append(head)

            if len(snake_list) > snake_length:
                del snake_list[0]

            if snake_x < 0 or snake_x > screen_width or snake_y<0 or snake_y>screen_height:
                pygame.mixer.music.load('end.mp3')
                pygame.mixer.music.play()
                game_over = True

            if head in snake_list[:-1]:
                game_over = True
                pygame.mixer.music.load('end.mp3')
                pygame.mixer.music.play()
            
            
            # pygame.draw.rect(gameWindow, blue, [snake_x,snake_y, snake_size, snake_size])
            plot_snake(gameWindow, blue, snake_list, snake_size)
        pygame.display.update()
        clock.tick(fps)
    pygame.quit()
    quit()

welcome()
