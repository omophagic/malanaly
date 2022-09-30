import os
import sys
from subprocess import Popen, PIPE






CMD = "malwoverview.py -v 1 -V "



def test():

    tlabel = ""
    tclass = ""
    tdetect = ""

    with open("out.txt") as f:
        data = f.readlines()

    for i in data:
        tmp = i.strip('b\'')
        tmpdata = tmp.split('\\x1b[0m')

        if len(tmpdata) == 2:
            tmpkey = tmpdata[0].split(":")[0]
            tmpdata = tmpdata[1].split('\\x1b')[0]
            if tmpkey == "MD5 hash":
                print(tmpkey + " - " +  tmpdata)
            
            if tmpkey == "Malicious":
                print("Malicious Detections - " +  tmpdata)

            if tmpkey == "Times Submitted":
                print(tmpkey + " - " +  tmpdata)
        
        
        if len(tmpdata) == 1:
            try:
                tmpkey = tmpdata[0].split()[0].strip(":")
                tmpdata = tmpdata[0].split()[1].strip("\'")
                if tmpkey == "label":
                    print(tmpkey + " - " +  tmpdata)
            except:
                pass


    exit()
 
def viruscheck(filedir):
    vfile = ""
    for i in os.listdir(filedir):
        vfile = filedir + os.sep + i
        tmpcmd = CMD + vfile
        #tmpcmd = "file " + vfile
        print("=====================================================")
        print(vfile)
    
        out = Popen([tmpcmd], stdout=PIPE, stderr=PIPE, shell=True)
        data = out.stdout.readlines()

        for i in data:
            tmp = i.decode('utf-8')
            #tmp = tmp.strip('b\'')
            try:
                tmpkey = tmp.split(":")[0].strip()
                tmpdata = tmp.split(":")[1].strip()
            except:
                print(tmpkey, tmpdata)
                pass


            if tmpkey == "MD5 hash":
                print("\t" + tmpkey + " - " +  tmpdata)

            if tmpkey == "Malicious":
                print("\tMalicious Detections - " +  tmpdata)
                
            if tmpkey == "Times Submitted":
                print("\t" + tmpkey + " - " +  tmpdata)


            if tmpkey == "label":
                print("\t" + tmpkey + " - " +  tmpdata)
 


if __name__ == "__main__":
    filedir = sys.argv[1]
    filedir = os.path.abspath(filedir)
    viruscheck(filedir)
    #test()
