#Write a script that will work with the zombie rig and based on selected ctrls
#make the other side symmetrical (so that both sides look the same). 
#The minimum for this assignments should be a proc that will take whatever 
#is selected and mirror the attribute values to the other side.
#Write a little UI around it that lets the user specify if they want to mirror
#or if they want to switch (so that the right will be like left and left will be like right).

import maya.cmds as cmds


def mirrorAnimation(*args):
    nurbs = cmds.ls(sl=True)
    for nurb in nurbs:
        control = nurb
        control_mirror = control.split("_")
        control_mirror = "_".join(["lf" if name == "rt" else "rt" if name == "lf" else name for name in control_mirror])
        attributes = cmds.listAttr(control_mirror, keyable=True)
        if attributes is None:
            continue
        for attr in attributes:
            if attr.startswith("translate"):
                cmds.setAttr(f"{control_mirror}.{attr}", -cmds.getAttr(f"{control}.{attr}"))
            elif attr.startswith("rotate"):
                cmds.setAttr(f"{control_mirror}.{attr}", cmds.getAttr(f"{control}.{attr}"))
            elif attr.startswith("scale"):
                cmds.setAttr(f"{control_mirror}.{attr}", cmds.getAttr(f"{control}.{attr}"))

        attributes = cmds.listAttr(control_mirror, keyable=True, userDefined=True)
        if attributes is None:
            continue
        for attr in attributes:
            cmds.setAttr(f"{control_mirror}.{attr}", cmds.getAttr(f"{control}.{attr}"))

mirrorAnimation()