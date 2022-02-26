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

import sys,json,dataclasses,contextlib

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
    unknown: str

def startVM(vminfo: VMInfo):
    print(f"Starting {vminfo.name}") # print starting message

    command = f"qemu-system-{vminfo.cpuArch} " # create the command we will launch
    command += f"-m {vminfo.memoryCapacity} " # append memory information
    command += f"-smp maxcpus={vminfo.cpuCores * vminfo.cpuCount * vminfo.cpuThreads},sockets={vminfo.cpuCount},cores={vminfo.cpuCores},threads={vminfo.cpuThreads} " # append cpu topology
    command += f"-cpu {vminfo.cpuModel} " # append cpu model
    if(not vminfo.cpuHpet): command += f"-no-hpet " # append no hpet if hpet is disabled
    if(not vminfo.cpuAcpi): command += f"-no-acpi " # append no acpi if acpi is disabled 
    command += f"{vminfo.unknown}" # append additional/unknown options
    print(command)

def checkSignature(jsonData: object):
    if("signature" in jsonData):
        return jsonData["signature"] == "qvirt" # determine if the signature is qvirt
    else:
        return False

def getJSON(filename: str):
    file = open(filename,"r") # open file as read-only
    data = json.loads(file.read()) # read as json data
    return data # return it

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
        "", # unknown
        ) 

    # parse all json data into a class
    with contextlib.suppress(AttributeError): info.name = jsonData["name"]
    with contextlib.suppress(AttributeError): info.memoryCapacity = jsonData["memory"]["capacity"]
    with contextlib.suppress(AttributeError): info.cpuCount = jsonData["cpu"]["count"]
    with contextlib.suppress(AttributeError): info.cpuCores = jsonData["cpu"]["cores"]
    with contextlib.suppress(AttributeError): info.cpuThreads = jsonData["cpu"]["threads"]
    with contextlib.suppress(AttributeError): info.cpuArch = jsonData["cpu"]["arch"]
    with contextlib.suppress(AttributeError): info.cpuModel = jsonData["cpu"]["model"]
    with contextlib.suppress(AttributeError): info.cpuHpet = jsonData["cpu"]["hpet"]
    with contextlib.suppress(AttributeError): info.cpuAcpi = jsonData["cpu"]["acpi"]
    with contextlib.suppress(AttributeError): info.unknown = jsonData["additionalOptions"]

    return info

def virtmain(arguments: list[str]):
    if(len(arguments) < 2 or len(arguments) > 2):
        print(f"Usage: python3 {arguments[0]} <path to vm config>") # display usage if there isn't any vm config supplied or if there are more options
    
    configFile = arguments[1] # config file path is the first argument
    jsonData = getJSON(configFile) # get json object

    assert checkSignature(jsonData), "failed to check signature"

    startVM(parseJSON(jsonData))
    
if __name__ == "__main__":
    virtmain(sys.argv)