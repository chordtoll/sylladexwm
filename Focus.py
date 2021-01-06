import _xlib
import X
class focus:
    def __init__(self,wm):
        self.wm=wm
        self.oldfocus=None
    def focus(self,window):
        print(f"Focused window {window}")
        if self.oldfocus:   #When we defocus a window, grab mouse clicks so we can refocus on click.
            _xlib.lib.XGrabButton(self.wm.display,X.AnyButton,0,self.oldfocus,True,X.ButtonPressMask,X.GrabModeAsync,X.GrabModeAsync,X.NONE,X.NONE)
        
        _xlib.lib.XUngrabButton(self.wm.display,X.AnyButton,0,window)   #Ungrab mouse clicks on the newly focused window

        _xlib.lib.XSetInputFocus(self.wm.display,window,X.RevertToParent, X.CurrentTime)    #Actually focus the window
        
        X.ConfigureWindow(_xlib, self.wm.display, window, stack_mode = X.Above) #Put it on top

        self.oldfocus=window    #Store the currently focused window for the next time focus changes