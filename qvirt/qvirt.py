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

import sys,json

def checkSignature(jsonData: object):
    passed = False
    try:
        passed = jsonData["signature"] == "qvirt" # determine if the signature is qvirt
    except:
        passed = False # return false on error
    return passed

def getJSON(filename: str):
    file = open(filename,"r") # open file as read-only
    data = json.loads(file.read()) # read as json data
    return data # return it

def virtmain(arguments: list[str]):
    if(len(arguments) < 2 or len(arguments) > 2):
        print(f"Usage: python3 {arguments[0]} <path to vm config>") # display usage if there isn't any vm config supplied or if there are more options
    
    configFile = arguments[1] # config file path is the first argument
    jsonData = getJSON(configFile) # get json object

    if(checkSignature(jsonData)):
        print(jsonData)
    else:
        print("Signature check failed!")


if __name__ == "__main__":
    virtmain(sys.argv)