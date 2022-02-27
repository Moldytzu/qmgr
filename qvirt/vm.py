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

import pickle,codecs,dataclasses,sys,json
from contextlib import suppress

@dataclasses.dataclass
class Drive:
    type: str
    file: str
    bus: str

@dataclasses.dataclass
class VMInfo():
    name: str = "Untitled" # vm name
    memoryCapacity: str = "128M" # memory capacity
    cpuCount: int = 1 # cpu sockets/count
    cpuCores: int = 1 # cpu cores
    cpuThreads: int = 1 # cpu threads
    cpuHpet: int = 0 # hpet
    cpuAcpi: int = 1 # acpi
    cpuArch: str = "x86_64" # arch
    cpuModel: str = "base" # model
    machineType: str = "pc" # type
    machineAccelerator: str = "tcg" # acceleration
    biosBootOrder: str = "c" # boot order
    biosBootMenu: int = 1 # boot menu
    biosFile: str = "" # bios
    devices: list = dataclasses.field(default_factory=list) # devices
    usb: int = 0 # usb
    display: int = 1 # display
    displayFull: int = 0 # full screen
    displayType: str = "gtk" # display framework
    displayCard: str = "std" # graphics card
    drives: list = dataclasses.field(default_factory=list) # drives
    unknown: str = "" # additional

def checkSignature(jsonData: object):
    return ("signature" in jsonData) and (jsonData["signature"] == "qvirt") # determine if the signature is qvirt

def getJSON(filename: str):
    file = open(filename,"r") # open file as read-only
    return json.loads(file.read()) # read as json data

def parseJSON(jsonData: object):
    info = VMInfo() # default info already is set

    # parse all json data into a class
    with suppress(KeyError): info.name = jsonData["name"]
    with suppress(KeyError): info.memoryCapacity = jsonData["memory"]["capacity"]
    with suppress(KeyError): info.cpuCount = jsonData["cpu"]["count"]
    with suppress(KeyError): info.cpuCores = jsonData["cpu"]["cores"]
    with suppress(KeyError): info.cpuThreads = jsonData["cpu"]["threads"]
    with suppress(KeyError): info.cpuArch = jsonData["cpu"]["arch"]
    with suppress(KeyError): info.cpuModel = jsonData["cpu"]["model"]
    with suppress(KeyError): info.cpuHpet = jsonData["cpu"]["hpet"]
    with suppress(KeyError): info.cpuAcpi = jsonData["cpu"]["acpi"]
    with suppress(KeyError): info.machineType = jsonData["machine"]["type"]
    with suppress(KeyError): info.machineAccelerator = jsonData["machine"]["accelerator"]
    with suppress(KeyError): info.biosBootOrder = jsonData["bios"]["bootOrder"]
    with suppress(KeyError): info.biosBootMenu = jsonData["bios"]["bootMenu"]
    with suppress(KeyError): info.biosFile = jsonData["bios"]["file"]
    with suppress(KeyError): info.devices = jsonData["devices"]
    with suppress(KeyError): info.usb = jsonData["usb"]["enabled"]
    with suppress(KeyError): info.display = jsonData["display"]["enabled"]
    with suppress(KeyError): info.displayFull = jsonData["display"]["fullscreen"]
    with suppress(KeyError): info.displayType = jsonData["display"]["type"]
    with suppress(KeyError): info.displayCard = jsonData["display"]["card"]
    with suppress(KeyError): info.unknown = jsonData["additionalOptions"]

    with suppress(KeyError):
        drives = jsonData["drives"]
        info.drives = list()
        for drive in drives:
            with suppress(AttributeError):
                info.drives.append(Drive(drives[drive]["type"],drives[drive]["file"],drives[drive]["bus"]))

    return info

def encodeInfo(info: VMInfo):
    return codecs.encode(pickle.dumps(info),"hex").decode().replace("\n","")

def decodeInfo(info: str):
    return pickle.loads(codecs.decode(sys.argv[4].encode(), "hex"))