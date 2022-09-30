import os
import sys
from zipfile import ZipFile
import py7zr
from subprocess import Popen, PIPE
import time


PASS_LIST = ["infected", "VelvetSweatshop"]
XLS_LIST = ["VelvetSweatshop", "50821", "27158", "68443"]

def unzip(zipdir):

    #for i in PASS_LIST:

    print("Trying: " + PASS_LIST[0])
    try:
        with ZipFile(zipdir) as f:
            f.extractall(pwd=bytes(PASS_LIST[0], 'utf-8'))
            print("\tCorrect Password")
    except:
        print("\tIncorrect Password")

    unzippedir = zipdir.strip(".zip")

    for i in os.listdir(unzippedir):
        if ".zip" in i or ".7z" in i:
            tmp = unzippedir + os.sep + i
            cmd = "7z x " + tmp + " -p\"" + PASS_LIST[0] + "\""
            try:
                out = Popen([cmd], stdout=PIPE, stderr=PIPE, shell=True)

                if out.stdout:
                    print("Extracted file")
            except:
                pass

    os.system("mkdir output")
    time.sleep(5)
    os.system("mv *.xls* output/")


    enc = False

    for i in os.listdir("output"):
        cmd = "msoffcrypto-tool output" + os.sep + i + " --test -v"
        out = Popen([cmd], stdout=PIPE, stderr=PIPE, shell=True)
        for x in out.stderr.readlines():
            x = x.decode('utf-8')
            if "Version" in x:
                continue
            if "not" in x:
                continue
            enc = True

        if enc == True:
            print(i)
            for passs in XLS_LIST:
                cmd = "msoffcrypto-tool output" + os.sep + i + " " + i + " -p " + passs
                try:
                    out = Popen([cmd], stdout=PIPE, stderr=PIPE, shell=True)
                    if out.stdout:
                        print(cmd)
                except:
                    pass
            
            enc = False

    time.sleep(5)
    os.system("mv *.xls* output/")

if __name__ == "__main__":

    zipdir = sys.argv[1]
    zipdir = os.path.abspath(zipdir)
    unzip(zipdir)
