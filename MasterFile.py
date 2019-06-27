 #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 15:59:59 2019

@author: linux
"""

import Location_Json_Creator
Location_Json_Creator.run()

import json
import os
import sys
from PDFProcessing import PDFPreprocess as PDFp
from textProcessing import TextManipulation as TxtMan
from FileCleaner import Cleaner as CLN
import Document_index_check
import re
import time
import logging




def Master(pdf_path, Do='n'):
    global Collector
    global IndexWordListNew
    global IndexWordList
    Collector = []
    try:
        '''
        Cleaner class on start up will be called to clean and remove
        previosly created JSON file, it is called using function of class Cleaner in
        FileCleaner.py'''
        
        logging.info('Cleaning on startup is started')
        CLN.CleanerOnStart()
        logging.info('Cleaning on startup is done')
        
        logging.info('Opening page 3 of the PDF')
        #Calling OCR2Text function of PDFProcessing
        Content = PDFp.OCR2Text(pdf_path)
        #Text is recieved from the OCR
        ContentFound = Content.find('Contents')
        logging.info('Value of ContentFound is %s', ContentFound)
        if ContentFound == -1:
            logging.warning('Content is not found on page 3')
        else:
            logging.info('Content is found on page 3')
        
        '''
        Using the get_info fucntion of class PDFPreprocess in file PDFProcessing.py
        the ouput returns an dict having information about,
        * Author
        * Creator
        * Producer
        * Subject
        * Title
        * NumberOfPages
        
        Creator infromation is used to identify the type of file, i.e either OCR/Image based
        or Text readable file
        '''
        Creator = PDFp.get_info(pdf_path)['Creator']
        logging.info('Creator of the PDF is: %s', Creator)
        
        if '()' == Creator or '(HP Scan)' == Creator:
            
            '''
            split function of PDFPreprocess class in PDFProcessing.py
            will split the pdf into diffrent pages and remove all the pages
            above the content page that have index infromation regarding the heading
            this information is usually found on page 3 hence pahe 1 and page 2 are removed
            '''
            logging.info('The detected file is a type of OCR file')
            PDFp.split(pdf_path)
            print('OCR File')
            sys.exit()
            
        else:
            if (Do == 'n' and ContentFound != -1):
                logging.info('PDF follows normal format and the content page is on page number 3')
                logging.info('Calling IndexScrapping in master file')
                IndexWordListNew = PDFp.IndexScrapping(pdf_path)
                logging.info('Exiting IndexScrapping in master file')
                print(IndexWordListNew)
                PDFp.split(pdf_path)
                
            else:
                logging.info('PDF do not follows normal format and the content page is not on page number 3')
                logging.info('Calling IndexSearch function of Document_index_check in master file')
                IndexWordListNew = Document_index_check.IndexSearch(pdf_path)
                logging.info('Exiting IndexSearch function of Document_index_check in master file')
                print(IndexWordListNew)


        pdf_path = 'repaired.pdf'
        logging.info('Calling StartFunction in master file')
        OutputText = TxtMan.StartFunction(pdf_path)

        logging.info('Calling MatcherFunction in master file')
        TxtMan.MatcherFunction(IndexWordListNew, OutputText)
    
        time.sleep(0.01)
        for loop in range(len(IndexWordListNew)):         
            Collector.append(json.loads(open('JSONObject'+str(loop)+'.json').read()))
            
    except:
        logging.error('Error occured in Master File')
            
    
    finally:
        
        Jsonpdf_path = re.sub('.*/','', pdf_path)
        Jsonpdf_path = re.sub(r'.pdf', '', Jsonpdf_path)
        cwd = os.getcwd()
        
        with open(Jsonpdf_path + '_JSON.json', 'w') as CombineJson:  
            logging.warning('Creating %s_JSON.json file in %s', Jsonpdf_path , cwd)
            
            for listitem in Collector:
                CombineJson.write('%s\n' % listitem)
                
        logging.info('Execution is finished')
        print('Finished...')
        time.sleep(2)
        
        logging.info('Cleaning on End is started')
        CLN.CleanOnEnding()
        os.remove(re.sub(r'.pdf', '', pdf_path)+".txt")
        logging.info('Cleaning on End is completed')
        return Collector
    
    
    
    
    

    