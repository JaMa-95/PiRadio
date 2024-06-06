import time
from mpd import MPDClient
client = MPDClient()               # create client object
client.timeout = 10                # network timeout in seconds (floats allowed), default: None
client.idletimeout = None          # timeout for fetching the result of the idle command is handled seperately, default: None
client.connect("localhost", 6600)  # connect to localhost:6600
print(client.mpd_version)          # print the MPD version
client.clear()
client.add("https://relax.stream.publicradio.org/relax.mp3?srcid")  # add the URL stream to the playlist
#client.add("https://stream.radiojarasas.com/asawhwyhz188a0uv")
client.play()     
client.setvol(20)
time.sleep(5)
print(client.status())
print(client.currentsong())                        # start playing the stream
print(client.stats())                    # print the current song
time.sleep(2)
client.stop()
print("----------------------")
print(client.status())
print(client.currentsong())                        # start playing the stream
print(client.stats())      
client.disconnect()                # disconnect from the server