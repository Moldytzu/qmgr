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

import sys,subprocess
from .vm import *

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
        command += f"-display {vminfo.displayType} " if not vminfo.displayFull else f"-display {vminfo.displayType},window-close=off " # display type
        command += f"-vga {vminfo.displayCard} " # video card
        if(vminfo.displayFull): command += f"-full-screen " # full screen
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

if __name__ == "__main__":
    usageTxt = f"Usage: python3 {sys.argv[0]} <run|create> [additional arguments]"
    
    assert len(sys.argv) > 1, usageTxt  # display usage
    assert sys.argv[1] == "run" or sys.argv[1] == "create", usageTxt # display usage, again

    if(sys.argv[1] == "run"):
        assert len(sys.argv) == 3, f"Usage python3 {sys.argv[0]} run <virtual machine configuration file>" # display usage
        jsonData = getJSON(sys.argv[2]) # config file path is the first argument
        assert checkSignature(jsonData), "failed to check signature"
        startVM(parseJSON(jsonData))
    elif(sys.argv[1] == "create"):
        assert len(sys.argv) == 4 or len(sys.argv) == 5, f"Usage python3 {sys.argv[0]} create <name> <virtual machine configuration file> [pickle serialized VMInfo]" # display usage
        info = VMInfo()
        with suppress(IndexError): info = decodeInfo(sys.argv[4]) # load vm info from string
        info.name = sys.argv[2]
        encoded = encodeInfo(info)
        print(f"Writing {encoded} to {sys.argv[3]}")
        f = open(sys.argv[3],"w")
        f.write('''{"name": "%s","memory": {"capacity":"%s"},"cpu": {"count":%d,"cores":%d,"threads":%d,"arch":"%s","model":"%s","hpet":%d,"acpi":%d},"drives": {},"machine": {"type": "%s","accelerator": "%s"},"bios": {"bootOrder": "%s","bootMenu": %d,"file": "%s"},"devices": [],"usb": {"enabled": %d},"display": {"enabled": %d,"type": "%s","card": "%s","fullscreen": %d},"additionalOptions": "%s","signature": "qvirt"}
        ''' % (info.name,info.memoryCapacity,info.cpuCount,info.cpuCores,info.cpuThreads,info.cpuArch,info.cpuModel,info.cpuHpet,info.cpuAcpi,info.machineType,info.machineAccelerator,info.biosBootOrder,info.biosBootMenu,info.biosFile,info.usb,info.display,info.displayType,info.displayCard,info.displayFull,info.unknown))