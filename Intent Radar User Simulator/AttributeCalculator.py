import platform
import DocuKeyDataExtractor
import csv

global RELEVANT_DOC_AMOUNT
global NOVEL_DOC_AMOUNT
global RELEVANT_KEY_AMOUNT
global SPECIFIC_KEY_AMOUNT

RELEVANT_DOC_AMOUNT = 3551
NOVEL_DOC_AMOUNT = 2672
DOC_CSV_SIZE = 5794

RELEVANT_KEY_AMOUNT = 985
SPECIFIC_KEY_AMOUNT = 758
KEY_CSV_SIZE = 1440

# Supporting method
# Count the relevant/novel/obvious documents in a list of document data
def count_documents_with_attribute(document_data, attribute, context):
    count = 0
    if attribute == "relevant":
        index = 2
    elif attribute == "novel":
        index = 4
    else:
        index = 3
    for line in document_data:
        if line[index] == '1':
            count = count + 1
    return count

# Supporting method
# Count the relevant/specific/general keywords in a list of keyword data
def count_keywords_with_attribute(keyword_data, attribute, context):
    count = 0
    if attribute == "relevant":
        index = 1
    elif attribute == "specific":
        index = 3
    else:
        index = 2
    for line in keyword_data:
        if line[index] == '1' and line[4] == context:
            count = count + 1
    return count

# The novel documents are counted in relation to relevant documents.
# Relevant documents are counted in relation to all documents.

# counted_document_amount specifies how many of the documents shown to the user we
# are interested in taking into account in our calculations. The latter documents are
# not as interesting because the user might never get to them.
def calc_document_relevancy_novelty_precision(documents_datas, context, counted_document_amount):
    novel_shares = []
    novel_amounts = []
    relevant_shares = []
    relevant_amounts = []
    for data in documents_datas:
        # Only take into account the first documents
        counted_data = data[1:max(len(data), counted_document_amount)]
        novel_amounts.append(count_documents_with_attribute(counted_data, "novel", context))
        relevant_amounts.append(count_documents_with_attribute(counted_data, "relevant", context))
    for i in range(0, len(documents_datas)):
        if len(documents_datas[i]) == 0:
            relevant_shares.append(0)
        else:
            relevant_shares.append(relevant_amounts[i] / len(documents_datas[i]))
        if relevant_amounts[i] == 0:
            novel_shares.append(0)
        else:
            novel_shares.append(novel_amounts[i] / relevant_amounts[i])
    return relevant_shares, novel_shares

def calc_document_relevancy_novelty_recall(documents_datas_cumul, context, counted_document_amount):
    relevant_amounts = []
    novel_amounts = []
    for data in documents_datas_cumul:
        # Only take into account the first documents
        counted_data = data[1:max(len(data), counted_document_amount)]
        novel_amounts.append(count_documents_with_attribute(counted_data, "novel", context))
        relevant_amounts.append(count_documents_with_attribute(counted_data, "relevant", context))
    # Create the new lists which contain the relevant and novel amounts as proportions:
    # in other words, recall.
    novel_amounts_prop = [x / NOVEL_DOC_AMOUNT for x in novel_amounts]
    relevant_amounts_prop = [x / RELEVANT_DOC_AMOUNT for x in relevant_amounts]
    return relevant_amounts_prop, novel_amounts_prop

# The specific keywords are counted in relation to relevant keywords.
# Relevant keywords are counted in relation to all keywords
def calc_keyword_relevancy_specificity_precision(keywords_datas, context):
    relevant_shares = []
    relevant_amounts = []
    specific_shares = []
    specific_amounts = []
    for data in keywords_datas:
        relevant_amounts.append(count_keywords_with_attribute(data, "relevant", context))
        specific_amounts.append(count_keywords_with_attribute(data, "specific", context))
    for i in range(0, len(keywords_datas)):
        # In the baseline case there are no keywords
        if len(keywords_datas[i]) == 0:
            relevant_shares.append(0)
        else:
            relevant_shares.append(relevant_amounts[i] / len(keywords_datas[i]))
        if relevant_amounts[i] == 0:
            specific_shares.append(0)
        else:
            specific_shares.append(specific_amounts[i] / relevant_amounts[i])
    return relevant_shares, specific_shares

def calc_keyword_relevancy_specificity_recall(keywords_datas_cumul, context):
    relevant_amounts = []
    specific_amounts = []
    for data in keywords_datas_cumul:
        relevant_amounts.append(count_keywords_with_attribute(data, "relevant", context))
        specific_amounts.append(count_keywords_with_attribute(data, "specific", context))
    relevant_amounts_prop = [x / RELEVANT_KEY_AMOUNT for x in relevant_amounts]
    specific_amounts_prop = [x / SPECIFIC_KEY_AMOUNT for x in specific_amounts]
    return relevant_amounts_prop, specific_amounts_prop

def check_if_keyword_relevant(keyword, context):
    slash = "/"
    # Windows uses different separators in file paths than other OS's.
    if platform.system() == "Windows":
        slash = "\\"
    else: slash = "/"
    extractor = DocuKeyDataExtractor
    with open('Attachments_Dataa' + slash + 'All_keywords.csv', 'rt') as keywords_file:
        reader = csv.reader(keywords_file)
        for line in reader:
            if line[0] == keyword:
                if line[4] == context:
                    if line[1] == '1':
                        return 'yes'
                    else:
                        return 'no'
    keywords_file.close()
    return 'not found'


