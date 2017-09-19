#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import sounddevice as sd

def makeSineWave(duration, freq):
    fs = 48000    

    i=0
    audio=[]
    while( i!=(fs*duration) ):
    
        audio.append( math.sin((i*2*math.pi)*freq/fs)  )
        i+=1
    return audio

def printWave(audio, escala):
    fs=48000
    #Queremos plotar um segundo
    #precisamos da duração inicial pra saber quanto do audio equivale a um segundo

    #preparamos primeiro um mapa vazio 25x21
    height= 181
    width= 920
    graph=[]
    for i in range(height):
        graph.append([])
        graph[i]=[" "]*width
        graph[i].append('\n')
    
    for i in range(width):
        graph[ int((audio[int(fs*i*escala/width)]+1)*((height-1)//2)) ][i]='▓'

    final=[]
    for line in graph:
        line= ''.join(line)
        final.append(line)
    final= ''.join(final)
    
    print(final)

fs = 48000

#audio = sd.rec(int(duration*fs), fs, channels=1)
#audio= makeSineWave(3, 1209000)
audio= makeSineWave(3, 1)
sd.wait()

# reproduz o som
printWave(audio, 0.01)
#sd.play(audio, fs)

# aguarda fim da reprodução
sd.wait()
