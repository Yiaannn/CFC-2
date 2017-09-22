import audio

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

printWave(audio.track1.track, 0.01)

tmp1= audio.AudioTrack.generate(['sineWave'], [587.33], 30, 'Do')

tmp2= audio.AudioTrack.generate(['sineWave'], [1046.502], 30, 'Do2')

audio.trackDo.play()
audio.trackSilence.play()
audio.trackDo.play()
audio.trackSilence.play()
audio.trackDo.play()
audio.trackSilence.play()
audio.trackDo.play()
audio.trackSilence.play()


audio.trackRe.play()
audio.trackSilence.play()
audio.trackRe.play()
audio.trackSilence.play()
tmp1.play()
audio.trackSilence.play()

audio.trackMi.play()
audio.trackSilence.play()
audio.trackMi.play()
audio.trackSilence.play()
audio.trackMi.play()
audio.trackSilence.play()
audio.trackMi.play()
audio.trackSilence.play()

audio.trackFa.play()
audio.trackSilence.play()
audio.trackFa.play()
audio.trackSilence.play()
audio.trackFa.play()
audio.trackSilence.play()
audio.trackFa.play()
audio.trackSilence.play()

audio.trackSol.play()
audio.trackSilence.play()
audio.trackSol.play()
audio.trackSilence.play()
audio.trackSol.play()
audio.trackSilence.play()
audio.trackSol.play()
audio.trackSilence.play()

audio.trackLa.play()
audio.trackSilence.play()
audio.trackLa.play()
audio.trackSilence.play()
audio.trackLa.play()
audio.trackSilence.play()
audio.trackLa.play()
audio.trackSilence.play()

audio.trackSi.play()
audio.trackSilence.play()
audio.trackSi.play()
audio.trackSilence.play()
audio.trackSi.play()
audio.trackSilence.play()
audio.trackSi.play()
audio.trackSilence.play()

audio.trackDo2.play()
audio.trackSilence.play()
audio.trackDo2.play()
audio.trackSilence.play()
tmp2.play()
audio.trackSilence.play()
audio.trackSilence.play()
