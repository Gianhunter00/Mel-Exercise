import maya.cmds as cmds

def resetAnimation(nurbs):
    for nurb in nurbs:
        control = cmds.listRelatives(nurb, p=True)[0]
        attributes = cmds.listAttr(control, keyable=True)
        if attributes is None:
            continue
        for attr in attributes:
            if attr.startswith("translate") or attr.startswith("rotate"):
                cmds.setAttr(f"{control}.{attr}", 0)
            elif attr.startswith("scale"):
                cmds.setAttr(f"{control}.{attr}", 1)

        attributes = cmds.listAttr(control, keyable=True, userDefined=True)
        if attributes is None:
            continue
        for attr in attributes:
            dv = cmds.addAttr(f"{control}.{attr}", q=True, dv=True)
            cmds.setAttr(f"{control}.{attr}", dv)

items = cmds.ls("*_ac_*", "*_fk_*", type="nurbsCurve")
resetAnimation(items)