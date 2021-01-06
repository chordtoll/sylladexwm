USPosition   = (1 << 0) # user specified x, y */
USSize       = (1 << 1) # user specified width, height */
 
PPosition    = (1 << 2) # program specified position */
PSize        = (1 << 3) # program specified size */
PMinSize     = (1 << 4) # program specified minimum size */
PMaxSize     = (1 << 5) # program specified maximum size */
PResizeInc   = (1 << 6) # program specified resize increments */
PAspect      = (1 << 7) # program specified min and max aspect ratios */
PBaseSize    = (1 << 8) # program specified base for incrementing */
PWinGravity  = (1 << 9) # program specified window gravity */