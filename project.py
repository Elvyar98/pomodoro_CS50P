from tkinter import *
import math
import sys
import pygame

# Colours
GREEN = "#8A9A5B"
BROWN = "#7B3F00"
YELLOW = "#FFCE1B"
BLUE = "#0080FF"
RED = "#FF0000"

# Sounds
pygame.mixer.init()

cheering = pygame.mixer.Sound("audio/cheering.wav")
sofia = pygame.mixer.Sound("audio/cheering.wav")
bell = pygame.mixer.Sound("audio/bell.wav")
gong = pygame.mixer.Sound("audio/gong.wav")
beach = pygame.mixer.Sound("audio/beach.wav")
white_noise = pygame.mixer.Sound("audio/white_noise.wav")

focus_channel = pygame.mixer.Channel(1)

# Constants
WORK_MIN: float = 0
BREAK: float = 0
ROUNDS: float = 0

REPS: int = 0
TIMER = None
STATE = False  # True = work False = break
IS_PAUSED = False
PAUSED_TIME = 0


# play
def play_sound(sound):
    sound.play()


# sound during work and rest
def play_focus():
    if STATE:
        focus_channel.play(white_noise, loops=-1)
    else:
        focus_channel.play(beach, loops=-1)


# stop
def stop_focus():
    focus_channel.stop()


# Countdown
def count_down(count):
    global TIMER, IS_PAUSED, PAUSED_TIME

    min_sec = f"{math.floor(count / 60)}:{int(count % 60):02}"
    canvas.itemconfig(timer_text, text=min_sec)

    if count > 0:
        PAUSED_TIME = count
        TIMER = root.after(1000, count_down, count - 1)
    else:
        TIMER = None
        IS_PAUSED = False
        start_button.config(text="Start", fg=BLUE)
        start_timer()


# Start/Pause/Resume timer
def toggle_timer():
    global TIMER, IS_PAUSED, PAUSED_TIME

    if TIMER is None and not IS_PAUSED:
        start_timer()
        start_button.config(text="Pause", fg=RED)
    elif TIMER is not None and not IS_PAUSED:
        root.after_cancel(TIMER)
        TIMER = None
        IS_PAUSED = True
        start_button.config(text="Resume", fg=GREEN)
        stop_focus()

        if STATE:
            title_label.config(text="Work - PAUSED", fg=RED)
        else:
            title_label.config(text="Break - PAUSED", fg=RED)
    elif IS_PAUSED:
        IS_PAUSED = False
        start_button.config(text="Pause", fg=RED)

        if STATE:
            title_label.config(text="Time to lock in big dawg", fg=BROWN)
        else:
            title_label.config(text="You deserve a break big guy", fg=YELLOW)

        play_focus()
        count_down(PAUSED_TIME)


# Start timer
def start_timer():
    global REPS, STATE, PAUSED_TIME

    if TIMER is not None:
        return

    REPS += 1
    work_sec: float = WORK_MIN * 60
    break_sec: float = BREAK * 60

    if math.floor(REPS / 2) == ROUNDS:
        stop_focus()
        play_sound(cheering)  # cheering
        play_sound(sofia)  # audio
        title_label.config(text=f"Good Boy!\n You completed {ROUNDS}/{ROUNDS} Rounds")
        start_button.config(text="Start", fg=BLUE)
        return

    elif REPS % 2 == 0:
        STATE = False
        stop_focus()
        play_sound(bell)
        play_focus()
        title_label.config(text="You deserve a break big guy", fg=YELLOW)
        PAUSED_TIME = break_sec
        count_down(break_sec)

    else:
        STATE = True
        stop_focus()
        play_sound(gong)
        play_focus()
        title_label.config(text="Time to lock in big dawg", fg=BROWN)
        rounds_label.config(text=f"Round {math.floor(REPS/2)+1}/{ROUNDS}")
        PAUSED_TIME = work_sec
        count_down(work_sec)


# Reset timer
def reset_timer():
    global REPS, TIMER, IS_PAUSED, PAUSED_TIME

    if TIMER is not None:
        root.after_cancel(TIMER)
        TIMER = None

    IS_PAUSED = False
    PAUSED_TIME = 0

    canvas.itemconfig(timer_text, text="00:00")
    title_label.config(text="Timer", fg=BROWN)
    rounds_label.config(text="")
    start_button.config(text="Start", fg=BLUE)  # Reset button text

    REPS = 0
    stop_focus()


def main():
    global WORK_MIN, BREAK, ROUNDS

    if len(sys.argv) >= 4:
        WORK_MIN = float(sys.argv[1])
        BREAK = float(sys.argv[2])
        ROUNDS = float(sys.argv[3])

    else:
        WORK_MIN = 50
        BREAK = 10
        ROUNDS = 4


if __name__ == "__main__":
    main()


# Graphic User Interface
root = Tk()
root.title("Pomodoro Elvis Edition")
root.config(bg=GREEN)

# Let the window expand
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

# Main container
mainframe = Frame(root, bg=GREEN)
mainframe.grid(row=0, column=0, sticky="nsew")

# Grid structure
for c in range(3):
    mainframe.columnconfigure(c, weight=1)
for r in range(4):
    mainframe.rowconfigure(r, weight=1)

# Title
title_label = Label(mainframe, text="Pomodoro", fg=BROWN, bg=GREEN, font=("Times", 20))
title_label.grid(row=0, column=1)

# Canvas (square, auto-scaling)
canvas = Canvas(mainframe, bg=GREEN, highlightthickness=0)
canvas.grid(row=1, column=1, sticky="nsew")

# Timer text (position updated dynamically)
timer_text = canvas.create_text(
    0, 0, text="00:00", fill="white", font=("Helvetica", 35, "bold")
)

# Buttons
start_button = Button(
    mainframe,
    text="Start",
    command=toggle_timer,
    fg=BLUE,
    bg=GREEN,
    highlightthickness=0,
)
start_button.grid(row=2, column=0, sticky="e", padx=10)

reset_button = Button(
    mainframe,
    text="Reset",
    command=reset_timer,
    fg=BROWN,
    bg=GREEN,
    highlightthickness=0,
)
reset_button.grid(row=2, column=2, sticky="w", padx=10)

# Rounds label
rounds_label = Label(mainframe, fg=YELLOW, bg=GREEN)
rounds_label.grid(row=3, column=1)


# ---------------- Canvas Resize Logic ----------------
def resize_canvas(event):
    size = min(event.width, event.height)
    canvas.config(width=size, height=size)
    canvas.coords(timer_text, size // 2, size // 2)


canvas.bind("<Configure>", resize_canvas)

root.mainloop()
