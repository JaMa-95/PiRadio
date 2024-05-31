import time
from mpd import MPDClient
client = MPDClient()               # create client object
client.timeout = 10                # network timeout in seconds (floats allowed), default: None
client.idletimeout = None          # timeout for fetching the result of the idle command is handled seperately, default: None
client.connect("localhost", 6600)  # connect to localhost:6600
print(client.mpd_version)          # print the MPD version
print(client.find("any", "house")) # print result of the command "find any house"
print(client.status())
client.add("https://streams.radiomast.io/8846a94e-9874-4692-a1a0-ec7aadbe2771")  # add the URL stream to the playlist
client.play()                               # start playing the stream
time.sleep(2)
print(client.currentsong())                        # print the current song
client.stop()
client.disconnect()                # disconnect from the server