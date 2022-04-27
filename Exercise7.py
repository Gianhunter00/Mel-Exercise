#Write a procedure that has 4 arguments: 3 strings (objA, objB, objC) and 1 int x_number
#when running the proc, objC should get duplicated x_number of times
#and be distributed evenly in a line between objA and objB.
import maya.cmds as cmds

def duplicate_inline(obja, objb, objc, x_number, *args):
    bb_x_max_a = cmds.getAttr(obja + ".boundingBoxMaxX")
    bb_x_min_a = cmds.getAttr(obja + ".boundingBoxMinX")
    obj_width_a = (bb_x_max_a - bb_x_min_a)

    bb_x_max_b = cmds.getAttr(objb + ".boundingBoxMaxX")
    bb_x_min_b = cmds.getAttr(objb + ".boundingBoxMinX")
    obj_width_b = (bb_x_max_b - bb_x_min_b)

    bb_x_max_c = cmds.getAttr(objc + ".boundingBoxMaxX")
    bb_x_min_c = cmds.getAttr(objc + ".boundingBoxMinX")
    obj_width_c = (bb_x_max_c - bb_x_min_c)

    pos_a = cmds.getAttr(obja + ".translate")[0]
    pos_b = cmds.getAttr(objb + ".translate")[0]
    for i in range(x_number):
        pos_a = (pos_a[0] + obj_width_a + obj_width_c + (obj_width_c * i), pos_a[1], pos_a[2])
        pos_b = (pos_b[0] + obj_width_b + obj_width_c + (obj_width_c * i), pos_b[1], pos_b[2])

        cmds.move(pos_a[0], pos_a[1], pos_a[2], objc)
        cmds.duplicate(objc, rr=True)

        cmds.move(pos_b[0], pos_b[1], pos_b[2], objc)
        cmds.duplicate(objc, rr=True)
    cmds.delete(objc)
    
sel = cmds.ls(sl=True)
duplicate_inline(sel[0], sel[1], sel[2], 5)