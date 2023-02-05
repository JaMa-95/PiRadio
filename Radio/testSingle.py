import time
import vlc

url = "http://184.154.43.106:8243/stream"
instance = vlc.Instance('--input-repeat=-1', '--fullscreen')
player = instance.media_player_new()
media = instance.media_new(url)
media.get_mrl()
player.set_media(media)
player.play()
player.audio_set_volume(50)
time.sleep(10)
is_playing = player.is_playing()
print(is_playing)