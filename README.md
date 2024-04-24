# This repository include a text matching analytics project which uses fuzzywuzzy algorithm to match compliance words from call text.

## The repo structure is as follows

1) data
- data.csv: a sample of call transcripts data taken from Kaggle[https://www.kaggle.com/datasets/mealss/call-transcripts-scam-determinations]

2) src
- app.py: a Python module includes the class and functions to load, process, and find matching compliance words using fuzzywuzzy algorthim

3) utils
- utils.py: a Python module includes basic unit testing for the functions in the app.py module.

## Python Packaging
1) Poetry installed
2) pandas = "^1.1.5"
3) fuzzywuzzy = "^0.18.0"
4) loguru = "^0.7.2"
5) nltk = "^3.6.7"
6) pytest = "^7.0.1"

## To run the modules using the command line:
- python app.py
- pytest utils.py


