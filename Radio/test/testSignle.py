import time
import vlc
# from Radio.radioFrequency import KurzFrequencies, LangFrequencies, MittelFrequencies, UKWFrequencies, SprFrequencies

url = "https://streams.radiomast.io/8846a94e-9874-4692-a1a0-ec7aadbe2771"
instance = vlc.Instance('--input-repeat=-1', '--fullscreen')
player = instance.media_player_new()
equalizer = vlc.AudioEqualizer()
#player.set_equalizer(equalizer)
media = instance.media_new(url)
media.get_mrl()
player.set_media(media)
player.play()
print("start")
player.audio_set_volume(30)
time.sleep(50)

print(f"preamp: {equalizer.get_preamp()}")

print(equalizer.get_amp_at_index(0))  # 60 Hz
print(equalizer.get_amp_at_index(1))  # 170 Hz
print(equalizer.get_amp_at_index(2))  # 310 Hz
print(equalizer.get_amp_at_index(3))  # 600 Hz
print(equalizer.get_amp_at_index(4))  # 1 kHz
print(equalizer.get_amp_at_index(5))  # 3 kHz
print(equalizer.get_amp_at_index(6))  # 6 kHz
print(equalizer.get_amp_at_index(7))  # 12 kHz

print("------------------")
print(equalizer.set_amp_at_index(40, 0))  # 60 Hz
print(equalizer.set_amp_at_index(20, 1))  # 170 Hz
print(equalizer.set_amp_at_index(20, 2))  # 310 Hz
print(equalizer.set_amp_at_index(0, 3))  # 600 Hz
print(equalizer.set_amp_at_index(0, 4))  # 1 kHz
print(equalizer.set_amp_at_index(0, 5))  # 3 kHz
print(equalizer.set_amp_at_index(0, 6))  # 6 kHz
print(equalizer.set_amp_at_index(0, 7))  # 12 kHz
player.set_equalizer(equalizer)
print("eualizer set")
print("------------------")
print(f"preamp: {equalizer.get_preamp()}")

print(equalizer.get_amp_at_index(0))  # 60 Hz
print(equalizer.get_amp_at_index(1))  # 170 Hz
print(equalizer.get_amp_at_index(2))  # 310 Hz
print(equalizer.get_amp_at_index(3))  # 600 Hz
print(equalizer.get_amp_at_index(4))  # 1 kHz
print(equalizer.get_amp_at_index(5))  # 3 kHz
print(equalizer.get_amp_at_index(6))  # 6 kHz
print(equalizer.get_amp_at_index(7))  # 12 kHz
time.sleep(10)

is_playing = player.is_playing()
print(is_playing)

non_working_url = []
for radio_frequency in KurzFrequencies().frequency_values:
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
