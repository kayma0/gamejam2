import pygame
import random

pygame.init()
pygame.mixer.init()

# ---------- load words ----------
WORD_LIST = []
with open("words.txt") as f:
    for line in f:
        w = line.strip()
        if w:
            WORD_LIST.append(w)
WORD_LIST.sort(key=len)

# ---------- window ----------
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Station X: Typing Racer")
clock = pygame.time.Clock()
fps = 60

# ---------- colours/fonts ----------
ACCENT = (199, 134, 51)
BG = (12, 12, 16)
PANEL = (224, 206, 173)
TEXT_LIGHT = (250, 250, 250)
TEXT_DARK = (20, 20, 20)

header_font = pygame.font.SysFont("arial", 50, bold=True)
banner_font = pygame.font.SysFont("arial", 28, bold=True)
word_font = pygame.font.SysFont("arial", 48, bold=True)
menu_font = pygame.font.SysFont("arial", 44, bold=True)
small_font = pygame.font.SysFont("arial", 24, bold=True)

# ---------- background ----------
def load_background(path):
    try:
        img = pygame.image.load(path).convert()
        return pygame.transform.scale(img, (WIDTH, HEIGHT))
    except Exception:
        return None

BACKGROUND_IMAGE = load_background("media/gamepage.png")

# ---------- sounds ----------
def safe_sound(path, volume=0.25):
    try:
        s = pygame.mixer.Sound(path)
        s.set_volume(volume)
        return s
    except Exception:
        return None

click = safe_sound("sound/keypress.mp3", 0.25)
woosh = safe_sound("sound/confirm.mp3", 0.25)
wrong = safe_sound("sound/error.mp3", 0.25)

# ---------- difficulty ----------
DIFFICULTY_RULES = {
    "easy":   {"lives": 3, "timer_seconds": 60, "speed_range": (2, 4),   "len_filter": (1, 5)},
    "medium": {"lives": 2, "timer_seconds": 60, "speed_range": (3, 5),   "len_filter": None},
    "hard":   {"lives": 0, "timer_seconds": 60, "speed_range": (4.5, 6.5),"len_filter": None},
}

def filter_words_by_length(bounds):
    if not bounds:
        return WORD_LIST
    lo, hi = bounds
    return [w for w in WORD_LIST if lo <= len(w) <= hi]

# ---------- word object ----------
class Word:
    def __init__(self, text, speed, y, x):
        self.text = text
        self.speed = speed
        self.y = y
        self.x = x

    def draw(self, active_string):
        screen.blit(word_font.render(self.text, True, TEXT_LIGHT), (self.x, self.y))
        typed_len = len(active_string)
        if active_string == self.text[:typed_len]:
            screen.blit(word_font.render(active_string, True, ACCENT), (self.x, self.y))

    def update(self):
        self.x -= self.speed

# ---------- UI drawing ----------
def draw_pause_button():
    # ✅ physical clickable pause button TOP-LEFT
    rect = pygame.Rect(20, 20, 55, 45)
    pygame.draw.rect(screen, (150, 90, 40), rect, border_radius=10)
    pygame.draw.rect(screen, (255, 255, 255), rect, 2, border_radius=10)
    # pause icon
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(rect.x + 16, rect.y + 12, 6, 22))
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(rect.x + 33, rect.y + 12, 6, 22))
    return rect

def draw_hud(lives, score, active_string, high_score, time_left):
    # bottom panel + border
    pygame.draw.rect(screen, PANEL, [0, HEIGHT - 100, WIDTH, 100], 0)
    pygame.draw.rect(screen, ACCENT, [0, 0, WIDTH, HEIGHT], 5)
    pygame.draw.line(screen, ACCENT, (0, HEIGHT - 100), (WIDTH, HEIGHT - 100), 2)
    pygame.draw.line(screen, ACCENT, (WIDTH - 500, HEIGHT - 100), (WIDTH - 500, HEIGHT), 2)

    # top text row
    screen.blit(banner_font.render(f"Lives: {lives}", True, TEXT_LIGHT), (100, 18))
    screen.blit(banner_font.render(f"Best: {high_score}", True, TEXT_LIGHT), (WIDTH - 300, 18))
    screen.blit(banner_font.render(f"Time: {int(time_left)}s", True, TEXT_LIGHT), (WIDTH // 2 - 80, 18))

    # bottom row
    word_box_text = f"\"{active_string}\"" if active_string else ' "" '
    screen.blit(header_font.render(word_box_text, True, TEXT_DARK), (30, HEIGHT - 75))
    screen.blit(header_font.render(f"Score: {score}", True, TEXT_DARK), (WIDTH - 480, HEIGHT - 75))

def draw_pause_menu():
    # overlay
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))

    # box
    box = pygame.Rect(220, 170, WIDTH - 440, 300)
    pygame.draw.rect(screen, (0, 0, 0), box, border_radius=16)
    pygame.draw.rect(screen, ACCENT, box, 4, border_radius=16)

    title = menu_font.render("PAUSED", True, TEXT_LIGHT)
    screen.blit(title, (box.x + 30, box.y + 25))

    # buttons
    resume_rect = pygame.Rect(box.x + 70, box.y + 170, 220, 70)
    back_rect   = pygame.Rect(box.x + box.w - 290, box.y + 170, 220, 70)

    for r, label in [(resume_rect, "RESUME"), (back_rect, "BACK")]:
        pygame.draw.rect(screen, (150, 90, 40), r, border_radius=12)
        pygame.draw.rect(screen, (255, 255, 255), r, 2, border_radius=12)
        t = small_font.render(label, True, (255, 255, 255))
        screen.blit(t, t.get_rect(center=r.center))

    return resume_rect, back_rect

# ---------- gameplay helpers ----------
def generate_level(words_src, speed_range, score):
    objs = []
    play_top = 150
    play_bottom = HEIGHT - 150
    play_h = play_bottom - play_top

    count = min(6, 3 + (score // 500))
    speed_factor = 1.0 + (score // 1000) * 0.15

    spacing = play_h / count
    for i in range(count):
        smin, smax = speed_range
        speed = random.randint(int(smin * speed_factor), int(smax * speed_factor))
        y = int(play_top + (i + 0.5) * spacing)
        x = random.randint(WIDTH, WIDTH + 1000)
        text = random.choice(words_src).lower()
        objs.append(Word(text, speed, y, x))
    return objs

def check_answer(word_objects, submit, score):
    for w in list(word_objects):
        if w.text == submit:
            points = w.speed * len(w.text) * 10 * (len(w.text) / 4)
            score += int(points)
            word_objects.remove(w)
            if woosh:
                woosh.play()
    return score

def check_high_score(score, difficulty="easy"):
    filename = f"high_score_{difficulty}.txt"
    try:
        with open(filename, "r") as f:
            best = int(f.readline().strip() or "0")
    except Exception:
        best = 0

    if score > best:
        try:
            with open(filename, "w") as f:
                f.write(str(int(score)))
        except Exception:
            pass
        best = score
    return best

# ---------- main game ----------
def run_game(difficulty="easy"):
    rules = DIFFICULTY_RULES.get(difficulty, DIFFICULTY_RULES["easy"])
    lives = rules["lives"]
    timer_limit = rules["timer_seconds"]
    speed_range = rules["speed_range"]

    words_src = filter_words_by_length(rules["len_filter"]) or WORD_LIST

    word_objects = []
    high_score = check_high_score(0, difficulty)

    paused = False
    new_level = True

    submit = ""
    active_string = ""
    score = 0
    time_left = float(timer_limit)

    while True:
        dt = clock.tick(fps) / 1000.0

        # background
        if BACKGROUND_IMAGE:
            screen.blit(BACKGROUND_IMAGE, (0, 0))
        else:
            screen.fill(BG)

        # pause button always drawn
        pause_rect = draw_pause_button()

        # timer only counts down if not paused
        if not paused and time_left > 0:
            time_left = max(0, time_left - dt)

        # HUD always drawn
        draw_hud(lives, score, active_string, high_score, time_left)

        # menu if paused
        resume_rect = back_rect = None
        if paused:
            resume_rect, back_rect = draw_pause_menu()

        # gameplay only if not paused
        if not paused:
            if new_level:
                word_objects = generate_level(words_src, speed_range, score)
                new_level = False

            for w in list(word_objects):
                w.draw(active_string)
                w.update()
                if w.x < -200:
                    word_objects.remove(w)
                    lives -= 1

            if len(word_objects) == 0:
                new_level = True

            if submit:
                before = score
                score = check_answer(word_objects, submit, score)
                submit = ""
                if before == score and wrong:
                    wrong.play()

        # ✅ game over -> let typing_game.py play video/audio screen
        if lives < 0 or time_left <= 0:
            check_high_score(score, difficulty)
            return "game_over"

        # events (clicks handled here, not in draw functions)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                check_high_score(score, difficulty)
                return "quit"

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # click pause button
                if pause_rect.collidepoint(event.pos):
                    paused = True

                # click menu buttons (only if paused)
                if paused and resume_rect and resume_rect.collidepoint(event.pos):
                    paused = False
                if paused and back_rect and back_rect.collidepoint(event.pos):
                    check_high_score(score, difficulty)
                    return "back"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = not paused

                if not paused:
                    if len(event.unicode) == 1 and (event.unicode.isalnum() or event.unicode == "-"):
                        active_string += event.unicode
                        if click:
                            click.play()

                    if event.key == pygame.K_BACKSPACE and len(active_string) > 0:
                        active_string = active_string[:-1]

                    if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        submit = active_string
                        active_string = ""

        pygame.display.flip()