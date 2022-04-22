import maya.cmds as cmds

#cmds.polyCube(w=1, h=1, d=1, sx=1, sy=1, sz=1, ax=(0, 1, 0), cuv=4, ch=1)
#sphere = cmds.polySphere()
#cmds.move(-2, 0, 0, sphere, r=True)
#
# cmds.window()
# if True:
#    cmds.rowLayout()
#
#    cmds.setParent("..")
#
# cmds.showWindow()

import maya.cmds as cmds
import random

def duplicateOnCurve():
    selection = cmds.ls(sl=True)
    curve = selection[0]
    obj = selection[1]
    bb_x_max = cmds.getAttr(obj + ".boundingBoxMaxX")
    bb_x_min = cmds.getAttr(obj + ".boundingBoxMinX")
    
    obj_width = (bb_x_max - bb_x_min) * 0.6
    
    mpo = cmds.pathAnimation(curve, obj,
                             fractionMode=True,
                             follow=True,
                             followAxis="x",
                             upAxis="y",
                             worldUpType="vector",
                             worldUpVector=(0, 1, 0))

    curve_len = cmds.arclen(curve)

    nr_duplicates = int(curve_len/obj_width)

    step = 1/nr_duplicates

    for i in range(nr_duplicates):
        cmds.setAttr(mpo + ".uValue", step * i)
        cmds.xform(obj, q=True, ws=True, t=True)
        dup = cmds.duplicate(obj)
        rot_x = random.randint(-15, 15)
        if i % 2:
            rot_x += 90
        cmds.rotate(rot_x, 0, 0, dup, r=True, os=True, fo=True)
    cmds.delete(obj)    

duplicateOnCurve()