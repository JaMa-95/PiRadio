# Radio


https://learn.adafruit.com/adafruit-i2s-stereo-decoder-uda1334a/raspberry-pi-usage
https://raspberrypi.stackexchange.com/questions/639/how-to-get-pulseaudio-running
https://pimylifeup.com/raspberry-pi-vlc/

https://raspberrypi.stackexchange.com/questions/108694/how-to-start-a-python-script-at-boot


sudo nano /lib/systemd/system/radio.service

https://unix.stackexchange.com/questions/56083/how-to-write-a-shell-script-that-gets-executed-on-login



# LED
https://dordnung.de/raspberrypi-ledstrip/ws2812

# AUDIO
sudo adduser root pulse-access
To run pythons script and pulseAudio with root access. Root access is needed by ws2811 led strip. Pulse Audio is by default not usable from root
