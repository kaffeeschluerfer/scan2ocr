import os
import re
def date_search(ocr_file):

    dic_month ={"Januar" : "01", "Februar":"02", "März":"03", "April" : "04", "Mai":"05", "Juni":"06", "Juli" : "07", "August":"08", "September":"09", "Oktober" : "10", "November":"11", "Dezember":"12"}
    ymd_date = "0"
    
    if os.path.isfile(ocr_file):
        pdfText=open(ocr_file, "r").read()
        regDate = re.compile(r""" #Datum Suchmuster
        ((\d\d?).(\d\d?).(201\d)) #1
        |
        ((\d\d)..? (Januar|Februar|März|April|Mai|Juni|Juli|August|September|Oktober|November|Dezember) .(20?\d\d)) #2 14. Juni 2019
        |
        (lalal)
        """, re.VERBOSE)
        txtDate=regDate.findall(pdfText)
        print(txtDate) 
        
        # [('', '', '', '', '14. Juni 2019', '14', 'Juni', '2019', ''), ('14.06.2019', '14', '06', '2019', '', '', '', '', '')]
        year = 0000
        month = 00 
        day = 00 
        for t in txtDate:
            if  "2019" in t:
                int_tupel= t.index("2019")
                year=t[int_tupel]
                month = t[int_tupel-1]
                if month in dic_month:
                    month=dic_month[month]
                day = t[int_tupel-2]
                ymd_date = str(year) + str(month )+ str(day)
                print(ymd_date)
                return(ymd_date)
                break
                
        #TODO: Datum in Format 20190131 umwandln
    else:
        print("Kein Datum gefunden")
        return("kein_Datum")

if __name__ == "__main__":
    file = 'scan.pdf.txt'
    date_search(file)
