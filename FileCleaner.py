#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  9 09:42:24 2019

@author: ubuntu
"""
import json
import os
cwd = os.getcwd()
with open( cwd+'/Location.json') as data_file:    
    data = json.load(data_file)

import sys
sys.path.insert(0, data['FilePath'])
import logging

class Cleaner:
    '''----CLEANER CLASS----
    It has two functions 1) StartUpCleaner
                         2) CleanOnEnding
    
    StartUpCleaner --> Call this function at the begining of master file to remove .json file
    CleanUP --> Call this function at the end final execution to remove Summary, HeadWords, SectionalText, CSV and sectional JSONs
    '''
    
    def CleanerOnStart():
        '''
        ----------
        Function
        ----------
        * Removes previously created .json created files
        * Call on start of application
        
        --------
        INPUT
        --------
        None
        
        -------
        RETURN
        -------
        None
        
        '''
        try:
            logging.warning('Removing Combined Json')
            os.system(data['RemoveCombinedJson'])
        except:
            logging.error('Exception occured in CleanerOnStart FileCleaner File')
            pass
    
    def CleanOnEnding():
        '''
        ----------
        Function
        ----------
        * Call on the end of the program
        * Removes summary files
        * Removes HeadWord Files
        * Remove SectionalText Files
        * Remove CSV files
        * Remove repaired pdf file
        * Remove Repaired Json file
        
        --------
        INPUT
        --------
        None
        
        -------
        RETURN
        -------
        None
        
        '''
        try:
            logging.warning('Removing Summary')
            os.system(data['RemoveSummary'])
            
            logging.warning('Removing Head Words')
            os.system(data['RemoveHeadWords'])
            
            logging.warning('Removing Sectional Text')
            os.system(data['RemoveSectionalText'])
            
            logging.warning('Removing Sectional Topics')
            os.system(data['TopicCSVRemove'])
            
            logging.warning('Removing Json objects')
            os.system(data['JSONRemover'])
            
            logging.warning('Removing repaired.pdf')
            os.remove('repaired.pdf')
            
            logging.warning('Removing repaired_JSON.json')
            os.remove('repaired_JSON.json')
        except:
            logging.error('Exception occured in CleaningOnEnd FileCleaner File')
            pass
    