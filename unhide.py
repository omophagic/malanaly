
import sys
sys.path.append('C:\\Python27\\Lib\\site-packages\\oledump')
from oledump import *
import oledump
import optparse
from subprocess import Popen, PIPE
import os

# -p plugin_biff --pluginoptions "-o bound -a" ..\malanaly\lab02-analyzing-xlms\sample01.bin




def unhide(FILE):
    PYTHON_VERS = 'python27'
    OLEDUMP = 'C:\Tools\oledump\oledump.py'
    PLUGIN_P = '-p'
    PLUGIN = 'plugin_biff'
    PLUGIN_O = '--pluginoptions'
    PLUGIN_OPTIONS = '-o bound -a'
    p = Popen([PYTHON_VERS, OLEDUMP, PLUGIN_P, PLUGIN, PLUGIN_O, PLUGIN_OPTIONS, FILE], stdout=PIPE, stderr=PIPE, shell=True)

    sheet_found = False
    hidden_sheets = False
    hidden_sheet_hex = {}

    output = p.stdout.readlines()
    print("Looking for sheets:")
    print("-------------------")
    for i in output:
        if "BOUNDSHEET" in i:
            sheetname = i.split('-')[-1].strip()
            sheet_found = True

        if sheet_found and "BOUNDSHEET" not in i:
            print(i)
            sheet_hex = i.split(':')[1].split("\\")[0].strip()
           
            hidden_bit = sheet_hex[13:14]

            if hidden_bit == "0":
                #hidden_sheet_hex[sheetname] = sheet_hex[:23]
                print("\t[!] Sheet - " + sheetname + ": not hidden")
            elif hidden_bit == "1":
                hidden_sheet_hex[sheetname] = sheet_hex[:23]
                hidden_sheets = True
                print("\t[!] Sheet - " + sheetname + ": hidden")
            elif hidden_bit == "2":
                hidden_sheet_hex[sheetname] = sheet_hex[:23]
                hidden_sheets = True
                print("\t[!] Sheet - " + sheetname + ": very hidden")

    #============================================================
    if hidden_sheets:
        print("============================================")
        print("Un-hiding Sheets:")
        print("-----------------")
        tmp = FILE.split("\\")[-1].split(".")[0]
        copy = tmp + "_original.bin"
        os.system("cp " + FILE + " " + copy)
            
        
        for i in hidden_sheet_hex:
         
            tmp = hidden_sheet_hex[i]

            f = open(FILE, 'r+b')

            data = f.read()
            tmp = "".join(tmp)

            hex_location = data.find(bytearray.fromhex(tmp))
         
            f.seek(hex_location)

            new_data = list(tmp)
            new_data[13] = "0"
            new_data = "".join(new_data)
          
            new_data = bytearray.fromhex(new_data)

            f.write(new_data)
            f.close()
            print("\t[+] Sheet - " + i + ": no longer hidden")
    
            

if __name__ == "__main__":
    FILE = sys.argv[1]
    # parser = optparse.OptionParser()
    # parser.add_option('-p', '--plugins', type=str, default='')
    # parser.add_option('--pluginoptions', type=str, default='')
    # parser.add_option('--plugindir', type=str, default='')
    # (options, args) = parser.parse_args()
    
    unhide(FILE)
    #os.system("cp sample01_original.bin sample01.bin")