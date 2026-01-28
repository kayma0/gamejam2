# gamejam2

This is a typing game based on the Bletchley Park women codebreakers in the UK during World War Two, created for GameJam using Python with Pygame and OpenCV. The player types radio code words under a time limit to stop a bomb.

In this game you type letters and numbers to match moving words on screen and then press space or enter to submit the word. A correct word increases the score and removes that word while wrong or missed words reduce the number of lives as the timer continues to count down. When time or lives reach zero a fail video plays, and if the mission ends with points still on the board a success video plays instead. The mouse is used for Begin, Continue, difficulty selection, Pause, Resume, Back and Logbook, and pressing Escape or clicking the pause button opens a pause menu that temporarily stops the timer.

The code is split into two main Python files. One file manages the screens of the game and it starts the typing part once a difficulty has been chosen. The other file manages the actual game which means updating moving word objects, handling the number of lives, timer, score and pause menu.

References
Typing game and input
https://github.com/plemaster01/PythonTypingRacer/blob/main/typingRacer.py#L28
https://www.youtube.com/watch?v=3RDMRpUHFBE

Text colour while typing
https://stackoverflow.com/questions/43531695/how-can-you-change-the-colour-of-text-in-pygame-on-keypress

Buttons, UI, lives and timers
https://thepythoncode.com/article/make-a-button-using-pygame-in-python
https://www.youtube.com/watch?v=muooVha_gps
https://quirkycort.github.io/tutorials/20-Pygame-Zero-Basics/35-Grab/90-timer.html
