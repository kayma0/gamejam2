#import necessary modules
import copy
import random
import pygame
import cv2

pygame.init()
pygame.mixer.init()

#load and play bgmusic
pygame.mixer.music.load("sound/intro_music.mp3")
pygame.mixer.music.set_volume(0.25)
pygame.mixer.music.play(0)

#load word list from file
with open("words.txt") as f:
    wordList = [w.strip() for w in f.readlines()]

len_indexes = []
length = 1
wordList.sort(key=len)
intro_vid = "intro.mp4"
outro_vid = "outro.mp4" 

for i in range(len(wordList)):
    if len(wordList[i]) > length:
        len_indexes.append(i)
        length  += 1

len_indexes.append(len(wordList))

#screen dimensions
WIDTH = 1200
HEIGHT = 800
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Station X: Scrambled Files')
surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
timer = pygame.time.Clock()
fps = 60
score = 0

# Play intro video
video = cv2.VideoCapture(intro_vid)
video_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
video_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps_video = video.get(cv2.CAP_PROP_FPS)

last_frame = None
playing_video = True
while playing_video:
    ret, frame = video.read()
    if not ret:
        playing_video = False
        break
    
    # Convert frame to pygame surface
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
    
    # Scale to fit screen
    surf = pygame.transform.scale(frame, (WIDTH, HEIGHT))
    last_frame = surf 
    screen.blit(surf, (0, 0))
    pygame.display.flip()
    
    # Handle quit event during video
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing_video = False
            running = False
    
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
    
    # Draw last frame of intro video
    if last_frame:
        screen.blit(last_frame, (0, 0))
    else:
        screen.fill((0, 0, 0))
    
    # Draw button
    pygame.draw.rect(screen, (150, 90, 40), button_rect, border_radius=12)
    pygame.draw.rect(screen, (255, 255, 255), button_rect, 2, border_radius=12)
    text = font.render("BEGIN", True, (0, 0, 0))
    text_rect = text.get_rect(center=button_rect.center)
    screen.blit(text, text_rect)
    
    pygame.display.flip() #basically updates the screen
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            begin_screen = False
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                button_clicked = True
                begin_screen = False

# Play outro video if button was clicked
if button_clicked:
    video = cv2.VideoCapture(outro_vid)
    fps_video = video.get(cv2.CAP_PROP_FPS)
    
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
                playing_video = False
        
        timer.tick(fps_video)
    
    video.release()

    # Load and display instructions image with continue button
    instructions_img = pygame.image.load("instructions.png")
    instructions_img = pygame.transform.scale(instructions_img, (WIDTH, HEIGHT))
    
    # Continue button setup
    continue_button_width = 220
    continue_button_height = 60
    continue_button_x = WIDTH - continue_button_width - 40  # bottom right
    continue_button_y = HEIGHT - continue_button_height - 40
    continue_button_rect = pygame.Rect(continue_button_x, continue_button_y, continue_button_width, continue_button_height)
    
    waiting_for_input = True
    while waiting_for_input:
        timer.tick(fps)
        
        screen.blit(instructions_img, (0, 0))
        
        # Draw continue button
        pygame.draw.rect(screen, (150, 90, 40), continue_button_rect, border_radius=12)
        pygame.draw.rect(screen, (255, 255, 255), continue_button_rect, 2, border_radius=12)
        text = font.render("CONTINUE", True, (255, 255, 255))
        text_rect = text.get_rect(center=continue_button_rect.center)
        screen.blit(text, text_rect)
        
        pygame.display.flip()

         # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting_for_input = False
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if continue_button_rect.collidepoint(event.pos):
                    waiting_for_input = False

# Main game loop
running = True
while running:
    timer.tick(fps)
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    pygame.display.flip()


#ends game properly
pygame.quit()

