import os
from Utilities import runProcess

def setWallpaper():
    #runProcess(["feh", "--bg-scale", f"{os.path.split(os.path.realpath(__file__))[0]}/DefaultWallpaper.png"])
    runProcess(["xrandr", "--output", "eDP-1", "--same-as", "HDMI-1"])
