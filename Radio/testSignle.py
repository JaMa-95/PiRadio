import time
import vlc
from radioFrequency import KurzFrequencies, LangFrequencies, MittelFrequencies, UKWFrequencies, SprFrequencies

url = "http://184.154.43.106:8243/stream"
instance = vlc.Instance('--input-repeat=-1', '--fullscreen')
player = instance.media_player_new()
media = instance.media_new(url)
media.get_mrl()
player.set_media(media)
player.play()
player.audio_set_volume(30)
time.sleep(500)
is_playing = player.is_playing()
print(is_playing)

non_working_url = []
for radio_frequency in KurzFrequencies().frequencies:
    url = radio_frequency.radio_url
    instance = vlc.Instance('--input-repeat=-1', '--fullscreen')
    player = instance.media_player_new()
    media = instance.media_new(url)
    media.get_mrl()
    player.set_media(media)
    player.play()
    counter = 0
    is_playing = player.is_playing()
    time.sleep(6)
    player.stop()
print()
