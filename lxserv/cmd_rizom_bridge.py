# pylint: disable=W0611, W0613, C0103, C0111


import lx
import lxifc
import lxu.command
import ruvb_scripts


class To_Rizom(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def basic_Enable(self, msg):
        return True

    def cmd_Interact(self):
        pass

    def basic_Execute(self, msg, flags):
        ruvb_scripts.rizom_bridge.to_rizom()

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
        ruvb_scripts.rizom_bridge.from_rizom()

    def cmd_Query(self, index, vaQuery):
        lx.notimpl()


lx.bless(From_Rizom, "coh.fromRizom")


class Rizom_Path(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def basic_Enable(self, msg):
        return True

    def cmd_Interact(self):
        pass

    def basic_Execute(self, msg, flags):
        ruvb_scripts.rizom_bridge.rizom_path_update()

    def cmd_Query(self, index, vaQuery):
        lx.notimpl()


lx.bless(Rizom_Path, "coh.rizomPath")
