import numpy as np
import math
import random
import AttributeCalculator

# Method that chooses one of the given keywords, taking into account the current context the user
# is searching info from
def choose(keywords, context):
    keyword = keywords[0]
    i = 0
    while (i < len(keywords)):
        # There is always a 50% chance of picking the current keyword and a 50% of moving to the next.
        # An exponential distribution.
        rand_word_check = random.random()
        if (rand_word_check < 0.5):
            keyword = keywords[i]
            # Checks if the keyword is among the keywords listed as relevant in the "All_keywords.csv" file.
            relevancy = AttributeCalculator.check_if_keyword_relevant(keyword, context)
            if relevancy == "yes":
                i = len(keywords)
        else:
            i += 1
    if keywords == None:
        hello = 5
    elif len(keywords) == 0:
        hello = 6
    return keyword