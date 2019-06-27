#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 14:43:26 2019

@author: ubuntu
"""

import json
import os
import logging
cwd = os.getcwd()

def run():
    logging.critical('Creating Location.json file')
    LocationJsonObject = {
         "FilePath": cwd+"/Code",
         "JSONRemover": "rm "+cwd+"/JSONObject*.json",
         "RemoveSummary": "rm "+cwd+"/Summary*.txt",
         "RemoveHeadWords": "rm "+cwd+"/HeadWords*.csv",
         "RemoveSectionalText": "rm "+cwd+"/SectionalText*.txt",
         "RemoveCombinedJson": "rm "+cwd+"/*_JSON.json",
         "TopicCSVRemove": "rm "+cwd+"/Topics.csv",
         "PdfProcess": cwd+"/pdf_process"
    }
    
    with open( cwd+'/Location.json', 'w') as data_file:    
        json.dump(LocationJsonObject, data_file, indent=5)
    logging.critical('Location.json file created')