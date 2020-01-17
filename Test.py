from sklearn import svm
import pandas as pd
import pyaudio
import wave
import statistics
from statistics import mean
import sys

def BToD(data): 
    tab =[]
    for d in data :
        tab.append(d)
    return mean(tab)

def lire(lien,output): 
    #convert string to list
    f = open(lien, "r")
    lines=f.readlines()
    f.close()
    ls=[]
    for line in lines: 
        res = line.strip(']\n[').split(', ') 
        ls.append(res)
    #convert
    for i in range(len(ls)):
        for j in range(len(ls[i])):
            ls[i][j]=float(ls[i][j])
        ls[i].append(output)
    return ls
def record(seconds=1):
    chunk = 1024  # Record in chunks of 1024 samples
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels = 2
    fs = 44100  # Record at 44100 samples per second
    p = pyaudio.PyAudio()  # Create an interface to PortAudio
    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)
    dt=[]
    # Store data in chunks for 3 seconds
    for i in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk)
        dt.append(BToD(data))
    # Stop and close the stream 
    stream.stop_stream()
    stream.close()
    # Terminate the PortAudio interface
    p.terminate()
    return [dt] 

#-------------------------------------------------------------------
ls1=lire("play.txt",0)
ls2= lire("stop.txt",1)
for l in ls2:
    ls1.append(l)
df = pd.DataFrame(ls1)
y=df.iloc[:,-1].values.tolist()
x=df.iloc[:,0:-1].values.tolist()
clf = svm.SVC()
clf.fit(x, y)
print("-"*100)
while True:
    print("Debut")
    inp=record(2)
    print("final")
    res=int(clf.predict(inp))
    if res==0:
        print("....")
    elif res==1:
        print("Stop !!")
        sys.exit()
        
