import maya.cmds as mc
from pathlib import Path
import os

############################
###   BUILD THE WINDOW   ###
############################   

class ModuleLoader():
    """
    Tool window that creates a mod file for a module.
    """
    def __init__(self):
        self.winName = "moduleLoader"
        self.winWidth = 460
        self.winHeight = 360

        if mc.window(self.winName, exists=True):
            mc.deleteUI(self.winName)
        
        mc.window(self.winName, widthHeight=(self.winWidth, self.winHeight), title="Module Loader")

        #Setup the main layout for the window.
        mainLayout = mc.columnLayout(adj=True, margins=10, rowSpacing=15, columnAlign="left", adjustableColumn=True)

        self.modLocInput = mc.textFieldButtonGrp(label="Module Location: ",
                                            parent=mainLayout, 
                                            adjustableColumn=2,
                                            columnAlign=(1, "left"),
                                            columnWidth3=(100, 250, 50),
                                            buttonLabel="Choose Folder",
                                            buttonCommand=lambda: self.get_file_path(self.modLocInput),
                                            placeholderText="Select the folder where your module file is saved."
                                            )
        self.modNameInput = mc.textFieldGrp(label="Module Name: ",
                                            parent=mainLayout, 
                                            adjustableColumn=2,
                                            columnAlign=(1, "left"),
                                            columnWidth3=(60, 100, 50),
                                            placeholderText="Name your module!"
                                            )
        self.modVerInput = mc.textFieldGrp(label="Module Version: ",
                                            parent=mainLayout, 
                                            adjustableColumn=2,
                                            columnAlign=(1, "left"),
                                            columnWidth3=(60, 50, 50),
                                            text="1.0"
                                            )
        self.mayaFolderInput = mc.textFieldButtonGrp(label="Maya Version Folder: ",
                                            parent=mainLayout, 
                                            adjustableColumn=2,
                                            columnAlign=(1, "left"),
                                            columnWidth3=(100, 250, 50),
                                            buttonLabel="Choose Folder",
                                            buttonCommand=lambda: self.get_file_path(self.mayaFolderInput),
                                            placeholderText="Select the version folder of Maya you are working in."
                                            )
        
        #Make the button that runs the tool.
        mc.button(label="Install Module!!",
                  parent=mainLayout,
                  command = self.install_module)


        mc.showWindow()


########################
###   UI FUNCTIONS   ###
########################  
    
    def get_file_path(self, textBox, *argv):
        """
        Opens a fileDialog and inputs the selected filepath into the given textField.
        """
        filePath = mc.fileDialog2(caption="Select a folder: ",
                                fileMode=3,
                                okCaption="Set file path"
                                )
        mc.textFieldGrp(textBox, e=True, text=filePath[0])

    
##########################
###   TOOL FUNCTIONS   ###
########################## 

    def read_data(self, *args):
        """
        Saves and returns the information from the window inputs.
        """
        self.getModLoc = mc.textFieldButtonGrp(self.modLocInput, q=True, text=True) 
        self.getModName = mc.textFieldGrp(self.modNameInput, q=True, text=True)
        self.getModVer = mc.textFieldGrp(self.modVerInput, q=True, text=True)
        self.getMayaFolder = mc.textFieldButtonGrp(self.mayaFolderInput, q=True, text=True)
        return self.getModLoc, self.getModName, self.getModVer, self.getMayaFolder
    

    def mod_file_write(self, *args):
        """
        Writes the .mod file with the infro from the window.
        """
        #Create a mod file.
        open(f"{self.getMayaFolder}/modules/{self.getModName}.mod", "w")
        #Open the file with python for editting.
        modFile = open(file=f"{self.getMayaFolder}/modules/{self.getModName}.mod", mode="w")
        #Write the information into the mod file.
        modFile.write(f"+ {self.getModName} {self.getModVer} {self.getModLoc}\n{self.getModLoc}")


    def install_module(self, *args):
        """
        Uses the inputs in the window install a Maya module. Creates the necessary files and folders if they do not exist.
        """
        self.read_data()     #-> self.getModLoc, self.getModName, self.getModVer, self.getMayaFolder

        #Check if the Maya folder has a "module" folder.
        filePath = Path(fr"{self.getMayaFolder}/modules")
        if not os.path.exists(filePath):
            #Create it if it doesn't exist.
            print(f"{filePath} does not exist.")
            Path.mkdir(f"{self.getMayaFolder}/modules")
        else:
            print(f"{filePath} exists.")
        #Check if a mod file already exists in the "module" folder.
        filePath = Path(f"{self.getMayaFolder}/modules/{self.getModName}.mod")
        if filePath.is_file():
            print(f"{self.getMayaFolder}/modules/{self.getModName}.mod already exists!")
            #If it exists, create a popup asking if you'd like to overwrite the existing file.
            copyCheck = mc.confirmDialog(title="Module File Exists!",
                                        message=f"{self.getModName}.mod already exists at this location. \nDo you want to overwrite it?",
                                        button=["Replace file", "Cancel"],
                                        defaultButton="Replace file",
                                        cancelButton="Cancel"
                                        )
            if copyCheck ==  "Replace file":
                self.mod_file_write()
                print(f"{self.getMayaFolder}/modules/{self.getModName}.mod overwritten.")
            else:
                print("Module installation cancelled.")
        else:
            self.mod_file_write()
            print(f"{self.getMayaFolder}/modules/{self.getModName}.mod created!")
                   
        #Load all module you have installed in Maya.
        mc.loadModule(allModules=True)



ModuleLoader()