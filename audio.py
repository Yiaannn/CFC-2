import math
import sounddevice as sd
import gsignal
import numpy as np
import scipy.signal as sig

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
    listeners=[]
    tick= 0
    mode= 0 #0: idle 1: playing 2: recording -1:testes
    recbuffer=[]
    tracknames=gsignal.Trackable([])
    displayfourierrecord=False

    def gsend(listener, signal):
            listener.gread(signal)

    def init():
        fs=48000
        sd.default.samplerate= fs
        sd.default.channels= 1

        AudioTrack.tracklist=[
            AudioTrack.generate(['sineWave', 'sineWave'], [697, 1209], 60, '1'),
            AudioTrack.generate(['sineWave', 'sineWave'], [697, 1336], 60, '2'),
            AudioTrack.generate(['sineWave', 'sineWave'], [697, 1477], 60, '3'),
            AudioTrack.generate(['sineWave', 'sineWave'], [697, 1633], 60, 'A'),

            AudioTrack.generate(['sineWave', 'sineWave'], [770, 1209], 60, '4'),
            AudioTrack.generate(['sineWave', 'sineWave'], [770, 1336], 60, '5'),
            AudioTrack.generate(['sineWave', 'sineWave'], [770, 1477], 60, '6'),
            AudioTrack.generate(['sineWave', 'sineWave'], [770, 1633], 60, 'B'),

            AudioTrack.generate(['sineWave', 'sineWave'], [852, 1209], 60, '7'),
            AudioTrack.generate(['sineWave', 'sineWave'], [852, 1336], 60, '8'),
            AudioTrack.generate(['sineWave', 'sineWave'], [852, 1477], 60, '9'),
            AudioTrack.generate(['sineWave', 'sineWave'], [852, 1633], 60, 'C'),

            AudioTrack.generate(['sineWave', 'sineWave'], [941, 1209], 60, '*'),
            AudioTrack.generate(['sineWave', 'sineWave'], [941, 1336], 60, '0'),
            AudioTrack.generate(['sineWave', 'sineWave'], [941, 1477], 60, '#'),
            AudioTrack.generate(['sineWave', 'sineWave'], [941, 1633], 60, 'D'),

            AudioTrack.generate(['sineWave'], [523.251], 10, 'Do'),
            AudioTrack.generate(['sineWave'], [587.33], 10, 'Re'),
            AudioTrack.generate(['sineWave'], [659.255], 10, 'Mi'),
            AudioTrack.generate(['sineWave'], [698.456], 10, 'Fa'),
            AudioTrack.generate(['sineWave'], [783.991], 10, 'Sol'),
            AudioTrack.generate(['sineWave'], [880], 10, 'La'),
            AudioTrack.generate(['sineWave'], [987.767], 10, 'Si')
        ]

        AudioTrack.updateTrackNames()
        AudioTrack.loaded=AudioTrack.tracklist[0]

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

            if(AudioTrack.tick%2==0):
                content= [item for sublist in tmp for item in sublist]

                tmp= np.fft.rfft(content)
                fourier=[]    
                for i in tmp:
                    fourier.append(abs(float(i.real)))

                fourier=AudioTrack.normalize( fourier )
                content=AudioTrack.normalize( content )

                AudioTrack.detectTone(fourier)

                if (AudioTrack.displayfourierrecord):
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
        
        AudioTrack.tracklist.append(AudioTrack(channels, "default-saved"))
        AudioTrack.updateTrackNames()
    
    def load(audiotrack):
        AudioTrack.loaded= audiotrack

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
            tmp[i]= int( 24000*tmp[i]/len(fourier) )

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

    def gread(signal):
        #TODO:Eu preciso uma forma melhor  de ordenar meus listeners, mas por enquanto 0 eh o static e 1 o dynamic
        #TODO: este eh um ponto de falha, mudar os nodes ligados podem mudar a ordem estabelecida
        if signal.type == gsignal.ACTION:
            AudioTrack.play()

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

        if signal.type == gsignal.SAVE:
            if (AudioTrack.mode == 0):
                AudioTrack.save()
            else:
                print("Erro: Não foi possível salvar a ammostra de som, está certo de que ainda não está gravando?")
                #TODO: fazer display gráfico do erro, usar algo estilo toast em android?
            
            

        if signal.type == gsignal.SELECT:
            AudioTrack.tracklist[signal.content].displayfourier= AudioTrack.loaded.displayfourier
            AudioTrack.loaded.displayfourier= False

            AudioTrack.loaded=AudioTrack.tracklist[signal.content]
            AudioTrack.detectTone(AudioTrack.loaded.fourier)

            signal= gsignal.build( {
                "type": gsignal.RESET ,
                "content": AudioTrack.loaded } )
            AudioTrack.gsend(AudioTrack.listeners[0], signal)

        if signal.type == gsignal.SELECT2:
            AudioTrack.loaded.displayfourier=bool(signal.content)
            signal= gsignal.build( {
                "type": gsignal.RESET ,
                "content": AudioTrack.loaded } )
            AudioTrack.gsend(AudioTrack.listeners[0], signal)

        if signal.type == gsignal.SELECT3:
            AudioTrack.displayfourierrecord= bool(signal.content)

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
