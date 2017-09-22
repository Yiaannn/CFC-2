import math
import sounddevice as sd
import gsignal
import numpy as np

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
        
        self.track=[] #cada pos equivale às samples já somadas
        
        for i in range(len(channels[0])):
            samples=[]
            for channel in channels:
                samples.append(channel[i])
            self.track+=AudioTrack.addSamples(samples)
        self.track=AudioTrack.normalize(self.track)

    def update():
        if (AudioTrack.mode==2):
            tmp=AudioTrack.recbuffer[AudioTrack.tick*728 : (AudioTrack.tick+1)*728]

            if(AudioTrack.tick%2==0):
                signal= gsignal.build( {
                    "type": gsignal.ACTION ,
                    "content": [item for sublist in tmp for item in sublist]} )
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

    def normalize(track):
        normalizer= max(track)
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
            AudioTrack.loaded=AudioTrack.tracklist[signal.content]
            signal= gsignal.build( {
                "type": gsignal.RESET ,
                "content": AudioTrack.loaded } )
            AudioTrack.gsend(AudioTrack.listeners[0], signal)

    def __getitem__(self, key):
        return self.track[key]

    def __len__(self):
        return len(self.track)            

trackDo2= AudioTrack.generate(['sineWave'], [1046.502], 10, 'Do2')
trackRe2= AudioTrack.generate(['sineWave'], [1175], 10, 'Re2')
trackMi2= AudioTrack.generate(['sineWave'], [1319], 10, 'Mi2')
trackFa2= AudioTrack.generate(['sineWave'], [1397], 10, 'Fa2')
trackSol2= AudioTrack.generate(['sineWave'], [1568], 10, 'Sol2')
trackLa2= AudioTrack.generate(['sineWave'], [1760], 10, 'La2')
trackSi2= AudioTrack.generate(['sineWave'], [1976], 10, 'Si2')

trackSilence= AudioTrack.generate(['sineWave'], [1], 5, 'Silence')
