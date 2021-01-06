import _xlib
import X
from X.XK import latin1
from Utilities import runProcess

class keyboard:
    def __init__(self, wm, display, rootWindow):
        self.wm = wm
        self.display = display
        self.rootWindow = rootWindow
        self.configureKeys()

    """Bind keys"""
    def configureKeys(self):

        grabbedKeys =[[X.Mod1Mask, latin1.XK_T]
                     ,[X.Mod1Mask, latin1.XK_R]
                     ,[X.Mod1Mask, latin1.XK_Q]
                     ,[X.Mod1Mask, latin1.XK_P]
                     ]

        for modifier,key in grabbedKeys:  # For each key to grab,
            code = _xlib.lib.XKeysymToKeycode(self.display,key) #Resolve the key to a code
            
            # Receive events when the key is pressed
            _xlib.lib.XGrabKey(self.display,code,modifier,self.rootWindow,0,_xlib.lib.GrabModeAsync,_xlib.lib.GrabModeAsync)
        
    """Handle key presses"""
    def handleKeyEvent(self, event):

        sym = _xlib.lib.XLookupKeysym(_xlib.ffi.cast("XKeyEvent *",event),1)    #Resolve the code back to a key

        #Do the things. This will later be made user-configurable
        if sym == latin1.XK_T: runProcess("/usr/bin/lxterminal")
        if sym == latin1.XK_R: runProcess("/usr/bin/dmenu_run")
        if sym == latin1.XK_P: runProcess("/home/asent/code/sylladexwm/screenshot.sh")
        if sym == latin1.XK_Q: self.wm.running=False

