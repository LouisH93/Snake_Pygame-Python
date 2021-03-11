'''A simple retro 2D snake game built using pygame.'''
import pygame as pg
import random, time, sys
from math import sqrt

# CONSTANTS
SIZE = 30 # snake-player.png image size
BACKGROUND_COLOUR = (0,0,0) # black
TEXT_COLOUR = (0, 255, 0) # green


class Snake:
    def __init__(self, game_window, length):
        self.game_window = game_window 
        self.length = length
        self.snake = pg.image.load('Snake-assets/snake-player.png')
        self.xcor = [SIZE]*length # When length is equal to 2 for example, self.xcor and self.ycor = [30, 30]
        self.ycor = [SIZE]*length 
        self.direction = 'down'


    def draw_snake(self):
        for i in range(self.length):
            '''Draw the 0th elements of xcor and ycor lists, followed by the 1st, 2nd and so on elements to give the illusion of a
            moving snake''' 
            self.game_window.blit(self.snake, (self.xcor[i], self.ycor[i]))
        

    def move_left(self):
        '''Method will be called when keybinding event for K_LEFT is triggered'''
        self.direction = 'left'
        self.draw_snake()
        

    def move_right(self):
        '''Method will be called when keybinding event for K_RIGHT is triggered'''
        self.direction = 'right'
        self.draw_snake()


    def move_up(self):
        '''Method will be called when keybinding event for K_UP is triggered'''
        self.direction = 'up'
        self.draw_snake()


    def move_down(self):
        '''Method will be called when keybinding event for K_DOWN is triggered, this is also the default movement direction as
        initialised in the __init__ method'''
        self.direction = 'down'
        self.draw_snake()


    def default_movement(self):
        '''Reverse range for self.xcor[1:] and self.ycor[1:], self.xcor[1] = self.xcor[0] for example, giving the illusion of seamless
        movement in the direction the snake's head is facing'''
        for i in range(self.length -1, 0, -1):
            self.xcor[i] = self.xcor[i - 1]
            self.ycor[i] = self.ycor[i - 1]
        '''The head of the snake moves in the direction of the keybinding event trigger by SIZE(30) pixels'''
        if self.direction == 'left':
            self.xcor[0] -= SIZE
        if self.direction == 'right':
            self.xcor[0] += SIZE
        if self.direction == 'up':
            self.ycor[0] -= SIZE
        if self.direction == 'down':
            self.ycor[0] += SIZE
        '''Re-drawing the background colour for each iteration of the mainloop will keep the snake at the intended length, as per the default
        size, and also the increase in size as per the game logic.'''
        self.game_window.fill((BACKGROUND_COLOUR))
        self.draw_snake()


    def increment_length(self):
        '''Method will be called when the snake collides with the apple, a new block will be appended to xcor and ycor lists each time a
        collision occurs'''
        self.length += 1
        self.xcor.append(SIZE)
        self.ycor.append(SIZE)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Apple:
    def __init__(self, game_window):
        self.game_window = game_window
        self.apple = pg.image.load('Snake-assets/apple.png')
        self.xcor = random.randint(30, 730)
        self.ycor = random.randint(50, 550)


    def draw_apple(self):
        self.game_window.blit(self.apple, (self.xcor, self.ycor))
        

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class GameText:
    def __init__(self, game_window):
        self.game_window = game_window
        self.score_value = 0
        self.score_xcor = 300
        self.score_ycor = 10
        self.score_font = pg.font.Font('freesansbold.ttf', 32)

        self.title_xcor = 180
        self.title_ycor = 130
        self.title_font = pg.font.Font('freesansbold.ttf', 100)
        self.message1_xcor = 240
        self.message1_ycor = 250
        self.message1_font = pg.font.Font('freesansbold.ttf', 24)
        self.message2_xcor = 180
        self.message2_ycor = 300
        self.message2_font = pg.font.Font('freesansbold.ttf', 32)

        self.game_over_xcor = 200
        self.game_over_ycor = 250
        self.game_over_font = pg.font.Font('freesansbold.ttf', 64)
        self.play_again_xcor = 160
        self.play_again_ycor = 324
        self.play_again_font = pg.font.Font('freesansbold.ttf', 32)


    def display_score(self):
        '''Simple method to display the score'''
        render_font = self.score_font.render(f'Score: {self.score_value}', True, (TEXT_COLOUR))
        self.game_window.blit(render_font, (self.score_xcor, self.score_ycor))


    def display_game_over(self):
        '''Simple method to display a game over message and prompt user input'''
        self.game_window.fill((BACKGROUND_COLOUR))
        render_font1 = self.game_over_font.render('GAME OVER!', True, (TEXT_COLOUR))
        self.game_window.blit(render_font1, (self.game_over_xcor, self.game_over_ycor))
        render_font2 = self.play_again_font.render('Play Again: Enter / Quit: Escape', True, (TEXT_COLOUR))
        self.game_window.blit(render_font2, (self.play_again_xcor, self.play_again_ycor))
        pg.display.update()


    def intro_screen(self):
        '''Simple method to display an intro screen, game will run when keybinding event for K_RETURN is triggered'''
        self.game_window.fill((BACKGROUND_COLOUR))
        render_font1 = self.title_font.render('SNAKE!', True, (TEXT_COLOUR))
        self.game_window.blit(render_font1, (self.title_xcor, self.title_ycor))
        render_font2 = self.message1_font.render('Use Arrow Keys To Move', True, (TEXT_COLOUR))
        self.game_window.blit(render_font2, (self.message1_xcor, self.message1_ycor))
        render_font3 = self.message2_font.render('Press Enter To Continue', True, (TEXT_COLOUR))
        self.game_window.blit(render_font3, (self.message2_xcor, self.message2_ycor))
        pg.display.update()
        
            
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Game:
    def __init__(self):
        '''Game class will be a composite for all other classes. The game_window properties of the other classes will be self.screen.'''
        pg.init()
        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode((800, 600))
        self.caption = pg.display.set_caption('Snake')
        self.icon = pg.image.load('Snake-assets/snake-icon.png')
        pg.display.set_icon(self.icon)
        self.snake = Snake(self.screen, 2)
        self.apple = Apple(self.screen)
        self.game_text = GameText(self.screen)


    def is_collision(self, x1, x2, y1, y2):
        '''Equation for measuring the distance between two coordinates. This will determine collisions between the snake and the apple'''
        distance = sqrt((self.apple.xcor - self.snake.xcor[0])**2 + (self.apple.ycor - self.snake.ycor[0])**2)
        if distance < 30:
            return True
        return False


    def snake_collision(self, x1, x2, y1, y2, x):
        '''Same equation as above, x represents self.snake.xcor[3:], same for self.snake.ycor. This will determine whether the snake
        collides with itself'''
        distance = sqrt((self.snake.xcor[x] - self.snake.xcor[0])**2 + (self.snake.ycor[x] - self.snake.ycor[0])**2)
        if distance < 30:
            return True
        return False
        
        
    def play(self):
        self.snake.default_movement()
        self.apple.draw_apple()
        self.game_text.display_score()
        time.sleep(0.2) # Slows down the execution of each iteration of the mainloop by .2 seconds
        pg.display.update()
        self.clock.tick(120)
        
        '''Snake length and score incrementation, and re-drawing of apple at different coordinates'''
        if self.is_collision(self.snake.xcor, self.snake.ycor, self.apple.xcor, self.apple.ycor):
            self.apple.xcor = random.randint(30, 730)
            self.apple.ycor = random.randint(50, 550)
            self.snake.increment_length()
            self.game_text.score_value += 1


        for x in range(3, self.snake.length):
            '''When snake collides with itself, snake and apple dissapear off screen and an exception is raised, which will be
            used to trigger the game over message'''
            if self.snake_collision(self.snake.xcor[0], self.snake.ycor[0], self.snake.xcor[x], self.snake.ycor[x], x):
                self.snake.xcor = [2000 for x in self.snake.xcor]
                self.apple.xcor = 2000
                raise Exception
                break
                
             
    def run(self):
    '''Intro screen, game over message and all keybinding events '''


        intro = True
        while intro:
            self.game_text.intro_screen()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        pg.quit()
                        sys.exit()
                    if event.key == pg.K_RETURN:
                        intro = False

        pause = False
        running = True
        while running:
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    
                    if event.key == pg.K_LEFT:
                        self.snake.move_left()
                        
                    if event.key == pg.K_RIGHT:
                        self.snake.move_right()
                        
                    if event.key == pg.K_UP:
                        self.snake.move_up()
                        
                    if event.key == pg.K_DOWN:
                        self.snake.move_down()

                    if event.key == pg.K_RETURN:
                        snake = Game()
                        snake.run()

                    if event.key == pg.K_ESCAPE:
                        pg.quit()
                        sys.exit()


            try:
                if not(pause):
                    self.play()
            except Exception:
                self.game_text.display_game_over()
                pause = True

                
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
snake = Game()
snake.run()

    


