#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 21 09:08:52 2019

@author: ubuntu
"""

'''

* Summary
* Intial Code
* Json Creator

'''

import json
from summa import summarizer
from summarizer import summarize
import re
from unidecode import unidecode
import io
import unicodedata
import contractions
import inflect
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize 
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
import csv
import logging


class TextManipulation:
    X = []
    Y = []
    SectionalText = ''
    
    @classmethod
    def ReaderJsonCreator(self, CallNumber):
        '''
        ----------
        Function
        ----------
        * Reads Different files like:
            > Topics.csv
            > HeadWords.csv
            > Summary.txt
            > JsonObject.json
        * Read first row of HeadWords.csv
        * Calls jsonAppender and pass row zero of HeadWords
          SummaryText of each section, and Topic of that section.
        
        --------
        INPUT
        --------
        CallNumber = Used to iterate over differend files differentiated based on
                     number
        
        -------
        RETURN
        -------
        None
        
        '''
        global rowZero, rowOne
        rowZero = []
        rowOne = []
        global SummaryText
        SummaryText = []
        global JSONFile
        
        logging.info('Inside ReaderJsonCreator')
        logging.info('Opening Topics.csv')
        with open('Topics.csv', 'r') as TopicsFile:
            Topics = TopicsFile.read()
        
        Topics = re.split("," , Topics)
        logging.info('Topics read from Topics.csv are: %s', Topics)
        Topic = Topics[CallNumber]
        logging.info('Current call number for ReaderJsonCreator is: %s', CallNumber)
        logging.info('Current topic is: %s', Topic)
        
        
        CallNumber = str(CallNumber)
        CSVFile = 'HeadWords'+CallNumber+'.csv'
        TXTFile = 'Summary'+CallNumber+'.txt'
        JSONFile = 'JSONObject'+CallNumber+'.json'
        logging.info('Inside JSONCreator')
        
        logging.info('Opening Summary%s.txt in read mode',CallNumber )
        with open(TXTFile, 'r') as file:
            SummaryText = file.read()
            
        logging.info('HeadWords%s.csv', CallNumber)            
        with open(CSVFile) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            
            for col in readCSV:
                rowZero.append(col[0])
                logging.info('Exiting ReaderJsonCreator')
                logging.info('''Calling jsonAppender with following inputs: 
                    rowZero = %s, 
                    SummaryText = %s, 
                    Topic = %s''',
                    rowZero, SummaryText, Topic)
                
            self.jsonAppender(rowZero, 
                         SummaryText, Topic)

    @classmethod
    def jsonAppender(self, rowZero, 
                     SummaryText, Topic):
        '''
        ----------
        Function
        ----------
        * Cleans SummaryText of each section
        * Cleans Topics of each section
        * Creates a Dict named data with Keywords as:
            > Topics
            > Words
            > Summary
        * Dumps data dict into a JSONFile in append mode
        
        --------
        INPUT
        --------
        rowZero = Most Significat Words of one section
        SummaryTest = Summary of one section
        Topics = Topic of one section
        
        -------
        RETURN
        -------
        None
        
        '''
        logging.info('Inside JSONAppender')
        logging.info('Cleaning Summary Text')
        SummaryText = re.sub('\u2211', '', SummaryText)
        SummaryText = re.sub('\u2019', "'", SummaryText)
        SummaryText = re.sub("\n", "", SummaryText)
        SummaryText = re.split("[.]", SummaryText)
        
        logging.info('Cleaning Topic')
        Topic = re.sub('[()]', '', Topic)
        Topic = re.sub('Casual Leave', 'Casual Leave (C L)', Topic)
        Topic = re.sub('Privilege Leave Sick Leave', 'Privilege Leave, Sick Leave (P L)', Topic)
        Topic = re.sub("\n", "", Topic)
        
        logging.info('Creating Data Dict')
        data = {'Topic': Topic,
                'Words': rowZero,
                'Summary': SummaryText
                }
        
        logging.info('Dumping Data Dict in %s', JSONFile)
        with open(JSONFile, 'a') as f:  
            json.dump(data, f, indent=5)
        logging.info('Exiting JSONAppender')
        
# =============================================================================
#         
# =============================================================================
    
    @classmethod
    def SummaryTheText(self, SectionalText, CallNumber = 0):
        '''
        ----------
        Function
        ----------
        * recievs sectional text
        * Cleans the sectional text
        * Summarise based on text size
        * Saves the summary to Summary.txt file for each section
        
        --------
        INPUT
        --------
        SectionalText = Section Vise text for summarization
        CallNumber = Used to iterate over differend files differentiated based on
                     number (Default = 0)
        
        -------
        RETURN
        -------
        None
        
        '''
        OutputFileNamePAth = 'Summary'+str(CallNumber)+'.txt'
        logging.info("Inside SummaryCreator")
        logging.info("Creating Summary by opening Summary%s.txt", CallNumber)
        with open(OutputFileNamePAth, 'w') as f:
            
            text = re.sub("∑", " \n", SectionalText)
            text =  unidecode(text)
            text = re.sub(r'[^\x00-\x7F]+', '', text)
        
        
            
            if(len(text) <= 300):
                text = summarize ('Test', text, count = 4)
                text = "\n".join(text)
                text = re.sub('IntroductionThis', 'Introduction This', text )
            else:
                text = summarizer.summarize(text, ratio = 0.5)
            print(len(SectionalText))
            print("Summary -->")
            print(text)
            if(len(text) == 0):
                text = summarize ('Test', SectionalText, count = 4)
                text = "\n".join(text)
                text = summarizer.summarize(text, ratio = 0.6)
            text = re.sub("\n", "", text)
            f.write(text)
        f.close()
        logging.info("Summary Created")
        logging.info("Exiting SummaryCreator")
        
        
        
# =============================================================================
# 
# =============================================================================
    @classmethod
    def extract_text_from_pdf(self, pdf_path):
        '''
        ----------
        Function
        ----------
        * Opens PDF page by page and stores text inside text object

        --------
        INPUT
        --------
        pdf_path = path to the pdf
        
        -------
        RETURN
        -------
        text = raw text object
        
        '''
        """ Converting PDF to Text"""
        logging.info('Inside extract_text_from_pdf')
        resource_manager = PDFResourceManager()
        fake_file_handle = io.StringIO()
        converter = TextConverter(resource_manager, fake_file_handle)
        page_interpreter = PDFPageInterpreter(resource_manager, converter)
     
        with open(pdf_path, 'rb') as fh:
            for page in PDFPage.get_pages(fh, 
                                          caching=True,
                                          check_extractable=True):
                page_interpreter.process_page(page)
     
            text = fake_file_handle.getvalue()
     
        converter.close()
        fake_file_handle.close()
     
        #if the text is non zero
        if text:
            logging.info('Exiting extract_text_from_pdf')
            return text
        
        logging.info('Exiting extract_text_from_pdf')
        
    # =============================================================================
    # 
    # =============================================================================
    @classmethod 
    def PdfToText(self, pdf_path):
        '''
        ----------
        Function
        ----------
        * Call extract_text_from_pdf
        * check if the pdf is readable 
        * calls OCRFunction if the file is OCR readable
        * Else return raw text from pdf
        
        --------
        INPUT
        --------
        pdf_path = path to pdf
        
        -------
        RETURN
        -------
        OutputText = raw text from pdf
        
        '''
        logging.info('Inside PdfToText')
        """Calling PDF to Text function"""
        global OutputText
        OutputText = self.extract_text_from_pdf(pdf_path)
        if (OutputText[3] == '\x0c'):
            print('This Is a OCR based PDF, Please use OCR function on it')
            logging.info('Exiting PdfToText')
            self.OCRFunction()
            
        else:
            print('Text Fetched...')
            OutputText = re.sub('Privilege Leave, Sick Leave ()', 'Privilege Leave Sick Leave ()', OutputText)
            logging.info('Exiting PdfToText')
            return OutputText
    
    # =============================================================================
    # 
    # =============================================================================
    
    @classmethod
    def TextObjToTextFile(self, OutputText, OutputFileNamePAth):
        '''
        ----------
        Function
        ----------
        * Converts raw text from pdf to text file in write mode
        
        --------
        INPUT
        --------
        * OutputText = raw text obejct
        * OutputFileNamePAth = path to generate text file on
        
        -------
        RETURN
        -------
        None
        
        '''
        logging.info('Inside TextObjToTextFile')
        """ Storing PDF to text output object into an output.txt file"""
        f = open(OutputFileNamePAth, 'w') 
        lines = OutputText
        f.write(lines)
        f.close()
        logging.info('Inside TextObjToTextFile')
        
    # =============================================================================
    # 
    # =============================================================================
    @classmethod   
    def NLP_PreProcessing(self, OutputTextFromPdf):
        '''
        ----------
        Function
        ----------
        * Use regex to process and clean raw text
        
        --------
        INPUT
        --------
        OutputTextFromPdf = raw text from pdf
        
        -------
        RETURN
        -------
        RepairText = clean processed text
        
        '''
        logging.info('Inside NLP_PreProcessing')
        """ Using custom regex"""
        CustomRegexWords = ("us | this | shall | use | one | two | three | may | every | also | us | give | companys | acidaes | others | company | Company")
        customRegex = re.sub(CustomRegexWords, " ", OutputTextFromPdf)
        """Remove white spaces """
        WitoutSpaceList = re.split('^[0-9]+_[LU]_|-|\.txt$', customRegex) 
        """Joining the list to a string """
        WitoutSpaceString = "".join(WitoutSpaceList)
        """Removing double spaces"""
        WithoutDoubleSpace = re.sub(r"  ", " ", WitoutSpaceString)
        """Removing triple spaces"""
        WithoutTripleSpace = re.sub(r"   ", " ", WithoutDoubleSpace)
        """Removing concatination i'd to i would"""
        WithoutConcatination = contractions.fix(WithoutTripleSpace)
        """Removing Apostrophe"""
        WithoutApostrophe = re.sub(r"' | \x0c", "", WithoutConcatination)
        """Removeing any commas"""
        WithoutComma = re.sub(r",", " ", WithoutApostrophe)
        """Removeing double"""
        WithoutExclamation = re.sub(r"!", " ", WithoutComma)
        """Removeing rest of the Punctuations"""
        WithoutPunctuations = re.sub(r'[^\w\s]',' ',WithoutExclamation)
        """Manualy subsituting some other text"""
        RepairText = re.sub(r"I D", "ID", WithoutPunctuations) #    print(WithoutPunctuations)
        RepairText = re.sub(r'willour', 'will our', RepairText)
        print(" ")
        print('Text Repaired...')
        print(" ")
        logging.info('Exiting NLP_PreProcessing')
        return RepairText
    
    # =============================================================================
    # 
    # =============================================================================
    @classmethod
    def StopWordsRemoval(self, words):
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
        stop_words = set(stopwords.words('english'))
        filtered_sentence = [w for w in words if not w in stop_words]
        filtered_sentence = [] 
        for w in words: 
            if w not in stop_words:
                filtered_sentence.append(w) 
        
        return filtered_sentence
        
    @classmethod
    def remove_non_ascii(self, words):
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
        """Remove non-ASCII characters from list of tokenized words"""
        new_words = []
        for word in words:
            new_word = unicodedata.normalize('NFKD', word).encode('ascii', 'ignore').decode('utf-8', 'ignore')
            new_words.append(new_word)
        return new_words
     
    @classmethod
    def to_lowercase(self, words):
        '''
        ----------
        Function
        ----------
        * Convert tokenized text to lower case

        --------
        INPUT
        --------
        words = tokenized text
        
        -------
        RETURN
        -------
        new_words = cleaned tokenized text
        
        '''
        """Convert all characters to lowercase from list of tokenized words"""
        new_words = []
        for word in words:
            new_word = word.lower()
            new_words.append(new_word)
        return new_words
        
    @classmethod
    def replace_numbers(self, words):
        '''
        ----------
        Function
        ----------
        * Remove numbers

        --------
        INPUT
        --------
        words = tokenized text
        
        -------
        RETURN
        -------
        new_words = cleaned tokenized text
        
        '''
        """Replace all interger occurrences in list of tokenized words with textual representation"""
        p = inflect.engine()
        new_words = []
        for word in words:
            if word.isdigit():
                new_word = p.number_to_words(word)
                new_words.append(new_word)
            else:
                new_words.append(word)
        return new_words
        
    @classmethod
    def remove_stopwords(self, words):
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
        """Remove stop words from list of tokenized words"""
        new_words = []
        for word in words:
            if word not in stopwords.words('english'):
                new_words.append(word)
        return new_words
        
    @classmethod
    def lemmatize_verbs(self, words):
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
        """Lemmatize verbs in list of tokenized words"""
        lemmatizer = WordNetLemmatizer()
        lemmas = []
        for i in range(len(words)):
            lemma = lemmatizer.lemmatize(words[i])
            lemmas.append(lemma)
        return lemmas
        
    @classmethod
    def TextTokanization(self, RepairedText):
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
        TokenizedOutput = word_tokenize(RepairedText)
        return TokenizedOutput
    
    @classmethod
    def normalize(self, TokanizedText):
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
        NoramizedTextStage1 = self.remove_non_ascii(TokanizedText)
        NoramizedTextStage2 = self.to_lowercase(NoramizedTextStage1)
        NoramizedTextStage3 = self.replace_numbers(NoramizedTextStage2)
        NoramizedText = self.remove_stopwords(NoramizedTextStage3)
        return NoramizedText
    
    @classmethod
    def lemmatizer(self, TokanizedText):
        '''
        ----------
        Function
        ----------
        * Performs lemmatization
     
        --------
        INPUT
        --------
        TokanizedText
        
        -------
        RETURN
        -------
        Lemmatized twxt
        
        '''
        lemmas = self.lemmatize_verbs(TokanizedText)
        return lemmas
    
    def OCRFunction(self): 
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
        raise Exception("OCR Function To Be Implemented")
    
    @classmethod
    def Finaliser( self, pathToPdf, PathToText):
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
        logging.info('Inside Finaliser')
        logging.info('Calling PdfToText from Finaliser to create text file')
        OutputText = self.PdfToText(pathToPdf)
        
    #Step 2 - Object to txt
        logging.info('Calling TextObjToTextFile')
        self.TextObjToTextFile(OutputText, PathToText)
        
    #step 3 - Processing the raw text
        logging.info('Cleaining the text using NLP_PreProcessing function')
        RepairedText = self.NLP_PreProcessing(OutputText)
        
    #step 4 - Tokenizing the Repaired Text
        logging.info('Performaing tokinization TextTokanization function')
        TokanText = self.TextTokanization(RepairedText)
        
        logging.info('Removing stop words using StopWordsRemoval function')
        TokenTextWithoutStopWords = self.StopWordsRemoval(TokanText)
        
        #STep 5 - Normalising the tokens
        logging.info('Permorming normalization using normalize function')
        NormalizedText = self.normalize(TokenTextWithoutStopWords)
        
    #Step 6 - stems and lemmatizers
        logging.info('Performing lemmatization using lemmatizer function')
        Lemmatised = self.lemmatizer(NormalizedText)
        
        logging.info('Inside Finaliser')
        vectorizer = TfidfVectorizer(lowercase=True, 
                                     stop_words = stopwords.words('english'), 
                                     min_df=1,
                                     max_df=1.0)
        
        logging.info('Inside Finaliser')
        matrix = vectorizer.fit_transform(Lemmatised).todense()
        """ transform the matrix to a pandas df """
        matrix = pd.DataFrame(matrix, columns=vectorizer.get_feature_names())
        """ sum over each document (axis=0) """
        logging.info('Exiting Finaliser')
        return OutputText
    
    # =============================================================================
    # 
    # =============================================================================
    
    @classmethod
    def StartFunction(self, pdf_toread):
        '''
        ----------
        Function
        ----------
        * Subsitute string with .pdf to ''
        * Calls Finaliser and pass path to pdf and path to .txt file to produce
        
        --------
        INPUT
        --------
        pdf_toread = path to pdf
        
        -------
        RETURN
        -------
        OutputText = raw text converted from pdf
        
        '''
        logging.info('Inside StartFunction')
        pdf_toread = pdf_toread
        text_toread = re.sub(".pdf", "", pdf_toread)
        logging.info('Calling Finaliser from start function')
        OutputText = self.Finaliser(pdf_toread, text_toread+".txt")
        logging.info('Exiting StartFunction')
        return OutputText
        
    # =============================================================================
    # 
    # =============================================================================
        
    @classmethod
    def FinaliserSection(self, SectionalText, CallNumber):
        '''
        ----------
        Function
        ----------
        * Cleans sectional text using NLP_PreProcessing
        * Call SummaryTheText and summarize the sectional text
        * Tokensize the text using TextTokanization
        * Remove stop words using StopWordsRemoval
        * normalise the text using normalize
        * Lemmatize using lemmatizer
        * perform TfIdf Cevtorisation using TfidfVectorizer
        
        --------
        INPUT
        --------
        * SectionalText
        * CallNumber
        
        -------
        RETURN
        -------
        Top 10 significant words for each section
        
        '''
    #step 3 - Processing the raw text
        SectionalText = re.sub('IntroductionThis', 'Introduction This', SectionalText)
        with open("SectionalText"+str(CallNumber)+".txt", 'w') as f:
            f.write(SectionalText)

        RepairedText = self.NLP_PreProcessing(SectionalText)
        self.SummaryTheText(SectionalText, CallNumber)
    #step 4 - Tokenizing the Repaired Text
        TokanText = self.TextTokanization(RepairedText)
        TokenTextWithoutStopWords = self.StopWordsRemoval(TokanText)
        #STep 5 - Normalising the tokens
        NormalizedText = self.normalize(TokenTextWithoutStopWords)
    #Step 6 - stems and lemmatizers
        Lemmatised = self.lemmatizer(NormalizedText)
        vectorizer = TfidfVectorizer(lowercase=True, 
                                     stop_words = stopwords.words('english'), 
                                     min_df=1,
                                     max_df=1.0)
        matrix = vectorizer.fit_transform(Lemmatised).todense()
        """ transform the matrix to a pandas df """
        matrix = pd.DataFrame(matrix, columns=vectorizer.get_feature_names())
        """ sum over each document (axis=0) """
        top_words = matrix.sum(axis=0).sort_values(ascending=False)
        print('Top words section wise is done...')
        
        top_words.head(10).to_csv(r'HeadWords'+str(CallNumber)+'.csv')
        
        self.ReaderJsonCreator(CallNumber)
        return top_words.head(10)
        
        
    @classmethod
    def MatcherFunction(self, WordList, RepairedText):
        '''
        ----------
        Function
        ----------
        * Inputs the complete text inside a PDF
        * Inputs the list of Headings
        * Matches heading with the raw text
        * Divide each section based on wordslist
        * Incriment CallNumber With eavery index matched
        * Calls FinaliserSection to perform Stemming, normalising, tokensing and TfIdf vectorisation
        * Recieves most significat words
        
        --------
        INPUT
        --------
        WordsList = List of Index words to match
        RepairedText = Complete raw text of PDF to detect sections from
        
        -------
        RETURN
        -------
        None
        
        '''
        logging.info('Inside MatcherFunction')
        logging.info('Recieved WordsList is: %s', WordList)
        global i, CallNumber
        i = 0 
        CallNumber = 0
        global X, Y
        global SectionalText
        X = []
        Y = []
        SectionalText = ''
        
        while (i < len(WordList)):
            match = re.search(WordList[i], RepairedText)
            # If-statement after search() tests if it succeeded
            if match:
                print("")
                logging.info('Match found %s', WordList[i])
                print ('found', match.group())
                LocationTupple = match.span()
                X.append(LocationTupple[0])
                Y.append(LocationTupple[1])
                print (match.span())
                i = i + 1
                
            else:
                print("")
                logging.info('Match was not found for %s', WordList[i])
                print ('did not find')
                i = i + 1
                
        logging.info('Total Number of matches found are: %s', len(X))
        while (CallNumber < len(X)):
            print('')
            print('Length of X is = ')
            print(len(X))
            print('Value of CallNumber is ')
            print(CallNumber)
            logging.info('Completed %s/%s', CallNumber, len(X))
            
            if (CallNumber < len(X) - 1):
                SectionalText = RepairedText[(X[CallNumber]):X[CallNumber+1]]
                SectionalText = re.sub(WordList[CallNumber], '', SectionalText)
                print("")
                print("Value of CallNumber inside the If function")
                print(CallNumber)
                
                logging.info('Calling FinaliserSection function from if condiction')
                Top10Words = self.FinaliserSection(SectionalText, CallNumber)
                self.SummaryTheText(SectionalText, CallNumber)
                CallNumber += 1
                
            else:
                SectionalText = RepairedText[(X[CallNumber]):]
                SectionalText = re.sub(WordList[CallNumber], '', SectionalText)
                print("")
                print("Value of CallNumber inside else")
                print(CallNumber)
    
                logging.info('Calling FinaliserSection function from else condiction')
                Top10Words = self.FinaliserSection(SectionalText, CallNumber)
                self.SummaryTheText(SectionalText, CallNumber)
                CallNumber += 1
                
        logging.info('Exiting MatcherFunction')