# E-Paper Stats
## *Your Raspberry Pi computer statistics companion*
### Pre-requisite hardware/ software
- Raspberry Pi 3 and upwards
- E-paper display Hat 2.7 inch - I use thee one from [waveshare]
- Python 3.10 and up
- Raspberry Pi OS (Could work with Ubuntu 23.04 upwards but not tested yet  

### Introduction 
I have the epaper hat since 2020. But never got down to doing much with it.  
So I decided to display some of the system statistics on the epaper hat using python.
|Supported statistics|Remarks|
| -------------------| ------|
|Temp|Reading from Temperature sensor of the Pi|
|Fan on | Inddicate fan on status and also the RPM (*only for Pi 5*)|
|Memory| Available, used and percentage utilised|
|hostname and IP| Hostname assigned and IP assigned on the local WIFI network|

### How to use - Installation

You first have to clone this git hub respository
```
git clone https://github.com/mipsmonsta/epaper-stats.git .
```
### Running once or recurring at startup
To run the script once-off, you can invoke the script after going into the repository directory.

```
python ./examples/estats.py
```
To run the scripts at start-up of the OS (Rasperry Pi OS), do this:

```
sudo nano /etc/rc.local
```
Add the line into the `rc.local` script
```
sudo python /home/<your clone respository folder>/examples/estats.py
sudo reboot now
```
When restarted and with the e-paper hat installed, **violia**. *If not*, have your enabled SPI using [raspi-config]? 

# Code - Explained

Driver code for the epaper display is from the [waveshare epaper repository] with slight modification to 
bring up to modern Python standard. Driver codes are in the form of two files 'epd2in7.py' and 'epdconfig.py'.  
If you want to support other waveshare epaper sizes, you just have to hunt down the equivalent two files from the waveshare repository and replace. Some modification coding would be required, but nothing daunting.

Rest of the code are authored by me. If forked, pls mention me and include the MIT licence preamble.

# LICENCE - MIT

Copyright 2024 Yaojin Tham

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

[waveshare]: https://www.waveshare.com/2.7inch-e-paper-hat.htm
[raspi-config]:https://www.raspberrypi.com/documentation/computers/configuration.html
[waveshare epaper repository]: https://github.com/waveshareteam/e-Paper