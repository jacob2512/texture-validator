import wx
import wx.lib.inspection

import os

class MainFrame(wx.Frame):
    
    def __init__(self):
    
        self.debug_enabled = False
        
        self.base_texture_dir = os.path.abspath(os.getcwd())+"\\TestRepo\\TestProject\\Assets\\Textures"
        # self.prefix_map = {
        #     "Characters":"CHR",
        #     "Environments":"ENV",
        #     "Materials":"MAT"
        # }
        
        
        wx.Frame.__init__(self, None, wx.ID_ANY, title='Texture Prep Tool', size=(1080,720))
        
        self.main_panel = wx.Panel(self, id=wx.ID_ANY)
        
        # self.provider = wx.SimpleHelpProvider()
        # wx.HelpProvider.Set(self.provider)
        
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
        self.validation_button.SetToolTip(wx.ToolTip("Validation rules"))
        self.validation_button.Disable();
        self.validation_sizer.Add(self.validation_button, proportion=0, flag=wx.ALL|wx.RIGHT, border=5)
        
        self.validation_separator = wx.StaticLine(self.main_panel, style=wx.LI_VERTICAL)
        self.validation_sizer.Add(self.validation_separator, proportion=0, flag=wx.EXPAND|wx.CENTER, border=5)
        
        # rename (optional)
        
        self.rename_label = wx.StaticText(self.main_panel, label='2.1 Rename Texture')
        self.validation_sizer.Add(self.rename_label, proportion=0, flag=wx.ALL|wx.LEFT, border=5)
        
        self.rename_newname = wx.TextCtrl(self.main_panel, id=wx.ID_ANY)
        self.rename_newname.Bind(wx.EVT_CHAR, self.onRenameKeypress)
        self.rename_newname.Disable();
        self.validation_sizer.Add(self.rename_newname, proportion=1, flag=wx.ALL|wx.CENTER, border=5)
        
        self.rename_button = wx.Button(self.main_panel, label='Rename')
        self.rename_button.Bind(wx.EVT_BUTTON, self.onRenameButtonClick)
        self.rename_button.Disable();
        self.validation_sizer.Add(self.rename_button, proportion=0, flag=wx.ALL|wx.RIGHT, border=5)
        
        # submission
        self.submission_sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.submission_label = wx.StaticText(self.main_panel, label='3. Submit to Version Control')
        self.submission_sizer.Add(self.submission_label, proportion=0, flag=wx.ALL|wx.LEFT, border=5)
        
        self.submission_note = wx.TextCtrl(self.main_panel, id=wx.ID_ANY, style=wx.TE_MULTILINE|wx.TE_READONLY)
        self.submission_sizer.Add(self.submission_note, proportion=1, flag=wx.EXPAND, border=5)
        
        self.submission_button = wx.Button(self.main_panel, label='Submit')
        self.submission_button.Bind(wx.EVT_BUTTON, self.onSubmissionButtonClick)
        self.submission_button.Disable();
        self.submission_sizer.Add(self.submission_button, proportion=0, flag=wx.ALL | wx.CENTER, border=5)
        
        # output
        self.output_sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.output_label = wx.StaticText(self.main_panel, label='Output:')
        self.output_sizer.Add(self.output_label, proportion=0, flag=wx.ALL|wx.LEFT, border=5)
        
        self.log_output = wx.TextCtrl(self.main_panel, id=wx.ID_ANY, style=wx.TE_MULTILINE|wx.TE_READONLY)
        self.output_sizer.Add(self.log_output, proportion=1, flag=wx.ALL|wx.EXPAND, border=5)
        
        self.log_output.SetFocus()
        
        # add all parts to main panel
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.main_sizer.Add(self.selection_sizer, proportion=0, flag=wx.ALL|wx.EXPAND, border=5)
        self.main_sizer.Add(self.validation_sizer, proportion=0, flag=wx.ALL|wx.EXPAND, border=5)
        self.main_sizer.Add(self.submission_sizer, proportion=0, flag=wx.ALL|wx.EXPAND, border=5)
        self.main_sizer.Add(self.output_sizer, proportion=1, flag=wx.ALL|wx.EXPAND, border=5)
        self.main_panel.SetSizer(self.main_sizer)
        
        
        # self.printToLog(self.base_texture_dir)
        
        self.Layout()
        if self.debug_enabled:
            wx.lib.inspection.InspectionTool().Show()
        self.Show()
        
        

    def printToLog(self, message):
        print(str(message))
        self.log_output.AppendText(str(message)+"\n")
        

    def onSelectionButtonClick(self, event):
        self.printToLog("Selection Button clicked.")

        openFileDialog = wx.FileDialog(self, 
            message="Select Texture File", defaultDir="", defaultFile="", 
            wildcard="Texture files (*.bmp;*.jpg;*.png)|*.bmp;*.jpg;*.png", 
            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

        openFileDialog.ShowModal()
        self.selection_filepath.SetValue(openFileDialog.GetPath())
        openFileDialog.Destroy()
        
        self.printToLog("selected "+ self.selection_filepath.GetValue())
        
        # set validation button state
        if len(self.selection_filepath.GetValue()) > 0:
            self.validation_button.Enable();
            self.rename_newname.Enable();
            self.rename_button.Enable();
        else:
            self.validation_button.Disable();
            self.rename_newname.Disable();
            self.rename_button.Disable();
    
    def hasValidPrefix(self, name):
        return
        
    def hasValidSuffix(self, name):
        return

    def hasValidCharacters(self, name):
        return

    def onValidationButtonClick(self, event):
        self.printToLog("Validation Button clicked.")
        
        full_path = self.selection_filepath.GetValue()
        # curr_dir = os.path.dirname(full_path)
        # self.printToLog("dir is "+curr_dir)
        # curr_filename = os.path.basename(full_path).rsplit(".")[0]
        
        if self.isValidPrefix(full_path):
            return
        
        # check for name length

        # check for path length
        
        # check for duplicates in repo
        
        
    def onRenameKeypress(self, event):
        keycode = event.GetKeyCode()
        if keycode < 255:
            # valid ASCII
            if (chr(keycode).isalnum() or chr(keycode) == '_'
                or keycode == wx.WXK_BACK
                or keycode == wx.WXK_DELETE
                ):
                # Valid keycode
                # self.printToLog(keycode)
                event.Skip()
                
    
    def renameFile(self, file_dir, old_filename, new_filename, file_ext):
        old_filename_w_path = os.path.join(file_dir, old_filename+"."+file_ext)
        new_filename_w_path = os.path.join(file_dir, new_filename+"."+file_ext)
        
        self.printToLog(old_filename_w_path)
        self.printToLog(new_filename_w_path)
        os.rename(old_filename_w_path, new_filename_w_path)
        
        self.printToLog("renamed from "+old_filename+" to "+new_filename)
        
    def onRenameButtonClick(self, event):
        self.printToLog("Rename Button clicked.")
        
        new_filename = self.rename_newname.GetValue()
        if len(new_filename) > 0:
            full_path = self.selection_filepath.GetValue()
            curr_dir = os.path.dirname(full_path)
            # self.printToLog("dir is "+curr_dir)
            curr_filename = os.path.basename(full_path).rsplit(".")[0]
            # self.printToLog("name is "+curr_filename)
            curr_ext = full_path.rsplit(".")[1]
            # self.printToLog("ext is "+curr_ext)
            self.renameFile(curr_dir,curr_filename,new_filename,curr_ext)
    
    
    def onSubmissionButtonClick(self, event):
        self.printToLog("Submission Button clicked.")
    
    
if __name__ == '__main__':
    app = wx.App()
    main_frame = MainFrame()
    app.MainLoop()