# python

"""Code to be ran on startup to set up important user values"""

import lx


if lx.eval('!!query scriptsysservice userValue.isDefined ? coh.polyset_toggle'):
    pass

else:
    lx.eval('user.defNew coh.polyset_toggle integer')
    lx.eval('user.def coh.polyset_toggle list "on;off"')
