#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 09:37:03 2019

@author: ubuntu
"""

import re
import csv
import os

from bs4 import BeautifulSoup as soup

run = 0
page_soup = ''
name_box = ''
name_boxX = ''

def IndexSearch(Pdf_path):
    global page_soup
    global name_box
    global name_boxX
    global d
    d=[]
    global run
    run = 0
    global html_path
    html_path = re.sub('.pdf', '', Pdf_path)
    print(Pdf_path)
    #Pdf_path = re.sub(' ', '_', Pdf_path)
    os.system('pdf2txt.py -o '+html_path+'.html -t html '+ Pdf_path+'')
    page = html_path+'.html'
    page_soup = soup(open(page), "lxml")
    
    #'Sexual_harassment_policy.pdf'
    name_box = page_soup.find_all('span',{'style':"font-family: b'Arial-BoldMT'; font-size:10px"})
    
    def DocumentContentScrapper(name_box, run=0):
        
        #ATTENDANCE.pdf
        if ((len(name_box) < 2) or name_box == None) and (run ==0):
            name_box = page_soup.find_all('span',{'style':"font-family: b'SRPRLN+Arial,Bold'; font-size:13px"})
            run = run + 1
            if (len(name_box) < 2):
                DocumentContentScrapper(name_box, run)
            else:
                return name_box
            
        #Professional_Certification_Reimbursement_Policy.pdf
        elif ((len(name_box) < 2) or name_box == None) and (run == 1):
            name_box = page_soup.find_all('span',{'style':"font-family: b'AVVSPU+Arial-BoldMT'; font-size:19px"})
            run = run + 1
            if (len(name_box) < 2):
                DocumentContentScrapper(name_box, run)
            else:
                return name_box
            
        #Performance_Improvement_Plan.pdf
        elif ((len(name_box) < 2) or name_box == None) and (run == 2):
            name_box = page_soup.find_all('span',{'style':"font-family: b'Arial,Bold'; font-size:9px"})
            #name_box = page_soup.find_all('span',{'style':"font-family: b'Arial-BoldMT'; font-size:10px"})
            run = run + 1
            if (len(name_box) < 2):
                DocumentContentScrapper(name_box, run)
            else:
                return (name_box)
            
            
        elif ((len(name_box) < 2) or name_box == None) and (run == 3):
            name_box = page_soup.find_all('span',{'style':"font-family: b'AVVSPU+Arial-BoldMT'; font-size:19px"})
            run = run + 1
            if (len(name_box) < 2):
                DocumentContentScrapper(name_box, run)
            else:
                return name_box
            
        else:
            print('OK')
            return name_box
    
    name_box = DocumentContentScrapper(name_box)
    b = name_box
    b = str(b)
    b = re.sub(r'<.*?>', '', b)
    b = re.sub(r'[]]|PROTECTION TO COMPLAINANT / VICTIM|[[]|discretion |Annexure A|Annexure B| Annexure C|:|Acidaes Solutions Pvt. Ltd’s|Meeting Date', '', b )
    b = re.sub("   ", "" , b)
    b = re.sub("^[ \t]+|[ \t]+$", "", b)
    c = re.split(',', b)
    for i in range(0 , len(c)):
        if len(c[i]) >= 6:
            if c[i][0] == ' ':
                c[i] = c[i][1:-1]
            c[i] = re.sub('   *', '', c[i])
            d.append(c[i])
            
    with open('Topics.csv', 'w+') as f:
        writer = csv.writer(f)
        writer.writerow(d)
    
    return(d)

        
