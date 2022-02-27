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

import pathlib
import tkinter as tk
import tkinter.ttk as ttk
import pygubu

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "qmgr.ui"

class MainWindow:
    def __init__(self, master=None):
        self.builder = builder = pygubu.Builder() # build
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI) # load UI
        self.window = builder.get_object('window', master) # get main window
        builder.connect_callbacks(self) # connect callbacks

    def run(self):
        self.window.mainloop() # run main loop

if __name__ == '__main__':
    app = MainWindow()
    app.run()