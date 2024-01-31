# E-Paper Stats
## *Your Raspberry Pi statistics company*
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


[waveshare]: https://www.waveshare.com/2.7inch-e-paper-hat.htm
[raspi-config]:https://www.raspberrypi.com/documentation/computers/configuration.html