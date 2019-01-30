
################################################################################
#
# scriptname.py
#
# Version:
#
# Author:
#
# Description:
#
# Last Update:
#
################################################################################

# pylint: disable=W0611, W0613, C0103, C0111


import lx
import lxifc
import lxu.command
import ruvb_scripts


class To_Rizom(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add('selection_sets_enabled', lx.symbol.sTYPE_STRING)
        self.basic_SetFlags(0, lx.symbol.fCMDARG_OPTIONAL)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def basic_Enable(self, msg):
        return True

    def cmd_Interact(self):
        pass

    def basic_Execute(self, msg, flags):
        reload(ruvb_scripts)
        ruvb_scripts.rizom_bridge.to_rizom(self)

    def cmd_Query(self, index, vaQuery):
        lx.notimpl()


lx.bless(To_Rizom, "coh.toRizom")


class From_Rizom(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def basic_Enable(self, msg):
        return True

    def cmd_Interact(self):
        pass

    def basic_Execute(self, msg, flags):
        reload(ruvb_scripts)
        ruvb_scripts.rizom_bridge.from_rizom()

    def cmd_Query(self, index, vaQuery):
        lx.notimpl()


lx.bless(From_Rizom, "coh.fromRizom")
