import datetime
import time
import os
import pyaudio
import wave
import sys

class AudioFile:
    chunk = 1024

    def __init__(self, file):
        """ Init audio stream """ 
        self.wf = wave.open(file, 'rb')
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format = self.p.get_format_from_width(self.wf.getsampwidth()),
            channels = self.wf.getnchannels(),
            rate = self.wf.getframerate(),
            output = True
        )

    def play(self):
        """ Play entire file """
        data = self.wf.readframes(self.chunk)
        while data != '':
            self.stream.write(data)
            data = self.wf.readframes(self.chunk)

            if data == b'':
                break

    def close(self):
        """ Graceful shutdown """ 
        self.stream.close()
        self.p.terminate()

on_break = False

break_time = 5 # in minutes

# ask for number of minutes to work
sessions = int(input("How many sessions do you want to work? "))

# convert the minutes into seconds
#time_left = 25 * 60 * sessions
#time_completed = 0
active_timer = 25 * 60

dir_path = os.path.dirname(os.path.realpath(__file__))
dir_path = os.path.join(dir_path, "audio")

print("starting...")

a = AudioFile(os.path.join(dir_path, "start.wav"))
a.play()
a.close()

print("now!")

while sessions > 0:

    if on_break:
        sys.stdout.write(f"[BREAK] {datetime.timedelta(seconds=active_timer)} time left, sessions left {sessions}\r")
        sys.stdout.flush()

        if active_timer <= 0:
            # Usage example for pyaudio
            
            a = AudioFile(os.path.join(dir_path, "start.wav"))
            a.play()
            a.close()

            on_break = False

            # break time
            active_timer = 25 * 60

            sessions -= 1
        
    else:
        
        #print(time_left,flush=True)
        sys.stdout.write(f"[WORK] {datetime.timedelta(seconds=active_timer)} time left, sessions left {sessions}\r")
        sys.stdout.flush()

        if active_timer <= 0:
            # Usage example for pyaudio
            
            a = AudioFile(os.path.join(dir_path, "stop.wav"))
            a.play()
            a.close()

            on_break = True
            #print("break time!")

            # break time
            active_timer = break_time * 60

    
    active_timer -= 1
    time.sleep(1)

print("session finished!")