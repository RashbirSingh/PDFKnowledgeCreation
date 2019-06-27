#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 12:51:29 2019

@author: ubuntu
"""


from flask import Flask, request
from flask_restful import Api
from flask import jsonify
from flask_cors import CORS
import logging

app = Flask(__name__)
api = Api(app)
CORS(app)

logging.basicConfig(filename='PDFReader.log',
                        filemode='a',
                        format='%(asctime)s:%(msecs)d - %(name)s %(levelname)s - %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.INFO)

logging.getLogger('pdfminer.pdfinterp').disabled = True
logging.getLogger('pdfminer.pdfdocument').disabled = True
logging.getLogger('pdfminer.pdfpage').disabled = True

import MasterFile

@app.route("/pdftoextract", methods =['GET'])
def hello():
    pdftoextract = request.args.get('pdftoextract')
    logging.info('Recieved pdftoextract path is: %s', pdftoextract)
    result = MasterFile.Master(pdftoextract)
    return jsonify(result) 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 5089, debug = True)
