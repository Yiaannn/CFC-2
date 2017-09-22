class Gcolor:
    BLACK= (0, 0, 0)
    WHITE= (255, 255, 255)
    RED= (255, 0, 0)
    GREEN=(0, 255, 0)
    BLUE= (0, 0, 255)
    
    SUN= (255, 215, 0)
    MERCURY= (238, 18, 137)
    VENUS= (135, 206, 250)
    EARTH= (30, 144, 255)
    MARS= (255, 0, 0)
    JUPITER= (214, 164, 13)
    SATURN= (138, 161, 10)
    URANUS= (14, 48, 201)
    NEPTUNE= (14, 161, 201)
    
    def sanitize(color):
        if isinstance(color, Gcolor):
            color= color.color[:]
        else:
            color= list(color)
            
        return color
    
    def set(self, color):
        color= Gcolor.sanitize(color)
        self.color= color
        
    def get(self):
        return tuple( self.color )
        
    def __init__(self, color):
        self.set(color)
    
    def paint(light):
        light= light[:]
        for i in range(3):
            light[i]**= 1/2
            light[i]= int(light[i])
            
        return light
        
    def enlight(color):
        color= Gcolor.sanitize(color)
        for i in range(3):
           color[i]**= 2
            
        return color
            
    #----#
        
    def illuminate(color ):
        color= Gcolor.sanitize(color)
        increment= 255 - max(color)
        
        for i in range(3):
            color[i]+= increment
            
        return color
        
    def mix(color1, color2, factor):
        color1= Gcolor.sanitize(color1)
        color2= Gcolor.sanitize(color2)
        
        light1= Gcolor.enlight(color1)
        light2= Gcolor.enlight(color2)

        for i in range(3):
            light1[i]= light1[i]*(1-factor) + light2[i]*factor
        
        return Gcolor.paint(light1)
        
    def darken(color, factor):
        color= Gcolor.sanitize(color)
        
        for i in range(3):
            color[i]*= (1-factor)
            color[i]= int(color[i])
            
        return color
    
    def chill(color, factor):
        #eu não sei o que acabei fazendo mas gostei do resultado
        color= Gcolor.sanitize(color)
        color= Gcolor.illuminate(color)
        
        light= Gcolor.enlight(color)
        factor+= 1
        factor/= 2
        
        nlight= Gcolor.enlight( Gcolor.WHITE)
        for i in range(len(color)):
            nlight[i]-= light[i]
        ncolor= Gcolor.paint(nlight)
        
        ncolor= Gcolor.illuminate(ncolor)
        color= Gcolor.mix(ncolor, color, factor)
        color= Gcolor.illuminate(color)
        
        return color
    
    def burn(color, factor):
        #se esta função acabar sendo algo vagamente similar ao contrário de chill já estou feliz
        color=Gcolor.sanitize(color)
        color=Gcolor.illuminate(color)
        
        factor*= -1
        
        color= Gcolor.chill(color, factor)
        light= Gcolor.enlight(color)
        nlight= Gcolor.enlight( Gcolor.WHITE)
        
        for i in range(len(color)):
            nlight[i]-= light[i]
            
        ncolor= Gcolor.paint(nlight)
        ncolor= Gcolor.illuminate(ncolor)
        
        return ncolor

    
    