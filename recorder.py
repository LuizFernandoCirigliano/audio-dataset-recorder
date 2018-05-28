import pyaudio
import wave
import string
import random
import os

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 2
WORDS = ["A", "B", "C", "D", "E", "F", "G"]

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK,
                start=False)

for word in WORDS:
    DIR = "data/train/" + word + "/"
    os.makedirs(DIR, exist_ok=True)
    print("* * * " + word + " * * * ")

    while(True):
        key = input("n: for next word \n" +
                    "x: ends execution \n" +
                    "other key to continue")
        if key == "n":
            break
        elif key == "x":
            stream.close()
            p.terminate()
            exit()

        frames = []
        output_filename = ''.join(random.choices(
            string.ascii_lowercase, k=5)) + ".wav"

        stream.start_stream()

        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)

        stream.stop_stream()

        print("Saving " + DIR + output_filename)
        wf = wave.open(DIR + output_filename, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

    print("* * * Done recording for: " + word + " * * *")

stream.close()
p.terminate()
