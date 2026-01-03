# Pomodoro Clock
    #### Video Demo:  https://youtu.be/wDfzMLFEq8E
    #### Description:

    I've built a pomodoro clock that accepts command line arguments for work time, break time and rounds. I choose to use functions instead of using classes simple because i really can't wrap my head around OOP yet. 
    
    The GUI, built using Tkinter, consists of a main window with 2 buttons and a canvas. Start/Pause and reset. The canvas is where the timer text is. All of these are set to resize and auto-center if the main window gets bigger or smaller. The main window also has a title_label. The label changes text depending on what state the timer is in. Something that I find fun and engaging. It makes the program feel more dynamic. 
    
    Using pygame i've managed to add sound to each phase of the program. The program starts with a work session and playing in the background is some white noise that is continously on loop. When the work session ends and it's time for a break a bell sounds and ocean wave audio keeps playing during the break. When i've done all the rounds a cheering audio starts playing. In order for sounds to be playing simultaneously the continuous sounds (white noise and ocean waves) are played in a different channel. I first tried using simpleaudio for the sound, however it kept crashing because I couldn't get it to play two sounds at once. My code was getting verbose in order to safegaurd against the crash. Finding pygame was so relieving. I wanted to add a tick tock sound as well but I ultimately choose not to. Mainly because it would have interfere with my focus while using this app. Which I am doing while writing this :D.

    All the audio is stored in project/audio. They're royalty free free downloads so I will not get copyright struck. Since pygame is a bit tricky with mp3 files I first converted all the audio to wav using bash script. ffmpeg -i sound.mp3 sound.wav. 

    The reason I chose ton use command line arguments instead of prompting for how long each session should be is because I wanted the program to feel like an internal tool. It just feels faster to directly start the program from the desired state instead of "manually" inputing digits. Basically I included it because it felt cool and it would have been difficult to have a a main function otherwise.

    Overall I'm positively surprised of how versatile TKinter is. Tkinter was used for the GUI, text changing and the countdown logc. I thought I had to use datetime or time for my countdown. However using .after() in a recursive manner actually turned out very well. 

    I'm quite happy with how simple the program is. The app feels very powerful for only 247 lines. During the course I had a tendency of writing very verbose code, something which I tried to rein in during my final project. Although i can probably write more efficient code, I'm very happy with what I've accomplished now. 

    The project mapp contains project.py, test_project.py, scope_of_work.md, project/audio and README.md
    The file that is most interesting is the test_project.py, I learned that since I'm using a lot of global variables that I had to mock them through unittest.mock in the test file for me to able to use pytest. It was a valuable lesson in how much more there is to learn. 


    