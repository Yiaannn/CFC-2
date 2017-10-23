import math
import sounddevice as sd
import gsignal
import numpy as np
import scipy.signal as sig
import wave
import struct
from syscomm import SysComm

class Sample:
    #samples serão 16 milisec, mesma do main
    
    fs=48000
    size=728 #(fs*(16/1000))

    def __init__(self, audio):
        self.audio=audio

    def generate(waveform, freq, offset=0):

        if(waveform=="sineWave"):
            i=0
            sample=[]
            while( i!=(Sample.size) ):
            
                sample.append( math.sin(((i+offset)*2*math.pi)*freq/Sample.fs)  )
                i+=1

        return Sample(sample)

    def __getitem__(self, key):
        return self.audio[key]

    def __len__(self):
        return len(self.audio)

class AudioTrack:
    #audiotracks tem sequencias de samples em vários canais

    tracklist=[]
    loaded=None
    trackablegraph=None
    listeners=[]
    tick= 0
    mode= 0 #0: idle 1: playing 2: recording -1: tests
    recbuffer=[]
    tracknames=gsignal.Trackable([])
    displaymode= gsignal.Trackable(["Time Domain", "Frequency Domain"])

    def gsend(listener, signal):
            listener.gread(signal)

    def init():
        fs=48000
        sd.default.samplerate= fs
        sd.default.channels= 1

        #
        #AudioTrack.tracklist=[
        #    AudioTrack.generate(['sineWave', 'sineWave'], [697, 1209], 60, '1'),
        #    AudioTrack.generate(['sineWave', 'sineWave'], [697, 1336], 60, '2'),
        #    AudioTrack.generate(['sineWave', 'sineWave'], [697, 1477], 60, '3'),
        #    AudioTrack.generate(['sineWave', 'sineWave'], [697, 1633], 60, 'A'),

        #    AudioTrack.generate(['sineWave', 'sineWave'], [770, 1209], 60, '4'),
        #    AudioTrack.generate(['sineWave', 'sineWave'], [770, 1336], 60, '5'),
        #    AudioTrack.generate(['sineWave', 'sineWave'], [770, 1477], 60, '6'),
        #    AudioTrack.generate(['sineWave', 'sineWave'], [770, 1633], 60, 'B'),

        #    AudioTrack.generate(['sineWave', 'sineWave'], [852, 1209], 60, '7'),
        #    AudioTrack.generate(['sineWave', 'sineWave'], [852, 1336], 60, '8'),
        #    AudioTrack.generate(['sineWave', 'sineWave'], [852, 1477], 60, '9'),
        #    AudioTrack.generate(['sineWave', 'sineWave'], [852, 1633], 60, 'C'),

        #    AudioTrack.generate(['sineWave', 'sineWave'], [941, 1209], 60, '*'),
        #    AudioTrack.generate(['sineWave', 'sineWave'], [941, 1336], 60, '0'),
        #    AudioTrack.generate(['sineWave', 'sineWave'], [941, 1477], 60, '#'),
        #    AudioTrack.generate(['sineWave', 'sineWave'], [941, 1633], 60, 'D'),

        #    AudioTrack.generate(['sineWave'], [523.251], 10, 'Do'),
        #    AudioTrack.generate(['sineWave'], [587.33], 10, 'Re'),
        #    AudioTrack.generate(['sineWave'], [659.255], 10, 'Mi'),
        #    AudioTrack.generate(['sineWave'], [698.456], 10, 'Fa'),
        #    AudioTrack.generate(['sineWave'], [783.991], 10, 'Sol'),
        #    AudioTrack.generate(['sineWave'], [880], 10, 'La'),
        #    AudioTrack.generate(['sineWave'], [987.767], 10, 'Si')
        #]

        tracknames= SysComm.listdirectory("tracks")
        tracknames.sort()
        
        for name in tracknames:
            reader= wave.open("tracks/"+name, "rb")
            AudioTrack.tracklist.append( AudioTrack.generatefromwave(reader, name[:-4]) )
            reader.close()

        #TODO:teste modulation
        tmp= AudioTrack.modulateamplitude(AudioTrack.generate(['sineWave'], [523.251], 240, 'Do'), AudioTrack.generate(['sineWave'], [4000], 240, 'Base'))
        AudioTrack.tracklist.append(tmp)
        tmp= AudioTrack.demodulateamplitude(tmp)
        AudioTrack.tracklist.append(tmp)

        AudioTrack.loaded= AudioTrack.tracklist[0]
        AudioTrack.trackablegraph= gsignal.Trackable(AudioTrack.loaded.track)

        AudioTrack.updateTrackNames()
        #TODO:Request display para fazer o panel

    def __init__(self, channels, name):
        self.channels=channels
        self.name= name
        self.displayfourier= False

        self.track=[] #cada pos equivale às samples já somadas
        
        for i in range(len(channels[0])):
            samples=[]
            for channel in channels:
                samples.append(channel[i])
            self.track+=AudioTrack.addSamples(samples)
        self.track=AudioTrack.normalize(self.track)
        fourier= np.fft.rfft(self.track) 

        self.fourier= []        
        for i in fourier:
            self.fourier.append(abs(float(i.real)))

        self.fourier=AudioTrack.normalize( self.fourier )

    def update():
        if (AudioTrack.mode==2 and AudioTrack.tick>=2):
            tmp=AudioTrack.recbuffer[(AudioTrack.tick-2)*728 : (AudioTrack.tick-1)*728]

            print("DEBUG ABABA")

            if(AudioTrack.tick%2==0):
                content= [item for sublist in tmp for item in sublist]

                tmp= np.fft.rfft(content)
                fourier=[]    
                for i in tmp:
                    fourier.append(abs(float(i.real)))

                fourier=AudioTrack.normalize( fourier )
                content=AudioTrack.normalize( content )

                AudioTrack.detectTone(fourier)

                if (AudioTrack.displaymode.iterator == 1):
                    content=fourier


                signal= gsignal.build( {
                    "type": gsignal.ACTION ,
                    "content": content } )
                AudioTrack.gsend(AudioTrack.listeners[1], signal)
            

        AudioTrack.tick+= 1
        if(AudioTrack.tick==660):
            AudioTrack.tick-=1
            AudioTrack.mode= 0

    def updateTrackNames():
        AudioTrack.tracknames.content=[]
        for track in AudioTrack.tracklist:
            AudioTrack.tracknames.content.append(track.name)

    def save():
        #TODO: pegar o AudioTrack gravado e salvar na tracklist
        channels=[]
        channels.append([])
        for i in range(AudioTrack.tick):
            tmp=AudioTrack.recbuffer[ i*728: (i+1)*728]
            channels[0].append([item for sublist in tmp for item in sublist])
        
        track= AudioTrack(channels, "default-saved")
        AudioTrack.tracklist.append(track)
        AudioTrack.savetrack(track, track.name)

        AudioTrack.updateTrackNames()
    
    #def playStep(self, step):
    #    sd.play(self.track[step], AudioTrack.fs)

    def play():
        #TODO: tratar o caso loaded=None
        sd.play(AudioTrack.loaded)

    def addSamples(samples):
        result=[]
        for i in range(Sample.size):
            result.append(0)
            for sample in samples:
                result[i]+=sample[i]

        return result

    def orderedpeaks(self):

        fourier= self.fourier
        
        for i in range(len(fourier)):
            if fourier[i]<0.1:
                fourier[i]=0

        peaks= sig.argrelextrema(np.array(fourier), np.greater)[0]
        peakandintensity=[]

        for peak in peaks:
            peakandintensity.append( (peak, fourier[peak]) )

        peakandintensity.sort(key=lambda intensity: intensity[1], reverse= True)
        
        orderedpeaks=[]
        for peak in peakandintensity:
            orderedpeaks.append(peak[0])

        for i in range(len(orderedpeaks)):
            orderedpeaks[i]= 24000*orderedpeaks[i]/( len(fourier) - 1 )

        return orderedpeaks
        

    def detectTone(fourier):
        tones=[697, 770, 852, 941, 1209, 1336, 1477, 1633]

        #TODO: estou certo de que é possível detectar tons de forma bem mais precisa e eficiente que esta

        
        for i in range(len(fourier)):
            if fourier[i]<0.1:
                fourier[i]=0
        #TODO: DEBUG: testar valores pra order tentando filtrar só os picos de interesse
        #tmp= sig.find_peaks_cwt( fourier, np.arange(20,200,20) )
        tmp= sig.argrelextrema(np.array(fourier), np.greater)[0]

        for i in range(len(tmp)):
            tmp[i]= int( 24000*tmp[i]/( len(fourier) - 1 ) )


        picos=[]
        for i in range(len(tmp)):
            for tone in tones:
                #posso usar uma tolerancia de erro de 10%
                if ( ( abs(tone-tmp[i]) <= 5 ) and  ( tone not in picos ) ):
                    picos.append(tone)

        print("Picos detectados: ", picos)

        #usar os picos detectados para relacionar com os tons

        database= [
            ["1", 697, 1209] ,
            ["2", 697, 1336] ,
            ["3", 697, 1477] ,
            ["A", 697, 1633] ,
            ["4", 770, 1209] ,
            ["5", 770, 1336] ,
            ["6", 770, 1477] ,
            ["B", 770, 1633] ,
            ["7", 852, 1209] ,
            ["8", 852, 1336] ,
            ["9", 852, 1477] ,
            ["C", 852, 1633] ,
            ["*", 941, 1209] ,
            ["0", 941, 1336] ,
            ["#", 941, 1477] ,
            ["D", 941, 1633] ]

        detectados=[]

        for reference in database:
            if set(reference[1:]).issubset(picos):
                detectados.append(reference[0])

        print("Tons detectados: ", detectados)
        

    def normalize(track):
        normalizer= max(  abs(max(track)), abs(min(track))  )
        for i in range(len(track)):
            track[i]/=normalizer

        return track

    def generate(waveform, freq, duration, name):
        #waveform e freq são listas, um valor para cada canal
        #duration equivale à quantidade de samples
        #TODO: jogar um erro se waveform e freq não forem do mesmo tamanho

        channels=[]
        
        for i in range(len(waveform)):
            channels.append([])
            for j in range(duration):
                channels[i].append( Sample.generate(waveform[i], freq[i], offset= Sample.size*j ) )

        return AudioTrack(channels, name)

    def generatefromwave(wave, name):
        maxchannels= wave.getnchannels()
        amp= wave.getsampwidth()

        raw= wave.readframes(wave.getnframes())
        track=[]
        i=0
        while (i!= len(raw)):
            value= struct.unpack("<h", raw[i:i+amp])
            value= value[0]
            #value de -2**15 a 2**15 (ou outros valores dependendo de amp)
            value= value/2**(8*(amp)-1)

            track.append( value)
            i+=amp

        #TODO:descobrir como o readnbytes me da os canais
        #primeira tentativa: assumir que os canais estao concatenados:  
        channels=[]
        size= wave.getnframes()
        for i in range(maxchannels):
            channels.append( [] )

            j=0
            while ((j+1)*728) <= len(track):
                channels[i].append(track[j*728 : (j+1)*728])
                j+=1

        return AudioTrack(channels, name)
        
    def savetrack(audiotrack, name):

        writer= wave.open("tracks/"+name+".wav", "wb")
        writer.setnchannels(1)
        writer.setsampwidth(2)
        writer.setframerate(48000)

        for i in range(len(audiotrack)):
            temp= int( audiotrack[i]*2**15 )
            if temp >  0:
                temp-=1

            data= struct.pack('<h', temp)
            writer.writeframesraw(data)

        writer.close()

    def modulateamplitude(audiotrack, audiotrackcarrier):
        #TODO: Checar se ambos os tracks tem o mesmo tamanho e jogar um erro se não
        
        track= []
        for i in range(len(audiotrackcarrier)):
            if audiotrackcarrier[i] != 0:
                track.append((audiotrack[i]+1)*audiotrackcarrier[i]/2)
            else:
                track.append((audiotrack[i]+1)*0.0000001/2)

        channels= []
        channels.append([])
        j=0
        while ((j+1)*728) <= len(track):
            channels[0].append(track[j*728 : (j+1)*728])
            j+=1

        return AudioTrack(channels, "default-modulated")

    def demodulateamplitude(audiotracksignal):
        #TODO: Checar se ambos os tracks tem o mesmo tamanho e jogar um erro se não
        
        track= []
        virtualpeak= round( ( audiotracksignal.orderedpeaks()[0] + audiotracksignal.orderedpeaks()[-1] ) / 2) 
        audiotrackcarrier= AudioTrack.generate(['sineWave'], [virtualpeak], len(audiotracksignal)//728, 'Carrier')

        for i in range(len(audiotrackcarrier)):
            if audiotrackcarrier[i] != 0:
                track.append( audiotracksignal[i]*2/audiotrackcarrier[i] - 1 )
            else:
                track.append( audiotracksignal[i]*2/0.0000001 - 1 )

        channels= []
        channels.append([])
        j=0
        while ((j+1)*728) <= len(track):
            channels[0].append(track[j*728 : (j+1)*728])
            j+=1

        return AudioTrack(channels, "default-demodulated")
        


    def gread(signal):
        #TODO:Eu preciso uma forma melhor  de ordenar meus listeners, mas por enquanto 0 eh o static e 1 o dynamic
        #TODO: este eh um ponto de falha, mudar os nodes ligados podem mudar a ordem estabelecida
        if signal.type == gsignal.ACTION:
            AudioTrack.play(AudioTrack.mainload)

        if signal.type == gsignal.ACTION2:
            if (AudioTrack.mode == 0):
                AudioTrack.mode= 2
                AudioTrack.tick= 0
                AudioTrack.recbuffer=np.zeros( (480000, 1) )
                sd.rec(out= AudioTrack.recbuffer)
            elif(AudioTrack.mode == 2):
                AudioTrack.mode= 0
                sd.stop()
            else:
                print("Erro: Não foi iniciar uma gravação, o controlador de áudio está ocupado")
                #TODO: fazer display gráfico do erro, usar algo estilo toast em android?

        if signal.type == gsignal.SELECT4:
            AudioTrack.mainload= signal.content
            

        if signal.type == gsignal.SAVE:
            if (AudioTrack.mode == 0):
                AudioTrack.save()
            else:
                print("Erro: Não foi possível salvar a ammostra de som, está certo de que ainda não está gravando?")
                #TODO: fazer display gráfico do erro, usar algo estilo toast em android?
            
            

        if signal.type == gsignal.SELECT:

            AudioTrack.loaded=AudioTrack.tracklist[signal.content]

            if ( AudioTrack.displaymode.iterator == 0 ):
                AudioTrack.trackablegraph.content= AudioTrack.loaded.track
            else:
                AudioTrack.trackablegraph.content= AudioTrack.loaded.fourier

            AudioTrack.detectTone(AudioTrack.loaded.fourier)

        if signal.type == gsignal.SELECT2:
            if ( AudioTrack.displaymode.iterator == 0 ):
                AudioTrack.trackablegraph.content= AudioTrack.loaded.track
            else:
                AudioTrack.trackablegraph.content= AudioTrack.loaded.fourier

    def __getitem__(self, key):
        if (self.displayfourier):
            return self.fourier[key]
        return self.track[key]

    def __len__(self):
        if (self.displayfourier):
            return len(self.fourier)
        return len(self.track)            

trackDo2= AudioTrack.generate(['sineWave'], [1046.502], 10, 'Do2')
trackRe2= AudioTrack.generate(['sineWave'], [1175], 10, 'Re2')
trackMi2= AudioTrack.generate(['sineWave'], [1319], 10, 'Mi2')
trackFa2= AudioTrack.generate(['sineWave'], [1397], 10, 'Fa2')
trackSol2= AudioTrack.generate(['sineWave'], [1568], 10, 'Sol2')
trackLa2= AudioTrack.generate(['sineWave'], [1760], 10, 'La2')
trackSi2= AudioTrack.generate(['sineWave'], [1976], 10, 'Si2')

trackSilence= AudioTrack.generate(['sineWave'], [1], 5, 'Silence')
