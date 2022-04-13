import numpy as np


# Combines the existing and new keywords, documents and matrices. Also calculates the upper
# confidence bound (UCB) scores for the keywords.
class LinRel:

    mu = 0.5
    keyword_doc_matrix = []
    keywords = []
    documents = []

    # Initialize the variables and make them global
    def __init__(self):
        global documents
        documents = []
        global keywords
        keywords = []
        global keyword_doc_matrix
        keyword_doc_matrix = np.zeros((0,0))
        global mu
        mu = 0.5

    # Checks which keywords a certain document contains.
    def get_doc_keywords(self, document, keywords, documents, matrix):
        document_i = documents.index(document)
        document_keywords = []
        for k in range(0, np.shape(matrix)[0]):
            if matrix[k, document_i] == 1:
                document_keywords.append(keywords[k])
        return document_keywords

    # doc_keywords contains the keywords in the matrix in the same order as in the matrix.
    # clicked_words has the keywords that have been clicked by the user.
    # clicked_weights is a vector of the weights of the keywords that have been clicked.
    def get_keyword_scores(self, new_keywords, new_documents, new_matrix, clicked_words, clicked_weights, c):

        global documents
        global keywords
        global keyword_doc_matrix
        global mu

        # Add the information of the new matrix to the old one
        for new_d_i in range(0, len(new_documents)):
            new_document = new_documents[new_d_i]
            doc_keywords = self.get_doc_keywords(new_document, new_keywords, new_documents, new_matrix)

            # If the document to be added is already in the matrix
            if new_document in documents:
                old_d_i = documents.index(new_document)
                for keyword in doc_keywords:
                    # If the keyword is not among the old keywords
                    if keyword not in keywords:
                        # Add a new row representing the new keyword
                        keywords.append(keyword)
                        debugA = np.shape(keyword_doc_matrix)[1]
                        new_row = np.zeros((1, debugA))
                        new_row[0, old_d_i] = 1
                        keyword_doc_matrix = np.vstack((keyword_doc_matrix, new_row))
                    # If both the document and the keyword are already marked
                    # in the matrix, nothing needs to be done.
            # If the document is not in the matrix, a new column needs to be added
            else:
                documents.append(new_document)
                # Make a new column of the right size.
                new_column = np.zeros((np.shape(keyword_doc_matrix)[0], 1))
                # Go through the keywords in the document
                for keyword in doc_keywords:
                    # If the keyword is known, get its index and mark it in the new column
                    if keyword in keywords:
                        keyword_i = keywords.index(keyword)
                        new_column[keyword_i] = 1
                    # If the keyword is not know, create a new row for the keyword, add that
                    # to the existing matrix and make sure to add the keyword to the
                    # new column we are creating
                    else:
                        row_for_new_keyword = np.zeros((1, np.shape(keyword_doc_matrix)[1]))
                        keyword_doc_matrix = np.vstack((keyword_doc_matrix, row_for_new_keyword))
                        keywords.append(keyword)
                        # Add a '1' to the the column to be added to mark the keyword to be added
                        if np.shape(new_column) == (0, 0):
                            new_column = np.ones((1,1))
                        else:
                            new_column = np.vstack((new_column, np.ones((1,1)) ))
                keyword_doc_matrix = np.hstack((keyword_doc_matrix, new_column))

        # Convert the short vector 'weights' containing the weights only for the keywords that have
        # been clicked to a longer vector weights_zeroes containing also zeroes for the keywords
        # that have not been clicked.
        weights_zeros = np.zeros(len(keywords))
        if len(clicked_words) == 0:
            weights_zeros = np.random.rand(len(keywords))
        else:
            for i in range(0, len(clicked_words)):
                word = clicked_words[i]
                weight = clicked_weights[i]
                if word in doc_keywords:
                    index = doc_keywords.index(word)
                    weights_zeros[index] = weight

        temp_matrix = keyword_doc_matrix.T.dot(keyword_doc_matrix)
        iden_matrix = np.identity(np.shape(temp_matrix)[0])
        # Pseudo-inverse constant that stays constant for each keyword. (X'X + mu)^-1 * X'
        pinv_constant = np.linalg.solve(temp_matrix + iden_matrix*self.mu, keyword_doc_matrix.T)
        # Above, should mu be added to all

        keyword_scores = []

        # Calculate the upper confidence bounds for the keywords
        for i in range(0, np.shape(keyword_doc_matrix)[0]):

            debug1 = keyword_doc_matrix[i]
            ai = keyword_doc_matrix[i].dot(pinv_constant)

            # Exploration component, l^2 norm (euclidean norm) with adjustment factor c
            exploration = c / 2 * np.sqrt(np.dot(ai, ai.T))

            ols = float(np.dot(ai, weights_zeros))

            # Upper confidence bound
            ucb = float(ols + exploration)
            keyword_scores.append(ucb)

        zipped_list = zip(keyword_scores, keywords)
        zipped_list = sorted(zipped_list, key = lambda x: x[0], reverse = True)
        keyword_scores, keywords = zip(*zipped_list)
        keywords = list(keywords)

        return keyword_scores, keywords, documents