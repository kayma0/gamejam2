import random
import time
import pygame
from create_words import words

# game settings
lives = 3
timer_start = 7.0
timer_min = 2.5
timer_drop = 0.3
points = 10
width = 1200
height = 800

# scramble the word
def mix(word):
	letters = list(word)
	random.shuffle(letters)
	return "".join(letters)

# pick a word
def pick_word(words, round_num):
	return random.choice(words)


def run_game():
	pygame.init()
	screen = pygame.display.set_mode((width, height))
	pygame.display.set_caption("Station X: Codebreak")
	clock = pygame.time.Clock()

	title_font = pygame.font.SysFont("arial", 56, bold=True)
	word_font = pygame.font.SysFont("arial", 52, bold=True)
	label_font = pygame.font.SysFont("arial", 32)
	ui_font = pygame.font.SysFont("arial", 28)
	small_font = pygame.font.SysFont("arial", 22)

	player_lives = lives
	score = 0
	timer_length = timer_start
	typed = ""
	rounds = 0
	
	word = pick_word(words, rounds)
	scrambled = mix(word)
	start_time = time.time()
	game_over = False
	run = True
	
	while run:
		clock.tick(60)
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					run = False
					
				if game_over:
					if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
						player_lives = lives
						score = 0
						timer_length = timer_start
						typed = ""
						rounds = 0
						word = pick_word(words, rounds)
						scrambled = mix(word)
						start_time = time.time()
						game_over = False
				else:
					if event.key == pygame.K_BACKSPACE:
						if len(typed) > 0:
							typed = typed[:-1]
					elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
						if typed.lower() == word:
							score = score + (len(word) * points)
							rounds = rounds + 1
							timer_length = timer_length - timer_drop
							if timer_length < timer_min:
								timer_length = timer_min
							word = pick_word(words, rounds)
							scrambled = mix(word)
							start_time = time.time()
							typed = ""
						else:
							player_lives = player_lives - 1
							rounds = rounds + 1
							timer_length = timer_length - timer_drop
							if timer_length < timer_min:
								timer_length = timer_min
							word = pick_word(words, rounds)
							scrambled = mix(word)
							start_time = time.time()
							typed = ""
					elif event.unicode.isalpha():
						typed = typed + event.unicode.lower()

		if not game_over:
			time_passed = time.time() - start_time
			time_left = timer_length - time_passed
			
			if time_left <= 0:
				player_lives = player_lives - 1
				rounds = rounds + 1
				timer_length = timer_length - timer_drop
				if timer_length < timer_min:
					timer_length = timer_min
				word = pick_word(words, rounds)
				scrambled = mix(word)
				start_time = time.time()
				typed = ""

			if player_lives <= 0:
				game_over = True

		screen.fill((245, 242, 235))
		
		# draw lives
		lives_text = label_font.render("Lives:", True, (20, 20, 20))
		screen.blit(lives_text, (40, 750))
		for i in range(player_lives):
			pygame.draw.circle(screen, (150, 90, 40), (130 + i * 26, 762), 12)

		# draw title box
		pygame.draw.rect(screen, (200, 180, 165), (60, 40, 1080, 90), border_radius=14)
		pygame.draw.rect(screen, (150, 90, 40), (60, 40, 1080, 90), 3, border_radius=14)
		title = title_font.render("Station X: Scrambled Files", True, (150, 90, 40))
		screen.blit(title, (300, 60))

		# draw timer bar
		time_remaining = timer_length - (time.time() - start_time)
		if game_over:
			time_remaining = 0
		if time_remaining < 0:
			time_remaining = 0
		bar_width = int((time_remaining / timer_length) * 1000)
		pygame.draw.rect(screen, (200, 190, 180), (100, 120, 1000, 28), border_radius=10)
		pygame.draw.rect(screen, (150, 90, 40), (100, 120, bar_width, 28), border_radius=10)

		if game_over:
			# show game over
			fail_text = word_font.render("MISSION FAILED", True, (200, 60, 60))
			screen.blit(fail_text, (400, 370))
			
			score_text = ui_font.render("Final score: " + str(score), True, (20, 20, 20))
			screen.blit(score_text, (480, 430))
			
			restart_text = small_font.render("Press Enter to retry or Esc to quit", True, (20, 20, 20))
			screen.blit(restart_text, (380, 480))
		else:
			# draw scrambled word box
			pygame.draw.rect(screen, (100, 100, 100), (143, 203, 920, 110), border_radius=12)
			pygame.draw.rect(screen, (230, 220, 210), (140, 200, 920, 110), border_radius=12)
			pygame.draw.rect(screen, (150, 90, 40), (140, 200, 920, 110), 3, border_radius=12)
			scrambled_text = word_font.render(scrambled, True, (20, 20, 20))
			screen.blit(scrambled_text, (500, 230))

			# draw input box
			pygame.draw.rect(screen, (100, 100, 100), (143, 373, 920, 110), border_radius=12)
			pygame.draw.rect(screen, (230, 220, 210), (140, 370, 920, 110), border_radius=12)
			pygame.draw.rect(screen, (150, 90, 40), (140, 370, 920, 110), 3, border_radius=12)
			
			user_text = typed
			if user_text == "":
				user_text = "_"
			input_text = word_font.render(user_text, True, (20, 20, 20))
			screen.blit(input_text, (500, 400))

		# draw score and time
		score_display = small_font.render("Score: " + str(score), True, (20, 20, 20))
		screen.blit(score_display, (550, 720))
		
		time_text = "Time: " + str(int(time_remaining)) + "s"
		time_display = small_font.render(time_text, True, (20, 20, 20))
		screen.blit(time_display, (550, 735))

		pygame.display.flip()
