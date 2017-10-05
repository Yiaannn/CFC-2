from collections import namedtuple

MOVE= 0
CLICK= 1
SCROLLUP= 2
SCROLLDOWN= 3
COLLISION= 4
ACTION= 5
REINDEX= 6
LCLICK= 7
WATCH0= 8
WATCH1= 9
WATCH2= 10
RESET= 11
DELETE= 12
SELECT= 13
ACTION2= 14
SAVE= 15
SELECT2= 16
SELECT3= 17
        
def build(paramdict):
    for param in paramdict:
        if isinstance(paramdict[param], dict):
            paramdict[param] = build(paramdict[param])
            
    Signal= namedtuple("Signal", paramdict.keys())
    signal= Signal(*paramdict.values())
    
    return signal
        
def edit(signal, keylist, value):
        signal= signal._asdict()
        if  getattr(signal[keylist[0] ], "_asdict", None) != None:
            signal[keylist[0]]= edit(signal[keylist[0]], keylist[1:], value)
        else:
            signal[keylist[0]] = value
            
        return build(signal)

class SGcommons:
    MOVE= 0
    CLICK= 1
    SCROLLUP= 2
    SCROLLDOWN= 3
    COLLISION= 4
    ACTION= 5
    REINDEX= 6
    LCLICK= 7
    WATCH0= 8
    WATCH1= 9
    WATCH2= 10
    RESET= 11
    DELETE= 12
    SELECT= 13
    ACTION2= 14
    SAVE= 15

    listeners=[]

    def gread(signal):
        print("Gcommons error: read_signal não implementado")
        #TODO: toda classe que implementa Gcommons precisa de signalread, mas o contexto pode ser tanto estático quanto dinâmico, como lidar com isso?        

    def gsend(listener, signal):
        listener.gread(signal)

    def gjoin(gcommon):
        gcommon.listeners.append(SGcommons)
        self.listeners.append(gcommon)

        return gcommon
    
    def gbuild(paramdict):
        for param in paramdict:
            if isinstance(paramdict[param], dict):
                paramdict[param] = build(paramdict[param])
                
        Signal= namedtuple("Signal", paramdict.keys())
        signal= Signal(*paramdict.values())
        
        return signal

class DGcommons:
    MOVE= 0
    CLICK= 1
    SCROLLUP= 2
    SCROLLDOWN= 3
    COLLISION= 4
    ACTION= 5
    REINDEX= 6
    LCLICK= 7
    WATCH0= 8
    WATCH1= 9
    WATCH2= 10
    RESET= 11
    DELETE= 12
    SELECT= 13
    ACTION2= 14
    SAVE= 15


    def gread(self, signal):
        print("Gcommons error: read_signal não implementado")
        #TODO: toda classe que implementa Gcommons precisa de signalread, mas o contexto pode ser tanto estático quanto dinâmico, como lidar com isso?        
 
    def gsend(self, listener, signal):
        listener.gread(signal)

    def gjoin(self, gcommon):
        gcommon.listeners.append(self)
        self.listeners.append(gcommon)

        return gcommon
            
    def gbuild(paramdict):
        for param in paramdict:
            if isinstance(paramdict[param], dict):
                paramdict[param] = build(paramdict[param])
                
        Signal= namedtuple("Signal", paramdict.keys())
        signal= Signal(*paramdict.values())
        
        return signal

class Trackable:

    def __init__(self, content):
        self.content= content
