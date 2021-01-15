NONE=0

Above                 = 0
Below                 = 1
TopIf                 = 2
BottomIf              = 3
Opposite              = 4

AnyButton = 0
CurrentTime = 0

ShiftMask      = 1<<0
LockMask       = 1<<1
ControlMask    = 1<<2
Mod1Mask       = 1<<3
Mod2Mask       = 1<<4
Mod3Mask       = 1<<5
Mod4Mask       = 1<<6
Mod5Mask       = 1<<7
Button1Mask    = 1<<8
Button2Mask    = 1<<9
Button3Mask    = 1<<10
Button4Mask    = 1<<11
Button5Mask    = 1<<12



AnyModifier    = 1<<15

RevertToParent     = 2

NoEventMask              =0
KeyPressMask             =1<<0
KeyReleaseMask           =1<<1
ButtonPressMask          =1<<2
ButtonReleaseMask        =1<<3
EnterWindowMask          =1<<4
LeaveWindowMask          =1<<5
PointerMotionMask        =1<<6
PointerMotionHintMask    =1<<7
Button1MotionMask        =1<<8
Button2MotionMask        =1<<9
Button3MotionMask        =1<<10
Button4MotionMask        =1<<11
Button5MotionMask        =1<<12
ButtonMotionMask         =1<<13
KeymapStateMask          =1<<14
ExposureMask             =1<<15
VisibilityChangeMask     =1<<16
StructureNotifyMask      =1<<17
ResizeRedirectMask       =1<<18
SubstructureNotifyMask   =1<<19
SubstructureRedirectMask =1<<20
FocusChangeMask          =1<<21
PropertyChangeMask       =1<<22
ColormapChangeMask       =1<<23
OwnerGrabButtonMask      =1<<24



GrabModeSync      = 0
GrabModeAsync     = 1



#/* Event names.  Used in "type" field in XEvent structures.  Not to be
#confused with event masks above.  They start from 2 because 0 and 1
#are reserved in the protocol for errors and replies. */

KeyPress            = 2
KeyRelease          = 3
ButtonPress         = 4
ButtonRelease       = 5
MotionNotify        = 6
EnterNotify         = 7
LeaveNotify         = 8
FocusIn             = 9
FocusOut            = 10
KeymapNotify        = 11
Expose              = 12
GraphicsExpose      = 13
NoExpose            = 14
VisibilityNotify    = 15
CreateNotify        = 16
DestroyNotify       = 17
UnmapNotify         = 18
MapNotify           = 19
MapRequest          = 20
ReparentNotify      = 21
ConfigureNotify     = 22
ConfigureRequest    = 23
GravityNotify       = 24
ResizeRequest       = 25
CirculateNotify     = 26
CirculateRequest    = 27
PropertyNotify      = 28
SelectionClear      = 29
SelectionRequest    = 30
SelectionNotify     = 31
ColormapNotify      = 32
ClientMessage       = 33
MappingNotify       = 34
GenericEvent        = 35
LASTEvent           = 36

ClipByChildren      = 0
IncludeInferiors    = 1

def ConfigureWindow(_xlib, display, window, x=None, y=None, width=None, height=None, border_width=None, sibling=None, stack_mode=None):
    attrMask = 0
    configs = _xlib.ffi.new("XWindowChanges *")
    if x is not None:
        configs.x = x
        attrMask |= 1<<0
    if y is not None:
        configs.y = y
        attrMask |= 1<<1
    if width is not None:
        configs.width = width
        attrMask |= 1<<2
    if height is not None:
        configs.height = height
        attrMask |= 1<<3
    if border_width is not None:
        configs.border_width = border_width
        attrMask |= 1<<4
    if sibling is not None:
        configs.sibling = sibling
        attrMask |= 1<<5
    if stack_mode is not None:
        configs.stack_mode = stack_mode
        attrMask |= 1<<6
    _xlib.lib.XConfigureWindow(display,window,attrMask,configs)

def ChangeWindowAttributes(_xlib, display, window, border_pixel=None, event_mask=None):
    attrMask = 0
    configs = _xlib.ffi.new("XSetWindowAttributes *")
    if border_pixel is not None:
        configs.border_pixel = border_pixel
        attrMask |= 1<<3
    if event_mask is not None:
        configs.event_mask = event_mask
        attrMask |= 1<<11
    _xlib.lib.XChangeWindowAttributes(display,window,attrMask,configs)

def GetGeometry(_xlib,display,window):
    wg_root = _xlib.ffi.new("Window *")
    wg_x = _xlib.ffi.new("int *")
    wg_y = _xlib.ffi.new("int *")
    wg_w = _xlib.ffi.new("unsigned int *")
    wg_h = _xlib.ffi.new("unsigned int *")
    wg_bw = _xlib.ffi.new("unsigned int *")
    wg_depth=_xlib.ffi.new("unsigned int *")
    _xlib.lib.XGetGeometry(display,window,
        wg_root,
        wg_x,
        wg_y,
        wg_w,
        wg_h,
        wg_bw,
        wg_depth)
    return {'root':wg_root[0],'x':wg_x[0],'y':wg_y[0],'w':wg_w[0],'h':wg_h[0],'bw':wg_bw[0],'depth':wg_depth[0]}

def QueryExtension(_xlib,display,name):
    opcode = _xlib.ffi.new("int *")
    event = _xlib.ffi.new("int *")
    error = _xlib.ffi.new("int *")
    _xlib.lib.XQueryExtension(display, name, opcode,event,error)
    return {'opcode':opcode[0],'event':event[0],'error':error[0]}