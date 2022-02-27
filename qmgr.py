'''
    qmgr
    Copyright (C) 2022  Moldovan Alexandru

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

from genericpath import exists
import os
import pathlib,pygubu,glob
from tkinter import messagebox
import tkinter as tk
from qvirt.vm import *

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "qmgr.ui"

class MainWindow:
    def __init__(self, master=None):
        self.builder = builder = pygubu.Builder() # build
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI) # load UI
        self.window = builder.get_object('window') # get main window
        self.newdialog = builder.get_object('newDialog') # get dialog
        self.modifydialog = builder.get_object('modifyDialog') # get modify dialog
        self.vmTree = builder.get_object('vmTree') # get tree
        self.vmName = builder.get_object('vmName') # get name
        self.startButton = builder.get_object('startButton') # get start
        self.modifyButton = builder.get_object('modifyButton') # get modify
        self.deleteButton = builder.get_object('deleteButton') # get delete
        self.newButton = builder.get_object('newButton') # get new
        self.okButton = builder.get_object('okButton') # get ok
        self.nameEntry = builder.get_object('name') # name entry
        builder.connect_callbacks(self) # connect callbacks

        self.selected = []
        self.startButton.config(command = self.startVM)
        self.newButton.config(command = self.newVM)
        self.okButton.config(command = self.doNewVM)
        self.deleteButton.config(command = self.deleteVM)
        self.newdialog.withdraw() # hide new dialog

        # populate tree view
        self.populateTree()

    def populateTree(self):
        self.vmTree.bind("<ButtonRelease-1>",self.onItemSelect)
        self.vmTree.delete(*self.vmTree.get_children()) # delete all items first
        self.vmTree['columns']=("Name","Path") # set columns
        self.vmTree.column("#0", width=0, stretch=tk.NO) # hide first column
        self.vmTree.column("Name", width=100, stretch=tk.NO) # hide first column
        self.vmTree.column("Path", width=500, stretch=tk.NO) # hide first column
        vms = glob.glob(f"{PROJECT_PATH}/vms/*.vm") # get all vm configs
        for vm in vms:
            jsonData = getJSON(vm)
            if(not checkSignature(jsonData)): continue
            info = parseJSON(jsonData) # get info from each config
            self.vmTree.insert('',tk.END,values=(info.name,vm)) # insert data

    def onItemSelect(self, event):
        item = self.vmTree.item(self.vmTree.focus())
        if(item["values"] == ""): return # skip if not clicked on an item
        self.selected = item["values"]
        self.vmName.config(text = item["values"][0])

    def startVM(self):
        if(self.selected == []): return # skip if no item is selected
        self.window.withdraw()
        info = parseJSON(getJSON(self.selected[1])) # get info from the vm
        startVM(info)
        self.window.deiconify()

    def newVM(self):
        self.newdialog.deiconify()

    def deleteVM(self):
        if(self.selected == []): return # skip if no item is selected
        if(messagebox.askquestion("qmgr","Are you sure you want to delete this virtual machine?") == "no"): return
        os.remove(self.selected[1])
        self.populateTree() # refresh tree
    
    def doNewVM(self):
        fname = f"./vms/{self.nameEntry.get()}.vm"
        if(exists(fname)):
            messagebox.showinfo("qmgr",f"Can't create {fname}. A machine with that filename already exists.") # don't overwrite
            return # return
        info = VMInfo()
        info.name = self.nameEntry.get() # set name
        exportInfo(info,fname)
        self.populateTree() # refresh tree
        self.nameEntry.delete(0, tk.END) # delete text from extry
        self.newdialog.withdraw() # hide the dialog

    def run(self):
        self.window.mainloop() # run main loop

if __name__ == '__main__':
    app = MainWindow()
    app.run()