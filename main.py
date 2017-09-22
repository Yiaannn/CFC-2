import os
from gcolor import Gcolor
import gtime
from syscomm import SysComm
from display import Display

os.environ['SDL_VIDEO_WINDOW_POS'] = "0, 0"
#--MAIN LOOP--


while not SysComm.quit:
    current_time= gtime.current()
    
    #update system interface
    SysComm.update()

    #draw things
    Display.update()
    
    gtime.update()
    elapsed_time= gtime.current()-current_time
    if elapsed_time < 16:
        gtime.sleep( 16 - elapsed_time)
