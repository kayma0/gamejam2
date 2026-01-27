import pygame
import cv2

from game_process import run_game


def draw_back_button(screen, WIDTH):
    back_rect = pygame.Rect(20, 20, 120, 45)
    pygame.draw.rect(screen, (150, 90, 40), back_rect, border_radius=10)
    pygame.draw.rect(screen, (255, 255, 255), back_rect, 2, border_radius=10)

    back_font = pygame.font.SysFont("arial", 28, bold=True)
    text = back_font.render("BACK", True, (255, 255, 255))
    screen.blit(text, text.get_rect(center=back_rect.center))
    return back_rect


def play_video(screen, clock, path, WIDTH, HEIGHT):
    video = cv2.VideoCapture(path)
    fps_video = video.get(cv2.CAP_PROP_FPS) or 30

    last_frame = None
    while True:
        ret, frame = video.read()
        if not ret:
            break

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
        surf = pygame.transform.scale(frame, (WIDTH, HEIGHT))

        last_frame = surf
        screen.blit(surf, (0, 0))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                video.release()
                return None

        clock.tick(fps_video)

    video.release()
    return last_frame


def end_video_screen(screen, clock, WIDTH, HEIGHT, video_path, audio_path):
    # stop menu/background music
    try:
        pygame.mixer.music.stop()
    except Exception:
        pass

    # play end audio once
    end_snd = None
    try:
        end_snd = pygame.mixer.Sound(audio_path)
        end_snd.play()
    except Exception:
        end_snd = None

    # play end video
    last_frame = play_video(screen, clock, video_path, WIDTH, HEIGHT)
    if last_frame is None:
        return "quit"

    # button to return to levels
    btn_font = pygame.font.SysFont("arial", 30, bold=True)
    btn_w, btn_h = 200, 60
    btn_x = (WIDTH - btn_w) // 2
    btn_y = HEIGHT - 100
    btn_rect = pygame.Rect(btn_x, btn_y, btn_w, btn_h)

    while True:
        clock.tick(60)
        screen.blit(last_frame, (0, 0))

        pygame.draw.rect(screen, (150, 90, 40), btn_rect, border_radius=12)
        pygame.draw.rect(screen, (255, 255, 255), btn_rect, 2, border_radius=12)
        txt = btn_font.render("CONTINUE", True, (255, 255, 255))
        screen.blit(txt, txt.get_rect(center=btn_rect.center))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn_rect.collidepoint(event.pos):
                    try:
                        if end_snd:
                            end_snd.stop()
                    except Exception:
                        pass
                    return "levels"


# ---------- screens ----------
def begin_screen(screen, clock, WIDTH, HEIGHT, last_frame):
    font = pygame.font.SysFont("arial", 38, bold=True)
    button_width = 150
    button_height = 60
    button_x = (WIDTH - button_width) // 2
    button_y = (HEIGHT - button_height) - 80
    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

    while True:
        clock.tick(60)

        if last_frame:
            screen.blit(last_frame, (0, 0))
        else:
            screen.fill((0, 0, 0))

        pygame.draw.rect(screen, (150, 90, 40), button_rect, border_radius=12)
        pygame.draw.rect(screen, (255, 255, 255), button_rect, 2, border_radius=12)
        text = font.render("BEGIN", True, (255, 255, 255))
        screen.blit(text, text.get_rect(center=button_rect.center))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    return "next"


def instructions_screen(screen, clock, WIDTH, HEIGHT):
    instructions_img = pygame.image.load("media/instructions.png").convert()
    instructions_img = pygame.transform.scale(instructions_img, (WIDTH, HEIGHT))

    font = pygame.font.SysFont("arial", 38, bold=True)
    hint_font = pygame.font.SysFont("arial", 28, bold=True)

    continue_button_width = 220
    continue_button_height = 60
    continue_button_x = WIDTH - continue_button_width - 40
    continue_button_y = HEIGHT - continue_button_height - 40
    continue_button_rect = pygame.Rect(
        continue_button_x, continue_button_y, continue_button_width, continue_button_height
    )
    # top-right corner hitbox to lead to logbook
    top_right_rect = pygame.Rect(WIDTH - 250, 20, 200, 200)

    while True:
        clock.tick(60)
        screen.blit(instructions_img, (0, 0))

    #gives indication that what the user is hovering over is for the logbook
        mx, my = pygame.mouse.get_pos()
        if top_right_rect.collidepoint((mx, my)):
            logbook_hint = hint_font.render("Logbook", True, (255, 255, 255))
            screen.blit(logbook_hint, (WIDTH - 100, 100))

        # back button (top-left)
        back_rect = draw_back_button(screen, WIDTH)

        pygame.draw.rect(screen, (150, 90, 40), continue_button_rect, border_radius=12)
        pygame.draw.rect(screen, (255, 255, 255), continue_button_rect, 2, border_radius=12)
        text = font.render("CONTINUE", True, (255, 255, 255))
        screen.blit(text, text.get_rect(center=continue_button_rect.center))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(event.pos):
                    return "back"
                if top_right_rect.collidepoint(event.pos):
                    return "logbook"
                if continue_button_rect.collidepoint(event.pos):
                    return "next"

def logbook_screen(screen, clock, WIDTH, HEIGHT):
    logbook_img = pygame.image.load("media/logbook.png").convert()  
    logbook_img = pygame.transform.scale(logbook_img, (WIDTH, HEIGHT))
    
    while True:
        clock.tick(60)
        screen.blit(logbook_img, (0, 0))
        
        # back button
        back_rect = draw_back_button(screen, WIDTH)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(event.pos):
                    return "back"
                
def level_select(screen, clock, WIDTH, HEIGHT):
    levels_img = pygame.image.load("media/levels.png").convert()
    levels_img = pygame.transform.scale(levels_img, (WIDTH, HEIGHT))

    # top-right corner hitbox to lead to logbook
    top_right_rect = pygame.Rect(WIDTH - 250, 20, 200, 200)

    # clickable hitboxes 
    y_circle = int(HEIGHT * 0.36)
    radius = int(min(WIDTH, HEIGHT) * 0.15)

    easy_center = (int(WIDTH * 0.20), y_circle)
    medium_center = (int(WIDTH * 0.50), y_circle)
    hard_center = (int(WIDTH * 0.80), y_circle)

    def clicked_circle(mouse_pos, center, r):
        mx, my = mouse_pos
        cx, cy = center
        return (mx - cx) ** 2 + (my - cy) ** 2 <= r ** 2

    hint_font = pygame.font.SysFont("arial", 28, bold=True)

    while True:
        clock.tick(60)
        screen.blit(levels_img, (0, 0))
        # back button
        back_rect = draw_back_button(screen, WIDTH)

        # hover hint
        mx, my = pygame.mouse.get_pos()
        hint = None
        if clicked_circle((mx, my), easy_center, radius):
            hint = "EASY"
        elif clicked_circle((mx, my), medium_center, radius):
            hint = "MEDIUM"
        elif clicked_circle((mx, my), hard_center, radius):
            hint = "HARD"

        if hint:
            tip = hint_font.render(f"Click: {hint}", True, (255, 255, 255))
            screen.blit(tip, (160, 28))
        
        if top_right_rect.collidepoint((mx, my)):
                logbook_hint = hint_font.render("Logbook", True, (255, 255, 255))
                screen.blit(logbook_hint, (WIDTH - 100, 100))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if back_rect.collidepoint(event.pos):
                    return "back"
                pos = event.pos
                if top_right_rect.collidepoint(event.pos):
                    return "logbook"
                if clicked_circle(pos, easy_center, radius):
                    return "easy"
                if clicked_circle(pos, medium_center, radius):
                    return "medium"
                if clicked_circle(pos, hard_center, radius):
                    return "hard"


# ---------- main game ----------
def main():
    pygame.init()
    pygame.mixer.init()

    # background music
    try:
        pygame.mixer.music.load("sound/intro_music.mp3")
        pygame.mixer.music.set_volume(0.25)
        pygame.mixer.music.play(-1)
    except Exception:
        pass

    WIDTH, HEIGHT = 1200, 800
    screen = pygame.display.set_mode([WIDTH, HEIGHT])
    pygame.display.set_caption("Station X: Scrambled Files")
    clock = pygame.time.Clock()

    intro_vid = "media/intro.mp4"
    outro_vid = "media/outro.mp4"

    fail_vid = "media/fail_screen.mp4"
    fail_audio = "sound/fail_sound.mp3"
    
    success_vid = "media/level_complete.mp4"
    success_audio = "sound/success_sound.mp3"

    last_frame = play_video(screen, clock, intro_vid, WIDTH, HEIGHT)
    if last_frame is None:
        pygame.quit()
        return

    while True:
        choice = begin_screen(screen, clock, WIDTH, HEIGHT, last_frame)
        if choice == "quit":
            break

        # play your second video 
        end_frame = play_video(screen, clock, outro_vid, WIDTH, HEIGHT)
        if end_frame is None:
            break

        ins = instructions_screen(screen, clock, WIDTH, HEIGHT)
        if ins == "quit":
            break
        if ins == "logbook":
            logbook_screen(screen, clock, WIDTH, HEIGHT)
            continue
        if ins == "back":
            continue

        while True:
            diff = level_select(screen, clock, WIDTH, HEIGHT)
            if diff == "quit":
                pygame.quit()
                return
            if diff == "back":
                ins2 = instructions_screen(screen, clock, WIDTH, HEIGHT)
                if ins2 == "quit":
                    pygame.quit()
                    return
                if ins2 == "back":
                    # back to begin screen
                    break  # break out to BEGIN
                # if next, go back to level select again
                continue       
            
            if diff == "logbook": 
                logbook_screen(screen, clock, WIDTH, HEIGHT)
                continue

            result = run_game(diff)  # "back" | "quit" | "game_over" | "level_complete"

            if result == "quit":
                pygame.quit()
                return

            if result == "back":
                # back to level select
                continue

            if result == "game_over":
                end = end_video_screen(screen, clock, WIDTH, HEIGHT, fail_vid, fail_audio)
                if end == "quit":
                    pygame.quit()
                    return
                # end == "levels" -> show level select again
                continue
            
            if result == "level_complete":
                end = end_video_screen(screen, clock, WIDTH, HEIGHT, success_vid, success_audio)
                if end == "quit":
                    pygame.quit()
                    return
                # end == "levels" -> show level select again
                continue

        # if we broke out, it returns to BEGIN loop

    pygame.quit()


if __name__ == "__main__":
    main()