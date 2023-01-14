import pygame
import random
from sys import exit

pygame.init()

# ------------------------------------- Setup Variables ------------------------------------------

# Frames per second
FPS = 60

# colors
black = (0, 0, 0)
white = (255, 255, 255)
gray = (50, 50, 50)

game_over = False

# Window size and initialization
surface_width = 1820
surface_height = 980
surface = pygame.display.set_mode((surface_width, surface_height), )

pygame.display.set_caption("Pong")
clock = pygame.time.Clock()


# ------------------------------------- Functions ------------------------------------------

# Block creation
def blocks(x_pos, y_pos, block_width, block_height):
    pygame.draw.rect(surface, white, [round(x_pos), round(y_pos), block_width, block_height])


# Text obj creation
def make_text_obj(text, font, color):
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()


# Text surface creation
def msg_surface(text, x, y, font_size, color):
    title_text_surface, title_text_rectangle = make_text_obj(text, font_size, color)
    title_text_rectangle.center = round(x), round(y)
    surface.blit(title_text_surface, title_text_rectangle)


# ------------------------------------- Main Function ------------------------------------------
def main():

    # Game active activation
    game_active = False

    # Load sound effects
    ball_bounce_sound_1 = pygame.mixer.Sound(r"./Audio/Hit 1.wav")
    ball_bounce_sound_2 = pygame.mixer.Sound(r"./Audio/Hit 2.wav")
    lose_sound = pygame.mixer.Sound(r"./Audio/Lose.wav")
    win_sound = pygame.mixer.Sound(r"./Audio/Win.wav")
    enemy_score_sound = pygame.mixer.Sound(r"./Audio/Bad Score.wav")
    score_sound = pygame.mixer.Sound(r"./Audio/Score.wav")

    # load and play music
    pygame.mixer.music.load(r"./Audio/Music.wav")
    pygame.mixer.music.play(1)

    # Surface center
    surface_width_center = (surface_width / 2)
    surface_height_center = (surface_height / 2)

    # Paddle height and width
    paddle_height = 100
    paddle_width = 20

    # Center of paddle
    paddle_center = (paddle_height / 2)

    # Paddle speed initial variables
    left_paddle_speed = 0
    right_paddle_speed = 0

    # Left paddle initial position
    left_paddle_y = surface_height_center - paddle_center
    left_paddle_x = 100
    left_paddle_score = 0

    # Right paddle initial position
    right_paddle_y = surface_height_center - paddle_center
    right_paddle_x = (surface_width - 130)
    right_paddle_score = 0

    # Ball initial speed
    ball_speed_x = 40
    ball_speed_y = 40

    # Ball size
    ball_height = 20
    ball_width = 20

    # Ball x and y pos (initial position for intro screen but reassigned when game start)
    ball_x = random.randrange(0, surface_width - ball_width)
    ball_y = 0

    # Center of ball
    ball_center = (ball_height / 2)

    # Intro Screen activation
    intro_screen = True

    # Difficulty Menu activation
    difficulty_menu = False

    # Ball x position for serve
    left_paddle_serve = left_paddle_x + paddle_width + 5
    right_paddle_serve = right_paddle_x - ball_width - 5

    # Serve activation
    left_serve = False
    right_serve = False

    # Win/Lose activation
    win = False
    lose = False

    # Points to win
    points_to_win = 11

    # Difficulty activation
    easy = False
    medium = False
    hard = False

    # Difficulty lock
    medium_unlock = False
    hard_unlock = False

    # Font Sizes
    medium_text = pygame.font.Font(r'.\Fonts\8-Bit Madness.ttf', 80)
    large_text = pygame.font.Font(r'.\Fonts\8-Bit Madness.ttf', 100)
    larger_text = pygame.font.Font(r'.\Fonts\8-Bit Madness.ttf', 150)
    controls_text = pygame.font.Font(r'.\Fonts\8-Bit Madness.ttf', 40)
    press_key_intro_text = pygame.font.Font(r'.\Fonts\8-Bit Madness.ttf',50)
    pong_intro_text = pygame.font.Font(r'.\Fonts\8-Bit Madness.ttf', 400)

    # -------------------------------------------------- Main Loop -----------------------------------------------------
    while not game_over:

        # Event Detection
        for event in pygame.event.get():

            # Quit Detection
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # Mouse Click Detection
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_press = True
            else:
                mouse_press = False

            # Intro Screen Key Detection
            if (event.type == pygame.KEYDOWN) and intro_screen:
                difficulty_menu = True
                intro_screen = False

        # ------------------------------- Active Game Loop -------------------------------------
        if game_active:

            # Player paddle controls
            keysPressed = pygame.key.get_pressed()
            if keysPressed[pygame.K_UP]:
                left_paddle_y -= left_paddle_speed
                if left_paddle_y < 0:
                    left_paddle_y = 0
            elif keysPressed[pygame.K_DOWN]:
                left_paddle_y += left_paddle_speed
                if left_paddle_y > (surface_height - paddle_height):
                    left_paddle_y = surface_height - paddle_height

            # CPU paddle controls
            if ball_speed_x > 0:
                if (ball_y + ball_center) < (right_paddle_y + 40):
                    right_paddle_y -= right_paddle_speed
                    if right_paddle_y < 0:
                        right_paddle_y = 0
                elif (ball_y + ball_center) > (right_paddle_y + paddle_height - 40):
                    right_paddle_y += right_paddle_speed
                    if right_paddle_y > (surface_height - paddle_height):
                        right_paddle_y = surface_height - paddle_height

            # Ball movement
            ball_x += ball_speed_x
            ball_y += ball_speed_y

            # Score Detection
            if ball_x > surface_width - 10:
                left_paddle_score += 1
                left_serve = True
                if (left_paddle_score < points_to_win) and (right_paddle_score < points_to_win):
                    score_sound.play()
            elif ball_x < 0:
                right_paddle_score += 1
                right_serve = True
                if (left_paddle_score < points_to_win) and (right_paddle_score < points_to_win):
                    enemy_score_sound.play()

            #  Top and bottom wall ball bounce
            if ball_y > surface_height - ball_height:
                ball_speed_y = -ball_speed_y
            elif ball_y < 0:
                ball_speed_y = abs(ball_speed_y)

            # Win detection
            if left_paddle_score >= points_to_win:
                win = True
                win_sound.play()
                if easy:
                    medium_unlock = True
                if medium:
                    hard_unlock = True

            # Lose detection
            elif right_paddle_score >= points_to_win:
                lose = True
                lose_sound.play()

            # Left paddle ball bounce
            if ball_x <= (left_paddle_x + paddle_width) and (ball_y >= left_paddle_y) and (
                    ball_y <= (left_paddle_y + paddle_height)):
                ball_x = left_paddle_x + paddle_width
                ball_speed_x = abs(ball_speed_x)
                ball_y_check = ball_speed_y + random.choice([-4, 4])
                if ball_y_check != -ball_speed_y:
                    ball_speed_y = ball_y_check
                if (not left_serve) and (not right_serve):
                    ball_bounce_sound_1.play()

            # Right paddle ball bounce
            elif (ball_x >= right_paddle_x) and (ball_y >= right_paddle_y) and (
                    ball_y <= (right_paddle_y + paddle_height)):
                ball_x = right_paddle_x
                ball_speed_x = -ball_speed_x
                ball_y_check = ball_speed_y + random.choice([-4, 4])
                if ball_y_check != -ball_speed_y:
                    ball_speed_y = ball_y_check
                if (not left_serve) and (not right_serve):
                    ball_bounce_sound_2.play()

            # Paddle center position
            left_paddle_center = left_paddle_y + (paddle_center - ball_center)
            right_paddle_center = right_paddle_y + (paddle_center - ball_center)

            # Left paddle serve and ball position
            if left_serve:
                ball_x = left_paddle_serve
                ball_y = left_paddle_center
                ball_speed_y = random.choice([-2, 2])
                if keysPressed[pygame.K_SPACE]:
                    left_serve = False

            # Right paddle serve and ball position
            elif right_serve:
                ball_speed_y = random.choice([-2, 2])
                ball_x = right_paddle_serve
                ball_y = right_paddle_center
                if keysPressed[pygame.K_SPACE]:
                    right_serve = False

            surface.fill(black)

            # Draw Scores
            msg_surface(str(right_paddle_score), (surface_width - (surface_width / 4)), (surface_height / 4) - 150, large_text, white)
            msg_surface(str(left_paddle_score), (surface_width / 4), (surface_height / 4) - 150, large_text, white)

            # Draw Paddles
            blocks(left_paddle_x, left_paddle_y, paddle_width, paddle_height)
            blocks(right_paddle_x, right_paddle_y, paddle_width, paddle_height)

            # Draw Center Line
            blocks(905, 40, 5, surface_height - 80)

            # Draw Ball
            blocks(ball_x, ball_y, ball_height, ball_width)

        # ------------------------------------- Win/Lose Menu Loop ------------------------------------------

        # Mouse Position
        mouse_pos = pygame.mouse.get_pos()

        # Text Size (Win/Lose menu)
        try_again_text = medium_text
        difficulty_text = medium_text
        quit_text = medium_text

        # Paddle, ball and score reset if win/lose activated
        if win or lose:
            left_paddle_score = 0
            right_paddle_score = 0

            difficulty_menu = False
            game_active = False

            ball_x = surface_width_center
            ball_y = surface_height_center
            left_paddle_y = surface_height_center - paddle_center
            right_paddle_y = surface_height_center - paddle_center

            surface.fill(black)

            # Mouse Position and choice detection (Win/Lose)

            # Mouse over TRY AGAIN text detection
            if (mouse_pos[0] > 750) and (mouse_pos[0] < 1070) and (mouse_pos[1] > 415) and (mouse_pos[1] < 460):
                try_again_text = large_text
                if mouse_press:
                    game_active = True
                    right_serve = False
                    left_serve = True
                    lose = False
                    win = False

            # Mouse over CHOOSE DIFFICULTY text detection
            elif (mouse_pos[0] > 570) and (mouse_pos[0] < 1250) and (mouse_pos[1] > 517) and (mouse_pos[1] < 560):
                difficulty_text = large_text
                if mouse_press:
                    difficulty_menu = True
                    lose = False
                    win = False
                    mouse_press = False

            # Mouse over QUIT text detection
            elif (mouse_pos[0] > 840) and (mouse_pos[0] < 980) and (mouse_pos[1] > 617) and (mouse_pos[1] < 660):
                quit_text = large_text
                if mouse_press:
                    pygame.quit()
                    exit()

            # Win/Lose Screen Text
            msg_surface("DIFFICULTY SETTINGS", surface_width_center, surface_height_center + 50, difficulty_text, white)
            msg_surface("QUIT", surface_width_center, surface_height_center + 150, quit_text, white)

            if win:
                msg_surface("YOU WON!", surface_width_center, surface_height_center - 175, larger_text, white)
                msg_surface("PLAY AGAIN", surface_width_center, surface_height_center - 50, try_again_text, white)
                blocks(660, 355, 500, 5)
                left_paddle_score = 0
            elif lose:
                msg_surface("YOU'RE A LOSER!", surface_width_center, surface_height_center - 175, larger_text, white)
                msg_surface("TRY AGAIN", surface_width_center, surface_height_center - 50, try_again_text, white)
                blocks(445, 355, 935, 5)
                right_paddle_score = 0

        # ------------------------------------- Difficulty Menu Loop ------------------------------------------

        # Text size (Difficulty Menu)
        easy_difficulty_text = medium_text
        medium_difficulty_text = medium_text
        hard_difficulty_text = medium_text

        if difficulty_menu:

            # Intro music stop
            pygame.mixer.music.stop()

            # Difficulty text color
            medium_color = gray
            hard_color = gray

            # Mouse Position and Choice Detection (Difficulty Menu)

            # Mouse over EASY text detection
            if (mouse_pos[0] > 830) and (mouse_pos[0] < 990) and (mouse_pos[1] > 415) and (mouse_pos[1] < 460):
                easy_difficulty_text = large_text
                if mouse_press:
                    game_active = True
                    difficulty_menu = False
                    win = False
                    lose = False
                    left_serve = True
                    right_serve = False
                    easy = True
                    medium = False
                    hard = False

            # Mouse over MEDIUM text detection
            elif (mouse_pos[0] > 795) and (mouse_pos[0] < 1025) and (mouse_pos[1] > 517) and (mouse_pos[1] < 560) and medium_unlock:
                medium_difficulty_text = large_text
                if mouse_press:
                    game_active = True
                    difficulty_menu = False
                    left_serve = True
                    right_serve = False
                    win = False
                    lose = False
                    easy = False
                    medium = True
                    hard = False

            # Mouse over HARD text detection
            elif (mouse_pos[0] > 830) and (mouse_pos[0] < 990) and (mouse_pos[1] > 617) and (mouse_pos[1] < 660) and hard_unlock:
                hard_difficulty_text = large_text
                if mouse_press:
                    game_active = True
                    difficulty_menu = False
                    left_serve = True
                    right_serve = False
                    win = False
                    lose = False
                    easy = False
                    medium = False
                    hard = True

            # Difficulty: paddle and ball movement variables
            if easy:
                left_paddle_speed = 20
                right_paddle_speed = 10
                ball_speed_x = 30
                ball_speed_y = random.choice([-3, 3])
            elif medium:
                left_paddle_speed = 30
                right_paddle_speed = 15
                ball_speed_x = 40
                ball_speed_y = random.choice([-3, 3])
            elif hard:
                left_paddle_speed = 30
                right_paddle_speed = 20
                ball_speed_x = 50
                ball_speed_y = random.choice([-3, 3])

            # White difficulty text if unlocked
            if medium_unlock:
                medium_color = white
            if hard_unlock:
                hard_color = white

            surface.fill(black)

            # Line under CHOOSE DIFFICULTY text
            blocks(525, 320, 770, 5)

            # Difficulty Text
            msg_surface("CHOOSE DIFFICULTY", surface_width_center, surface_height_center - 200, large_text, white)
            msg_surface("EASY", surface_width_center, surface_height_center - 50, easy_difficulty_text, white)
            msg_surface("MEDIUM", surface_width_center, surface_height_center + 50, medium_difficulty_text, medium_color)
            msg_surface("HARD", surface_width_center, surface_height_center + 150, hard_difficulty_text, hard_color)

            # Controls Text
            msg_surface("UP ARROW - UP", (surface_width - (surface_width / 4)), (surface_height - 100), controls_text, white)
            msg_surface("DOWN ARROW - DOWN", surface_width_center - 500, (surface_height - 100), controls_text, white)
            msg_surface("SPACE - SERVE", surface_width_center, (surface_height - 100), controls_text, white)

        # ------------------------------------- Intro Screen Loop ------------------------------------------
        if intro_screen:

            # Text Color
            text_color = white

            # Edge of screen for ball (Intro)
            top_edge = 0
            right_edge = surface_width - ball_width
            left_edge = 0
            bottom_edge = surface_height - ball_height

            # Ball bounce left and right of screen (Intro)
            ball_x += ball_speed_x
            if ball_x > right_edge:
                ball_speed_x = -ball_speed_x
            elif ball_x < left_edge:
                ball_speed_x = abs(ball_speed_x)

            # Ball bounce top and bottom of screen (Intro)
            ball_y += ball_speed_y
            if ball_y > bottom_edge:
                ball_speed_y = -ball_speed_y
            elif ball_y < top_edge:
                ball_speed_y = abs(ball_speed_y)

            surface.fill(black)

            # Intro Screen Text
            msg_surface("PONG", surface_width_center, surface_height_center - 50, pong_intro_text, text_color)
            msg_surface("[ PRESS ANY KEY ]", surface_width_center, surface_height_center + 100, press_key_intro_text, text_color)

            # Intro screen draw ball
            blocks(ball_x, ball_y, ball_width, ball_height)

        pygame.display.update()
        clock.tick(FPS)


# Main loop function activation
main()
pygame.quit()