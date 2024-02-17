import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib/waveshare_epd')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
import epd2in7
import utility
import time
from PIL import Image,ImageDraw,ImageFont, ImageOps
import traceback
import signal
from gpiozero import Button

KEY1PIN, KEY2PIN, KEY3PIN, KEY4PIN = 5, 6, 13, 19

def drawForegroundStats(baseImage: Image, jitter:int = 0) -> Image:

    # ready font
    defaultFont = 'Roboto-Bold.ttf'
    font35 = ImageFont.truetype(os.path.join(picdir, defaultFont), 35)
    font20 = ImageFont.truetype(os.path.join(picdir, defaultFont), 20)
    font15 = ImageFont.truetype(os.path.join(picdir, defaultFont), 15)
    font10 = ImageFont.truetype(os.path.join(picdir, defaultFont), 10)

    # draw object
    draw = ImageDraw.Draw(baseImage)

    xCoord = 50 + jitter

    # hostname stats
    hostNameText = utility.SysUtils.get_hostname()
    hostIPText = utility.SysUtils.get_ip()
    draw.text((xCoord, 15), hostNameText, font=font20, fill=255)
    draw.text((xCoord, 40), hostIPText, font=font15, fill=255)

    # temperature
    tempText = utility.SysUtils.get_temp()
    draw.text((xCoord, 90), tempText, font=font20, fill=0)
    fanOn, rpm = utility.SysUtils.get_raspi5_fan_rpm()
    if fanOn:
        draw.text((xCoord, 110), f"Fan On @ {rpm} rpm", font=font10, fill=0)

    # mem stats: used, total and utilised
    memStats = utility.SysUtils.get_mem_tuple()
    draw.text((xCoord, 145), memStats[0], font=font15, fill=255)
    draw.text((xCoord, 165), memStats[1], font=font10, fill=255)
    draw.text((xCoord, 185), memStats[2], font=font15, fill=255)

    # datetime stats snapshot
    dateTimeStats = utility.SysUtils.get_datetime()
    dateTimeStats = dateTimeStats.split(' ')
    draw.text((xCoord, 215), dateTimeStats[0], font=font10, fill=0)
    draw.text((xCoord, 235), dateTimeStats[1], font=font15, fill=0)

    return baseImage

def signal_handler(sig, frame):
    epd.init()
    epd.Clear(0xFF)
    # show goodbye end screen
    epd.display(epd.getbuffer(imageEnd))

    epd.sleep()

    logging.info("Terminate signals SIGTERM or SIGINT")
    sys.exit(0)

def main(): 


    try:

        logging.info("epd2in7 Demo")   
        isJitter = False
        while True:

            logging.info("init and Clear")
            epd.init()
            epd.Clear(0xFF)

            '''4Gray display'''
            logging.info("4Gray display--------------------------------")
            # epd.Init_4Gray()
            # estats background
            filePath = os.path.join(picdir, 'e_paper_stats.jpg')
            Himage = Image.open(filePath)
            # Process to greyscale (4 color) 
            GImage = Himage.convert('L')
            GImage.quantize(colors=4)

            # draw foreground stats
            GImage = drawForegroundStats(GImage, jitter= 5 if isJitter else 0)

            # uncomment to save screen image
            # savedPath = os.path.join(picdir, "saved_pic_name.jpg")
            # if not os.path.exists(savedPath):
            #     GImage.save(savedPath)
            
            # apply config processing of display image
            if config.isRotateUpsideDown():
                logging.info("Config says rotate upside down")
                GImage = GImage.rotate(180)

            epd.display(epd.getbuffer(GImage))
            # epd.display_4Gray(epd.getbuffer_4Gray(GImage))

            # toggle jitter
            isJitter = not isJitter

            # logging.info("Clear...")
            # epd.Clear(0xFF)
            logging.info("Goto Sleep...")
            epd.sleep()
            time.sleep(30)

    except IOError as e:
        traceback.print_exc()
        logging.info(e)

# key functions

# callback for Key1 button on e-paper display
def handleKey1Press():
    # change display to not upside down if upside down
    # and vice versa
    config.toggleUpsideDown()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    epd = epd2in7.EPD()


    # load config.json for display configuration
    config = utility.DisplayConfig()
    endPath = os.path.join(picdir, 'e_paper_endscreen.png')
    imageEnd = Image.open(endPath)
    if config.isRotateUpsideDown():
        imageEnd = imageEnd.rotate(180)

    # configure key buttons
    btnKey1 = Button(KEY1PIN)
    btnKey1.when_pressed = handleKey1Press


    # register for signals for gracefull shutdown
    signal.signal(signal.SIGTERM , signal_handler)
    signal.signal(signal.SIGINT , signal_handler)

    main()