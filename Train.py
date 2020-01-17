'''
import sounddevice as sd
from scipy.io.wavfile import write
import matplotlib.pyplot as plt

fs = 44100  # Sample rate
seconds = 3  # Duration of recording

myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
sd.wait()  # Wait until recording is finished

write('output.wav', fs, myrecording)  # Save as WAV file 

print(type(myrecording))
print(myrecording)
plt.plot(myrecording)
plt.show()
'''
import pyaudio
import wave
import statistics
from statistics import mean
import time


def BToD(data): 
    tab =[]
    for d in data :
        tab.append(d)
    return mean(tab)

chunk = 1024  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 2
fs = 44100  # Record at 44100 samples per second
seconds = 2
filename = "output.wav"

p = pyaudio.PyAudio()  # Create an interface to PortAudio
fichier = open("stop.txt", "a")

for i in range(10):
    print('Recording')
    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)
    frames = []  # Initialize array to store frames
    dt=[]
    # Store data in chunks for 3 seconds
    for i in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk)
        dt.append(BToD(data))
        frames.append(data)

    fichier.write(str(dt)+"\n")
    print('Finished recording')
    time.sleep(2)

print("terminée")
# Stop and close the stream 
stream.stop_stream()
stream.close()
# Terminate the PortAudio interface
p.terminate()

# Save the recorded data as a WAV file
wf = wave.open(filename, 'wb')
wf.setnchannels(channels)
wf.setsampwidth(p.get_sample_size(sample_format))
wf.setframerate(fs)
wf.writeframes(b''.join(frames))
wf.close()

fichier.close()



