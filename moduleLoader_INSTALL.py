import maya.cmds as mc
import os



def onMayaDroppedPythonFile(*args):
    """
    Installs the script as a button when it's dragged into the Maya viewport
    """
    shelfName = "Custom"  # Change to existing shelf name if you like.
    buttonLabel = "Module Loader"
    tooltip = "Opens a window for loading modules."
    iconName = "ModLoaderIcon.png"  # Your custom icon file name.

    # Find icon path (assumes icon is next to this .py file)
    scriptPath = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(scriptPath, iconName)

    # Confirm shelf exists.
    if not mc.shelfLayout(shelfName, exists=True):
        print(f"Shelf '{shelfName}' not found. Please create it or change to an existing shelf (e.g., 'Polygons').")
        return

    #remove existing button with same label.
    children = mc.shelfLayout(shelfName, query=True, childArray=True) or []
    for child in children:
        if mc.shelfButton(child, query=True, label=True) == buttonLabel:
            mc.deleteUI(child)

    # Command that will run your tool when the button is clicked.
    cmd = 'import moduleLoader.moduleLoader as ml; ml.ModuleLoader()'

    # Add the button to the shelf.
    mc.shelfButton(
        label=buttonLabel,
        parent=shelfName,
        command=cmd,
        sourceType="Python",
        annotation=tooltip,
        image=icon_path 
        )

    mc.inViewMessage(amg=f"<hl>{buttonLabel}</hl> added to <hl>{shelfName}</hl> shelf!", pos='topCenter', fade=True)


