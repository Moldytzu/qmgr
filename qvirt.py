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

from qvirt.vm import *

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