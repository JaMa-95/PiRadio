import time
import vlc

url = "http://184.154.43.106:8243/stream"
instance = vlc.Instance('--input-repeat=-1', '--fullscreen')
player = instance.media_player_new()
media = instance.media_new(url)
media.get_mrl()
player.set_media(media)
player.play()
time.sleep(10)
is_playing = player.is_playing()
print(is_playing)

import inspect
import os
from playsound import playsound
dirname = os.path.dirname(os.path.abspath(inspect.stack()[0][1]))
filename = os.path.join(dirname, "/data/Army-radio-static.mp3")
print(filename)	
playsound(filename)
