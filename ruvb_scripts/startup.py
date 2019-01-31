# python

"""Script to run on startup to make sure polyset toggle user value is setup"""

import lx

if lx.eval('!!query scriptsysservice userValue.isDefined ? coh.polysets_toggle'):
    pass

else:
    lx.eval('user.defNew coh.polysets_toggle integer')
    lx.eval('user.def coh.polysets_toggle list "on;off"')
