import numpy
from collections import defaultdict
import TFIDF
import random
import UCB
import Kernel

class DK(object):
    
    # Algorithm parameters
    MU = 0.5
    C = 2
    E = 0.001
    RENEW = 0.9
    


    # Initialize the DK object by list of objects of type Article
    def __init__(self, articles_display = 10, keywords_display = 10):
        
        # Global parameters
        self.articles_display = articles_display
        self.keywords_display = keywords_display                   
 
        # Attributes for Linrel algorithm
        # keywords_presented - array of string keywords about which we have already got the feedback
        self.relevance_scores = []
        # List of keywords that we have seen so far
        self.keywords = []
    
        # We store the articles from the previous iteration
        self.old_articles = []
        self.old_articles_sorted = []
        self.old_article_to_id = []
 
        # In order to be ably to give change in the weight, not the weight itself
        self.old_selection_criteria = dict()
    
        # List containing keywords rejected by the user
        self.stop_list = list()   
        
        # We provide search engine with two relevance vectors - the current and the previous
        self.old_relevance = dict()
        self.new_relevance = dict() 
        
        # for bandits
        self.previous_keywords = dict()
        self.thompson = UCB.THOMPSON()
        
#        self.ucb_tuned = UCB.UCB_TUNED()
#        self.dorota = UCB.DOROTA()
        
        
    def Sample (self, probability_dict):
        
        r = random.random()
        cumulative_sum = 0
        
        for keyword in probability_dict:
            if cumulative_sum < r:
                cumulative_sum = cumulative_sum+probability_dict[keyword]
                sampled_word = keyword
                       
        return sampled_word
          
    # Before we get any user feedback on keywords, we are choosing first #keywords_display to show by counting weighted average sum of keywords in articles
    # Uses information only from initialization
    # Returns dictionary result_keywords - top #keywords_display keywords and their ranks      
    def FirstRound(self, articles):
        
        articles = list(set(articles).intersection(set(articles)))
        
        # Initialize old_articles
        for a in articles:
            self.old_articles.append(a)
        
        # Given a list of articles we have to fill in dictionaries keyword_to_article, article_to_counts, article_to_rank, articles_to_index and articles
        # as attributes of tfidf
        self.tfidf = TFIDF.TFIDF(articles)
        self.old_article_to_id = self.tfidf.article_to_id
        keyword_to_rank = dict()
        for keyword in self.tfidf.keyword_to_article:
            keyword_to_rank[keyword] = 0
            for article in self.tfidf.keyword_to_article[keyword]:
                keyword_to_rank[keyword] += self.tfidf.article_to_rank[article]
                
        
                
        keyword_to_rank_normed = dict()
        key_sum = sum(keyword_to_rank.values())
        for keyword in keyword_to_rank:
            keyword_to_rank_normed[keyword] = keyword_to_rank[keyword] / key_sum
            
        self.thompson.InitializePrior(keyword_to_rank_normed)
               
        sorted_keyword_to_rank = sorted(keyword_to_rank.keys(), key=lambda s: keyword_to_rank[s], reverse=True)
               
        result_keywords = dict()
        
        for keyword in sorted_keyword_to_rank:
            if len(result_keywords)<self.keywords_display/2:
                result_keywords[keyword] = keyword_to_rank[keyword]
        

        
        while len(result_keywords)<self.keywords_display:
            word = self.Sample(keyword_to_rank_normed)
            if word not in result_keywords:
                result_keywords[word] = keyword_to_rank[word]
        
        '''
        maxweight = max(result_keywords.values())
        for keyword in result_keywords:
            result_keywords[keyword] = result_keywords[keyword]/maxweight
            '''
                
        result_keywords = self.Max1(result_keywords)
            
        self.previous_keywords = result_keywords
        
        return result_keywords
        
    
    def Max1(self, dict_weights):
        maxweight = max(dict_weights.values())
        for keyword in dict_weights:
            dict_weights[keyword] = dict_weights[keyword]/maxweight

        return dict_weights    
    
    '''
    # Help function, returns vector representation of a keyword in from tf-idf model
    def GetKeywordArray(self, keyword, tfidf):
        keywordarray = numpy.zeros([1,tfidf.articles_to_index_num])
        for article in tfidf.keyword_representation[keyword]:
            keywordarray[0,tfidf.articles_to_index[article]] = tfidf.keyword_representation[keyword][article]
        return keywordarray
        '''
    
    def MergeArticleSets(self, new_articles):
        
        #print len(new_articles)
        #print len(self.old_articles)
        #print 'Number of articles preserved = '
        #print len(list(set(self.old_articles).intersection(set(new_articles))))
        
        articles = []
        for article in self.old_articles_sorted:
            if len(articles)<(1-DK.RENEW)*len(self.old_articles):
                articles.append(article)
        for article in new_articles:
            if len(articles) < len(self.old_articles):
                if article not in articles:
                        articles.append(article)
        return articles
             

    # Learning function
    # User_feedback is a dictionary with keywords and their weighs about which we got the feedback
    def LinRel(self, new_articles, user_feedback):
        print 'LinRel started'
        
        self.old_relevance = self.new_relevance
        
        new_articles = list(set(new_articles).intersection(set(new_articles)))
        
        # Current dataset of articles is got by merging the old one and new
        articles = self.MergeArticleSets(new_articles)
        
        print 'Calculate kernel'
        
        # Get the information about tfidf model
        self.kernel = Kernel.Kernel(new_articles)
        
        print 'Kernel calculated'
        
        # Store new parameters of previous article dataset
        self.old_articles = articles
        self.old_articles_sorted = sorted(self.old_articles, key=lambda s: s.score, reverse=True)

        self.old_article_to_id = self.kernel.articles
        
        # Matrix representing topic models for documents that have already been presented
        keywords_presented = numpy.array([])
        
        for keyword in user_feedback:
            
            # Add keywords with 0 feedback to the stop list of words that will never appear again
            # If we are giving explicit feedback to a keyword form a stop list, remove it from a stop list
            if user_feedback[keyword]==0:
                self.stop_list.append(keyword)
            else:
                if keyword in self.stop_list:
                    self.stop_list.remove(keyword)
            
            self.keywords.append(keyword)
            self.relevance_scores.append(user_feedback[keyword])
            
        # To prevent 0 feedback on the first iteration  
            
        for keyword in self.keywords:
            keywordarray = self.kernel.Distance(keyword)
            if (numpy.shape(keywords_presented)[0]==0):
                keywords_presented = keywordarray
            else:
                keywords_presented = numpy.vstack((keywords_presented, keywordarray))     
        
        # LinRel computations        
        # Diagonal matrix with mu on the diagonal
        Mu = DK.MU*numpy.eye(len(self.kernel.keywords))
        # selection criteria is a dictionaty keyword - calculated rank
        selectioncriteria = dict();
        # article weights from linear regression by which we can sort them to rank
        article_weighs = numpy.zeros((1,len(self.kernel.articles)));
        # temporary variable which is the same for all keywords
        temp = numpy.linalg.inv(numpy.dot(keywords_presented.T, keywords_presented)+Mu)
        # For all the keywords
        for keyword in self.kernel.keywords:
            # Keyword representation in terms of article tf-idf for every keyword
            xI = self.kernel.Distance(keyword)
            aI = numpy.dot(numpy.dot(xI,temp),keywords_presented.T)
            # Calculate the criteria by which to decide with document to choose next
            # Upper confidence bound on score of the keyword
            selectioncriteria[keyword] = float(numpy.dot(aI, (numpy.array(self.relevance_scores)+DK.E).T)+DK.C/2*numpy.dot(aI, aI.T))
            # Weights from linear regression
#            article_weighs = numpy.dot(temp,numpy.dot(keywords_presented.T,(numpy.array(self.relevance_scores)+DK.E)))
            
        self.new_relevance = selectioncriteria
            
        combined_feedback = dict()
        for keyword in self.keywords:
            if keyword not in combined_feedback:
                if keyword in selectioncriteria:
                    if len(self.old_selection_criteria)==0:
                        combined_feedback[keyword] = selectioncriteria[keyword]
                    else:
                        if keyword in self.old_selection_criteria:
                            combined_feedback[keyword] = selectioncriteria[keyword]-self.old_selection_criteria[keyword]
                    
        self.old_selection_criteria = selectioncriteria
        
        # Next_keywords list contains only keywords that didn't receive 0 feedback
        next_keywords = list()
        sorted_keywords = sorted(selectioncriteria.keys(), key=lambda s: selectioncriteria[s], reverse=True)
        for keyword in sorted_keywords:
            if len(next_keywords) < self.keywords_display:
                if keyword not in self.stop_list:
                        next_keywords.append(keyword)
        
        '''      
        # Sort keywords by selection criteria and return indexes of first #keywords_display
        next_keywords = sorted(selectioncriteria.keys(), key=lambda s: selectioncriteria[s], reverse=True)[0:self.keywords_display]
        '''
        
        '''# Sort articles by their weighs and return indexes of first #article_display
        next_articles = numpy.argsort(article_weighs, axis = 0)[ : :-1][0:self.articles_display]'''
        
        
#        old_indexes_sorted = numpy.argsort(article_weighs, axis = 0)[ : :-1]
        
        # After sorting dictionaries we've got lists
        # Result shout also contain ratings, construct result_keywords, result_articles
        result_keywords = dict()
        for keyword in next_keywords:
            result_keywords[keyword] = selectioncriteria[keyword]
        result_articles = dict()
        
        # if last parameter selectioncriteria - desicion is based on all the keywords vector
        # if it is result_keywords - only on keywords that are shown
        article_weighs = self.Predict_Articles(user_feedback, selectioncriteria)
        
        # Sort articles by their weighs and return indexes of first #article_display
        next_articles = sorted(article_weighs.keys(), key=lambda s: article_weighs[s], reverse=True)[0:self.articles_display]
        
        result_articles = list()
        for article in next_articles:
            result_articles.append(article)
            #  [article] = article_weighs[article]
        
        self.previous_keywords = result_keywords
        
        print numpy.shape(self.kernel.articles)
         
        # ne pomnyu zachem eto    
        # self.old_ids_sorted = []
        # for i in old_indexes_sorted:
        #    self.old_ids_sorted.append(self.kernel.articles[i])
            
        result_keywords = self.Max1(result_keywords)

        return result_keywords, result_articles, combined_feedback, self.old_relevance, self.new_relevance
    
    def Predict_Articles(self, user_feedback, keywords_weights):
        
        keywords_new = dict()
        for keyword in user_feedback:
            if user_feedback[keyword] >= self.previous_keywords.get(keyword,0):
                keywords_new[keyword] = 1
            else:
                keywords_new[keyword] = -1
                
        #return self.ucb.UCB(keywords_new, self.article_to_keywords)
        return self.thompson.Bandit(keywords_new, self.kernel.article_to_keywords, keywords_weights)
=======
import numpy
from collections import defaultdict
import TFIDF
import random
import UCB
import Kernel

class DK(object):
    
    # Algorithm parameters
    MU = 0.5
    C = 2
    E = 0.001
    RENEW = 0.9
    


    # Initialize the DK object by list of objects of type Article
    def __init__(self, articles_display = 10, keywords_display = 10):
        
        # Global parameters
        self.articles_display = articles_display
        self.keywords_display = keywords_display                   
 
        # Attributes for Linrel algorithm
        # keywords_presented - array of string keywords about which we have already got the feedback
        self.relevance_scores = []
        # List of keywords that we have seen so far
        self.keywords = []
    
        # We store the articles from the previous iteration
        self.old_articles = []
        self.old_articles_sorted = []
        self.old_article_to_id = []
 
        # In order to be ably to give change in the weight, not the weight itself
        self.old_selection_criteria = dict()
    
        # List containing keywords rejected by the user
        self.stop_list = list()   
        
        # We provide search engine with two relevance vectors - the current and the previous
        self.old_relevance = dict()
        self.new_relevance = dict() 
        
        # for bandits
        self.previous_keywords = dict()
        self.thompson = UCB.THOMPSON()
        
#        self.ucb_tuned = UCB.UCB_TUNED()
#        self.dorota = UCB.DOROTA()
        
        
    def Sample (self, probability_dict):
        
        r = random.random()
        cumulative_sum = 0
        
        for keyword in probability_dict:
            if cumulative_sum < r:
                cumulative_sum = cumulative_sum+probability_dict[keyword]
                sampled_word = keyword
                       
        return sampled_word
          
    # Before we get any user feedback on keywords, we are choosing first #keywords_display to show by counting weighted average sum of keywords in articles
    # Uses information only from initialization
    # Returns dictionary result_keywords - top #keywords_display keywords and their ranks      
    def FirstRound(self, articles):
        
        articles = list(set(articles).intersection(set(articles)))
        
        # Initialize old_articles
        for a in articles:
            self.old_articles.append(a)
        
        # Given a list of articles we have to fill in dictionaries keyword_to_article, article_to_counts, article_to_rank, articles_to_index and articles
        # as attributes of tfidf
        self.tfidf = TFIDF.TFIDF(articles)
        self.old_article_to_id = self.tfidf.article_to_id
        keyword_to_rank = dict()
        for keyword in self.tfidf.keyword_to_article:
            keyword_to_rank[keyword] = 0
            for article in self.tfidf.keyword_to_article[keyword]:
                keyword_to_rank[keyword] += self.tfidf.article_to_rank[article]
                
        
                
        keyword_to_rank_normed = dict()
        key_sum = sum(keyword_to_rank.values())
        for keyword in keyword_to_rank:
            keyword_to_rank_normed[keyword] = keyword_to_rank[keyword] / key_sum
            
        self.thompson.InitializePrior(keyword_to_rank_normed)
               
        sorted_keyword_to_rank = sorted(keyword_to_rank.keys(), key=lambda s: keyword_to_rank[s], reverse=True)
               
        result_keywords = dict()
        
        for keyword in sorted_keyword_to_rank:
            if len(result_keywords)<self.keywords_display/2:
                result_keywords[keyword] = keyword_to_rank[keyword]
        

        
        while len(result_keywords)<self.keywords_display:
            word = self.Sample(keyword_to_rank_normed)
            if word not in result_keywords:
                result_keywords[word] = keyword_to_rank[word]
        
        '''
        maxweight = max(result_keywords.values())
        for keyword in result_keywords:
            result_keywords[keyword] = result_keywords[keyword]/maxweight
            '''
                
        result_keywords = self.Max1(result_keywords)
            
        self.previous_keywords = result_keywords
        
        return result_keywords
        
    
    def Max1(self, dict_weights):
        maxweight = max(dict_weights.values())
        for keyword in dict_weights:
            dict_weights[keyword] = dict_weights[keyword]/maxweight

        return dict_weights    
    
    '''
    # Help function, returns vector representation of a keyword in from tf-idf model
    def GetKeywordArray(self, keyword, tfidf):
        keywordarray = numpy.zeros([1,tfidf.articles_to_index_num])
        for article in tfidf.keyword_representation[keyword]:
            keywordarray[0,tfidf.articles_to_index[article]] = tfidf.keyword_representation[keyword][article]
        return keywordarray
        '''
    
    def MergeArticleSets(self, new_articles):
        
        #print len(new_articles)
        #print len(self.old_articles)
        #print 'Number of articles preserved = '
        #print len(list(set(self.old_articles).intersection(set(new_articles))))
        
        articles = []
        for article in self.old_articles_sorted:
            if len(articles)<(1-DK.RENEW)*len(self.old_articles):
                articles.append(article)
        for article in new_articles:
            if len(articles) < len(self.old_articles):
                if article not in articles:
                        articles.append(article)
        return articles
             

    # Learning function
    # User_feedback is a dictionary with keywords and their weighs about which we got the feedback
    def LinRel(self, new_articles, user_feedback):
        print 'LinRel started'
        
        self.old_relevance = self.new_relevance
        
        new_articles = list(set(new_articles).intersection(set(new_articles)))
        
        # Current dataset of articles is got by merging the old one and new
        articles = self.MergeArticleSets(new_articles)
        
        print 'Calculate kernel'
        
        # Get the information about tfidf model
        self.kernel = Kernel.Kernel(new_articles)
        
        print 'Kernel calculated'
        
        # Store new parameters of previous article dataset
        self.old_articles = articles
        self.old_articles_sorted = sorted(self.old_articles, key=lambda s: s.score, reverse=True)

        self.old_article_to_id = self.kernel.articles
        
        # Matrix representing topic models for documents that have already been presented
        keywords_presented = numpy.array([])
        
        for keyword in user_feedback:
            
            # Add keywords with 0 feedback to the stop list of words that will never appear again
            # If we are giving explicit feedback to a keyword form a stop list, remove it from a stop list
            if user_feedback[keyword]==0:
                self.stop_list.append(keyword)
            else:
                if keyword in self.stop_list:
                    self.stop_list.remove(keyword)
            
            self.keywords.append(keyword)
            self.relevance_scores.append(user_feedback[keyword])
            
        # To prevent 0 feedback on the first iteration  
            
        for keyword in self.keywords:
            keywordarray = self.kernel.Distance(keyword)
            if (numpy.shape(keywords_presented)[0]==0):
                keywords_presented = keywordarray
            else:
                keywords_presented = numpy.vstack((keywords_presented, keywordarray))     
        
        # LinRel computations        
        # Diagonal matrix with mu on the diagonal
        Mu = DK.MU*numpy.eye(len(self.kernel.keywords))
        # selection criteria is a dictionaty keyword - calculated rank
        selectioncriteria = dict();
        # article weights from linear regression by which we can sort them to rank
        article_weighs = numpy.zeros((1,len(self.kernel.articles)));
        # temporary variable which is the same for all keywords
        temp = numpy.linalg.inv(numpy.dot(keywords_presented.T, keywords_presented)+Mu)
        # For all the keywords
        for keyword in self.kernel.keywords:
            # Keyword representation in terms of article tf-idf for every keyword
            xI = self.kernel.Distance(keyword)
            aI = numpy.dot(numpy.dot(xI,temp),keywords_presented.T)
            # Calculate the criteria by which to decide with document to choose next
            # Upper confidence bound on score of the keyword
            selectioncriteria[keyword] = float(numpy.dot(aI, (numpy.array(self.relevance_scores)+DK.E).T)+DK.C/2*numpy.dot(aI, aI.T))
            # Weights from linear regression
#            article_weighs = numpy.dot(temp,numpy.dot(keywords_presented.T,(numpy.array(self.relevance_scores)+DK.E)))
            
        self.new_relevance = selectioncriteria
            
        combined_feedback = dict()
        for keyword in self.keywords:
            if keyword not in combined_feedback:
                if keyword in selectioncriteria:
                    if len(self.old_selection_criteria)==0:
                        combined_feedback[keyword] = selectioncriteria[keyword]
                    else:
                        if keyword in self.old_selection_criteria:
                            combined_feedback[keyword] = selectioncriteria[keyword]-self.old_selection_criteria[keyword]
                    
        self.old_selection_criteria = selectioncriteria
        
        # Next_keywords list contains only keywords that didn't receive 0 feedback
        next_keywords = list()
        sorted_keywords = sorted(selectioncriteria.keys(), key=lambda s: selectioncriteria[s], reverse=True)
        for keyword in sorted_keywords:
            if len(next_keywords) < self.keywords_display:
                if keyword not in self.stop_list:
                        next_keywords.append(keyword)
        
        '''      
        # Sort keywords by selection criteria and return indexes of first #keywords_display
        next_keywords = sorted(selectioncriteria.keys(), key=lambda s: selectioncriteria[s], reverse=True)[0:self.keywords_display]
        '''
        
        '''# Sort articles by their weighs and return indexes of first #article_display
        next_articles = numpy.argsort(article_weighs, axis = 0)[ : :-1][0:self.articles_display]'''
        
        
#        old_indexes_sorted = numpy.argsort(article_weighs, axis = 0)[ : :-1]
        
        # After sorting dictionaries we've got lists
        # Result shout also contain ratings, construct result_keywords, result_articles
        result_keywords = dict()
        for keyword in next_keywords:
            result_keywords[keyword] = selectioncriteria[keyword]
        result_articles = dict()
        
        # if last parameter selectioncriteria - desicion is based on all the keywords vector
        # if it is result_keywords - only on keywords that are shown
        article_weighs = self.Predict_Articles(user_feedback, selectioncriteria)
        
        # Sort articles by their weighs and return indexes of first #article_display
        next_articles = sorted(article_weighs.keys(), key=lambda s: article_weighs[s], reverse=True)[0:self.articles_display]
        
        result_articles = list()
        for article in next_articles:
            result_articles.append(article)
            #  [article] = article_weighs[article]
        
        self.previous_keywords = result_keywords
        
        print numpy.shape(self.kernel.articles)
         
        # ne pomnyu zachem eto    
        # self.old_ids_sorted = []
        # for i in old_indexes_sorted:
        #    self.old_ids_sorted.append(self.kernel.articles[i])
            
        result_keywords = self.Max1(result_keywords)

        return result_keywords, result_articles, combined_feedback, self.old_relevance, self.new_relevance
    
    def Predict_Articles(self, user_feedback, keywords_weights):
        
        keywords_new = dict()
        for keyword in user_feedback:
            if user_feedback[keyword] >= self.previous_keywords.get(keyword,0):
                keywords_new[keyword] = 1
            else:
                keywords_new[keyword] = -1
                
        #return self.ucb.UCB(keywords_new, self.article_to_keywords)
        return self.thompson.Bandit(keywords_new, self.kernel.article_to_keywords, keywords_weights)
>>>>>>> 2dc1347fcdc239041f53568385a0d7cb2262f4f2
