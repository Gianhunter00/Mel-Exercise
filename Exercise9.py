#Extend the script that we wrote in class for the zombie rig to also Save the current state of
#the controls and Load the saved states. Write a UI to use all three scripts that we wrote;

import maya.cmds as cmds

AIV_WINDOW_THREE_SCRIPT_NAME = "CHOOSE_SCRIPT"
AIV_WINDOW_FIRST_SCRIPT_NUMBER_OF_TIMES = "NUMBER_OF_TIMES"

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

def save_animation(*args):
    attr_dict = {}
    nurbs = cmds.ls("*_ac_*", "*_fk_*", type="nurbsCurve")
    for nurb in nurbs:
        control = cmds.listRelatives(nurb, p=True)[0]
        attributes = cmds.listAttr(control, keyable=True)
        if attributes is None:
            continue
        for attr in attributes:
            if attr.startswith("translate") or attr.startswith("rotate"):
                attr_dict[f"{control}.{attr}"] = cmds.getAttr(f"{control}.{attr}")
            elif attr.startswith("scale"):
                attr_dict[f"{control}.{attr}"] = cmds.getAttr(f"{control}.{attr}")

        attributes = cmds.listAttr(control, keyable=True, userDefined=True)
        if attributes is None:
            continue
        for attr in attributes:
            attr_dict[f"{control}.{attr}"] = cmds.getAttr(f"{control}.{attr}")
    with open("D://AIV 3//Mel-Exercise//savedSettings.txt", 'w') as f:
        for key in attr_dict.keys():
            f.writelines(f"{str(key)}:{str(attr_dict[key])}\n")
            
def load_animation(*args):
    with open("D://AIV 3//Mel-Exercise//savedSettings.txt", 'r') as f:
        for line in f:
            cmds.setAttr(f"{line.split(':')[0]}", float(line.split(':')[1]))
            

def window_for_the_three_script():
    window = AIV_WINDOW_THREE_SCRIPT_NAME
    if cmds.window(window, q=True, ex=True):
        cmds.deleteUI(window)
    cmds.window(window, title="Choose Script")
    cmds.columnLayout(adj=True)
    cmds.button(l="Duplicate In Line", c="before_opening_window(window_first_script)")
    cmds.button(l="Mirror Selected", c="before_opening_window(window_second_script)")
    cmds.button(l="Save And Load", c="before_opening_window(window_third_script)")
    cmds.setParent("..")
    cmds.showWindow(window)

def window_first_script():
    window = "DuplicateInLine"
    if cmds.window(window, q=True, ex=True):
        cmds.deleteUI(window)
    cmds.window(window, title="Duplicate In Line")
    cmds.columnLayout(adj=True)
    cmds.text(l="Please enter the number of time you want to duplicate")
    cmds.textField(AIV_WINDOW_FIRST_SCRIPT_NUMBER_OF_TIMES)
    cmds.button(l="Duplicate In Line", c=button_duplicate_inline)
    cmds.setParent("..")
    cmds.showWindow(window)
    
def window_second_script():
    window = "DuplicateInLine"
    if cmds.window(window, q=True, ex=True):
        cmds.deleteUI(window)
    cmds.window(window, title="Duplicate In Line")
    cmds.columnLayout(adj=True)
    cmds.button(l="MIRROR", c=mirrorAnimation)
    cmds.setParent("..")
    cmds.showWindow(window)

def window_third_script():
    window = "SaveAndLoadSettings"
    if cmds.window(window, q=True, ex=True):
        cmds.deleteUI(window)
    cmds.window(window, title="Save And Load Settings")
    cmds.columnLayout(adj=True)
    cmds.button(l="SAVE", c=save_animation)
    cmds.button(l="LOAD", c=load_animation)
    cmds.setParent("..")
    cmds.showWindow(window)
    
def delete_window():
    if cmds.window(AIV_WINDOW_THREE_SCRIPT_NAME, q=True, ex=True):
        cmds.deleteUI(AIV_WINDOW_THREE_SCRIPT_NAME)

def button_duplicate_inline(*args):
    sel = cmds.ls(sl=True)
    duplicate_inline(sel[0], sel[1], sel[2], int(cmds.textField(AIV_WINDOW_FIRST_SCRIPT_NUMBER_OF_TIMES, q=True, tx=True)))

def before_opening_window(func, *args):
    delete_window();
    func()
    

window_for_the_three_script()
#save_animation()
#load_animation()