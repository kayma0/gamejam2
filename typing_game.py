# import necessary modules
import random
import pygame
import cv2

from game_process import run_game


def level_select(screen, clock, WIDTH, HEIGHT):
    # Load background image for level screen
    levels_img = pygame.image.load("media/levels.png").convert()
    levels_img = pygame.transform.scale(levels_img, (WIDTH, HEIGHT))

    # Clickable hitboxes (tweak these if the circles don’t line up perfectly)
    y_circle = int(HEIGHT * 0.36)
    radius = int(min(WIDTH, HEIGHT) * 0.10)

    easy_center = (int(WIDTH * 0.20), y_circle)
    medium_center = (int(WIDTH * 0.50), y_circle)
    hard_center = (int(WIDTH * 0.80), y_circle)

    def clicked_circle(mouse_pos, center, r):
        mx, my = mouse_pos
        cx, cy = center
        return (mx - cx) ** 2 + (my - cy) ** 2 <= r ** 2

    font = pygame.font.SysFont("arial", 28, bold=True)

    while True:
        clock.tick(60)
        screen.blit(levels_img, (0, 0))

        # optional hover hint
        mx, my = pygame.mouse.get_pos()
        hint = None
        if clicked_circle((mx, my), easy_center, radius):
            hint = "EASY"
        elif clicked_circle((mx, my), medium_center, radius):
            hint = "MEDIUM"
        elif clicked_circle((mx, my), hard_center, radius):
            hint = "HARD"

        if hint:
            tip = font.render(f"Click to choose: {hint}", True, (0, 0, 0))
            screen.blit(tip, (20, 20))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return None
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = event.pos
                if clicked_circle(pos, easy_center, radius):
                    return "easy"
                if clicked_circle(pos, medium_center, radius):
                    return "medium"
                if clicked_circle(pos, hard_center, radius):
                    return "hard"


pygame.init()
pygame.mixer.init()

# load and play bg music
pygame.mixer.music.load("sound/intro_music.mp3")
pygame.mixer.music.set_volume(0.25)
pygame.mixer.music.play(-1)

# screen dimensions
WIDTH = 1200
HEIGHT = 800
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Station X: Scrambled Files")
timer = pygame.time.Clock()
fps = 60

intro_vid = "media/intro.mp4"
outro_vid = "media/outro.mp4"

# Play intro video
video = cv2.VideoCapture(intro_vid)
fps_video = video.get(cv2.CAP_PROP_FPS) or 30

last_frame = None
playing_video = True
while playing_video:
    ret, frame = video.read()
    if not ret:
        playing_video = False
        break

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = pygame.surfarray.make_surface(frame.swapaxes(0, 1))

    surf = pygame.transform.scale(frame, (WIDTH, HEIGHT))
    last_frame = surf
    screen.blit(surf, (0, 0))
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

    timer.tick(fps_video)

video.release()

# Show BEGIN button on last frame of intro video
font = pygame.font.SysFont("arial", 48)
button_width = 200
button_height = 60
button_x = (WIDTH - button_width) // 2
button_y = (HEIGHT - button_height) - 80
button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
button_clicked = False

begin_screen = True
while begin_screen:
    timer.tick(fps)

    if last_frame:
        screen.blit(last_frame, (0, 0))
    else:
        screen.fill((0, 0, 0))

    pygame.draw.rect(screen, (150, 90, 40), button_rect, border_radius=12)
    pygame.draw.rect(screen, (255, 255, 255), button_rect, 2, border_radius=12)
    text = font.render("BEGIN", True, (0, 0, 0))
    text_rect = text.get_rect(center=button_rect.center)
    screen.blit(text, text_rect)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                button_clicked = True
                begin_screen = False

# Only continue if BEGIN was clicked
if button_clicked:
    # Play outro video
    video = cv2.VideoCapture(outro_vid)
    fps_video = video.get(cv2.CAP_PROP_FPS) or 30

    playing_video = True
    while playing_video:
        ret, frame = video.read()
        if not ret:
            playing_video = False
            break

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = pygame.surfarray.make_surface(frame.swapaxes(0, 1))

        surf = pygame.transform.scale(frame, (WIDTH, HEIGHT))
        screen.blit(surf, (0, 0))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

        timer.tick(fps_video)

    video.release()

    # Instructions screen with continue button
    instructions_img = pygame.image.load("media/instructions.png").convert()
    instructions_img = pygame.transform.scale(instructions_img, (WIDTH, HEIGHT))

    continue_button_width = 220
    continue_button_height = 60
    continue_button_x = WIDTH - continue_button_width - 40
    continue_button_y = HEIGHT - continue_button_height - 40
    continue_button_rect = pygame.Rect(
        continue_button_x, continue_button_y, continue_button_width, continue_button_height
    )

    waiting_for_input = True
    while waiting_for_input:
        timer.tick(fps)

        screen.blit(instructions_img, (0, 0))

        pygame.draw.rect(screen, (150, 90, 40), continue_button_rect, border_radius=12)
        pygame.draw.rect(screen, (255, 255, 255), continue_button_rect, 2, border_radius=12)
        text = font.render("CONTINUE", True, (255, 255, 255))
        text_rect = text.get_rect(center=continue_button_rect.center)
        screen.blit(text, text_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if continue_button_rect.collidepoint(event.pos):
                    waiting_for_input = False

    # Level select happens AFTER continue loop ends
    difficulty = level_select(screen, timer, WIDTH, HEIGHT)
    if difficulty is None:
        pygame.quit()
        raise SystemExit

    # hand off to gameplay
    run_game(difficulty)

pygame.quit()