import _xlib
import X
import X.composite
import X.render
def errh(err,xc):
    print(err,xc)

class compositor:
    def __init__(self, wm, display, rootWindow):
        self.wm = wm
        self.display = display
        self.rootWindow = rootWindow

        _xlib.lib.XCompositeRedirectSubwindows(self.display,self.rootWindow,X.composite.RedirectManual)

        attr = _xlib.ffi.new("XWindowAttributes *")
        _xlib.lib.XGetWindowAttributes( self.display, self.rootWindow, attr );
        self.format = _xlib.lib.XRenderFindVisualFormat( self.display, attr.visual );

        pa = _xlib.ffi.new("XRenderPictureAttributes *")
        pa.subwindow_mode = X.IncludeInferiors
        self.pict = _xlib.lib.XRenderCreatePicture(self.display,self.rootWindow,self.format,X.render.CPSubwindowMode,pa)

        print("Initialized compositor")
    def mapUpdate(self,wevent):
        window=event.xmap.window
        
        attr = _xlib.ffi.new("XWindowAttributes *")
        _xlib.lib.XGetWindowAttributes( self.display, window, attr );
        wformat = _xlib.lib.XRenderFindVisualFormat( self.display, attr.visual );

        dwg=X.GetGeometry(_xlib,self.display,window)
        pixmap = _xlib.lib.XCompositeNameWindowPixmap(self.display,window)
        pa = _xlib.ffi.new("XRenderPictureAttributes *")
        pa.subwindow_mode = X.IncludeInferiors
        img = _xlib.lib.XRenderCreatePicture(self.display,window,wformat,X.render.CPSubwindowMode,pa)
        
        _xlib.lib.XRenderComposite(self.display,3,img,X.NONE,self.pict,0,0,0,0,dwg['x']-5,dwg['y']-5,dwg['w'],dwg['h'])
    def propertyUpdate(self,event):
        window=event.xproperty.window
        
        attr = _xlib.ffi.new("XWindowAttributes *")
        _xlib.lib.XGetWindowAttributes( self.display, window, attr );
        wformat = _xlib.lib.XRenderFindVisualFormat( self.display, attr.visual );

        dwg=X.GetGeometry(_xlib,self.display,window)
        pixmap = _xlib.lib.XCompositeNameWindowPixmap(self.display,window)
        pa = _xlib.ffi.new("XRenderPictureAttributes *")
        pa.subwindow_mode = X.IncludeInferiors
        img = _xlib.lib.XRenderCreatePicture(self.display,window,wformat,X.render.CPSubwindowMode,pa)

        _xlib.lib.XRenderComposite(self.display,3,img,X.NONE,self.pict,0,0,0,0,dwg['x']-5,dwg['y']-5,dwg['w'],dwg['h'])
    def exposeUpdate(self,event):
        window=event.xexpose.window
        
        attr = _xlib.ffi.new("XWindowAttributes *")
        _xlib.lib.XGetWindowAttributes( self.display, window, attr );
        wformat = _xlib.lib.XRenderFindVisualFormat( self.display, attr.visual );

        dwg=X.GetGeometry(_xlib,self.display,window)
        pixmap = _xlib.lib.XCompositeNameWindowPixmap(self.display,window)
        pa = _xlib.ffi.new("XRenderPictureAttributes *")
        pa.subwindow_mode = X.IncludeInferiors
        img = _xlib.lib.XRenderCreatePicture(self.display,window,wformat,X.render.CPSubwindowMode,pa)

        _xlib.lib.XRenderComposite(self.display,3,img,X.NONE,self.pict,0,0,0,0,dwg['x']-5,dwg['y']-5,dwg['w'],dwg['h'])
    def damageUpdate(self,evt):
        window=evt.drawable
        
        attr = _xlib.ffi.new("XWindowAttributes *")
        _xlib.lib.XGetWindowAttributes( self.display, window, attr );
        wformat = _xlib.lib.XRenderFindVisualFormat( self.display, attr.visual );

        dwg=X.GetGeometry(_xlib,self.display,window)
        pixmap = _xlib.lib.XCompositeNameWindowPixmap(self.display,window)
        pa = _xlib.ffi.new("XRenderPictureAttributes *")
        pa.subwindow_mode = X.IncludeInferiors
        img = _xlib.lib.XRenderCreatePicture(self.display,window,wformat,X.render.CPSubwindowMode,pa)
        
        _xlib.lib.XRenderComposite(self.display,3,img,X.NONE,self.pict,0,0,0,0,dwg['x']-5,dwg['y']-5,dwg['w'],dwg['h'])
