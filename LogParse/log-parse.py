import os
import time
import csv
import sys

def dup_check(rfile, word):
    with open(rfile, "r") as refile:
        contents = refile.readlines()
        for content in contents:
            if word in content:
                return True

def wr_file(wfile, word):
    if not os.path.exists(wfile) or os.stat(wfile).st_size == 0 :
        with open(wfile, "w+") as myfile:
            myfile.write(word + "\n")
    elif dup_check(wfile, word) is not True :
        with open(wfile, "a") as myfile:
            myfile.write(word + "\n")

def parse_tab(rfile, wfile, word, start, end):
    with open(rfile, "r", encoding = "ISO-8859-1") as f:
        contents = f.readlines()
        for content in contents:
            check = content.split()
            result = all(elem in check for elem in word)
            if result:
                dip = str(check[start:end])
                wr_file(wfile, dip)

def parse_comma(rfile, wfile, word, start, end):
    with open(rfile, "r", encoding = "ISO-8859-1") as f:
        contents = csv.reader(f)
        for content in contents:
            result = all(elem in content for elem in word)
            if result:
                dip = str(content[start:end])
                wr_file(wfile, dip)

def cr_diec():
    file_path = os.getcwd()
    directory = file_path + '/log-parse'
    try:
        os.stat(directory)
        return directory
    except:
        os.mkdir(directory)
        return directory

def gogo(s_wrd, strt, end, tc, fext):
    path = cr_diec()
    pfile = path + '/' + time.strftime("%Y%m%d-%H%M%S") + '.txt'
    for x in os.listdir('.'):
        if fext in x:
            if tc.lower() == 'tab':
                parse_tab(x, pfile, s_wrd, strt, end)
            elif tc.lower() == 'comma':
                parse_comma(x, pfile, s_wrd, strt, end)
    return print('Check the parsed files !!! \n' + path)

if __name__ == "__main__":
    try:
        word = sys.argv[1]#This variable must be a list.
        strt = sys.argv[2]#Started column.
        end = sys.argv[3] #Ended column.
        tc = sys.argv[4]  #Is file format comma(csv) or tab.
        fext = sys.argv[5]#Searched file extension(.log or .txt etc..).
        gogo(word, strt, end, tc, fext)
    except Exception as e:
        print(e)
