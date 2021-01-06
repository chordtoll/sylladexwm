import _xlib
import X

class mouse:
    def __init__(self,wm):
        self.wm = wm
        self.dragWindow = None

    def configureMouse(self, window):
        #Grab all ALT+Button actions- these are WM instructions
        _xlib.lib.XGrabButton(
            self.wm.display,
            X.AnyButton,
            X.Mod1Mask,
            window,
            0,
            X.ButtonMotionMask | X.ButtonReleaseMask | X.ButtonPressMask,
            X.GrabModeAsync,
            X.GrabModeAsync,
            X.NONE,
            X.NONE)

    def handleMouseEvent(self, event):
        #Handle button press events
        if event.xbutton.type == X.ButtonPress:
            self.wm.focusHandler.focus(event.xbutton.window)    #Focus a window whenever it's clicked

        #Handle mouse drag events:
        if event.xbutton.type == X.MotionNotify:
            #Filter WM drag events
            if event.xbutton.state & (X.Button1Mask|X.Button3Mask) and event.xbutton.state & X.Mod1Mask:
                
                #If we're not dragging yet, start a drag
                if self.dragWindow is None:

                    self.dragWindow = event.xbutton.window  #Save the window for later

                    #Get the window geometry
                    wg_root = _xlib.ffi.new("Window *")
                    wg_x = _xlib.ffi.new("int *")
                    wg_y = _xlib.ffi.new("int *")
                    wg_w = _xlib.ffi.new("unsigned int *")
                    wg_h = _xlib.ffi.new("unsigned int *")
                    wg_bw = _xlib.ffi.new("unsigned int *")
                    wg_depth=_xlib.ffi.new("unsigned int *")
                    _xlib.lib.XGetGeometry(self.wm.display,event.xbutton.window,
                        wg_root,
                        wg_x,
                        wg_y,
                        wg_w,
                        wg_h,
                        wg_bw,
                        wg_depth)

                    #Calculate some parameters based on where the drag starts
                    self.moveX = wg_x[0] - event.xbutton.x_root
                    self.moveY = wg_y[0] - event.xbutton.y_root
                    self.width = wg_w[0] - event.xbutton.x_root
                    self.height= wg_h[0] - event.xbutton.y_root

                #If we are dragging, update the window
                else:
                    if event.xbutton.state== X.Button1Mask | X.Mod1Mask:    #ALT+L: We're moving a window
                        _xlib.lib.XMoveWindow(self.wm.display,self.dragWindow,self.moveX + event.xbutton.x_root,self.moveY + event.xbutton.y_root)
                    elif event.xbutton.state==X.Button3Mask | X.Mod1Mask:   #ALT+R: We're resizing a window
                        _xlib.lib.XResizeWindow(self.wm.display,self.dragWindow,self.width+event.xbutton.x_root,self.height+event.xbutton.y_root)

        if event.xbutton.type == X.ButtonRelease:
            self.dragWindow = None  #When the button is released, if we're dragging a window, drop it

        
