from gcolor import Gcolor
from panel import Panel
import gsignal
from syscomm import Mouse
import pygame
#TODO:DEBUG
import audio

pygame.display.set_caption("Orbital Simulator")
#pygame.display.set_icon()

class Display:
    WIDTH= 1600
    HEIGTH= 900
    CANVAS= pygame.display.set_mode( (WIDTH, HEIGTH) )
    
    def update():
        Display.CANVAS.fill(Gcolor.BLACK)
        MainFrame.update()
        Sidebar.update()
        pygame.display.flip()
        
    def read_signal(signal):
    
        if signal.position.x > (Display.WIDTH - Sidebar.WIDTH):
            signal= gsignal.edit(signal, ["position", "x"], signal.position.x - (Display.WIDTH - Sidebar.WIDTH) )
            Sidebar.gread(signal)
        else:
            MainFrame.read_signal(signal)
 
Mouse.set_listener(Display) 
     
class MainFrame:

    WIDTH= Display.WIDTH
    HEIGTH= Display.HEIGTH
    CANVAS= Display.CANVAS.subsurface( (0, 0), (WIDTH, HEIGTH) )

    #drawable=CelestialCluster.cluster
    drawable=[]

    def update():
        for thing in MainFrame.drawable:
            thing.draw(MainFrame)
    
    def read_signal(signal):
        if signal.type == gsignal.SCROLLUP or signal.type == gsignal.SCROLLDOWN:
            #Perspective.read_signal(signal)
            pass

class Sidebar:
    WIDTH= Panel.WIDTH
    HEIGTH= Panel.HEIGTH
    CANVAS= Display.CANVAS.subsurface( (Display.WIDTH - WIDTH, 0), (WIDTH, HEIGTH) )
    MENU= []
    active_panel= None
    

    listeners=[]
    def init():

        #TODO:depois tirar o audiotrack daqui
        audio.AudioTrack.init()

        Sidebar.MENU= [
            #Panel(Sidebar.CANVAS.subsurface( (0, 0), (Panel.WIDTH, Panel.HEIGTH) ), "Camera", Gcolor( Gcolor.darken( Gcolor.chill(Gcolor.EARTH, 0.7), 0.7) ), 0, Sidebar) ,
            #Panel(Sidebar.CANVAS.subsurface( (0, 0), (Panel.WIDTH, Panel.HEIGTH) ), "Create", Gcolor( Gcolor.darken( Gcolor.chill(Gcolor.VENUS, 0.7), 0.7) ), 1, Sidebar) ,
            #Panel(Sidebar.CANVAS.subsurface( (0, 0), (Panel.WIDTH, Panel.HEIGTH) ), "Erase", Gcolor( Gcolor.darken( Gcolor.chill(Gcolor.MARS, 0.7), 0.7) ), 2, Sidebar) ,
            Panel(Sidebar.CANVAS.subsurface( (0, 0), (Panel.WIDTH, Panel.HEIGTH) ), "Audio",  Gcolor( Gcolor.darken( Gcolor.chill(Gcolor.URANUS, 0.7), 0.7) ), 0, Sidebar, audio.AudioTrack) ,
            Panel(Sidebar.CANVAS.subsurface( (0, 0), (Panel.WIDTH, Panel.HEIGTH) ), "Modulation",  Gcolor( Gcolor.darken( Gcolor.chill(Gcolor.VENUS, 0.7), 0.7) ), 1, Sidebar, audio.AudioTrack) ,
            Panel(Sidebar.CANVAS.subsurface( (0, 0), (Panel.WIDTH, Panel.HEIGTH) ), "Recording",  Gcolor( Gcolor.darken( Gcolor.chill(Gcolor.MARS, 0.7), 0.7) ), 2, Sidebar, audio.AudioTrack) ]
            #Panel(Sidebar.CANVAS.subsurface( (0, 0), (Panel.WIDTH, Panel.HEIGTH) ), "Time",  Gcolor( Gcolor.darken( Gcolor.chill(Gcolor.SATURN, 0.7), 0.7) ), 4, Sidebar) ,
            #Panel(Sidebar.CANVAS.subsurface( (0, 0), (Panel.WIDTH, Panel.HEIGTH) ), "Save", Gcolor( Gcolor.darken( Gcolor.chill(Gcolor.NEPTUNE, 0.7), 0.7) ), 5, Sidebar) ]
        
        
    def update():
        #TODO:depois tirar o update daqui
        audio.AudioTrack.update()
        for i in range(len(Sidebar.MENU)):
            Sidebar.MENU[-i-1].update()
            
    def gread(signal):
        if signal.type == gsignal.ACTION:
            if not Sidebar.active_panel:
                Sidebar.active_panel= signal.target
            else:
                Sidebar.active_panel= None
                
        elif signal.type == gsignal.REINDEX:
            Sidebar.MENU.remove(signal.target)
            Sidebar.MENU.insert(0, signal.target)
            for i in range(len(Sidebar.MENU)):
                Sidebar.MENU[i].index= i
        
        else:
            panel_index= signal.position.y//Panel.BANNER_HEIGTH
            
            if not Sidebar.active_panel and panel_index < len(Sidebar.MENU):
               Sidebar.MENU[panel_index].gread(signal)
            elif Sidebar.active_panel:
                Sidebar.active_panel.gread(signal)
                
Sidebar.init()
