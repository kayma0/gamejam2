import pygame
import cv2

from game_process import run_game


# ---------- shared UI helpers ----------
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


# ---------- NEW: LOGBOOK POPUP ----------
def logbook_popup(screen, clock, WIDTH, HEIGHT, bg_surface):
    title_font = pygame.font.SysFont("arial", 44, bold=True)
    body_font = pygame.font.SysFont("arial", 26)
    btn_font = pygame.font.SysFont("arial", 28, bold=True)

    box_w, box_h = 760, 330
    box = pygame.Rect((WIDTH - box_w) // 2, (HEIGHT - box_h) // 2, box_w, box_h)

    open_rect = pygame.Rect(box.x + 70, box.bottom - 85, 220, 60)
    close_rect = pygame.Rect(box.right - 290, box.bottom - 85, 220, 60)

    while True:
        clock.tick(60)

        screen.blit(bg_surface, (0, 0))

        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        screen.blit(overlay, (0, 0))

        pygame.draw.rect(screen, (240, 229, 210), box, border_radius=18)
        pygame.draw.rect(screen, (150, 90, 40), box, 4, border_radius=18)

        screen.blit(title_font.render("LOGBOOK FOUND!", True, (20, 20, 20)), (box.x + 30, box.y + 30))

        lines = [
            "Dearest Recruit, this is your Logbook!",
            "It stores clues!",
            "Do you want to open it now?",
        ]
        y = box.y + 115
        for line in lines:
            screen.blit(body_font.render(line, True, (35, 35, 35)), (box.x + 30, y))
            y += 38

        pygame.draw.rect(screen, (150, 90, 40), open_rect, border_radius=12)
        pygame.draw.rect(screen, (255, 255, 255), open_rect, 2, border_radius=12)
        open_txt = btn_font.render("OPEN", True, (255, 255, 255))
        screen.blit(open_txt, open_txt.get_rect(center=open_rect.center))

        pygame.draw.rect(screen, (80, 80, 80), close_rect, border_radius=12)
        pygame.draw.rect(screen, (255, 255, 255), close_rect, 2, border_radius=12)
        close_txt = btn_font.render("CLOSE", True, (255, 255, 255))
        screen.blit(close_txt, close_txt.get_rect(center=close_rect.center))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "close"
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if open_rect.collidepoint(event.pos):
                    return "open"
                if close_rect.collidepoint(event.pos) or (not box.collidepoint(event.pos)):
                    return "close"


def end_video_screen(screen, clock, WIDTH, HEIGHT, video_path, audio_path):
    try:
        pygame.mixer.music.stop()
    except Exception:
        pass

    end_snd = None
    try:
        end_snd = pygame.mixer.Sound(audio_path)
        end_snd.play()
    except Exception:
        end_snd = None

    last_frame = play_video(screen, clock, video_path, WIDTH, HEIGHT)
    if last_frame is None:
        return "quit"

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
    continue_button_rect = pygame.Rect(continue_button_x, continue_button_y, continue_button_width, continue_button_height)

    top_right_rect = pygame.Rect(WIDTH - 250, 20, 200, 200)

    while True:
        clock.tick(60)
        screen.blit(instructions_img, (0, 0))

        mx, my = pygame.mouse.get_pos()

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
                    bg = screen.copy()
                    pop = logbook_popup(screen, clock, WIDTH, HEIGHT, bg)
                    if pop == "quit":
                        return "quit"
                    if pop == "open":
                        return "logbook"
                    continue
                if continue_button_rect.collidepoint(event.pos):
                    return "next"


def logbook_screen(screen, clock, WIDTH, HEIGHT, return_to="levels"):
    bg = pygame.image.load("media/logbook.png").convert()
    bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

    font = pygame.font.SysFont("arial", 26, bold=True)
    small_font = pygame.font.SysFont("arial", 22, bold=True)
    title_font = pygame.font.SysFont("arial", 34, bold=True)

    # ---------- LOAD WORD FILE (build a dictionary) ----------
    # expects lines like: word - definition  (or word: definition)
    word_map = {}
    entries = []

    with open("words2.txt", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line:
                continue

            # try split on " - " first, then ":" as backup
            if " — " in line:                 # em dash (long dash)
               w, d = line.split(" — ", 1)
            elif " - " in line:
                w, d = line.split(" - ", 1)
            elif ":" in line:
                w, d = line.split(":", 1)
            else:
                # if the line has no definition format, keep it in list anyway
                w, d = line, ""

            w_clean = w.strip().lower()
            d_clean = d.strip()

            entries.append(line)
            if w_clean and d_clean:
                word_map[w_clean] = d_clean

    # ---------- paging ----------
    PER_PAGE = 12
    page = 0
    total_pages = (len(entries) - 1) // PER_PAGE + 1 if entries else 1

    # ---------- center panel layout ----------
    panel_w = 900
    panel_h = 560
    panel = pygame.Rect((WIDTH - panel_w) // 2, (HEIGHT - panel_h) // 2, panel_w, panel_h)

    # ---------- SEARCH UI ----------
    search_rect = pygame.Rect(panel.x + 110, panel.y + 35, panel.w - 220, 48)
    search_active = False
    query = ""

    # result overlay state
    showing_result = False
    result_word = ""
    result_def = ""
    result_not_found = False

    # helper: wrap text to fit width
    def wrap_text(text, max_width, use_font):
        words = text.split()
        lines = []
        current = ""
        for w in words:
            test = (current + " " + w).strip()
            if use_font.size(test)[0] <= max_width:
                current = test
            else:
                if current:
                    lines.append(current)
                current = w
        if current:
            lines.append(current)
        return lines

    while True:
        clock.tick(60)
        screen.blit(bg, (0, 0))

        back_rect = draw_back_button(screen, WIDTH)

        # ---------- draw SEARCH BAR ----------
        # box
        pygame.draw.rect(screen, (245, 238, 225), search_rect, border_radius=10)
        pygame.draw.rect(
            screen,
            (150, 90, 40) if search_active else (180, 160, 140),
            search_rect,
            3,
            border_radius=10,
        )

        # label = title_font.render("Search", True, (40, 40, 40))
        # screen.blit(label, (search_rect.x - 95, search_rect.y + 8))

        # text inside bar
        shown = query if query else "SEARCH! Type a word and press Enter..."
        colour = (20, 20, 20) if query else (120, 120, 120)
        txt = small_font.render(shown, True, colour)
        screen.blit(txt, (search_rect.x + 12, search_rect.y + 12))

        # ---------- normal page list ----------
        start = page * PER_PAGE
        end = start + PER_PAGE
        visible = entries[start:end]

        y = panel.y + 120
        for line in visible:
            t = font.render(line, True, (25, 25, 25))
            screen.blit(t, t.get_rect(center=(WIDTH // 2, y)))
            y += 38

        # ---------- page number ----------
        page_text = small_font.render(f"{page + 1}/{total_pages}", True, (60, 60, 60))
        screen.blit(page_text, page_text.get_rect(center=(WIDTH // 2, panel.bottom + 25)))

        # ---------- buttons ----------

        prev_rect = pygame.Rect(panel.x + 40, panel.bottom + 3, 90, 45)
        next_rect = pygame.Rect(panel.right - 160, panel.bottom + 3, 90, 45)

        for rect, label_txt in [(prev_rect, "< Prev"), (next_rect, "Next >")]:
            pygame.draw.rect(screen, (150, 90, 40), rect, border_radius=10)
            pygame.draw.rect(screen, (255, 255, 255), rect, 2, border_radius=10)
            t = small_font.render(label_txt, True, (255, 255, 255))
            screen.blit(t, t.get_rect(center=rect.center))

        # ---------- RESULT POPUP (on top) ----------
        if showing_result:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            screen.blit(overlay, (0, 0))

            box_w, box_h = 880, 360
            box = pygame.Rect((WIDTH - box_w) // 2, (HEIGHT - box_h) // 2, box_w, box_h)

            pygame.draw.rect(screen, (245, 238, 225), box, border_radius=18)
            pygame.draw.rect(screen, (150, 90, 40), box, 4, border_radius=18)

            if result_not_found:
                title = title_font.render("Not found", True, (40, 40, 40))
                screen.blit(title, title.get_rect(center=(WIDTH // 2, box.y + 60)))

                msg = small_font.render("Try a different spelling!", True, (60, 60, 60))
                screen.blit(msg, msg.get_rect(center=(WIDTH // 2, box.y + 120)))
            else:
                title = title_font.render(result_word.upper(), True, (40, 40, 40))
                screen.blit(title, title.get_rect(center=(WIDTH // 2, box.y + 55)))

                wrapped = wrap_text(result_def, box.w - 80, small_font)
                y2 = box.y + 120
                for line in wrapped[:6]:  # keep it neat
                    line_surf = small_font.render(line, True, (25, 25, 25))
                    screen.blit(line_surf, line_surf.get_rect(center=(WIDTH // 2, y2)))
                    y2 += 34

            close_rect = pygame.Rect(box.centerx - 100, box.bottom - 80, 200, 55)
            pygame.draw.rect(screen, (150, 90, 40), close_rect, border_radius=12)
            pygame.draw.rect(screen, (255, 255, 255), close_rect, 2, border_radius=12)
            c = small_font.render("CLOSE", True, (255, 255, 255))
            screen.blit(c, c.get_rect(center=close_rect.center))

        pygame.display.flip()

        # ---------- events ----------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(event.pos):
                    return return_to

                # if popup showing, only allow closing it
                if showing_result:
                    if close_rect.collidepoint(event.pos):
                        showing_result = False
                    continue

                # click search bar to focus
                if search_rect.collidepoint(event.pos):
                    search_active = True
                else:
                    search_active = False

                if prev_rect.collidepoint(event.pos):
                    page = max(0, page - 1)

                if next_rect.collidepoint(event.pos):
                    page = min(total_pages - 1, page + 1)

            if event.type == pygame.KEYDOWN:
                # close popup with ESC
                if showing_result and event.key == pygame.K_ESCAPE:
                    showing_result = False
                    continue

                # typing into search
                if search_active:
                    if event.key == pygame.K_RETURN:
                        q = query.strip().lower()
                        if q:
                            if q in word_map:
                                result_word = q
                                result_def = word_map[q]
                                result_not_found = False
                            else:
                                result_word = q
                                result_def = ""
                                result_not_found = True
                            showing_result = True
                        search_active = False

                    elif event.key == pygame.K_BACKSPACE:
                        query = query[:-1]

                    elif event.key == pygame.K_ESCAPE:
                        search_active = False

                    else:
                        if len(event.unicode) == 1:
                            # allow letters/numbers/hyphen only
                            ch = event.unicode
                            if ch.isalnum() or ch in "-":
                                query += ch


def level_select(screen, clock, WIDTH, HEIGHT):
    levels_img = pygame.image.load("media/levels.png").convert()
    levels_img = pygame.transform.scale(levels_img, (WIDTH, HEIGHT))

    top_right_rect = pygame.Rect(WIDTH - 250, 20, 200, 200)

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

        back_rect = draw_back_button(screen, WIDTH)

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

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if back_rect.collidepoint(event.pos):
                    return "back"

                if top_right_rect.collidepoint(event.pos):
                    bg = screen.copy()
                    pop = logbook_popup(screen, clock, WIDTH, HEIGHT, bg)
                    if pop == "quit":
                        return "quit"
                    if pop == "open":
                        return "logbook"
                    continue

                pos = event.pos
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

        end_frame = play_video(screen, clock, outro_vid, WIDTH, HEIGHT)
        if end_frame is None:
            break

        ins = instructions_screen(screen, clock, WIDTH, HEIGHT)
        if ins == "quit":
            break

        if ins == "logbook":
            lb = logbook_screen(screen, clock, WIDTH, HEIGHT, return_to="levels")
            if lb == "quit":
                break
            ins = "next"

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
                    break
                continue

            if diff == "logbook":
                lb2 = logbook_screen(screen, clock, WIDTH, HEIGHT)
                if lb2 == "quit":
                    pygame.quit()
                    return
                continue

            result = run_game(diff)  # "back" | "quit" | "game_over" | "level_complete"

            if result == "quit":
                pygame.quit()
                return

            if result == "back":
                continue

            if result == "game_over":
                end = end_video_screen(screen, clock, WIDTH, HEIGHT, fail_vid, fail_audio)
                if end == "quit":
                    pygame.quit()
                    return
                continue

            if result == "level_complete":
                end = end_video_screen(screen, clock, WIDTH, HEIGHT, success_vid, success_audio)
                if end == "quit":
                    pygame.quit()
                    return
                continue

    pygame.quit()


if __name__ == "__main__":
    main()