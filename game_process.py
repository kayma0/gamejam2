import pygame
import random

pygame.init()

# read words from the list so we can pick them
WORD_LIST = []
with open("words.txt") as f:
    for word_line in f:
        clean = word_line.strip()
        if clean:
            WORD_LIST.append(clean)

# sort by length so easy mode can use short ones
WORD_LIST.sort(key=len)

# make the game window and timer
WIDTH = 1200
HEIGHT = 800
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Station X: Typing Racer")
surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
clock = pygame.time.Clock()
fps = 60

# colours and fonts the game will use
ACCENT = (199, 134, 51)
BG = (12, 12, 16)
PANEL = (224, 206, 173)
TEXT_LIGHT = (250, 250, 250)
TEXT_DARK = (20, 20, 20)

# try to load a background picture
def load_background(path):
    try:
        image = pygame.image.load(path).convert()
        return pygame.transform.scale(image, (WIDTH, HEIGHT))
    except Exception:
        return None

def run_game(difficulty="easy"):
    # main loop that runs the game
    rules = DIFFICULTY_RULES.get(difficulty, DIFFICULTY_RULES["easy"])
    lives = rules["lives"]
    timer_limit = rules["timer_seconds"]
    speed_range = rules["speed_range"]
    words_src = filter_words_by_length(rules["len_filter"])
    words_src = build_len_indexes(words_src)
    if not words_src:
        words_src = WORD_LIST

    word_objects = []
    high_score = check_high_score(0, difficulty)
    paused = False
    new_level = True
    submit = ""
    active_string = ""
    score = 0
    time_left = float(timer_limit)

    run = True
    while run:
        if BACKGROUND_IMAGE:
            screen.blit(BACKGROUND_IMAGE, (0, 0))
        else:
            screen.fill(BG)
        dt = clock.tick(fps) / 1000.0

        if not paused and lives >= 0 and time_left > 0:
            time_left = max(0, time_left - dt)

        pause_butt = draw_screen(lives, score, active_string, high_score, time_left)
        if paused:
            resume_butt, quit_butt = draw_pause()
            if resume_butt:
                paused = False
            if quit_butt:
                check_high_score(score, difficulty)
                break
        if new_level and not paused:
            word_objects = generate_level(words_src, speed_range, score)
            new_level = False
        else:
            for w in list(word_objects):
                w.draw(active_string)
                if not paused:
                    w.update()
                if w.x_pos < -200:
                    word_objects.remove(w)
                    lives -= 1
            if not paused and time_left <= 0:
                lives = -1
        if len(word_objects) <= 0 and not paused:
            new_level = True

        if submit != "":
            init = score
            score = check_answer(word_objects, submit, score)
            submit = ""
            if init == score and wrong:
                wrong.play()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                check_high_score(score, difficulty)
                run = False

            if event.type == pygame.KEYDOWN:
                if not paused:
                    if len(event.unicode) == 1 and event.unicode.isalnum():
                        active_string += event.unicode
                        if click:
                            click.play()
                    if event.key == pygame.K_BACKSPACE and len(active_string) > 0:
                        active_string = active_string[:-1]
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        submit = active_string
                        active_string = ""
                if event.key == pygame.K_ESCAPE:
                    paused = not paused

        if pause_butt:
            paused = True

        if lives < 0:
            paused = True
            lives = rules["lives"]
            word_objects = []
            new_level = True
            high_score = check_high_score(score, difficulty)
            score = 0
            time_left = float(timer_limit)

        pygame.display.flip()
    pygame.quit()
   
    surface.blit(header_font.render("MENU", True, TEXT_LIGHT), (box_x + 10, box_y + 10))
    
    btn_y = box_y + 120
    resume_btn = Button(box_x + 80, btn_y, ">", False, surface)
    resume_btn.draw()
    quit_btn = Button(box_x + box_w - 120, btn_y, "X", False, surface)
    quit_btn.draw()
    surface.blit(header_font.render("PLAY!", True, TEXT_LIGHT), (box_x + 40, btn_y + 60))
    surface.blit(header_font.render("QUIT", True, TEXT_LIGHT), (box_x + box_w - 220, btn_y + 60))
    screen.blit(surface, (0, 0))
    return resume_btn.clicked, quit_btn.clicked


def generate_level(words_src, speed_range, score):
    # make falling words 
    word_objs = []
    play_area_top = 150 
    play_area_bottom = HEIGHT - 150  
    play_area_height = play_area_bottom - play_area_top

    word_count = min(6, 3 + (score // 500))
    # speed of words increases with score
    speed_factor = 1.0 + (score // 1000) * 0.15
    if word_count <= 0:
        return word_objs
    vertical_spacing = play_area_height / word_count
    for i in range(word_count):
        base_speed_min, base_speed_max = speed_range
        speed = int(random.randint(int(base_speed_min * speed_factor), int(base_speed_max * speed_factor)))
        y_pos = int(play_area_top + (i + 0.5) * vertical_spacing)
        x_pos = random.randint(WIDTH, WIDTH + 1000)
        text = random.choice(words_src).lower()
        word_objs.append(Word(text, speed, y_pos, x_pos))
    return word_objs


def check_answer(word_objects, submit, score):
    # see if the typed word matches any  falling word
    for wrd in list(word_objects):
        if wrd.text == submit:
            points = wrd.speed * len(wrd.text) * 10 * (len(wrd.text) / 4)
            score += int(points)
            word_objects.remove(wrd)
            if woosh:
                woosh.play()
    return score


def check_high_score(score, difficulty="easy"):
    # update the saved high score if needed for this difficulty
    high_score = 0
    filename = f"high_score_{difficulty}.txt"
    try:
        with open(filename, "r") as file:
            high_score = int(file.readlines()[0])
    except Exception:
        high_score = 0
    if score > high_score:
        with open(filename, "w") as file:
            file.write(str(int(score)))
        high_score = score
    return high_score


def run_game(difficulty="easy"):
<<<<<<< HEAD
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    bg_img = pygame.image.load("media/gamepage.png").convert()
    bg_img = pygame.transform.scale(bg_img, (width, height))
    pygame.display.set_caption("Station X: Codebreak")
    clock = pygame.time.Clock()
=======
    # main loop that runs the game
    rules = DIFFICULTY_RULES.get(difficulty, DIFFICULTY_RULES["easy"])
    lives = rules["lives"]
    timer_limit = rules["timer_seconds"]
    speed_range = rules["speed_range"]
    words_src = filter_words_by_length(rules["len_filter"])
    words_src = build_len_indexes(words_src)
    if not words_src:
        words_src = WORD_LIST
>>>>>>> ece7a53 (Adjust word spawn band, tweak speeds, reset highscores)

    word_objects = []
    high_score = check_high_score(0, difficulty)
    paused = False
    new_level = True
    submit = ""
    active_string = ""
    score = 0

    
    time_left = float(timer_limit)

    run = True
    while run:
        if BACKGROUND_IMAGE:
            screen.blit(BACKGROUND_IMAGE, (0, 0))
        else:
            screen.fill(BG)
        dt = clock.tick(fps) / 1000.0

        if not paused and lives >= 0 and time_left > 0:
            time_left = max(0, time_left - dt)

        pause_butt = draw_screen(lives, score, active_string, high_score, time_left)
        if paused:
            resume_butt, quit_butt = draw_pause()
            if resume_butt:
                paused = False
            if quit_butt:
                check_high_score(score, difficulty)
                break
        if new_level and not paused:
            word_objects = generate_level(words_src, speed_range, score)
            new_level = False
        else:
            for w in list(word_objects):
                w.draw(active_string)
                if not paused:
                    w.update()
                if w.x_pos < -200:
                    word_objects.remove(w)
                    lives -= 1
            if not paused and time_left <= 0:
                lives = -1
        if len(word_objects) <= 0 and not paused:
            new_level = True

        if submit != "":
            init = score
            score = check_answer(word_objects, submit, score)
            submit = ""
            if init == score and wrong:
                wrong.play()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                check_high_score(score, difficulty)
                run = False

            if event.type == pygame.KEYDOWN:
                if not paused:
                    if len(event.unicode) == 1 and event.unicode.isalnum():
                        active_string += event.unicode
                        if click:
                            click.play()
                    if event.key == pygame.K_BACKSPACE and len(active_string) > 0:
                        active_string = active_string[:-1]
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        submit = active_string
                        active_string = ""
                if event.key == pygame.K_ESCAPE:
                    paused = not paused
           

        if pause_butt:
            paused = True

        if lives < 0:
            paused = True
            lives = rules["lives"]
            word_objects = []
            new_level = True
            high_score = check_high_score(score, difficulty)
            score = 0
            time_left = float(timer_limit)

<<<<<<< HEAD
        if not game_over:
            time_remaining = timer_length - (time.time() - start_time)

            if time_remaining <= 0:
                player_lives -= 1
                rounds += 1

                timer_length -= cfg["timer_drop"]
                if timer_length < cfg["timer_min"]:
                    timer_length = cfg["timer_min"]

                word = pick_word(words, rounds)
                scrambled = mix(word)
                start_time = time.time()
                typed = ""

            if player_lives <= 0:
                game_over = True

        screen.blit(bg_img, (0, 0))

        # lives
        lives_text = label_font.render("Lives:", True, (20, 20, 20))
        screen.blit(lives_text, (40, 750))
        for i in range(player_lives):
            pygame.draw.circle(screen, (150, 90, 40), (130 + i * 26, 762), 12)

        # title
        pygame.draw.rect(screen, (200, 180, 165), (60, 40, 1080, 90), border_radius=14)
        pygame.draw.rect(screen, (150, 90, 40), (60, 40, 1080, 90), 3, border_radius=14)
        title = title_font.render("Station X: Scrambled Files", True, (150, 90, 40))
        screen.blit(title, (300, 60))

        # timer bar
        time_remaining = timer_length - (time.time() - start_time)
        if game_over or time_remaining < 0:
            time_remaining = 0

        denom = max(timer_length, 0.001)
        bar_width = int((time_remaining / denom) * 1000)

        pygame.draw.rect(screen, (200, 190, 180), (100, 120, 1000, 28), border_radius=10)
        pygame.draw.rect(screen, (150, 90, 40), (100, 120, bar_width, 28), border_radius=10)

        if game_over:
            fail_text = word_font.render("MISSION FAILED", True, (200, 60, 60))
            screen.blit(fail_text, (400, 370))

            score_text = ui_font.render("Final score: " + str(score), True, (20, 20, 20))
            screen.blit(score_text, (480, 430))

            restart_text = small_font.render("Press Enter to retry or Esc to quit", True, (20, 20, 20))
            screen.blit(restart_text, (380, 480))
        else:
            # scrambled word box
            pygame.draw.rect(screen, (100, 100, 100), (143, 203, 920, 110), border_radius=12)
            pygame.draw.rect(screen, (230, 220, 210), (140, 200, 920, 110), border_radius=12)
            pygame.draw.rect(screen, (150, 90, 40), (140, 200, 920, 110), 3, border_radius=12)
            scrambled_text = word_font.render(scrambled, True, (20, 20, 20))
            screen.blit(scrambled_text, (500, 230))

            # input box
            pygame.draw.rect(screen, (100, 100, 100), (143, 373, 920, 110), border_radius=12)
            pygame.draw.rect(screen, (230, 220, 210), (140, 370, 920, 110), border_radius=12)
            pygame.draw.rect(screen, (150, 90, 40), (140, 370, 920, 110), 3, border_radius=12)

            user_text = typed if typed != "" else "_"
            input_text = word_font.render(user_text, True, (20, 20, 20))
            screen.blit(input_text, (500, 400))

        # score + time
        score_display = small_font.render("Score: " + str(score), True, (20, 20, 20))
        screen.blit(score_display, (550, 720))

        time_text = "Time: " + str(int(time_remaining)) + "s"
        time_display = small_font.render(time_text, True, (20, 20, 20))
        screen.blit(time_display, (550, 735))

        pygame.display.flip()
=======
        pygame.display.flip()
    pygame.quit()
>>>>>>> ece7a53 (Adjust word spawn band, tweak speeds, reset highscores)
