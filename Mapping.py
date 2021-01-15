import _xlib
import X
import X.hints
import X.damage
class mapping:
    def __init__(self, wm, display, rootWindow):
        self.wm = wm
        self.display = display
        self.windowList = []
        self.focusedWindow = _xlib.ffi.new("Window *")
        self.revertTo = _xlib.ffi.new("int *")

    def handleMapEvent(self, event):
        window = event.xmaprequest.window

        #Listen for the following events on this window:
        X.ChangeWindowAttributes(_xlib, self.display, window, event_mask = 
                                 _xlib.lib.PropertyChangeMask |     #Move/resize
                                 _xlib.lib.ExposureMask |           #Exposure change
                                 _xlib.lib.StructureNotifyMask)     #Unmap notification

        _xlib.lib.XDamageCreate(self.display,window,X.damage.DamageReportNonEmpty)
        
        _xlib.lib.XMapWindow(self.display,window)   #Map the window onto the screen

        self.wm.focusHandler.focus(window)  #Focus the new window

        X.ConfigureWindow(_xlib, self.display, window, stack_mode = X.Above)    #Put the new window on top

        self.windowList.append(window)  # Add window to list of open windows

        self.wm.mouseHandler.configureMouse(window)  # Register mouse handlers for the new window

    def handleUnmapEvent(self, event):                  #Called after a window has closed
        if event.xunmap.window in self.windowList:          #If we know about it,
            self.windowList.remove(event.xunmap.window)         #Forget about it

    def drawBorders(self):
        colormap = _xlib.lib.XDefaultColormap(self.display, _xlib.lib.XDefaultScreen(self.display)) #Grab our colormap

        for window in self.windowList:
            X.ConfigureWindow(_xlib, self.display, window, border_width = 2)    #Turn on a border
            borderColor = _xlib.ffi.new("XColor *")
            exactColor = _xlib.ffi.new("XColor *")
            if self.focusedWindow[0]==window:   #Grab a color: red if focused, else blue
                _xlib.lib.XAllocNamedColor(self.display, colormap, b"red", borderColor, exactColor)
            else:
                _xlib.lib.XAllocNamedColor(self.display, colormap, b"blue", borderColor, exactColor)

            X.ChangeWindowAttributes(_xlib, self.display, window, border_pixel=borderColor.pixel) #Set the border color

    def updateFocus(self):
        _xlib.lib.XGetInputFocus(self.wm.display,self.focusedWindow,self.revertTo)  #Update our focusedWindow properte
