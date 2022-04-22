import maya.cmds as cmds

AIV_RENAME_TEXTFIELD_NAME = "AIV_RENAME_TEXTFIELD_NAME"

def AIV_rename(items, new_name):
    items = [cmds.rename(item, f"tmp") for item in items]
    for i, item in enumerate(items, 1):
        cmds.rename(item, f"{new_name}{i}")
    
def AIV_rename_UI():
    window = "RenameUI"
    if cmds.window(window, q=True, ex=True):
        cmds.deleteUI(window)
    cmds.window(window, title="AIV Rename")
    cmds.columnLayout(adj=True)
    cmds.text(l="Please enter the new name")
    cmds.textField(AIV_RENAME_TEXTFIELD_NAME)
    cmds.button(l="Rename", c=AIV_rename_command)
    cmds.setParent("..")
    cmds.showWindow(window)
    
def AIV_rename_command(*args):
    new_name = cmds.textField(AIV_RENAME_TEXTFIELD_NAME, q=True, tx=True)
    AIV_rename(cmds.ls(sl=True), new_name)
    
AIV_rename_UI()