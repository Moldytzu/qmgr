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

import sys,json,dataclasses,subprocess
from contextlib import suppress

@dataclasses.dataclass
class Drive:
    type: str
    file: str
    bus: str

@dataclasses.dataclass
class VMInfo:
    name: str
    memoryCapacity: str
    cpuCount: int
    cpuCores: int
    cpuThreads: int
    cpuHpet: int
    cpuAcpi: int
    cpuArch: str
    cpuModel: str
    machineType: str
    machineAccelerator: str
    biosBootOrder: str
    biosBootMenu: int
    biosFile: str
    devices: list
    usb: int
    display: int
    displayFull: int
    displayType: str
    displayCard: str
    drives: list
    unknown: str

def startVM(vminfo: VMInfo):
    print(f"Starting \"{vminfo.name}\" virtual machine") # print starting message

    command = f"qemu-system-{vminfo.cpuArch} " # create the command we will launch
    command += f"-m {vminfo.memoryCapacity} " # append memory information
    command += f"-smp maxcpus={vminfo.cpuCores * vminfo.cpuCount * vminfo.cpuThreads},sockets={vminfo.cpuCount},cores={vminfo.cpuCores},threads={vminfo.cpuThreads} " # append cpu topology
    command += f"-cpu {vminfo.cpuModel} " # append cpu model
    command += f"-M type={vminfo.machineType},accel={vminfo.machineAccelerator} " # append machine info
    command += f"-boot order={vminfo.biosBootOrder},menu=" # boot menu and boot order
    command += "on " if vminfo.biosBootMenu == 1 else "off " 

    if(vminfo.display == 1):
        command += f"-display {vminfo.displayType} " # display type
        command += f"-vga {vminfo.displayCard} " # video card
        if(vminfo.displayFull): command += f"-full-screen -no-quit " # full screen
    else:
        command += f"-nographic " # no graphics

    for drive in vminfo.drives:
        command += f"-drive file={drive.file}," # drive file
        command += f"media=cdrom," if drive.type == "dvd" else f"media=disk," # drive type
        command += f"if={drive.bus} " # drive bus
    
    for device in vminfo.devices: command += f"-device {device} " # devices
    if(vminfo.usb == 1): command += f"-usb " # usb
    if(vminfo.biosFile != ""): command += f"-bios {vminfo.biosFile} " # bios file
    if(not vminfo.cpuHpet): command += f"-no-hpet " # append no hpet if hpet is disabled
    if(not vminfo.cpuAcpi): command += f"-no-acpi " # append no acpi if acpi is disabled 
    command += f"{vminfo.unknown}" # append additional/unknown options
    
    print(f"Running command: {command}")

    subprocess.run(command, shell=True, check=True)

def checkSignature(jsonData: object):
    return ("signature" in jsonData) and (jsonData["signature"] == "qvirt") # determine if the signature is qvirt

def getJSON(filename: str):
    file = open(filename,"r") # open file as read-only
    return json.loads(file.read()) # read as json data

def parseJSON(jsonData: object):
    info = VMInfo( # specify default information
        "Untitled", # name
        "128M", # memory capacity
        1, # cpu count
        1, # cpu cores
        1, # cpu threads
        0, # cpu hpet
        1, # cpu acpi
        "x86_64", # cpu arch
        "base", # cpu model
        "pc", # machine type
        "tcg", # machine accelerator
        "c", # boot order
        0, # boot menu
        "", # bios file
        list(), # devices
        0, # usb
        1, # display
        0, # fullscreen
        "sdl", # display type
        "std", # display card
        list(), # drives
        "", # unknown
        ) 

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

def virtmain(arguments: list[str]):
    assert len(arguments) != 3, f"Usage: python3 {arguments[0]} <path to vm config>" # display usage if there isn't any vm config supplied or if there are more options
    jsonData = getJSON(arguments[1]) # config file path is the first argument
    assert checkSignature(jsonData), "failed to check signature"
    startVM(parseJSON(jsonData))
    
if __name__ == "__main__":
    virtmain(sys.argv)