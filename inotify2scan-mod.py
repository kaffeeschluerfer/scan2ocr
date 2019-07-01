#!/usr/bin/python3 -u
#pip3 install inotify


import inotify.adapters #inotify
import subprocess
import os
import re
import shutil
import regdate


#TODO: Logging einfügen

'''
def date_search(ocr_file):
   
    if os.path.isfile(ocr_file):
        pdfText=open(ocr_file, "r").read()
        regDate = re.compile(r""" #Datum Suchmuster
        (\d\d?.\d\d?.201\d) #1
        |
        ((\d\d).(Januar|Februar|März|April|Mai|Juni|Juli|August|September|Oktober|November|Dezember).(\d\d\d\d)) #2
        |
        (lalal)
        """, re.VERBOSE)
        txtDate=regDate.search(pdfText)
        print(txtDate.group())
        return(txtDate.group())
        #TODO: Datum in Format 20190131 umwandln
    else:
        print("Kein Datum gefunden")
        return("kein_Datum")
'''

def _main():    
#TODO: Config File?
    scan_dir = "/mnt/store/Scans" #Scan-Directory
    scan_ino = "IN_CLOSE_WRITE"
    i = inotify.adapters.Inotify()
    i.add_watch(scan_dir)
    #i.add_watch('/tmp/test') # TestDir
    ocr_prog = ["/usr/bin/ocrmypdf"]
    ocr_opts=['-d', '-l','deu', '--sidecar']
    ocr_path = scan_dir + "/ocr/"
    if not os.path.isdir(ocr_path):
        os.mkdir(ocr_path)

#TODO: Keyboard Interrupt try       

    while (True):
        #inotify Check
        for event in i.event_gen(yield_nones=False):
            (_, type_names, path, filename) = event
            event_ino = type_names[0]
            #print("PATH=[{}] FILENAME=[{}] EVENT_TYPES={}".format(path, filename, type_names))            
            #if len(filename)>0 and event_ino == scan_ino:
            if (".pdf" in filename) and event_ino == scan_ino:
                print("Start OCR Script")

                ocr_input =  [path + "/"+filename]
                ocr_output = [ocr_path + filename]
                ocr_txt =  [ocr_path + filename + ".txt"]   
                popenlist = ocr_prog+ ocr_opts + ocr_txt + ocr_input + ocr_output
                print(popenlist)
                subprocess.run(popenlist, stdout=subprocess.PIPE)
                pdfdate= regdate.date_search(str(ocr_txt[0]))
                if os.path.isfile(ocr_output[0]):
                    shutil.move(ocr_output[0] , ocr_path + pdfdate + "_"+ filename)
                else:
                    print("Keine Datei im OCR Ordner zum verschieben")
                                
                                
if __name__ == '__main__':
    _main()
 
