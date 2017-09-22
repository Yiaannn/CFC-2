import gsignal
from gcolor import Gcolor
import pygame

pygame.font.init()

SIZE= 1
BASE_HEIGTH= 60
WIDTH= 1180
    
class Widget(gsignal.DGcommons):
    BASE_HEIGTH= 60
    WIDTH= 1180
    TAB= 20
    
    SIZE= 1
    
    FONT= pygame.font.SysFont('verdana',  30)
    
    def __init__(self):
        self.canvas= pygame.Surface( ( self.WIDTH, self.BASE_HEIGTH*self.SIZE ) )
    
    def update(self):
        pass
        
    def event_mouse(self, etype, position):
        pass
        
    def read_signal(self, signal):
        pass
        
    def draw(self):
        pass
        
class Label(Widget):
    FONT= pygame.font.SysFont('verdana',  42)
    HEIGTH= BASE_HEIGTH*SIZE
    
    def __init__(self, text, color):
        self.HEIGTH
        self.canvas= pygame.Surface( ( self.WIDTH, self.HEIGTH) )
        self.color= color
        self.text_color= Gcolor.darken( self.color.mix(self.color.WHITE, 0.5), 0.1)
        
        pygame.draw.rect(self.canvas, self.color.get(), ( (0, 0), (self.WIDTH, self.HEIGTH) ))
        self.canvas.blit( self.FONT.render(text, True, self.text_color), (self.TAB, 0) )
        
        
class DynamicGraph(Widget):
    SIZE= 5
    HEIGTH= BASE_HEIGTH*SIZE
    
    FONT= pygame.font.SysFont('verdana',  22)
    
    def __init__(self, color, sender):
        self.canvas= pygame.Surface( ( self.WIDTH, self.HEIGTH ) )
        self.color= color
        self.graph_color= self.color.darken(0.05)
        self.line_color= self.color.chill(0.8)
        self.line_thickness= 1
        self.support_line_color= self.color.darken(0.3)
        self.highlight_color= self.color.mix(self.color.WHITE, 0.5)
        self.text_color= Gcolor.darken( self.highlight_color, 0.1)
        self.color= self.color.get()
        #self.header= self.FONT.render(text, True, self.text_color)
        
        self.gWIDTH= self.WIDTH-4*self.TAB
        self.gHEIGTH= self.HEIGTH- 4*self.TAB
        self.min_value= 0
        self.max_value= 0
        self.min_is_set= False
        self.max_is_set= False
        
        sender.set_listener(self)
        
    def reset(self, ylabel):
        xlabel= self.FONT.render("Time (tu)", True, self.text_color)
        ylabel= self.FONT.render(ylabel, True, self.text_color)
        ylabel= pygame.transform.rotate(ylabel, 90)
        self.graph= pygame.Surface( ( self.gWIDTH, self.gHEIGTH ) )
        self.min_is_set= False
        self.max_is_set= False
        self.content= []
        self.previous_point= None
        
        self.tick= 0
        
        #init graph
        pygame.draw.rect(self.graph, self.graph_color, ((0, 0), (self.gWIDTH, self.gHEIGTH)))
        for i in range(10, self.gWIDTH, 10):
            pygame.draw.line(self.graph, self.support_line_color, (i,0), (i, self.gHEIGTH))
        for i in range(10, self.gHEIGTH, 10):
            pygame.draw.line(self.graph, self.support_line_color, (0,i), (self.gWIDTH, i))
            
        pygame.draw.rect(self.canvas, self.color, ( (0, 0), (self.WIDTH, self.HEIGTH) ) )
        self.canvas.blit(self.graph, (3*self.TAB, self.TAB ) )
        
        self.canvas.blit(ylabel, (self.TAB, self.TAB ) )
        self.canvas.blit(xlabel, (3*self.TAB, 2*self.TAB+self.gHEIGTH ) )

    def draw(self):
        #draw graph
        backdrop= self.graph.copy()
        self.graph.blit(backdrop, (-1, 0))
        if self.tick%10 != 0:
            pygame.draw.line(self.graph, self.graph_color, (self.gWIDTH-1, 0), (self.gWIDTH-1, self.gHEIGTH-1))
            for i in range(10, self.gHEIGTH, 10):
                self.graph.set_at( (self.gWIDTH-1,i), self.support_line_color )
        else:
            pygame.draw.line(self.graph, self.support_line_color, (self.gWIDTH-1, 0), (self.gWIDTH-1, self.gHEIGTH-1))
        
        
        point= (3*self.gWIDTH//4, int( (self.content -self.min_value)*self.gHEIGTH/(self.max_value - self.min_value) ) )
        if self.previous_point:
            pygame.draw.aaline(self.graph, self.line_color, self.previous_point, point)
            
        x, y= point
        self.previous_point= (x-1, y)
        self.tick+=1
        
        #draw canvas
        self.canvas.blit(self.graph, (3*self.TAB, self.TAB ) )

    def read_signal(self, signal):
        if signal.type == gsignal.ACTION:
            if not self.min_is_set or self.min_value > signal.content:
                self.min_value= signal.content
                self.min_is_set= True
            if not self.max_is_set or self.max_value < signal.content:
                self.max_value= signal.content
                self.max_is_set= True
                
            if self.min_is_set and self.max_is_set and self.min_value < self.max_value:
                self.content= signal.content
                self.draw()
                
        elif signal.type == gsignal.RESET:
            self.reset(signal.content)

class DynamicGraph2(Widget):
    SIZE= 5
    HEIGTH= BASE_HEIGTH*SIZE
    
    FONT= pygame.font.SysFont('verdana',  22)
    
    def __init__(self, color, valuerange, labels, sender):
        self.listeners= []

        self.canvas= pygame.Surface( ( self.WIDTH, self.HEIGTH ) )
        self.color= color
        self.graph_color= self.color.darken(0.05)
        self.line_color= self.color.chill(0.8)
        self.line_thickness= 1
        self.support_line_color= self.color.darken(0.3)
        self.highlight_color= self.color.mix(self.color.WHITE, 0.5)
        self.text_color= Gcolor.darken( self.highlight_color, 0.1)
        self.color= self.color.get()
        #self.header= self.FONT.render(text, True, self.text_color)
        
        self.gWIDTH= self.WIDTH-4*self.TAB
        self.gHEIGTH= self.HEIGTH- 4*self.TAB

        self.min_value= 0
        self.max_value= 0
        self.min_is_set= False
        self.max_is_set= False
        if (valuerange!= None):
            self.min_value= valuerange[0]
            self.max_value= valuerange[1]
            self.min_is_set= True
            self.max_is_set= True
        self.content=None

        self.xlabel= self.FONT.render(labels[0], True, self.text_color)
        self.ylabel= self.FONT.render(labels[1], True, self.text_color)
        self.ylabel= pygame.transform.rotate(self.ylabel, 90)
        
        #TODO: consertar essa gambiarra de listener2
        self.gjoin(sender)

        self.draw()
        
    def reset(self, content):
        self.content= content

        self.draw()

    def draw(self):
        #init graph
        self.graph= pygame.Surface( ( self.gWIDTH, self.gHEIGTH ) )

        pygame.draw.rect(self.graph, self.graph_color, ((0, 0), (self.gWIDTH, self.gHEIGTH)))
        for i in range(10, self.gWIDTH, 10):
            pygame.draw.line(self.graph, self.support_line_color, (i,0), (i, self.gHEIGTH))
        for i in range(10, self.gHEIGTH, 10):
            pygame.draw.line(self.graph, self.support_line_color, (0,i), (self.gWIDTH, i))
            
        pygame.draw.rect(self.canvas, self.color, ( (0, 0), (self.WIDTH, self.HEIGTH) ) )
        self.canvas.blit(self.graph, (3*self.TAB, self.TAB ) )
        
        self.canvas.blit(self.ylabel, (self.TAB, self.TAB ) )
        self.canvas.blit(self.xlabel, (3*self.TAB, 2*self.TAB+self.gHEIGTH ) )

        #draw graph
        if self.content:
            for xlength in range(self.gWIDTH-1):

                pointA= (xlength, int( (self.content[ int((len(self.content)-1)*(xlength/self.gWIDTH)) ]-(self.min_value ) ) * self.gHEIGTH / (self.max_value - self.min_value) ) )
                pointB= (xlength+1, int( (self.content[ int((len(self.content)-1)*((xlength+1)/self.gWIDTH)) ]-(self.min_value) ) * self.gHEIGTH / (self.max_value - self.min_value) ) )
                pygame.draw.aaline(self.graph, self.line_color, pointA, pointB)
            
        
        #draw canvas
        self.canvas.blit(self.graph, (3*self.TAB, self.TAB ) )
        
        
    def gread(self, signal):
        if signal.type == gsignal.ACTION:
            if not self.min_is_set or self.min_value > min(signal.content):
                #self.min_value= min(signal.content)
                self.min_is_set= True
            if not self.max_is_set or self.max_value < max(signal.content):
                #self.max_value= max(signal.content)
                self.max_is_set= True
                
            if self.min_is_set and self.max_is_set and self.min_value < self.max_value:
                self.content= signal.content
                self.draw()
                
        elif signal.type == gsignal.RESET:
            self.reset(signal.content)
        

class StaticGraph(Widget):
    SIZE= 5
    HEIGTH= BASE_HEIGTH*SIZE
    
    FONT= pygame.font.SysFont('verdana',  22)
    
    def __init__(self, color, valuerange, labels, values, sender):
        self.listeners=[]

        self.gWIDTH= self.WIDTH-4*self.TAB
        self.gHEIGTH= self.HEIGTH- 4*self.TAB

        self.color= color
        self.graph_color= self.color.darken(0.05)
        self.line_color= self.color.chill(0.8)
        self.line_thickness= 1
        self.support_line_color= self.color.darken(0.3)
        self.highlight_color= self.color.mix(self.color.WHITE, 0.5)
        self.text_color= Gcolor.darken( self.highlight_color, 0.1)
        self.color= self.color.get()
        #self.header= self.FONT.render(text, True, self.text_color)

        self.xlabel= self.FONT.render(labels[0], True, self.text_color)
        self.ylabel= self.FONT.render(labels[1], True, self.text_color)
        self.ylabel= pygame.transform.rotate(self.ylabel, 90)

        self.canvas= pygame.Surface( ( self.WIDTH, self.HEIGTH ) )
        self.graph= pygame.Surface( ( self.gWIDTH, self.gHEIGTH ) )

        
        self.min_value= valuerange[0]
        self.max_value= valuerange[1]
        self.values= values
        
        self.gjoin(sender)

        self.draw()
        
    def reset(self, values):
        self.graph= pygame.Surface( ( self.gWIDTH, self.gHEIGTH ) )
        self.values= values

        self.draw()
        
    def draw(self):
        
        #init graph
        pygame.draw.rect(self.graph, self.graph_color, ((0, 0), (self.gWIDTH, self.gHEIGTH)))
        for i in range(10, self.gWIDTH, 10):
            pygame.draw.line(self.graph, self.support_line_color, (i,0), (i, self.gHEIGTH))
        for i in range(10, self.gHEIGTH, 10):
            pygame.draw.line(self.graph, self.support_line_color, (0,i), (self.gWIDTH, i))
            
        pygame.draw.rect(self.canvas, self.color, ( (0, 0), (self.WIDTH, self.HEIGTH) ) )
        self.canvas.blit(self.graph, (3*self.TAB, self.TAB ) )
        
        self.canvas.blit(self.ylabel, (self.TAB, self.TAB ) )
        self.canvas.blit(self.xlabel, (3*self.TAB, 2*self.TAB+self.gHEIGTH ) )

        #draw graph
        for xlength in range(self.gWIDTH-1):
            #print(self.values[ int((len(self.values)-1)*(xlength/self.gWIDTH)) ]-(self.min_value )*self.gHEIGTH)
            pointA= (xlength, int( (self.values[ int((len(self.values)-1)*(xlength/self.gWIDTH)) ]-(self.min_value ) ) * self.gHEIGTH / (self.max_value - self.min_value) ) )
            pointB= (xlength+1, int( (self.values[ int((len(self.values)-1)*((xlength+1)/self.gWIDTH)) ]-(self.min_value) ) * self.gHEIGTH / (self.max_value - self.min_value) ) )
            pygame.draw.aaline(self.graph, self.line_color, pointA, pointB)
            
        
        #draw canvas
        self.canvas.blit(self.graph, (3*self.TAB, self.TAB ) )
        
        
    def gread(self, signal):
                
        if signal.type == gsignal.RESET:
            self.reset(signal.content)
        
class valueTracker(Widget):
    HEIGTH= BASE_HEIGTH*SIZE
    
    def __init__(self, text, color, sender):
        self.canvas= pygame.Surface( ( self.WIDTH, self.HEIGTH ) )
        self.color= color
        self.highlight_color= self.color.mix(self.color.WHITE, 0.5)
        self.text_color= Gcolor.darken( self.highlight_color, 0.1)
        self.header= self.FONT.render(text, True, self.text_color)
        self.content= ""
        
        sender.set_listener(self)
        
    def draw(self):
        pygame.draw.rect(self.canvas,  self.color.get(), ((0, 0), (self.WIDTH, self.BASE_HEIGTH*self.SIZE)) )
        self.canvas.blit(self.header, (self.TAB,0))
        
        content= self.FONT.render(str(self.content), True, self.highlight_color)
        self.canvas.blit( content, (self.header.get_width()+ 2*self.TAB, 0))
            
    def read_signal(self, signal):
        if signal.type == gsignal.ACTION:
            self.content= signal.content
            
            self.draw()
    
class BoundButton(Widget):
    HEIGTH= BASE_HEIGTH*SIZE
    
    def __init__(self, text, color, listener, signaltype, ):
        self.canvas= pygame.Surface( ( self.WIDTH, self.HEIGTH ) )
        self.color= color
        self.color2= Gcolor.darken(self.color, 0.2)
        self.highlight_color= self.color.mix(self.color.WHITE, 0.5)
        self.text_color= Gcolor.darken( self.highlight_color, 0.1)
        self.color= color.get()
        
        self.label= self.FONT.render(text, True, self.text_color)
        self.signaltype= signaltype
        self.listener= listener
        
        self.draw();

    def draw(self):
        #draw button
        temp= self.label.copy()
        pygame.draw.rect(temp, self.color2, ( (0, 0), (self.WIDTH, self.HEIGTH) ) )
        temp.blit(self.label, (0, 0) )
        
        #draw widget
        pygame.draw.rect(self.canvas, self.color, ( (0, 0), (self.WIDTH, self.HEIGTH) ) )
        self.canvas.blit(temp, (self.TAB,0))
        
    def gread(self, signal):
        if signal.type == gsignal.CLICK:
            signal= gsignal.build( {
                "type": self.signaltype ,
                "content": None } )
            self.gsend(self.listener, signal)
            
class Scrollbar(Widget):
    HEIGTH= BASE_HEIGTH*SIZE
    
    def __init__(self, text, color, trackablelist, return_index, listener):
        #self.listeners= []
        #self.gjoin(listener)
        self.listener= listener

        self.canvas= pygame.Surface( ( self.WIDTH, self.HEIGTH ) )
        self.color= color
        self.highlight_color= self.color.mix(self.color.WHITE, 0.5)
        self.text_color= Gcolor.darken( self.highlight_color, 0.1)
        self.header= self.FONT.render(text, True, self.text_color)
        
        self.trackablelist= trackablelist
        self.return_index= return_index
        
        self.tick= 0
        self.target=None

        self.retarget()

        self.draw()

    def draw(self):
        pygame.draw.rect(self.canvas,  self.color.get(), ((0, 0), (self.WIDTH, self.BASE_HEIGTH*self.SIZE)) )
        
        self.canvas.blit(self.header, (self.TAB,0))
        if len( self.trackablelist.content)!= 0:
            #content= self.FONT.render(str(self.scrollist[self.tick]), True, self.scrollist[self.tick].color.get())
            content= self.FONT.render(str(self.trackablelist.content[self.tick]), True, self.highlight_color)
            self.canvas.blit( content, (self.header.get_width()+ 2*self.TAB, 0))

    def retarget(self):
        self.tick%= len(self.trackablelist.content)
        self.target= self.trackablelist.content[self.tick]
        if self.return_index:
            self.target= self.tick
        
    def gread(self, signal):
        if signal.type == gsignal.CLICK:
            self.tick+= 1
            self.retarget()

            signal= gsignal.build( {
                "type": gsignal.SELECT ,
                "content": self.target } )
            self.gsend(self.listener, signal)
            self.draw()
            
        elif signal.type == gsignal.LCLICK:
            self.tick-= 1
            self.retarget()

            signal= gsignal.build( {
                "type": gsignal.SELECT ,
                "content": self.target } )
            self.gsend(self.listener, signal)
            self.draw()
'''
class Tool:

class Graph(Tool):
    
    def set()
'''
