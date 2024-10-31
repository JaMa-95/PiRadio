# PiRadio
Build your own web streaming radio by connecting buttons and potentiometers to your raspberry pi.
Use the webserver to change settings or control the radio from any device.

# TODO
- support logarithmic poti
- audio driver selection in settings

# Hardware
- Raspberry Pi 3, 4, 5, zero (others not tested)
- Optional: print [PCB](PCB) 
- assembly components according to PCB layout

# Installation
- enable I2C
- curl command
- cd PiRadio
- sudo ./install.sh

prefer using already available node modules. Raspberry takes a long time and mostly runs out of memory when installing packages
- npm --prefix ./Radio/react-app install ./Radio/react-app

# audio
## mpd
edit file /etc/mpd.conf

When using aux ouput or comment out when using uda1334
```commandline
    # An example of an ALSA output:
    #       
    audio_output {
            type            "alsa"
            name            "My ALSA Device"
    #       device          "hw:0,0"        # optional
            mixer_type      "software"      # optional
    #       mixer_device    "default"       # optional
    #       mixer_control   "PCM"           # optional
    #       mixer_index     "0"             # optional
    }
```
## uda1334
[Installation guide](https://learn.adafruit.com/adafruit-i2s-stereo-decoder-uda1334a/raspberry-pi-usage)


# helpful links
https://learn.adafruit.com/adafruit-i2s-stereo-decoder-uda1334a/raspberry-pi-usage
https://raspberrypi.stackexchange.com/questions/639/how-to-get-pulseaudio-running
https://pimylifeup.com/raspberry-pi-vlc/
