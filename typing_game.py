#import necessary modules
import copy
import random
import pygame
import cv2

pygame.init()

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
    screen.blit(surf, (0, 0))
    pygame.display.flip()
    
    # Handle quit event during video
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing_video = False
            running = False
    
    timer.tick(fps_video)

video.release()

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

