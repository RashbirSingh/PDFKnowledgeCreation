# Added Flask Support and Code is more robust

_List of files-_

| File Name        | Role           | Return Type  |
| ------------- |:-------------:| -----:|
| MasterFile.py      | Controls the flow of code | List |
| 'Server3_5002.py' , 'service.py', 'Service2-5010.py'      | Runs server at port 5002 and 5010      |   Json |
| JSONCreator.py | Created a syatem dependent Location.json      |    Json file in local machine |
| Initial_code.py      | Raw text cleaning and fetches text from a text readable file | Raw text from pdf in .txt format and top significant words |
| Cleaner.py      | Cleans the created files at the end of program execution | Nan |
| IndexScraping.py      | Search for topics in file having index on page 3 | List of headings |
| StartUpCleaner.py      | Cleans the previous created JSON files if any at the start of program | Nan |


_instruction to use -_

* Run command ```python JSONCreator.py``` in the directory containing all the files
> This will create a `Location.json file` that will have all the locations to the files that will be `dependent to the machine` and required to run various commands

* Run command ```python -c "from MasterFile import Master; print(Master('__Pdf_name.pdf__'))"```
 > It will return a list of `dictonaries` having -  <br>
 __1. Topic__ - _Heading of the paragraph_ <br>
 __2. Words__ - _Top most significat words_  <br>
 __3. Summary__ - _Short summary realted to the topic_  <br>

