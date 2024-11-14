import pygame
import random
from sys import exit

pygame.init()
GAME_WIDTH = 600
GAME_HEIGHT = 600
GRID_SQUARE_SIZE = 30
FRAMES_PER_SECOND = 10

class Snake():

    def __init__(self, column, row, apple):
        self.x = column * GRID_SQUARE_SIZE
        self.y = row * GRID_SQUARE_SIZE
        self.apple = apple
        
        self.key_check = False
        self.movement = (1, 0)
        self.score = 0
        self.can_move = True
        self.snake_position = [3 * GRID_SQUARE_SIZE, 9 * GRID_SQUARE_SIZE]
        self.snake_blocks = [[3 * GRID_SQUARE_SIZE, 9 * GRID_SQUARE_SIZE], [2 * GRID_SQUARE_SIZE, 9 * GRID_SQUARE_SIZE], [1 * GRID_SQUARE_SIZE, 9 * GRID_SQUARE_SIZE]]
        self.game_active = False
    
    def snake_head_coordinates(self):
        return self.snake_blocks[0]

    def update(self):
        
        self.snake_position[0] += int(self.movement[0] * GRID_SQUARE_SIZE)
        self.snake_position[1] += int(self.movement[1] * GRID_SQUARE_SIZE)
        self.snake_blocks.insert(0, list(self.snake_position))

    def render(self):
        
        for block in self.snake_blocks:
            pygame.draw.rect(screen, (0, 255, 0), (block[0], block[1], GRID_SQUARE_SIZE, GRID_SQUARE_SIZE))
        
        #pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y, GRID_SQUARE_SIZE, GRID_SQUARE_SIZE))
    
    def head_rect(self):
        
        return pygame.Rect(self.snake_blocks[0][0], self.snake_blocks[0][1], GRID_SQUARE_SIZE, GRID_SQUARE_SIZE)
        
        #return pygame.Rect(self.x, self.y, GRID_SQUARE_SIZE, GRID_SQUARE_SIZE)

    def screen_boundary(self):
        
        if self.snake_blocks[0][0] < 0 or self.snake_blocks[0][0] >= GAME_WIDTH:
            self.movement = (0, 0)
            self.can_move = False
            self.game_active = False
        if self.snake_blocks[0][1] < 40 or self.snake_blocks[0][1] >= GAME_HEIGHT:
            self.movement = (0, 0)
            self.can_move = False
            self.game_active = False
        
    def snake_body_collision(self):
        for block in self.snake_blocks[1:]:
            if self.snake_position[0] == block[0] and self.snake_position[1] == block[1]:
                self.movement = (0, 0)
                self.can_move = False
                self.snake_blocks.pop()
                self.game_active = False
        
    def check_collision(self):
        collide = pygame.Rect.colliderect(self.head_rect(), self.apple.rect_and_render(self.score))
        if collide:
            #self.snake_blocks.append([self.snake_blocks[-1][0] - self.previous_direction[0] * GRID_SQUARE_SIZE, self.snake_blocks[-1][1] - self.previous_direction[1] * GRID_SQUARE_SIZE])
            self.score += 1
            self.apple.collide_time = True
        else:
            self.snake_blocks.pop()

class Apple:
    def __init__(self, screen, color, radius):
        self.screen = screen
        self.color = color
        self.radius = radius
        self.x_row_pos = int(GRID_SQUARE_SIZE * 31 / 2)
        self.y_column_pos = int(GRID_SQUARE_SIZE * 19 / 2)
        self.collide_time = False
    
    def rand_x_row_pos(self):
        # 2n - 1 (n from 1 to 20)
        row_location = int(2 * random.randint(1, 20) - 1)
        return int(GRID_SQUARE_SIZE * row_location / 2)
    
    def rand_y_column_pos(self):
        # 2n - 1 (n from 3 to 20)
        column_location = int(2 * random.randint(3, 20) - 1)
        return int(GRID_SQUARE_SIZE * column_location / 2)
    
    def rect_and_render(self, snake_score):
        if snake_score == 0:
            return pygame.draw.circle(self.screen, self.color, [self.x_row_pos, self.y_column_pos], self.radius)
        #if collide_time == True:
        if self.collide_time == True:
            self.x_row_pos = self.rand_x_row_pos()
            self.y_column_pos = self.rand_y_column_pos()
        self.collide_time = False
        return pygame.draw.circle(self.screen, self.color, [self.x_row_pos, self.y_column_pos], self.radius)

def square_grid(no_of_squares):
    for column_2 in range(2, no_of_squares):
        for row_2 in range(no_of_squares):
            grid_square = pygame.Rect((int(GRID_SQUARE_SIZE * row_2), int(GRID_SQUARE_SIZE * column_2)), (GRID_SQUARE_SIZE, GRID_SQUARE_SIZE))
            pygame.draw.rect(screen, (0, 0, 255), grid_square, 1)

screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption('Snake Game')
apple = Apple(screen, (255, 0, 0), int(GRID_SQUARE_SIZE / 2))
snake = Snake(3, 9, apple)

clock = pygame.time.Clock()

no_of_squares = int(GAME_WIDTH / GRID_SQUARE_SIZE)

test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
title_font = pygame.font.Font('font/Pixeltype.ttf', 75)

game_name = test_font.render('Score: ' + str(0),False,(255,255,255))
game_name_rect = game_name.get_rect(center = (int(GAME_WIDTH/2),30))

title_name = title_font.render('  Snake Game', False, (255, 255, 255))
title_rect = title_name.get_rect(center = (int(GAME_WIDTH/2), 50))

snake_image = pygame.image.load('images/green_snake.jpg').convert_alpha()
snake_image_rect = snake_image.get_rect(center = (400, 260))

green_snake_icon = pygame.image.load('images/green_snake_icon.png').convert_alpha()
pygame.display.set_icon(green_snake_icon)

press_c_to_play = title_font.render('  Press c to play', False, (255, 255, 255))
press_c_to_play_rect = press_c_to_play.get_rect(center = (int(GAME_WIDTH/2), 300))

press_q_to_quit = title_font.render('  Press q to quit', False, (255, 255, 255))
press_q_to_quit_rect = press_q_to_quit.get_rect(center = (int(GAME_WIDTH/2), 420))

grid_square = pygame.Rect((0, 0), (GRID_SQUARE_SIZE, GRID_SQUARE_SIZE))

rand_location = random.randint(2, no_of_squares)
times_played = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if snake.game_active == True:
            if event.type == pygame.KEYDOWN:
                snake.key_check = True
                if snake.can_move == True:
                    if event.key == pygame.K_LEFT and snake.movement != (1, 0):
                        snake.movement = (-1, 0)
                    if event.key == pygame.K_RIGHT and snake.movement != (-1, 0):
                        snake.movement = (1, 0)
                    if event.key == pygame.K_UP and snake.movement != (0, 1): 
                        snake.movement = (0, -1)  
                    if event.key == pygame.K_DOWN and snake.movement != (0, -1): 
                        snake.movement = (0, 1)
                    
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    apple = Apple(screen, (255, 0, 0), int(GRID_SQUARE_SIZE / 2))
                    snake = Snake(3, 9, apple)
                    snake.game_active = True
                    times_played += 1
                if event.key == pygame.K_q:
                    pygame.quit()
                    exit()
                
    screen.fill((0, 0, 0))
    if snake.game_active == True:
        game_name = test_font.render('  Score: ' + str(snake.score), False, (255,255,255))
        game_name_rect = game_name.get_rect(center = (int(GAME_WIDTH/2),30))
        #apple_rect = pygame.draw.circle(screen, (255, 0, 0), [int(GRID_SQUARE_SIZE * 31 / 2), int(GRID_SQUARE_SIZE * 19 / 2)], int(GRID_SQUARE_SIZE / 2))
        if snake.key_check == False:
            snake.movement = (1, 0)
        #snake.snake_body_part()
        snake.render()
        snake.update()
        snake.screen_boundary()
        snake.check_collision()
        snake.snake_body_collision()
        apple.rect_and_render(snake.score)

        square_grid(no_of_squares)
        screen.blit(game_name, game_name_rect)
    
    else:
        screen.blit(snake_image, snake_image_rect)
        if times_played == 0:
            
            screen.blit(title_name, title_rect)
            screen.blit(press_c_to_play, press_c_to_play_rect)
            screen.blit(press_q_to_quit, press_q_to_quit_rect)
        else:
            
            score_font = pygame.font.Font('font/Pixeltype.ttf', 70)
            score_message = score_font.render('  Final Score: ' + str(snake.score),False,(255,255,255))
            score_message_rect = score_message.get_rect(center = (int(GAME_WIDTH/2), 70))
            press_c_to_play = title_font.render('  Press c to play again', False, (255, 255, 255))
            press_c_to_play_rect = press_c_to_play.get_rect(center = (int(GAME_WIDTH/2), 300))
            screen.blit(score_message, score_message_rect)
            screen.blit(press_c_to_play, press_c_to_play_rect)
            screen.blit(press_q_to_quit, press_q_to_quit_rect)
        
    pygame.display.update()
    clock.tick(FRAMES_PER_SECOND)
    





        