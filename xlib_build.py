from cffi import FFI
ffibuilder = FFI()

ffibuilder.set_source("_xlib",
    """ // passed to the real C compiler,
        // contains implementation of things declared in cdef()
        #include <X11/X.h>
        #include <X11/Xlib.h>
        #include <X11/Xutil.h>
        #include <X11/XKBlib.h>
        #include <X11/extensions/Xcomposite.h>
        #include <X11/extensions/Xrender.h>
        #include <X11/extensions/Xdamage.h>

        #define NONE 0
    """,
    libraries=['X11','Xcomposite','Xrender','Xdamage'])

Misc_h="""
    #define NONE 0
"""

XKB_h="""
extern KeySym XkbKeycodeToKeysym(Display *dpy, KeyCode kc, int group, int level);       //356
"""

XComposite_h="""
void XCompositeRedirectSubwindows(Display *dpy, Window window, int update);             //76
Pixmap XCompositeNameWindowPixmap (Display *dpy, Window window);                        //88
Window XCompositeGetOverlayWindow (Display *dpy, Window window);                        //91
"""

XRender_h="""
typedef uint32_t PictFormat;
typedef XID Picture;

typedef struct {                            //35
    short   red;
    short   redMask;
    short   green;
    short   greenMask;
    short   blue;
    short   blueMask;
    short   alpha;
    short   alphaMask;
} XRenderDirectFormat;

typedef struct {                            //46
    PictFormat      id;
    int         type;
    int         depth;
    XRenderDirectFormat direct;
    Colormap        colormap;
} XRenderPictFormat;

typedef struct _XRenderPictureAttributes {  //67
    int         repeat;
    Picture     alpha_map;
    int         alpha_x_origin;
    int         alpha_y_origin;
    int         clip_x_origin;
    int         clip_y_origin;
    Pixmap      clip_mask;
    Bool        graphics_exposures;
    int         subwindow_mode;
    int         poly_edge;
    int         poly_mode;
    Atom        dither;
    Bool        component_alpha;
} XRenderPictureAttributes;

typedef struct {                            //83
    unsigned short   red;
    unsigned short   green;
    unsigned short   blue;
    unsigned short   alpha;
} XRenderColor;

XRenderPictFormat * XRenderFindVisualFormat (Display *dpy, const Visual *visual);       //215

XRenderPictFormat * XRenderFindStandardFormat (Display *dpy, int format);               //231

Picture XRenderCreatePicture (Display *dpy, Drawable drawable,                          //240
              const XRenderPictFormat *format, unsigned long valuemask,
              const XRenderPictureAttributes  *attributes);

void XRenderComposite (Display *dpy, int op, Picture src, Picture mask,                 //275
          Picture dst, int src_x, int src_y, int mask_x, int mask_y,
          int dst_x, int dst_y, unsigned int width, unsigned int height);

void XRenderFillRectangle (Display *dpy, int op, Picture dst,                           //395
              const XRenderColor *color, int x, int y,
              unsigned int width, unsigned int height);
"""

Xdamage_h="""
typedef XID XserverRegion;

typedef XID Damage;

typedef struct {                                                                        //34
    int type;           /* event base */
    unsigned long serial;
    Bool send_event;
    Display *display;
    Drawable drawable;
    Damage damage;
    int level;
    Bool more;          /* more events will be delivered immediately */
    Time timestamp;
    XRectangle area;
    XRectangle geometry;
} XDamageNotifyEvent;

Damage XDamageCreate (Display *dpy, Drawable drawable, int level);                      //58

void XDamageSubtract (Display *dpy, Damage damage,                                      //64
              XserverRegion repair, XserverRegion parts);
"""

Xutil_h="""
/*                                                                                      77
 * new version containing base_width, base_height, and win_gravity fields;
 * used with WM_NORMAL_HINTS.
 */
typedef struct {
        long flags; /* marks which fields in this structure are defined */
    int x, y;       /* obsolete for new window mgrs, but clients */
    int width, height;  /* should set so old wm's don't mess up */
    int min_width, min_height;
    int max_width, max_height;
        int width_inc, height_inc;
    struct {
        int x;  /* numerator */
        int y;  /* denominator */
    } min_aspect, max_aspect;
    int base_width, base_height;        /* added by ICCCM version 1 */
    int win_gravity;            /* added by ICCCM version 1 */
} XSizeHints;

extern Status XGetWMNormalHints(Display* display, Window w,                             //501
    XSizeHints* hints_return, long* supplied_return);
"""

X_h=f"""
/* Input Event Masks. Used as event-mask window attribute and as arguments              147
   to Grab requests.  Not to be confused with event names.  */

#define NoEventMask                 0L
#define KeyPressMask                {1<<0 }L
#define KeyReleaseMask              {1<<1 }L
#define ButtonPressMask             {1<<2 }L
#define ButtonReleaseMask           {1<<3 }L
#define EnterWindowMask             {1<<4 }L
#define LeaveWindowMask             {1<<5 }L
#define PointerMotionMask           {1<<6 }L
#define PointerMotionHintMask       {1<<7 }L
#define Button1MotionMask           {1<<8 }L
#define Button2MotionMask           {1<<9 }L
#define Button3MotionMask           {1<<10}L
#define Button4MotionMask           {1<<11}L
#define Button5MotionMask           {1<<12}L
#define ButtonMotionMask            {1<<13}L
#define KeymapStateMask             {1<<14}L
#define ExposureMask                {1<<15}L
#define VisibilityChangeMask        {1<<16}L
#define StructureNotifyMask         {1<<17}L
#define ResizeRedirectMask          {1<<18}L
#define SubstructureNotifyMask      {1<<19}L
#define SubstructureRedirectMask    {1<<20}L
#define FocusChangeMask             {1<<21}L
#define PropertyChangeMask          {1<<22}L
#define ColormapChangeMask          {1<<23}L
#define OwnerGrabButtonMask         {1<<24}L

/* Key masks. Used as modifiers to GrabButton and GrabKey, results of QueryPointer,     218
   state in various key-, mouse-, and button-related events. */

#define ShiftMask       1
#define LockMask        2
#define ControlMask     4
#define Mod1Mask        8
#define Mod2Mask        16
#define Mod3Mask        32
#define Mod4Mask        64
#define Mod5Mask        128

// GrabPointer, GrabButton, GrabKeyboard, GrabKey Modes     316

#define GrabModeSync        0
#define GrabModeAsync       1

#define CWEventMask                 2048L       //403

typedef int Bool;

typedef unsigned long XID;
typedef unsigned long Mask;
typedef unsigned long Atom;     /* Also in Xdefs.h */
typedef unsigned long VisualID;
typedef unsigned long Time;

typedef XID Window;
typedef XID Drawable;
typedef XID Font;
typedef XID Pixmap;
typedef XID Cursor;
typedef XID Colormap;
typedef XID GContext;
typedef XID KeySym;

typedef unsigned char KeyCode;
"""

Xlib_h = """


typedef char *XPointer; //80
typedef int Bool;
typedef int Status;

/*  145
 * Extensions need a way to hang private data on some structures.
 */
typedef struct _XExtData {
    int number;     /* number returned by XRegisterExtension */
    struct _XExtData *next; /* next item on list of data for structure */
    int (*free_private)(    /* called to free private storage */
    struct _XExtData *extension
    );
    XPointer private_data;  /* data private to this extension. */
} XExtData;

/*  209
 * Graphics context.  The contents of this structure are implementation
 * dependent.  A GC should be treated as opaque by application code.
 */

typedef struct _XGC *GC;

/*  224
 * Visual structure; contains information about colormapping possible.
 */
typedef struct {
    XExtData *ext_data; /* hook for extension to hang data */
    VisualID visualid;  /* visual id of this visual */
    int class;      /* class of screen (monochrome, etc.) */
    unsigned long red_mask, green_mask, blue_mask;  /* mask values */
    int bits_per_rgb;   /* log base 2 of distinct color values */
    int map_entries;    /* color map entries */
} Visual;

/*  240
 * Depth structure; contains information for each possible depth.
 */
typedef struct {
    int depth;      /* this depth (Z) of the depth */
    int nvisuals;       /* number of Visual types at this depth */
    Visual *visuals;    /* list of visuals possible at this depth */
} Depth;

/*  249
 * Information about the screen.  The contents of this structure are
 * implementation dependent.  A Screen should be treated as opaque
 * by application code.
 */

struct _XDisplay;       /* Forward declare before use for C++ */

typedef struct {
    XExtData *ext_data; /* hook for extension to hang data */
    struct _XDisplay *display;/* back pointer to display structure */
    Window root;        /* Root window id. */
    int width, height;  /* width and height of screen */
    int mwidth, mheight;    /* width and height of  in millimeters */
    int ndepths;        /* number of depths possible */
    Depth *depths;      /* list of allowable depths on the screen */
    int root_depth;     /* bits per pixel */
    Visual *root_visual;    /* root visual */
    GC default_gc;      /* GC for the root root visual */
    Colormap cmap;      /* default color map */
    unsigned long white_pixel;
    unsigned long black_pixel;  /* White and Black pixel values */
    int max_maps, min_maps; /* max and min color maps */
    int backing_store;  /* Never, WhenMapped, Always */
    Bool save_unders;
    long root_input_mask;   /* initial root input mask */
} Screen;

/*  277
 * Format structure; describes ZFormat data the screen will understand.
 */
typedef struct {
    XExtData *ext_data; /* hook for extension to hang data */
    int depth;      /* depth of this image format */
    int bits_per_pixel; /* bits/pixel at this depth */
    int scanline_pad;   /* scanline must padded to this multiple */
} ScreenFormat;

/*  287
 * Data structure for setting window attributes.
 */
typedef struct {
    Pixmap background_pixmap;   /* background or None or ParentRelative */
    unsigned long background_pixel; /* background pixel */
    Pixmap border_pixmap;   /* border of the window */
    unsigned long border_pixel; /* border pixel value */
    int bit_gravity;        /* one of bit gravity values */
    int win_gravity;        /* one of the window gravity values */
    int backing_store;      /* NotUseful, WhenMapped, Always */
    unsigned long backing_planes;/* planes to be preserved if possible */
    unsigned long backing_pixel;/* value to use in restoring planes */
    Bool save_under;        /* should bits under be saved? (popups) */
    long event_mask;        /* set of events that should be saved */
    long do_not_propagate_mask; /* set of events that should not propagate */
    Bool override_redirect; /* boolean value for override-redirect */
    Colormap colormap;      /* color map to be associated with window */
    Cursor cursor;      /* cursor to be displayed (or None) */
} XSetWindowAttributes;

typedef struct {        //308
    int x, y;           /* location of window */
    int width, height;      /* width and height of window */
    int border_width;       /* border width of window */
    int depth;              /* depth of window */
    Visual *visual;     /* the associated visual structure */
    Window root;            /* root of screen containing window */
    int class;          /* InputOutput, InputOnly*/
    int bit_gravity;        /* one of bit gravity values */
    int win_gravity;        /* one of the window gravity values */
    int backing_store;      /* NotUseful, WhenMapped, Always */
    unsigned long backing_planes;/* planes to be preserved if possible */
    unsigned long backing_pixel;/* value to be used when restoring planes */
    Bool save_under;        /* boolean, should bits under be saved? */
    Colormap colormap;      /* color map to be associated with window */
    Bool map_installed;     /* boolean, is color map currently installed*/
    int map_state;      /* IsUnmapped, IsUnviewable, IsViewable */
    long all_event_masks;   /* set of events all people have interest in*/
    long your_event_mask;   /* my event mask */
    long do_not_propagate_mask; /* set of events that should not propagate */
    Bool override_redirect; /* boolean value for override-redirect */
    Screen *screen;     /* back pointer to correct screen */
} XWindowAttributes;

/*  396
 * Data structure for XReconfigureWindow
 */
typedef struct {
    int x, y;
    int width, height;
    int border_width;
    Window sibling;
    int stack_mode;
} XWindowChanges;

/*  407
 * Data structure used by color operations
 */
typedef struct {
    unsigned long pixel;
    unsigned short red, green, blue;
    char flags;  /* do_red, do_green, do_blue */
    char pad;
} XColor;

/*  417
 * Data structures for graphics operations.  On most machines, these are
 * congruent with the wire protocol structures, so reformatting the data
 * can be avoided on these architectures.
 */
typedef struct {
    short x1, y1, x2, y2;
} XSegment;

typedef struct {
    short x, y;
} XPoint;

typedef struct {
    short x, y;
    unsigned short width, height;
} XRectangle;

typedef struct {
    short x, y;
    unsigned short width, height;
    short angle1, angle2;
} XArc;

/*  481
 * Display datatype maintaining display specific data.
 * The contents of this structure are implementation dependent.
 * A Display should be treated as opaque by application code.
 */
typedef struct _XDisplay Display;

struct _XPrivate;       /* Forward declare before use for C++ */
struct _XrmHashBucketRec;

typedef struct
{
    XExtData *ext_data; /* hook for extension to hang data */
    struct _XPrivate *private1;
    int fd;         /* Network socket. */
    int private2;
    int proto_major_version;/* major version of server's X protocol */
    int proto_minor_version;/* minor version of servers X protocol */
    char *vendor;       /* vendor of the server hardware */
        XID private3;
    XID private4;
    XID private5;
    int private6;
    XID (*resource_alloc)(  /* allocator function */
        struct _XDisplay*
    );
    int byte_order;     /* screen byte order, LSBFirst, MSBFirst */
    int bitmap_unit;    /* padding and data requirements */
    int bitmap_pad;     /* padding requirements on bitmaps */
    int bitmap_bit_order;   /* LeastSignificant or MostSignificant */
    int nformats;       /* number of pixmap formats in list */
    ScreenFormat *pixmap_format;    /* pixmap format list */
    int private8;
    int release;        /* release of the server */
    struct _XPrivate *private9, *private10;
    int qlen;       /* Length of input event queue */
    unsigned long last_request_read; /* seq number of last event read */
    unsigned long request;  /* sequence number of last request. */
    XPointer private11;
    XPointer private12;
    XPointer private13;
    XPointer private14;
    unsigned max_request_size; /* maximum number 32 bit words in request*/
    struct _XrmHashBucketRec *db;
    int (*private15)(
        struct _XDisplay*
        );
    char *display_name; /* "host:display" string used on this connect*/
    int default_screen; /* default screen for operations */
    int nscreens;       /* number of screens on this server*/
    Screen *screens;    /* pointer to list of screens */
    unsigned long motion_buffer;    /* size of motion buffer */
    unsigned long private16;
    int min_keycode;    /* minimum defined keycode */
    int max_keycode;    /* maximum defined keycode */
    XPointer private17;
    XPointer private18;
    int private19;
    char *xdefaults;    /* contents of defaults from server */
    /* there is more to this structure, but it is private to Xlib */
}
*_XPrivDisplay;

/*  554
 * Definitions of specific events.
 */
typedef struct {
    int type;       /* of event */
    unsigned long serial;   /* # of last request processed by server */
    Bool send_event;    /* true if this came from a SendEvent request */
    Display *display;   /* Display the event was read from */
    Window window;          /* "event" window it is reported relative to */
    Window root;            /* root window that the event occurred on */
    Window subwindow;   /* child window */
    Time time;      /* milliseconds */
    int x, y;       /* pointer x, y coordinates in event window */
    int x_root, y_root; /* coordinates relative to root */
    unsigned int state; /* key or button mask */
    unsigned int keycode;   /* detail */
    Bool same_screen;   /* same screen flag */
} XKeyEvent;
typedef XKeyEvent XKeyPressedEvent;
typedef XKeyEvent XKeyReleasedEvent;

typedef struct {
    int type;       /* of event */
    unsigned long serial;   /* # of last request processed by server */
    Bool send_event;    /* true if this came from a SendEvent request */
    Display *display;   /* Display the event was read from */
    Window window;          /* "event" window it is reported relative to */
    Window root;            /* root window that the event occurred on */
    Window subwindow;   /* child window */
    Time time;      /* milliseconds */
    int x, y;       /* pointer x, y coordinates in event window */
    int x_root, y_root; /* coordinates relative to root */
    unsigned int state; /* key or button mask */
    unsigned int button;    /* detail */
    Bool same_screen;   /* same screen flag */
} XButtonEvent;
typedef XButtonEvent XButtonPressedEvent;
typedef XButtonEvent XButtonReleasedEvent;

typedef struct {
    int type;       /* of event */
    unsigned long serial;   /* # of last request processed by server */
    Bool send_event;    /* true if this came from a SendEvent request */
    Display *display;   /* Display the event was read from */
    Window window;          /* "event" window reported relative to */
    Window root;            /* root window that the event occurred on */
    Window subwindow;   /* child window */
    Time time;      /* milliseconds */
    int x, y;       /* pointer x, y coordinates in event window */
    int x_root, y_root; /* coordinates relative to root */
    unsigned int state; /* key or button mask */
    char is_hint;       /* detail */
    Bool same_screen;   /* same screen flag */
} XMotionEvent;
typedef XMotionEvent XPointerMovedEvent;

typedef struct {
    int type;       /* of event */
    unsigned long serial;   /* # of last request processed by server */
    Bool send_event;    /* true if this came from a SendEvent request */
    Display *display;   /* Display the event was read from */
    Window window;          /* "event" window reported relative to */
    Window root;            /* root window that the event occurred on */
    Window subwindow;   /* child window */
    Time time;      /* milliseconds */
    int x, y;       /* pointer x, y coordinates in event window */
    int x_root, y_root; /* coordinates relative to root */
    int mode;       /* NotifyNormal, NotifyGrab, NotifyUngrab */
    int detail;
    /*
     * NotifyAncestor, NotifyVirtual, NotifyInferior,
     * NotifyNonlinear,NotifyNonlinearVirtual
     */
    Bool same_screen;   /* same screen flag */
    Bool focus;     /* boolean focus */
    unsigned int state; /* key or button mask */
} XCrossingEvent;
typedef XCrossingEvent XEnterWindowEvent;
typedef XCrossingEvent XLeaveWindowEvent;

typedef struct {
    int type;       /* FocusIn or FocusOut */
    unsigned long serial;   /* # of last request processed by server */
    Bool send_event;    /* true if this came from a SendEvent request */
    Display *display;   /* Display the event was read from */
    Window window;      /* window of event */
    int mode;       /* NotifyNormal, NotifyWhileGrabbed,
                   NotifyGrab, NotifyUngrab */
    int detail;
    /*
     * NotifyAncestor, NotifyVirtual, NotifyInferior,
     * NotifyNonlinear,NotifyNonlinearVirtual, NotifyPointer,
     * NotifyPointerRoot, NotifyDetailNone
     */
} XFocusChangeEvent;
typedef XFocusChangeEvent XFocusInEvent;
typedef XFocusChangeEvent XFocusOutEvent;

/* generated on EnterWindow and FocusIn  when KeyMapState selected */
typedef struct {
    int type;
    unsigned long serial;   /* # of last request processed by server */
    Bool send_event;    /* true if this came from a SendEvent request */
    Display *display;   /* Display the event was read from */
    Window window;
    char key_vector[32];
} XKeymapEvent;

typedef struct {
    int type;
    unsigned long serial;   /* # of last request processed by server */
    Bool send_event;    /* true if this came from a SendEvent request */
    Display *display;   /* Display the event was read from */
    Window window;
    int x, y;
    int width, height;
    int count;      /* if non-zero, at least this many more */
} XExposeEvent;

typedef struct {
    int type;
    unsigned long serial;   /* # of last request processed by server */
    Bool send_event;    /* true if this came from a SendEvent request */
    Display *display;   /* Display the event was read from */
    Drawable drawable;
    int x, y;
    int width, height;
    int count;      /* if non-zero, at least this many more */
    int major_code;     /* core is CopyArea or CopyPlane */
    int minor_code;     /* not defined in the core */
} XGraphicsExposeEvent;

typedef struct {
    int type;
    unsigned long serial;   /* # of last request processed by server */
    Bool send_event;    /* true if this came from a SendEvent request */
    Display *display;   /* Display the event was read from */
    Drawable drawable;
    int major_code;     /* core is CopyArea or CopyPlane */
    int minor_code;     /* not defined in the core */
} XNoExposeEvent;

typedef struct {
    int type;
    unsigned long serial;   /* # of last request processed by server */
    Bool send_event;    /* true if this came from a SendEvent request */
    Display *display;   /* Display the event was read from */
    Window window;
    int state;      /* Visibility state */
} XVisibilityEvent;

typedef struct {
    int type;
    unsigned long serial;   /* # of last request processed by server */
    Bool send_event;    /* true if this came from a SendEvent request */
    Display *display;   /* Display the event was read from */
    Window parent;      /* parent of the window */
    Window window;      /* window id of window created */
    int x, y;       /* window location */
    int width, height;  /* size of window */
    int border_width;   /* border width */
    Bool override_redirect; /* creation should be overridden */
} XCreateWindowEvent;

typedef struct {
    int type;
    unsigned long serial;   /* # of last request processed by server */
    Bool send_event;    /* true if this came from a SendEvent request */
    Display *display;   /* Display the event was read from */
    Window event;
    Window window;
} XDestroyWindowEvent;

typedef struct {
    int type;
    unsigned long serial;   /* # of last request processed by server */
    Bool send_event;    /* true if this came from a SendEvent request */
    Display *display;   /* Display the event was read from */
    Window event;
    Window window;
    Bool from_configure;
} XUnmapEvent;

typedef struct {
    int type;
    unsigned long serial;   /* # of last request processed by server */
    Bool send_event;    /* true if this came from a SendEvent request */
    Display *display;   /* Display the event was read from */
    Window event;
    Window window;
    Bool override_redirect; /* boolean, is override set... */
} XMapEvent;

typedef struct {
    int type;
    unsigned long serial;   /* # of last request processed by server */
    Bool send_event;    /* true if this came from a SendEvent request */
    Display *display;   /* Display the event was read from */
    Window parent;
    Window window;
} XMapRequestEvent;

typedef struct {
    int type;
    unsigned long serial;   /* # of last request processed by server */
    Bool send_event;    /* true if this came from a SendEvent request */
    Display *display;   /* Display the event was read from */
    Window event;
    Window window;
    Window parent;
    int x, y;
    Bool override_redirect;
} XReparentEvent;

typedef struct {
    int type;
    unsigned long serial;   /* # of last request processed by server */
    Bool send_event;    /* true if this came from a SendEvent request */
    Display *display;   /* Display the event was read from */
    Window event;
    Window window;
    int x, y;
    int width, height;
    int border_width;
    Window above;
    Bool override_redirect;
} XConfigureEvent;

typedef struct {
    int type;
    unsigned long serial;   /* # of last request processed by server */
    Bool send_event;    /* true if this came from a SendEvent request */
    Display *display;   /* Display the event was read from */
    Window event;
    Window window;
    int x, y;
} XGravityEvent;

typedef struct {
    int type;
    unsigned long serial;   /* # of last request processed by server */
    Bool send_event;    /* true if this came from a SendEvent request */
    Display *display;   /* Display the event was read from */
    Window window;
    int width, height;
} XResizeRequestEvent;

typedef struct {
    int type;
    unsigned long serial;   /* # of last request processed by server */
    Bool send_event;    /* true if this came from a SendEvent request */
    Display *display;   /* Display the event was read from */
    Window parent;
    Window window;
    int x, y;
    int width, height;
    int border_width;
    Window above;
    int detail;     /* Above, Below, TopIf, BottomIf, Opposite */
    unsigned long value_mask;
} XConfigureRequestEvent;

typedef struct {
    int type;
    unsigned long serial;   /* # of last request processed by server */
    Bool send_event;    /* true if this came from a SendEvent request */
    Display *display;   /* Display the event was read from */
    Window event;
    Window window;
    int place;      /* PlaceOnTop, PlaceOnBottom */
} XCirculateEvent;

typedef struct {
    int type;
    unsigned long serial;   /* # of last request processed by server */
    Bool send_event;    /* true if this came from a SendEvent request */
    Display *display;   /* Display the event was read from */
    Window parent;
    Window window;
    int place;      /* PlaceOnTop, PlaceOnBottom */
} XCirculateRequestEvent;

typedef struct {
    int type;
    unsigned long serial;   /* # of last request processed by server */
    Bool send_event;    /* true if this came from a SendEvent request */
    Display *display;   /* Display the event was read from */
    Window window;
    Atom atom;
    Time time;
    int state;      /* NewValue, Deleted */
} XPropertyEvent;

typedef struct {
    int type;
    unsigned long serial;   /* # of last request processed by server */
    Bool send_event;    /* true if this came from a SendEvent request */
    Display *display;   /* Display the event was read from */
    Window window;
    Atom selection;
    Time time;
} XSelectionClearEvent;

typedef struct {
    int type;
    unsigned long serial;   /* # of last request processed by server */
    Bool send_event;    /* true if this came from a SendEvent request */
    Display *display;   /* Display the event was read from */
    Window owner;
    Window requestor;
    Atom selection;
    Atom target;
    Atom property;
    Time time;
} XSelectionRequestEvent;

typedef struct {
    int type;
    unsigned long serial;   /* # of last request processed by server */
    Bool send_event;    /* true if this came from a SendEvent request */
    Display *display;   /* Display the event was read from */
    Window requestor;
    Atom selection;
    Atom target;
    Atom property;      /* ATOM or None */
    Time time;
} XSelectionEvent;

typedef struct {
    int type;
    unsigned long serial;   /* # of last request processed by server */
    Bool send_event;    /* true if this came from a SendEvent request */
    Display *display;   /* Display the event was read from */
    Window window;
    Colormap colormap;  /* COLORMAP or None */
    Bool new;
    int state;      /* ColormapInstalled, ColormapUninstalled */
} XColormapEvent;

typedef struct {
    int type;
    unsigned long serial;   /* # of last request processed by server */
    Bool send_event;    /* true if this came from a SendEvent request */
    Display *display;   /* Display the event was read from */
    Window window;
    Atom message_type;
    int format;
    union {
        char b[20];
        short s[10];
        long l[5];
        } data;
} XClientMessageEvent;

typedef struct {
    int type;
    unsigned long serial;   /* # of last request processed by server */
    Bool send_event;    /* true if this came from a SendEvent request */
    Display *display;   /* Display the event was read from */
    Window window;      /* unused */
    int request;        /* one of MappingModifier, MappingKeyboard,
                   MappingPointer */
    int first_keycode;  /* first keycode */
    int count;      /* defines range of change w. first_keycode*/
} XMappingEvent;

typedef struct {
    int type;
    Display *display;   /* Display the event was read from */
    XID resourceid;     /* resource id */
    unsigned long serial;   /* serial number of failed request */
    unsigned char error_code;   /* error code of failed request */
    unsigned char request_code; /* Major op-code of failed request */
    unsigned char minor_code;   /* Minor op-code of failed request */
} XErrorEvent;

typedef struct {
    int type;
    unsigned long serial;   /* # of last request processed by server */
    Bool send_event;    /* true if this came from a SendEvent request */
    Display *display;/* Display the event was read from */
    Window window;  /* window on which event was requested in event mask */
} XAnyEvent;

/*  943
 *
 * GenericEvent.  This event is the standard event for all newer extensions.
 */

typedef struct
    {
    int            type;         /* of event. Always GenericEvent */
    unsigned long  serial;       /* # of last request processed */
    Bool           send_event;   /* true if from SendEvent request */
    Display        *display;     /* Display the event was read from */
    int            extension;    /* major opcode of extension that caused the event */
    int            evtype;       /* actual event type. */
    } XGenericEvent;

typedef struct {
    int            type;         /* of event. Always GenericEvent */
    unsigned long  serial;       /* # of last request processed */
    Bool           send_event;   /* true if from SendEvent request */
    Display        *display;     /* Display the event was read from */
    int            extension;    /* major opcode of extension that caused the event */
    int            evtype;       /* actual event type. */
    unsigned int   cookie;
    void           *data;
} XGenericEventCookie;

/*  969
 * this union is defined so Xlib can always use the same sized
 * event structure internally, to avoid memory fragmentation.
 */
typedef union _XEvent {
        int type;       /* must not be changed; first element */
    XAnyEvent xany;
    XKeyEvent xkey;
    XButtonEvent xbutton;
    XMotionEvent xmotion;
    XCrossingEvent xcrossing;
    XFocusChangeEvent xfocus;
    XExposeEvent xexpose;
    XGraphicsExposeEvent xgraphicsexpose;
    XNoExposeEvent xnoexpose;
    XVisibilityEvent xvisibility;
    XCreateWindowEvent xcreatewindow;
    XDestroyWindowEvent xdestroywindow;
    XUnmapEvent xunmap;
    XMapEvent xmap;
    XMapRequestEvent xmaprequest;
    XReparentEvent xreparent;
    XConfigureEvent xconfigure;
    XGravityEvent xgravity;
    XResizeRequestEvent xresizerequest;
    XConfigureRequestEvent xconfigurerequest;
    XCirculateEvent xcirculate;
    XCirculateRequestEvent xcirculaterequest;
    XPropertyEvent xproperty;
    XSelectionClearEvent xselectionclear;
    XSelectionRequestEvent xselectionrequest;
    XSelectionEvent xselection;
    XColormapEvent xcolormap;
    XClientMessageEvent xclient;
    XMappingEvent xmapping;
    XErrorEvent xerror;
    XKeymapEvent xkeymap;
    XGenericEvent xgeneric;
    XGenericEventCookie xcookie;
    long pad[24];
} XEvent;

extern Display *XOpenDisplay(const char* display_name);     //1483
extern KeySym XLookupKeysym(                                //1696
    XKeyEvent* key_event, int index);
extern KeySym *XGetKeyboardMapping(                         //1700
    Display* display, KeyCode first_keycode,
    int keycode_count, int* keysyms_per_keycode_return);
extern Window XRootWindowOfScreen(Screen* screen);          //1772
extern Colormap XDefaultColormap(Display* display,          //1818
    int screen_number);
extern Screen *XDefaultScreenOfDisplay(Display* display);   //1832
typedef int (*XErrorHandler) (                              //1843
    Display* display, XErrorEvent* error_event);
extern XErrorHandler XSetErrorHandler(                      //1848
    XErrorHandler handler);
extern Status XAllocNamedColor(Display* display,            //1998
    Colormap colormap, const char* color_name,
    XColor* screen_def_return, XColor* exact_def_return);
extern int XChangeWindowAttributes(Display* display,        //2095
    Window w, unsigned long valuemask,
    XSetWindowAttributes* attributes);  
extern int XConfigureWindow(                                //2174
    Display* display, Window w,
    unsigned int value_mask, XWindowChanges* values);
extern int XDefaultScreen(Display* display);                //2237
extern Status XGetGeometry(Display* display,                //2630
    Drawable d, Window* root_return, int* x_return,
    int* y_return, unsigned int* width_return,
    unsigned int* height_return,
    unsigned int* border_width_return,
    unsigned int* depth_return);
extern int XGetInputFocus(Display* display,                 //2648
    Window* focus_return, int* revert_to_return);           //2701
extern Status XGetWindowAttributes(Display* display,
    Window w, XWindowAttributes* window_attributes_return);
extern int XGrabButton(Display* display,                    //2707
    unsigned int button, unsigned int modifiers,
    Window grab_window, Bool owner_events,
    unsigned int event_mask, int pointer_mode,
    int keyboard_mode, Window confine_to,
    Cursor cursor);
extern int XGrabKey(                                        //2720
    Display* display, int keycode, unsigned int modifiers,
    Window grab_window, Bool owner_events,
    int pointer_mode, int keyboard_mode);
extern KeyCode XKeysymToKeycode(                            //2783
    Display* display, KeySym keysym);
extern int XMapWindow(Display* display, Window w);          //2816
extern int XMoveWindow(Display* display,                    //2844
    Window w, int x, int y);
extern int XNextEvent(Display* display,                     //2851
    XEvent* event_return);
extern int XPending(Display* display);                      //2891
extern Bool XQueryExtension(Display* display,               //2980
    const char* name,
    int* major_opcode_return,
    int* first_event_return,
    int* first_error_return);
extern int XResizeWindow(Display* display,                  //3109
    Window w, unsigned int width, unsigned int height);
extern int XSetInputFocus(Display* display, Window focus ,  //3261
    int revert_to ,Time time);
extern int XUngrabButton(Display* display,                  //3472
    unsigned int button, unsigned int modifiers ,
    Window grab_window);
extern int XUnmapWindow(Display* display, Window w);        //3515
"""

ffibuilder.cdef(Misc_h+X_h+Xlib_h+XKB_h+Xutil_h+XComposite_h+XRender_h+Xdamage_h)

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)