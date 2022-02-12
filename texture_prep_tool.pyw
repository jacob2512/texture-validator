import os

import wx
import wx.lib.inspection
from git import Repo

class MainFrame(wx.Frame):
    
    def __init__(self):
        
        # constants
        self.debug_enabled = False
        
        self.base_repo_path = os.path.abspath(os.getcwd())+"\\TestRepo"
        self.base_texture_dir = "TestProject\\Assets\\Textures"
        
        self.max_name_length = 64
        self.max_path_length = 260 # based on old Windows path limit
        
        # derived from the following articles:
        # https://ikrima.dev/ue4guide/wip/assets-naming-convention/
        # https://github.com/Allar/ue5-style-guide
        self.approved_prefixes = [
            "T_" # Texture
            ]
        self.approved_suffixes = [
            "_A",  # Alpha/Opacity Map
            "_AO", # Ambient Occlusion Map
            "_B",  # Bump Map
            "_C",  # Color Map
            "_D",  # Diffuse/Albedo/Base Color Map
            "_DP", # Displacement Map
            "_E",  # Emissive Map
            "_F",  # Flow Map
            "_H",  # Height Map
            "_L",  # Light Map
            "_M",  # Mask Map
            "_MT", # Metallic Map
            "_N",  # Normal Map
            "_R",  # Roughness Map
            "_S"   # Specular Map
            ]
        self.tx_type_map = {
            "Characters":"CHR",
            "Environments":"ENV",
            "Materials":"MAT"
        }
        
        self.default_text_color = wx.TextAttr(wx.NamedColour("BLACK"))
        self.error_text_color = wx.TextAttr(wx.NamedColour("RED"))
        self.success_text_color = wx.TextAttr(wx.NamedColour("BLUE"))
        self.versioncontrol_text_color = wx.TextAttr(wx.NamedColour("DARK SLATE BLUE"))
        
        # UI construction
        
        wx.Frame.__init__(self, None, wx.ID_ANY, title='Texture Prep Tool', size=(1080,720))
        
        self.main_panel = wx.Panel(self, id=wx.ID_ANY)
        
        # selection
        self.selection_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.selection_label = wx.StaticText(self.main_panel, label='1. Select the Texture')
        self.selection_sizer.Add(self.selection_label, proportion=0, flag=wx.ALL|wx.LEFT, border=5)
        
        self.selection_filepath = wx.TextCtrl(self.main_panel, id=wx.ID_ANY, style=wx.TE_MULTILINE|wx.TE_READONLY)
        # self.selection_filepath.SetEditable(0)
        # self.selection_filepath.Disable()
        self.selection_filepath.SetToolTip(wx.ToolTip("Full File Path of the Selected Texture"))
        self.selection_sizer.Add(self.selection_filepath, proportion=1, flag=wx.ALL|wx.CENTER, border=5)
        
        self.selection_button = wx.Button(self.main_panel, label='Select')
        self.selection_button.Bind(wx.EVT_BUTTON, self.onSelectionButtonClick)
        self.selection_button.SetToolTip(wx.ToolTip("Textures of the following types can be selected: bmp, jpg, png"))
        self.selection_sizer.Add(self.selection_button, proportion=0, flag=wx.ALL|wx.RIGHT, border=5)
        
        # validation
        self.validation_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.validation_label = wx.StaticText(self.main_panel, label='2. Validate Texture Name')
        self.validation_sizer.Add(self.validation_label, proportion=0, flag=wx.ALL|wx.LEFT, border=5)
        
        self.validation_button = wx.Button(self.main_panel, label='Validate')
        self.validation_button.Bind(wx.EVT_BUTTON, self.onValidationButtonClick)
        
        self.validation_button.SetToolTip(wx.ToolTip( 
            ("Name Validation Rules:\n"
            "-Only alphabets, numbers, and underscore are allowed\n"
            "-Path name length should be less than "+str(self.max_path_length)+"\n"
            "-File name length should be less than "+str(self.max_name_length)+"\n"
            "-Should start with any of the following: "+str(self.approved_prefixes)+"\n"
            "-Should have an infix right after the prefix: "+str(self.tx_type_map)+"\n"
            "-Should end with any of the following: "+str(self.approved_suffixes)+"\n"
            ) 
            ))
        
        self.validation_button.Disable()
        self.validation_sizer.Add(self.validation_button, proportion=0, flag=wx.ALL|wx.RIGHT, border=5)
        
        self.validation_separator = wx.StaticLine(self.main_panel, style=wx.LI_VERTICAL)
        self.validation_sizer.Add(self.validation_separator, proportion=0, flag=wx.EXPAND|wx.CENTER, border=5)
        
        # rename (optional part of validation)
        self.rename_label = wx.StaticText(self.main_panel, label='2.1 Rename Texture')
        self.validation_sizer.Add(self.rename_label, proportion=0, flag=wx.ALL|wx.LEFT, border=5)
        
        self.rename_newname = wx.TextCtrl(self.main_panel, id=wx.ID_ANY)
        self.rename_newname.Bind(wx.EVT_CHAR, self.onRenameKeypress)
        self.rename_newname.Disable()
        self.validation_sizer.Add(self.rename_newname, proportion=1, flag=wx.ALL|wx.CENTER, border=5)
        
        self.rename_button = wx.Button(self.main_panel, label='Rename')
        self.rename_button.Bind(wx.EVT_BUTTON, self.onRenameButtonClick)
        self.rename_button.Disable()
        self.validation_sizer.Add(self.rename_button, proportion=0, flag=wx.ALL|wx.RIGHT, border=5)
        
        # submission
        self.submission_sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.submission_label = wx.StaticText(self.main_panel, label='3. Submit to Version Control')
        self.submission_sizer.Add(self.submission_label, proportion=0, flag=wx.ALL|wx.LEFT, border=5)
        
        self.submission_note = wx.TextCtrl(self.main_panel, id=wx.ID_ANY, style=wx.TE_MULTILINE|wx.TE_READONLY)
        self.submission_note.Disable()
        self.submission_sizer.Add(self.submission_note, proportion=1, flag=wx.EXPAND, border=5)
        
        self.submission_button = wx.Button(self.main_panel, label='Submit')
        self.submission_button.Bind(wx.EVT_BUTTON, self.onSubmissionButtonClick)
        self.submission_button.Disable()
        self.submission_sizer.Add(self.submission_button, proportion=0, flag=wx.ALL | wx.CENTER, border=5)
        
        # output
        self.output_sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.output_label = wx.StaticText(self.main_panel, label='Output:')
        self.output_sizer.Add(self.output_label, proportion=0, flag=wx.ALL|wx.LEFT, border=5)
        
        self.log_output = wx.TextCtrl(self.main_panel, id=wx.ID_ANY, style=wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_RICH)
        self.output_sizer.Add(self.log_output, proportion=1, flag=wx.ALL|wx.EXPAND, border=5)
        
        self.log_output.SetFocus()
        
        # add all parts to main panel
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.main_sizer.Add(self.selection_sizer, proportion=0, flag=wx.ALL|wx.EXPAND, border=5)
        self.main_sizer.Add(self.validation_sizer, proportion=0, flag=wx.ALL|wx.EXPAND, border=5)
        self.main_sizer.Add(self.submission_sizer, proportion=0, flag=wx.ALL|wx.EXPAND, border=5)
        self.main_sizer.Add(self.output_sizer, proportion=1, flag=wx.ALL|wx.EXPAND, border=5)
        self.main_panel.SetSizer(self.main_sizer)
        
        self.debugTests()
        
        self.Layout()
        if self.debug_enabled:
            wx.lib.inspection.InspectionTool().Show()
        self.Show()
        

    def printToLog(self, message, color=None):
        print(str(message))
        if color:
            self.log_output.SetDefaultStyle(color)
        self.log_output.AppendText(str(message)+"\n")
        if color:
            self.log_output.SetDefaultStyle(self.default_text_color)
        
    def debugTests(self):
        # self.printToLog(self.base_texture_dir)
        # self.printToLog(self.hasValidPrefix("T_est_texture"))
        # self.printToLog(self.hasValidCharacters("ss_T9_"))
        
        self.repo = Repo(self.base_repo_path)
        # print(self.repo.working_tree_dir)
        # print(self.repo.is_dirty())
        
        # self.repo.git.reset() # git reset
        # self.printToLog("//Version Control Status//:\n"+self.repo.git.status(), self.versioncontrol_text_color) # git status
        
        # self.repo.git.add(all=True) # get all changes -> git add -A
        # self.repo.git.add("TestProject/Assets/Textures/Environments/T_ENV_sddsd02_N.png")
        # self.repo.index.remove("TestProject/Assets/Textures/Environments/T_ENV_sddsd02_N.png")
        
        print(self.repo.head) #HEAD
        print(self.repo.active_branch.name) #master
        print(self.repo.head.reference) #master
        print(self.repo.bare) # False, even with no commits and no tracked files
        print(self.repo.untracked_files)
        
        return
        

    def onSelectionButtonClick(self, event):
        self.printToLog("Selection in progress...")

        openFileDialog = wx.FileDialog(self, 
            message="Select Texture File", defaultDir="", defaultFile="", 
            wildcard="Texture files (*.bmp;*.jpg;*.png)|*.bmp;*.jpg;*.png", 
            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

        openFileDialog.ShowModal()
        self.selection_filepath.SetValue(openFileDialog.GetPath())
        openFileDialog.Destroy()
        
        self.printToLog("selected \""+ self.selection_filepath.GetValue()+"\"")
        
        # set validation and submission section state
        if len(self.selection_filepath.GetValue()) > 0:
        
            self.validation_button.Enable()
            self.rename_newname.Enable()
            self.rename_button.Enable()
            
        else:
            self.validation_button.Disable()
            self.rename_newname.Disable()
            self.rename_button.Disable()
        
        # submission should always be closed at this point
        self.submission_note.SetValue("")
        self.submission_note.Disable()
        self.submission_button.Disable()
            
    
    def isValidChar(self, char):
        if ord(char) < 255:
            # valid ASCII
            if (char.isalnum() or char == '_'
                or ord(char) == wx.WXK_BACK
                or ord(char) == wx.WXK_DELETE
                ):
                return True
        
        return False

    def hasValidCharacters(self, name):
        for char in name:
            if not self.isValidChar(char):
                return False
                
        return True
    
    def hasValidPathLength(self,path):
        if len(path) < self.max_path_length:
            return True
        
        return False
        
    def hasValidNameLength(self,name):
        if len(name) < self.max_name_length:
            return True
        
        return False
    
    def hasValidPrefix(self, name):
        for prefix in self.approved_prefixes:
            if name.startswith(prefix):
                return True
        
        return False
        
    def hasValidTypeInfix(self, path, name):
        parent_folder = path.split('\\')[-2]
        # print("pf is "+parent_folder)
        
        for folder,infix in self.tx_type_map.items():
            if folder == parent_folder:
                infix_array = name.split('_')
                if len(infix_array) > 2: # has to have at least prefix and infix
                    curr_infix = infix_array[1]
                    # print("ifx is "+curr_infix)
                    if infix == curr_infix:
                        return True
        
        return False
        
    def hasValidSuffix(self, name):
        for suffix in self.approved_suffixes:
            if name.endswith(suffix):
                return True
        
        return False

    def getRepoPath(self, path):
        return (self.base_texture_dir+str(path.split(self.base_texture_dir)[1])).replace("\\","/")
        
    def isNewFile(self, path):
        return (self.getRepoPath(path) in self.repo.untracked_files)

    def setSubmissionNote(self, path):
        
        commit_message = ""
        if self.isNewFile(path): # not yet in repo
            commit_message = "Adding "+self.getRepoPath(path)+"."
        else: # already in repo
            commit_message = "Changing "+self.getRepoPath(path)+"."
        
        # populate commit field with text
        self.submission_note.SetValue(commit_message)
        
    
    def onValidationButtonClick(self, event):
        self.printToLog("Validation requested...")
        
        full_path = self.selection_filepath.GetValue()
        curr_dir = os.path.dirname(full_path)
        # self.printToLog("dir is "+curr_dir)
        curr_filename = os.path.basename(full_path).split(".")[0]
        
        is_valid = True
                    
        if not self.hasValidCharacters(curr_filename):
            self.printToLog(curr_filename+" has invalid characters. Only alphabets, numbers, and underscore are allowed.", self.error_text_color)
            is_valid = False
        
        if not self.hasValidPathLength(full_path):
            self.printToLog(full_path+" has length "+len(full_path)+". Path name length should be less than "+ self.max_path_length, self.error_text_color)
            is_valid = False
            
        if not self.hasValidNameLength(curr_filename):
            self.printToLog(curr_filename+" has length "+len(curr_filename)+". File name length should be less than "+ self.max_name_length, self.error_text_color)
            is_valid = False
            
        if not self.hasValidPrefix(curr_filename):
            self.printToLog(curr_filename+" does not have a valid prefix. Please use any of the following: "+str(self.approved_prefixes), self.error_text_color)
            is_valid = False
        
        if not self.hasValidTypeInfix(full_path, curr_filename):
            self.printToLog(curr_filename+" does not have a valid type infix. The folder-to-infix mapping is "+str(self.tx_type_map), self.error_text_color)
            is_valid = False
        
        if not self.hasValidSuffix(curr_filename):
            self.printToLog(curr_filename+" does not have a valid suffix. Please use any of the following: "+str(self.approved_suffixes), self.error_text_color)
            is_valid = False
        
        # determine submission state
        if is_valid:
            self.printToLog(full_path+" has passed all validation checks - Submission Allowed.", self.success_text_color)
            self.submission_note.Enable()
            self.setSubmissionNote(full_path)
            self.submission_button.Enable()
        else:
            self.printToLog(full_path+" has failed validation checks - Please rectify and re-Validate.", self.error_text_color)
            self.submission_note.SetValue("")
            self.submission_note.Disable()
            self.submission_button.Disable()
        
        
    def onRenameKeypress(self, event):
        keycode = event.GetKeyCode()
        if self.isValidChar(chr(keycode)):
            # self.printToLog(keycode)
            event.Skip()

    
    def renameFile(self, file_dir, old_filename, new_filename, file_ext):
        old_filename_w_path = os.path.join(file_dir, old_filename+"."+file_ext)
        new_filename_w_path = os.path.join(file_dir, new_filename+"."+file_ext)
        
        self.printToLog("old path is "+old_filename_w_path)
        self.printToLog("new path is "+new_filename_w_path)
        os.rename(old_filename_w_path, new_filename_w_path)
        
        self.printToLog("File renamed from "+old_filename+"."+file_ext+" to "+new_filename+"."+file_ext+".", self.success_text_color)
        
    def onRenameButtonClick(self, event):
        self.printToLog("Rename requested...")
        
        new_filename = self.rename_newname.GetValue()
        if len(new_filename) > 0:
            full_path = self.selection_filepath.GetValue()
            curr_dir = os.path.dirname(full_path)
            # self.printToLog("dir is "+curr_dir)
            curr_filename = os.path.basename(full_path).split(".")[0]
            # self.printToLog("name is "+curr_filename)
            curr_ext = full_path.split(".")[1]
            # self.printToLog("ext is "+curr_ext)
            new_full_path = curr_dir+"\\"+new_filename+"."+curr_ext
            if os.path.exists(new_full_path):
                self.printToLog("File with name "+new_filename+" already exists in "+curr_dir+". Please choose another name.", self.error_text_color)
            else:
                self.renameFile(curr_dir,curr_filename,new_filename,curr_ext)
                
                # reset all UI elements after a rename
                self.selection_filepath.SetValue("")
                
                self.validation_button.Disable()
                self.rename_newname.SetValue("")
                self.rename_newname.Disable()
                self.rename_button.Disable()
                
                self.submission_note.SetValue("")
                self.submission_note.Disable()
                
    
    def onSubmissionButtonClick(self, event):
        self.printToLog("Submission requested...")
        
        full_path = self.selection_filepath.GetValue()
        
        if self.isNewFile(full_path):        
            self.repo.git.add(full_path)
            self.printToLog("//Version Control Status//:\n"+self.repo.git.status(), self.versioncontrol_text_color) # git status
        
        commit_note = self.submission_note.GetValue()
        self.repo.git.commit('-m',commit_note) #git commit -m 'commit note' ./path/to/my/file.ext
        self.printToLog("//Version Control Status//:\n"+self.repo.git.status(), self.versioncontrol_text_color) # git status
        
        
if __name__ == '__main__':
    app = wx.App()
    main_frame = MainFrame()
    app.MainLoop()