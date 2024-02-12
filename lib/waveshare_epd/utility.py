from PIL import Image
import os
import pathlib
import subprocess
from datetime import datetime
import logging
import re
import json

class DisplayConfig:
    def __init__(self):
        self.logger = logging.getLogger("Display_config")
        CONFIG_FILE_NAME = "config.json"
        PATHDIR = os.getcwd()
        filePath = os.path.join(PATHDIR, CONFIG_FILE_NAME)
    
        self.config = {}
        if os.path.exists(filePath):
            try:
                with open(filePath, "r") as f:
                    self.config = json.load(f)
                    self.logger.debug(self.config)
            except:
                pass

    def isRotateUpsideDown(self) -> bool:
        if "upsidedown" not in self.config:
            return False
        
        if self.config["upsidedown"] == True:
            return True
        
        return False
        


class ImageUtils:
    @staticmethod
    def isPictureExtensionFile(filePath):
        _, fileExt = os.path.splitext(filePath)
        return fileExt.lower() == '.jpg'

    @staticmethod
    def autoRotateImage(image: Image) -> Image:

        # Check for Exif orientation information
        try:
            exif = image._getexif()
            if exif is not None:
                orientation = exif.get(274)
        
                if orientation == 8 or 4:
                    image = image.rotate(90, expand = True)
                else:
                    image = image.rotate(180, expand = True)

        except (AttributeError, KeyError, IndexError):
            # Ignore cases where Exif informaiton is not availble

            pass

        return image

    
    '''Resize image to be full cropped with no black border. 
        Image width or Image height will match width or height respectively
        if aspect ratio of image defers from the target aspect ratio'''
    @staticmethod
    def resizeImage(image: Image, width, height)-> Image:

        image_width, image_height = image.size
        aspect_ratio = image_width / image_height

        target_aspect_ratio = width / height

        # Determine to resize based on width or height

        # image's width is longer than height, so we crop width
        if aspect_ratio > target_aspect_ratio: 
        
            # resize based on target height and then crop width
            new_width = int(height * aspect_ratio)
            resizedImage = image.resize((new_width, height), Image.ANTIALIAS)
            crop_x = (new_width - width) // 2
            crop_y = 0


        else:

            new_height = int(width / aspect_ratio)
            resizedImage = image.resize((width, new_height), Image.ANTIALIAS)
            crop_x = 0
            crop_y = (new_height - height) // 2

        cropped_image = resizedImage.crop((crop_x, crop_y, crop_x + width, crop_y + height))
    
        return cropped_image


class SysUtils:
    logger = logging.getLogger('Utils')
    current_dir = str(pathlib.Path(__file__).parent.parent.resolve())
    temp_unit = 'C'

    @staticmethod
    def shell_cmd(cmd):
        return subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT).decode("utf-8")

    @staticmethod
    def get_text_center(display, text, font):
        w, h = SysUtils.get_text_size(display, text, font)
        left = (display.width - w) / 2
        top = (display.height - h) / 2
        return [left, top]

    @staticmethod
    def get_text_size(display, text, font):
        left, top, right, bottom = display.draw.textbbox((0, 0), text, font=font)
        width = right - left if left > right else right - left
        height = top - bottom if bottom < top else bottom - top
        return [width, height]

    @staticmethod
    def requires_scroller(display, text, font):
        w, unused = SysUtils.get_text_size(display, text, font)
        return display.width < w

    @staticmethod
    def get_hostname(opt = ""):
        return str(SysUtils.shell_cmd("hostname " + opt + "| cut -d\' \' -f1")).strip()

    @staticmethod
    def get_ip():
        return SysUtils.get_hostname('-I')

    @staticmethod
    def get_datetime(format = None):
        if not format:
            format = SysUtils.datetime_format if hasattr(SysUtils, 'datetime_format') else "%d/%m/%Y %H:%M:%S"
        return datetime.now().strftime(format)
    
    @staticmethod
    def get_temp():
        temp =  float(SysUtils.shell_cmd("cat /sys/class/thermal/thermal_zone0/temp")) / 1000.00

        if (hasattr(SysUtils,'temp_unit') and SysUtils.temp_unit == 'F'):
            temp = "%0.1f °F " % (temp * 9.0 / 5.0 + 32)
        else:
            temp = "%0.1f °C " % (temp)

        return temp
    
    @staticmethod
    def get_raspi5_fan_rpm() -> (bool, str):
        # check if raspberry pi 5
        model = str(SysUtils.shell_cmd("cat /proc/device-tree/model"))

        if not model.strip().startswith("Raspberry Pi 5"):
            SysUtils.logger.info(model.strip())
            return (False, "NA")
        
        
        rpm =  str(SysUtils.shell_cmd("cat /sys/devices/platform/cooling_fan/hwmon/*/fan1_input")).strip()
        if rpm == "0":
            return (False, "0")

    
        return (True, rpm)
    
    @staticmethod
    def get_storage_tuple() -> tuple[str]:
        storage =  SysUtils.shell_cmd('df -h | awk \'$NF=="/"{printf "%d,%d,%s", $3,$2,$5}\'')
        storage = storage.split(',')
        return (f"USED: {storage[0]} GB", 
                f"TOTAL: {storage[1]} GB", 
                f"UTILISED: {storage[2]}")
    
    @staticmethod
    def get_mem_tuple() -> tuple[str]:
        mem =  SysUtils.shell_cmd("free -m | awk 'NR==2{printf \"%.1f,%.1f,%.0f%%\", $3/1000,$2/1000,$3*100/$2 }'")
        mem = mem.split(',')
        return (f"USED: {mem[0]} GB", 
                f"TOTAL: {mem[1]} GB", 
                f"UTILISED: {mem[2]}")

    @staticmethod
    def compile_text(text, additional_replacements = {}):
        replacements = {
            "{hostname}": lambda prop: SysUtils.get_hostname(),
            "{ip}": lambda prop: SysUtils.get_ip(),
            "{datetime}": lambda prop: SysUtils.get_datetime()
        }
        replacements = {**replacements, **additional_replacements}
        regex = re.compile("(%s)" % "|".join(map(re.escape, replacements.keys())))
        return regex.sub(lambda match: replacements[match.string[match.start():match.end()]](match.string[match.start():match.end()]), text)

    @staticmethod
    def does_text_width_fit(display, text, font):
        left, top, right, bottom = display.draw.textbbox((0, 0), text, font=font)
        return display.width > right - left

    @staticmethod
    def slugify(text):
        maxlength = 15
        slug = re.sub(r'[^a-z0-9\_ ]+', '', text.lower().strip()).replace(" ", "_")[0:maxlength].strip('_')
        return slug