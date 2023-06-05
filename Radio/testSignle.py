import time
import vlc
from radioFrequency import KurzFrequencies, LangFrequencies, MittelFrequencies, UKWFrequencies, SprFrequencies

url = "https://streams.radiomast.io/8846a94e-9874-4692-a1a0-ec7aadbe2771"
instance = vlc.Instance('--input-repeat=-1', '--fullscreen')
player = instance.media_player_new()
equalizer = vlc.AudioEqualizer()
media = instance.media_new(url)
media.get_mrl()
player.set_media(media)
player.play()
print("start")
player.audio_set_volume(20)
time.sleep(5)

equalizer.set_amp_at_index(0, 5)  # 60 Hz
equalizer.set_amp_at_index(1, 4)  # 170 Hz
equalizer.set_amp_at_index(2, 3)  # 310 Hz
equalizer.set_amp_at_index(3, 0)  # 600 Hz
equalizer.set_amp_at_index(4, 0)  # 1 kHz
equalizer.set_amp_at_index(5, 0)  # 3 kHz
equalizer.set_amp_at_index(6, 0)  # 6 kHz
equalizer.set_amp_at_index(7, 0)  # 12 kHz
player.set_equalizer(equalizer)
print("eualizer set")
time.sleep(10)

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
