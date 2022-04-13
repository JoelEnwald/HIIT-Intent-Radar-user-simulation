import csv
import platform


keywords_all = []
documents_all = []
reader = None
slash = "/"

# Read all the keyword and document data from file
# Windows uses different separators in file paths than other OS's.
if platform.system() == "Windows":
    slash = "\\"
with open('Attachments_Dataa' + slash + 'All_keywords.csv', 'rt') as keywords_file:
    reader = csv.reader(keywords_file)
    for line in reader:
        keywords_all.append(line)
keywords_file.close()
with open('Attachments_Dataa' + slash + 'All_documents.csv') as documents:
    reader = csv.reader(documents)
    for line in reader:
        documents_all.append(line)
documents.close()

# Get the data for given keywords
def get_keyword_data(keywords):
    data = []
    for keyword in keywords:
        found = 0
        # A terribly inefficient way to go through the keywords. Should sort
        # the list for efficiency.
        for line in keywords_all:
            if keyword == line[0]:
                found = 1
                data.append(line)
                break
        # If the keyword was not found among the CSV file All_keywords, add
        # the document with 0 parameters
        if found == 0:
            data.append([keyword, '0', '0', '0', 'Unknown context'])
    return data

# Get the data for given documents
def get_document_data(documents):
    data = []
    for document in documents:
        found = 0
        # Terribly inefficient
        for line in documents_all:
            if document == line[0]:
                found = 1
                data.append(line)
                break
        # If the document was not found among the CSV file All_documents, add
        # an unknown author and zero parameters for the document.
        if found == 0:
            data.append([document, 'Someone', 0,0,0, 'Unknown context'])
    return data
