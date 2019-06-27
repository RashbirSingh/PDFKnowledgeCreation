#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  9 10:58:51 2019

@author: ubuntu
"""
import json
import os
cwd = os.getcwd()
with open( cwd+'/Location.json') as data_file:    
    data = json.load(data_file)
    
import sys
sys.path.insert(0, data['FilePath'])

import PyPDF2 as pyd
from PyPDF2 import PdfFileReader, PdfFileWriter, PdfFileMerger
import re
import csv
from natsort import natsorted
import glob
from pdfrw import PdfReader
from PIL import Image as Img
from wand.image import Image as WImage
from pdf2image import convert_from_path
import pytesseract
import logging



class PDFPreprocess:
    global IndexWordList
    IndexWordListNew = []
    
    @classmethod 
    def get_info(self, path):
        
        '''
        ----------
        Function
        ----------
        * Looks at meta data using PdfReader
        * Return information in meta data of pdf
        
        --------
        INPUT
        --------
        PDF Path
        
        -------
        RETURN
        -------
        Dictionaly containg information as:
            Author': info.Info.Author,
            'Creator': info.Info.Creator,
           'Producer': info.Info.Producer,
           'Subject': info.Info.Subject,
           'Title': info.Info.Title,
           'NumberOfPages': number_of_pages
        
        '''
        logging.info('Inside PDFProcessing get_info')
        PDFinfo = PdfReader(path)
        number_of_pages = len(PDFinfo.pages)
        information = {'Author': PDFinfo.Info.Author,
                       'Creator': PDFinfo.Info.Creator,
                       'Producer': PDFinfo.Info.Producer,
                       'Subject': PDFinfo.Info.Subject,
                       'Title': PDFinfo.Info.Title,
                       'NumberOfPages': number_of_pages
                       }
        logging.info('Exiting PDFProcessing get_info')
        return information

    
    @classmethod 
    def IndexScrapping(self, Pdf_path, PageNo = 2):
        
        '''
        ----------
        Function
        ----------
        * Read page 3 for index
        * Convert pdf to text
        * Cleans text and give headings
        
        --------
        INPUT
        --------
        Pdf_path = PDF Path
        PageNo = Page Number where the content page is
        
        -------
        RETURN
        -------
        List of index iterable words
        
        '''
        IndexWordListNew = []
        logging.info('Inside PDFProcessing IndexScrapping')
        """ Geting Pdf Path"""
        #global pdf_toread
        pdf_toread = pyd.PdfFileReader(Pdf_path)
        if pdf_toread.isEncrypted:
            logging.warning('PDF is encrypted')
            pdf_toread.decrypt('')
            logging.info('PDF is decrypted now')
            
        """ Reading only content page"""
        page_one = pdf_toread.getPage(PageNo)
        """Extracting text on page 3"""
        indexContent = page_one.extractText()
        logging.info('index content %s', indexContent)
        """Removing next line"""
        WithoutNextLine = re.sub(r'\n','',indexContent)
        Withoutdot = WithoutNextLine.replace(".", "")
        """Custom text removal"""
        RepairText = re.sub("12", "" , Withoutdot)
        RepairText = re.sub(".*Contents ", "" , RepairText)
        RepairText = re.sub("Annexure I.*", "" , RepairText)
        RepairText = re.sub("C L", "" , RepairText)
        RepairText = re.sub("P L", "" , RepairText)
        RepairText = re.sub("Table of Contents", "" , RepairText)
        RepairText2 = re.sub("^[ \t]+|[ \t]+$", "", RepairText)
        RepairText2 =re.sub('forwardEncashment', 'forward/Encashment', RepairText2)
        RepairText2 =re.sub(r'Privilege Leave,', 'Privilege Leave', RepairText2)
    
        """Removing numbers"""
        IndexWordList = re.split("[0-9]| 10 | 11 | 12 |  10 |  11 |  12 | 10  | 11  | 12  |   10 |   11 |   12 |  12 |  ", RepairText2)
        """Printing the List"""
        logging.info('Inside IndexScrapping')
        for Index, Words in enumerate(IndexWordList):
            if len(Words) > 3:
                IndexWordListNew.append(IndexWordList[Index].strip())
        
        with open('Topics.csv', 'w+') as f:
            writer = csv.writer(f)
            writer.writerow(IndexWordListNew)
        logging.info('WordList is: %s', IndexWordListNew)
        logging.info('Exiting PDFProcessing IndexScrapping')
        return(IndexWordListNew)
        
    @classmethod    
    def pdf_splitter(self, path):
        
        '''
        ----------
        Function
        ----------
        * Removes previously created .json created files
        * Call on start of application
        
        --------
        INPUT
        --------
        PDF path
        
        -------
        RETURN
        -------
        None
        
        '''
        logging.info('Inside PDFProcessing pdf_splitter')
        pdf = PdfFileReader(path)
        for page in range(pdf.getNumPages()):
            pdf_writer = PdfFileWriter()
            pdf_writer.addPage(pdf.getPage(page))
            output_filename = 'page_{}.pdf'.format(page+1)
            with open(data['PdfProcess']+'/'+output_filename, 'wb') as out:
                pdf_writer.write(out)
            print('Created: {}'.format(output_filename))
        logging.info('Exiting PDFProcessing pdf_splitter')

    @classmethod 
    def split(self, Pdf_path):
        '''
        ----------
        Function
        ----------
        * Removes previously created .json created files
        * Call on start of application
        
        --------
        INPUT
        --------
        PDF path
        
        -------
        RETURN
        -------
        None
        
        '''
        logging.info('Inside PDFProcessing split')
        self.pdf_splitter(Pdf_path)
        self.merge(data['PdfProcess'])
        logging.info('Exiting PDFProcessing split')
        
# =============================================================================
#     
# =============================================================================


    @classmethod 
    def merger(self, output_path, input_paths):
        '''
        ----------
        Function
        ----------
        * merge all the other pages into single pdf
        * Creates an repaired.pdf in local directory
        
        
        --------
        INPUT
        --------
        * Inputs the name of the desired output file ('Repaired.pdf')
        * inputs the padh of differend pdf to be merged
        
        -------
        RETURN
        -------
        None
        
        '''
        logging.info('Inside PDFProcessing merger')
        pdf_merger = PdfFileMerger()
        for path in input_paths:
            pdf_merger.append(path)
        with open(output_path, 'wb') as fileobj:
            pdf_merger.write(fileobj)
        logging.info('Exiting PDFProcessing merger')
            
    @classmethod 
    def merge(self, Pdf_path):
        '''
        ----------
        Function
        ----------
        * Removes first 3 pages
        * Sort the pages based on page number
        * Calls merger and pass path of each seperated pdf
        * Removes newly created pdfs for merging
        
        
        --------
        INPUT
        --------
        PDF path
        
        -------
        RETURN
        -------
        None
        
        '''
        logging.info('Inside PDFProcessing merge')
        Pdf_path = re.sub(".pdf", "", Pdf_path)
        os.remove(data['PdfProcess']+'/'+'page_1.pdf')
        os.remove(data['PdfProcess']+'/'+'page_2.pdf')
        os.remove(data['PdfProcess']+'/'+'page_3.pdf')
        
        paths = glob.glob(data['PdfProcess']+'/page_*.pdf')
        paths = natsorted(paths, key=lambda y: y.lower())
        self.merger('repaired.pdf', paths)
        os.system('rm ' + data['PdfProcess']+'/'+'page_*.pdf')
        logging.info('Exiting PDFProcessing merge')
        
        
        
    @classmethod 
    def OCR2Text(self, path, PageNo = 3):
        
        '''
        ----------
        Function
        ----------
        * Convert OCR PDF to image
        * Convert jpeg image to text object
        * Created Sample.jpeg
        * Remove it after execution
        
        --------
        INPUT
        --------
        * PDF Path
        * Page Number of PDF (Default = 2 (i.e page number 3))
        
        -------
        RETURN
        -------
        plain string text object
        
        '''
        logging.info('Inside PDFProcessing OCR2Text')
# =============================================================================
#         image_file = open("sample.jpeg", "wb")
#         index = PageNo #Page Number Of Pdf
#         with WImage(filename=path + "[{}]".format(index), resolution=400) as img:
#         #with WImage(filename=path + "[{}]".format(index), resolution=400) as img:
#             #image_jpeg = img.convert('jpeg')
#             #image_jpeg.save(filename=image_file.name)
#             img.save(filename=image_file.name)
#         image_file.close()
# =============================================================================
        
        self.pdf_splitter(path)
        pageToImage = convert_from_path('/home/ubuntu/Desktop/My-Test-Code/pdf_process/page_'+str(PageNo)+'.pdf')
        for page in pageToImage:
            page.save('pdf_process/out.jpg', 'JPEG')
        text = pytesseract.image_to_string(Img.open('pdf_process/out.jpg'))
        os.system('rm pdf_process/*')
        #os.remove('sample.jpeg')
        logging.info('OCR2Text Converted text to: %s', text)
        logging.info('Exiting PDFProcessing OCR2Text')
        return text
    
    
