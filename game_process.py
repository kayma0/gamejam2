# game_process.py
import pygame
import random


pygame.init()

WORD_LIST = []
with open("words.txt") as f:
    for word_line in f:
        clean = word_line.strip()
        if clean:
            WORD_LIST.append(clean)

WORD_LIST.sort(key=len)

WIDTH = 1200
HEIGHT = 800
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Station X: Typing Racer")
surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
clock = pygame.time.Clock()
fps = 60

ACCENT = (199, 134, 51)
BG = (12, 12, 16)
PANEL = (224, 206, 173)
TEXT_LIGHT = (250, 250, 250)
TEXT_DARK = (20, 20, 20)

def load_background(path):
    try:
        image = pygame.image.load(path).convert()
        return pygame.transform.scale(image, (WIDTH, HEIGHT))
    except Exception:
        return None

BACKGROUND_IMAGE = load_background("media/gamepage.png")

header_font = pygame.font.SysFont("arial", 50, bold=True)
pause_font = pygame.font.SysFont("arial", 38, bold=True)
banner_font = pygame.font.SysFont("arial", 28, bold=True)
font = pygame.font.SysFont("arial", 48, bold=True)

pygame.mixer.init()

def safe_sound(path, volume=0.3):
    try:
        s = pygame.mixer.Sound(path)
        s.set_volume(volume)
        return s
    except Exception:
        return None

try:
    pygame.mixer.music.load("sound/intro_music.mp3")
    pygame.mixer.music.set_volume(0.15)
    pygame.mixer.music.play(-1)
except Exception:
    pass

click = safe_sound("sound/keypress.mp3", 0.25)
woosh = safe_sound("sound/confirm.mp3", 0.25)
wrong = safe_sound("sound/error.mp3", 0.25)

DIFFICULTY_RULES = {
    "easy": {
        "lives": 3,
        "timer_seconds": 60,
        "speed_range": (3, 4),
        "len_filter": (1, 5),  # five letters or less
    },
    "medium": {
        "lives": 2,
        "timer_seconds": 60,
        "speed_range": (3, 5),
        "len_filter": None,  
    },
    "hard": {
        "lives": 0, 
        "timer_seconds": 60,
        "speed_range": (4.5, 6.5),
        "len_filter": None,
    },
}

def filter_words_by_length(bounds):
    if not bounds:
        return WORD_LIST
    lo, hi = bounds
    keep_words = []
    for word in WORD_LIST:
        if lo <= len(word) <= hi:
            keep_words.append(word)
    return keep_words


# keep words sorted 
def build_len_indexes(words_src):
    return sorted(words_src, key=len)

class Word:
    def __init__(self, text, speed, y_pos, x_pos):
        self.text = text
        self.speed = speed
        self.y_pos = y_pos
        self.x_pos = x_pos

    def draw(self, active_string):
        # draw the word and paint part you typed
        screen.blit(font.render(self.text, True, TEXT_LIGHT), (self.x_pos, self.y_pos))
        act_len = len(active_string)
        if active_string == self.text[:act_len]:
            screen.blit(font.render(active_string, True, ACCENT), (self.x_pos, self.y_pos))

    def update(self):
        self.x_pos -= self.speed

class Button:
    def __init__(self, x_pos, y_pos, text, clicked, surf):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.text = text
        self.clicked = clicked
        self.surf = surf

    def draw(self):
        cir = pygame.draw.circle(self.surf, (45, 89, 135), (self.x_pos, self.y_pos), 35)
        if cir.collidepoint(pygame.mouse.get_pos()):
            butts = pygame.mouse.get_pressed()
            if butts[0]:
                pygame.draw.circle(self.surf, (190, 35, 35), (self.x_pos, self.y_pos), 35)
                self.clicked = True
            else:
                pygame.draw.circle(self.surf, (190, 89, 135), (self.x_pos, self.y_pos), 35)
        pygame.draw.circle(self.surf, "white", (self.x_pos, self.y_pos), 35, 3)
        self.surf.blit(pause_font.render(self.text, True, "white"), (self.x_pos - 15, self.y_pos - 25))

def draw_screen(lives, score, active_string, high_score, time_left):
    pygame.draw.rect(screen, PANEL, [0, HEIGHT - 100, WIDTH, 100], 0)
    pygame.draw.rect(screen, ACCENT, [0, 0, WIDTH, HEIGHT], 5)
    pygame.draw.line(screen, ACCENT, (0, HEIGHT - 100), (WIDTH, HEIGHT - 100), 2)
    pygame.draw.line(screen, ACCENT, (WIDTH - 500, HEIGHT - 100), (WIDTH - 500, HEIGHT), 2)

    pause_btn = Button(WIDTH - 52, HEIGHT - 52, "II", False, screen)
    pause_btn.draw()

    screen.blit(banner_font.render(f"Lives: {lives}", True, TEXT_LIGHT), (20, 10))
    screen.blit(banner_font.render(f"Best: {high_score}", True, TEXT_LIGHT), (WIDTH - 300, 10))
    screen.blit(banner_font.render(f"Time: {int(time_left)}s", True, TEXT_LIGHT), (WIDTH // 2 - 80, 10))

    word_box_text = f"\"{active_string}\"" if active_string else ' "" '
    screen.blit(header_font.render(word_box_text, True, TEXT_DARK), (30, HEIGHT - 75))
    screen.blit(header_font.render(f"Score: {score}", True, TEXT_DARK), (WIDTH - 480, HEIGHT - 75))
    return pause_btn.clicked

def draw_pause():
    # make sure the menu does not block the whole screen
    surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
  
    pygame.draw.rect(surface, (0, 0, 0, 180), [0, 0, WIDTH, HEIGHT], 0)
    box_x = 180
    box_y = 140
    box_w = WIDTH - 360
    box_h = 240
    pygame.draw.rect(surface, (0, 0, 0, 140), [box_x, box_y, box_w, box_h], 0, 5)
    pygame.draw.rect(surface, ACCENT + (220,), [box_x, box_y, box_w, box_h], 5, 5)

    surface.blit(header_font.render("MENU", True, TEXT_LIGHT), (box_x + 10, box_y + 10))

    btn_y = box_y + 120
    resume_btn = Button(box_x + 80, btn_y, ">", False, surface)
    resume_btn.draw()

    
    back_btn = Button(box_x + box_w - 120, btn_y, "<", False, surface)
    back_btn.draw()

    surface.blit(header_font.render("PLAY!", True, TEXT_LIGHT), (box_x + 40, btn_y + 60))
    surface.blit(header_font.render("BACK", True, TEXT_LIGHT), (box_x + box_w - 240, btn_y + 60))

    screen.blit(surface, (0, 0))
    return resume_btn.clicked, back_btn.clicked

def generate_level(words_src, speed_range, score):
    word_objs = []
    play_area_top = 150
    play_area_bottom = HEIGHT - 150
    play_area_height = play_area_bottom - play_area_top

    word_count = min(6, 3 + (score // 500))
    speed_factor = 1.0 + (score // 1000) * 0.15

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
    for wrd in list(word_objects):
        if wrd.text == submit:
            points = wrd.speed * len(wrd.text) * 10 * (len(wrd.text) / 4)
            score += int(points)
            word_objects.remove(wrd)
            if woosh:
                woosh.play()
    return score

def check_high_score(score, difficulty="easy"):
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
            resume_butt, back_butt = draw_pause()
            if resume_butt:
                paused = False
            if back_butt:
                check_high_score(score, difficulty)
                return "back"  # ✅ go back to level select

        if new_level and not paused:
            word_objects = generate_level(words_src, speed_range, score)
            new_level = False
        elif not paused:
            for w in list(word_objects):
                w.draw(active_string)
                w.update()
                if w.x_pos < -200:
                    word_objects.remove(w)
                    lives -= 1
            if time_left <= 0:
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
                return "quit"  

            if event.type == pygame.KEYDOWN:
                if not paused:
                    # allow letters numbers and hyphens while typing
                    if len(event.unicode) == 1 and (event.unicode.isalnum() or event.unicode == "-"):
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
            active_string = ""
            submit = ""

        pygame.display.flip()

    return "back"