import gsignal
import pygame

class Mouse:
    listener=None
    
    def set_listener(listener):
        Mouse.listener= listener
        
    def update():
        
        if Mouse.listener != None:
            x, y= pygame.mouse.get_pos()
            
            signal= gsignal.build( {
                "type": gsignal.MOVE ,
                "position": {"x": x, "y": y} } )
                
            
            for event in SysComm.event_stack:
                if  event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        signal= gsignal.build( {
                            "type": gsignal.CLICK ,
                            "position":  {"x": x, "y": y} } )
                            
                    elif event.button == 3:
                        signal= gsignal.build( {
                            "type": gsignal.LCLICK ,
                            "position":  {"x": x, "y": y} } )
                            
                    elif event.button == 4:
                        signal= gsignal.build( {
                            "type": gsignal.SCROLLDOWN ,
                            "position":  {"x": x, "y": y} } )
                            
                    elif event.button == 5:
                        signal= gsignal.build( {
                            "type": gsignal.SCROLLUP ,
                            "position": {"x": x, "y": y} } )
                    break;
            
            
            Mouse.listener.read_signal(signal)

class Keyboard:
    listener= None
    
    def set_listener(listener):
        Keyboard.listener= listener
        
    def update():
        pass

class SysComm:

    quit= False
    event_stack= []
    
    def update():
            
        pygame.event.pump()
        SysComm.event_stack= pygame.event.get()
        
        Mouse.update()
        Keyboard.update()
        
        #deal with the remainder
        
        while len(SysComm.event_stack) != 0:
            if SysComm.event_stack[0].type == pygame.QUIT:
                SysComm.quit= True
            SysComm.event_stack.pop(0)
