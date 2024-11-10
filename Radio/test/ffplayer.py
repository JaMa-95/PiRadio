import time
from ffpyplayer.player import MediaPlayer

player = MediaPlayer("http://stream.rtlradio.de/plusedm/mp3-192/")

print(player.get_metadata())
print(player.get_volume())


val = ""
while True:
    time.sleep(1)
    print(player.get_volume())
    volume = player.get_volume()
    if volume < 1:
        player.set_volume(volume + 0.1)
    else:
        player.set_volume(0.1)