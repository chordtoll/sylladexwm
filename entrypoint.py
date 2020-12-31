#!/usr/bin/env python

print("Starting")
from WM import wm
print("Imported WM")
windowManager = wm()
print("Initd WM")
windowManager.loop()