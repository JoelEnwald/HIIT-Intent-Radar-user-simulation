# Inputs a query to the server, extracts and compiles the documents from the response. Also
# gathers all the keywords present in the documents into a list, and builds the document-keyword matrix.

import requests, json
import numpy as np
from pprint import pprint
import xmltodict
from urllib.request import urlopen
import time
import platform
import KeywordChooser

# Makes a query to the database using the given search word.
# An example URL:
# http://focus.hiit.fi:8080/hiitwideinternal/service/articles/web/user/tuukka/keys/web%20mining,1.0,web%20warehouse,1.0.xml
def get_data(search_word, clicked_words, weights):
    # Parse the URL from the search words:
    urlKeywordPart = ''
    for i in range(0, len(clicked_words)):
        urlKeywordPart = urlKeywordPart + clicked_words[i] + ',' + str(weights[i]) + ','
    urlKeywordPart = urlKeywordPart[:-1]
    url = 'http://focus.hiit.fi:8080/hiitwideinternal/service/articles/' + search_word + '/user/tuukka' + \
          '/keys/' + urlKeywordPart + '.xml'
    url = url.replace(' ', '+')

    # print(url)
    # Save the HTTPresponse, change it to 'bytes'
    # If there is an internal server error or no data is returned, wait and try again.
    success = 0
    while (success == 0):
        try:
            file = urlopen(url)
        except Exception:
            time.sleep(1)
            continue
        data = file.read()
        file.close()
        # Parse 'data' to unorderedDict
        data = xmltodict.parse(data)
        if data['concept'] is None:
            time.sleep(1)
            continue
        success = 1
    data = data['concept']['fi.hiit.uix.domain.Article']
    return data

# Parses the data and returns, in a dictionary,
# two lists of keywords and documents, and a matrix where the rows are keywords,
# columns are documents, and there is a 1 where the given documents contains
# the given keyword, and 0 elsewhere.
def parse_data(data):
    # Convert 'data' to dict
    # The lists are dictionaries where the values are the index numbers.
    keywordsList = []

    documentsList = []
    document_scores = {}
    i = 0
    j = 0
    documentsAmount = len(data)

    # Create the keywords x documents matrix.
    # The row number of the matrix corresponds to the index number of the previous
    # dictionary. The columns are the documents.
    keywordsDocuments = np.zeros([0, documentsAmount])

    # Collect the keywords into a dictionary where the values are indexes.
    for document in data:
        if document['keywords'] is not None:
            # The object "document['keywords']['string']" may be either a string or an array of
            # strings, depending on if there is only one or multiple keywords. This has to be
            # taken into account.
            go_through = document['keywords']['string']
            # If there is one keyword, a string
            if type(go_through) is str:
                keyword = go_through
                if not keyword in keywordsList:
                    keywordsList.append(keyword)
                    # Add a new row to matrix
                    keywordsDocuments = np.vstack((keywordsDocuments, np.zeros(documentsAmount)))
                    keywordsDocuments[i][j] = 1
                    i = i + 1
                else:
                    keywordsDocuments[keywordsList.index(keyword)][j] = 1
            # If there are several keywords, an array
            else:
                for keyword in go_through:
                    if not keyword in keywordsList:
                        keywordsList.append(keyword)
                        # Add a new row to matrix
                        keywordsDocuments = np.vstack((keywordsDocuments, np.zeros(documentsAmount)))
                        keywordsDocuments[i][j] = 1
                        i = i + 1
                    else:
                        keywordsDocuments[keywordsList.index(keyword)][j] = 1
        documentsList.append(document['title'])
        document_scores[document['title']] = document['score']
        j = j + 1

    keywordsAmount = len(keywordsList)


    results = {'keywords':keywordsList, 'documents':documentsList, 'resultmatrix':keywordsDocuments,
               'scores':document_scores}
    return results