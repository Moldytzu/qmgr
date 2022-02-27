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

import pathlib,pygubu,glob
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
        self.vmTree = builder.get_object('vmTree') # get tree
        self.vmName = builder.get_object('vmName') # get name
        self.startButton = builder.get_object('startButton') # get start
        self.modifyButton = builder.get_object('modifyButton') # get modify
        self.deleteButton = builder.get_object('deleteButton') # get delete
        builder.connect_callbacks(self) # connect callbacks

        # populate tree view
        self.populateTree()

    def populateTree(self):
        self.vmTree['columns']=("Name","Path") # set columns
        self.vmTree.column("#0", width=0, stretch=tk.NO) # hide first column
        vms = glob.glob(f"{PROJECT_PATH}/*.vm") # get all vm configs
        for vm in vms:
            jsonData = getJSON(vm)
            if(not checkSignature(jsonData)): continue
            info = parseJSON(jsonData) # get info from each config
            self.vmTree.insert('',tk.END,values=(info.name,vm)) # insert data

    def run(self):
        self.window.mainloop() # run main loop

if __name__ == '__main__':
    app = MainWindow()
    app.run()