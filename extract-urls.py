from pyxlsb import open_workbook
import os
import sys
import optparse
import requests
import re

URLHAUS_API = "https://urlhaus-api.abuse.ch/v1/url/"
regex_uri = "https?:\/\/[a-zA-Z0-9\.\/\-\:]{5,}\.\w{1,}"

def setup_args():
    parser = optparse.OptionParser()

    parser.add_option('-d', '--directory',
    action="store", dest="directory",
    help="The folder that contains your Dridex docs", default=".")

    return parser.parse_args()

def extract_downloader_links(file_path):
  
    print("[*] Working file: " + file_path)
    #xls = open_workbook(file_path)
    xls = open_workbook(file_path)
    obf = []

    print("=========================")
    for sheet in xls.sheets:
        s = xls.get_sheet(sheet)
        for row in s.rows(sparse=True):
            for c in row:
                if c.v != None:
                    obf.append(c.v)
    urls = []
    script = ""
    tmp_urls = ""

    if len(obf) == 2:
        for y in range(len(obf[1])):
            tmp_urls = tmp_urls + chr(ord(obf[1][y]) + int(obf[0][y]))

        if tmp_urls:
            url_string = tmp_urls.split("RSab")
            for url in url_string[0].split("E,"):
                urls.append("https://" + url)
    else:
        for y in range(len(obf)):
            if isinstance(obf[y], float):
                script = script + chr(int(obf[y]))

        if script:
            tmp_urls = re.findall(regex_uri, script)
            for url in tmp_urls:
                urls.append(url)

    print("[*] Found " + str(len(urls)) + " URLs")
    for url in urls:
        print("[$] Found - " + url)
        data = {'url' : url}
        response = requests.post(URLHAUS_API, data)

        response = response.json()

        if response['larted'] == "true":
            print("\t[!] URL reported before")
            print("\t[!] Malware Families:")
            for i in response["payloads"]:
                print("\t\t" + i['signature'])
        else:
            print("\t[!] URL is new")
    


def main(argv):

    options, args = setup_args() 

    for file_name in os.listdir(options.directory):
        extract_downloader_links(options.directory + file_name)

if __name__ == '__main__':
	main(sys.argv[1:])