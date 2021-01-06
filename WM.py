import _xlib
import X.events

from Keyboard import keyboard
from Mouse import mouse
from Mapping import mapping
from Wallpaper import setWallpaper
from Focus import focus

class wm:
    def __init__(self):
        print("Start of init")

        _xlib.lib.XSetErrorHandler(self.errorHandler)   #Register our error handler

        self.running=True
        self.display = _xlib.lib.XOpenDisplay(_xlib.ffi.NULL)               # Initialise display
        self.screen = _xlib.lib.XDefaultScreenOfDisplay(self.display)       # Get default screen
        self.rootWindow = _xlib.lib.XRootWindowOfScreen(self.screen)        # Get root window

        X.ChangeWindowAttributes(_xlib,self.display,self.rootWindow,event_mask=_xlib.lib.SubstructureRedirectMask)  #TODO: remember what this does

        #Initialize our various handlers
        self.focusHandler = focus(self)
        self.keyboardHandler = keyboard(self, self.display, self.rootWindow)
        self.mouseHandler = mouse(self)
        self.mappingHandler = mapping(self, self.display, self.rootWindow)

        #The most important bit!
        print("Setting Wallpaper")
        setWallpaper()

        print("Init complete")

    #Currently, we're ignoring errors. Just print them out.
    @_xlib.ffi.callback("int(Display *, XErrorEvent *)")
    def errorHandler(display,event):
        print(f'''
              Serial : {event.serial       }
              Error  : {event.error_code   }
              Major  : {event.request_code }
              Minor  : {event.minor_code   }
              ''')

    def handleEvents(self):
        if _xlib.lib.XPending(self.display) > 0:  # If there is an event in the queue,
            event = _xlib.ffi.new("XEvent *")
            _xlib.lib.XNextEvent(self.display,event)  # Grab it

            #Send it to the appropriate handler
            if event.type == X.events.KeyPress:
                self.keyboardHandler.handleKeyEvent(event)
            elif event.type == X.events.ButtonPress:
                self.mouseHandler.handleMouseEvent(event)
            elif event.type == X.events.ButtonRelease:
                self.mouseHandler.handleMouseEvent(event)
            elif event.type == X.events.MotionNotify:
                self.mouseHandler.handleMouseEvent(event) 
            elif event.type == X.events.MapRequest:
                self.mappingHandler.handleMapEvent(event)
            elif event.type == X.events.MapRequest:
                self.mappingHandler.handleMapEvent(event)
            elif event.type == X.events.UnmapNotify:
                self.mappingHandler.handleUnmapEvent(event)

    #Main loop
    def loop(self):
        while self.running:
            self.handleEvents() #Process any new events
            self.mappingHandler.updateFocus()   #Check who's focused
            self.mappingHandler.drawBorders()   #Update borders to reflect that