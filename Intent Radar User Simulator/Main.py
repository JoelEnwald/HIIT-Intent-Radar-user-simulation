
# Write the results to files.
def write_results_to_files(documents_datas, documents_datas_cumul, keywords_datas, keywords_datas_cumul, context):

    doc_rele_prec, doc_nove_prec = calc.calc_document_relevancy_novelty_precision(documents_datas, context)
    write_values_to_a_file(doc_rele_prec, "doc_rele_prec.txt")
    write_values_to_a_file(doc_nove_prec, "doc_nove_prec.txt")

    doc_rele_rec, doc_nove_rec = calc.calc_document_relevancy_novelty_recall(documents_datas_cumul, context)
    write_values_to_a_file(doc_rele_rec, "doc_rele_rec.txt")
    write_values_to_a_file(doc_nove_rec, "doc_nove_rec.txt")

    key_rele_prec, key_speci_prec = calc.calc_keyword_relevancy_specificity_precision(keywords_datas, context)
    write_values_to_a_file(key_rele_prec, "key_rele_prec.txt")
    write_values_to_a_file(key_speci_prec, "key_speci_prec.txt")

    key_rele_rec, key_speci_rec = calc.calc_keyword_relevancy_specificity_recall(keywords_datas_cumul, context)
    write_values_to_a_file(key_rele_rec, "key_rele_rec.txt")
    write_values_to_a_file(key_speci_rec, "key_speci_rec.txt")

def write_timed_results_to_files(timed_scores):
    # Write the result vectors with the slots representing seconds to files.
    write_values_to_a_file(timed_scores['doc']['rele']['prec'], "doc_rele_prec_timed.txt")
    write_values_to_a_file(timed_scores['doc']['nove']['prec'], "doc_nove_prec_timed.txt")

    write_values_to_a_file(timed_scores['doc']['rele']['rec'], "doc_rele_rec_timed.txt")
    write_values_to_a_file(timed_scores['doc']['nove']['rec'], "doc_nove_rec_timed.txt")

    write_values_to_a_file(timed_scores['key']['rele']['prec'], "key_rele_prec_timed.txt")
    write_values_to_a_file(timed_scores['key']['speci']['prec'], "key_speci_prec_timed.txt")

    write_values_to_a_file(timed_scores['key']['rele']['rec'], "key_rele_rec_timed.txt")
    write_values_to_a_file(timed_scores['key']['speci']['rec'], "key_speci_rec_timed.txt")


def convert_results_to_time_format(documents_datas, keywords_datas, documents_datas_cumul, keywords_datas_cumul,
                                   context, times):
    doc_rele_prec_timed = [0]*TIMELIMIT
    doc_nove_prec_timed = [0]*TIMELIMIT
    doc_rele_rec_timed = [0]*TIMELIMIT
    doc_nove_rec_timed = [0]*TIMELIMIT
    key_rele_prec_timed = [0]*TIMELIMIT
    key_speci_prec_timed = [0]*TIMELIMIT
    key_rele_rec_timed = [0]*TIMELIMIT
    key_speci_rec_timed = [0]*TIMELIMIT

    # This is how the variables should be kept!
    timed_scores = {'doc' : {'rele' : {'prec' : [0]*TIMELIMIT, 'rec' : [0]*TIMELIMIT},
                                    'nove' : {'prec' : [0]*TIMELIMIT, 'rec' : [0]*TIMELIMIT}},
                        'key' : {'rele' : {'prec' : [0]*TIMELIMIT, 'rec' : [0]*TIMELIMIT},
                                    'speci' : {'prec' : [0]*TIMELIMIT, 'rec' : [0]*TIMELIMIT}}}

    doc_rele_prec, doc_nove_prec = calc.calc_document_relevancy_novelty_precision(documents_datas, context)
    doc_rele_rec, doc_nove_rec = calc.calc_document_relevancy_novelty_recall(documents_datas_cumul, context)
    key_rele_prec, key_speci_prec = calc.calc_keyword_relevancy_specificity_precision(keywords_datas, context)
    key_rele_rec, key_speci_rec = calc.calc_keyword_relevancy_specificity_recall(keywords_datas_cumul, context)

    # Change the precision and recall scores from being listed to by task to being listed by second of time.
    sum_of_times = 0
    for t in range(0, len(times)):
        i = math.ceil(sum_of_times)
        while i < sum_of_times + times[t] and i < TIMELIMIT:
            doc_rele_prec_timed[i] = doc_rele_prec_timed[i] + doc_rele_prec[t]
            doc_nove_prec_timed[i] = doc_nove_prec_timed[i] + doc_nove_prec[t]
            doc_rele_rec_timed[i] = doc_rele_rec_timed[i] + doc_rele_rec[t]
            doc_nove_rec_timed[i] = doc_nove_rec_timed[i] + doc_nove_rec[t]
            key_rele_prec_timed[i] = key_rele_prec_timed[i] + key_rele_prec[t]
            key_speci_prec_timed[i] = key_speci_prec_timed[i] + key_speci_prec[t]
            key_rele_rec_timed[i] = key_rele_rec_timed[i] + key_rele_rec[t]
            key_speci_rec_timed[i] = key_speci_rec_timed[i] + key_speci_rec[t]
            i = i + 1
        sum_of_times = sum_of_times + times[t]

    timed_scores['doc']['rele']['prec'] = doc_rele_prec_timed
    timed_scores['doc']['rele']['rec'] = doc_rele_rec_timed
    timed_scores['doc']['nove']['prec'] = doc_nove_prec_timed
    timed_scores['doc']['nove']['rec'] = doc_nove_rec_timed
    timed_scores['key']['rele']['prec'] = key_rele_prec_timed
    timed_scores['key']['rele']['rec'] = key_rele_rec_timed
    timed_scores['key']['speci']['prec'] = key_speci_prec_timed
    timed_scores['key']['speci']['rec'] = key_speci_rec_timed

    return timed_scores


def add_results_to_averages(documents_datas, documents_datas_cumul, keywords_datas, keywords_datas_cumul, context):
    global avg_doc_rel_prec
    global avg_doc_nov_prec
    global avg_doc_rel_rec
    global avg_doc_nov_rec
    global avg_key_rel_prec
    global avg_key_spec_prec
    global avg_key_rel_rec
    global avg_key_spec_rec

    doc_rele_prec, doc_nove_prec = calc.calc_document_relevancy_novelty_precision(documents_datas, context)
    avg_doc_rel_prec = [x + y for x, y in zip(avg_doc_rel_prec, doc_rele_prec)]
    avg_doc_nov_prec = [x + y for x, y in zip(avg_doc_nov_prec, doc_nove_prec)]

    doc_rele_rec, doc_nove_rec = calc.calc_document_relevancy_novelty_recall(documents_datas_cumul, context)
    avg_doc_rel_rec = [x + y for x, y in zip(avg_doc_rel_rec, doc_rele_rec)]
    avg_doc_nov_rec = [x + y for x, y in zip(avg_doc_nov_rec, doc_nove_rec)]

    key_rele_prec, key_speci_prec = calc.calc_keyword_relevancy_specificity_precision(keywords_datas, context)
    avg_key_rel_prec = [x + y for x, y in zip(avg_key_rel_prec, key_rele_prec)]
    avg_key_spec_prec = [x + y for x, y in zip(avg_key_spec_prec, key_speci_prec)]

    key_rele_rec, key_speci_rec = calc.calc_keyword_relevancy_specificity_recall(keywords_datas_cumul, context)
    avg_key_rel_rec = [x + y for x, y in zip(avg_key_rel_rec, key_rele_rec)]
    avg_key_spec_rec = [x + y for x, y in zip(avg_key_spec_rec, key_speci_rec)]

def add_timed_results_to_averages(timed_scores):
    global avg_doc_rel_prec_timed
    global avg_doc_nov_prec_timed
    global avg_doc_rel_rec_timed
    global avg_doc_nov_rec_timed
    global avg_key_rel_prec_timed
    global avg_key_spec_prec_timed
    global avg_key_rel_rec_timed
    global avg_key_spec_rec_timed

    avg_doc_rel_prec_timed = [x + y for x, y in zip(avg_doc_rel_prec_timed, timed_scores['doc']['rele']['prec'])]
    avg_doc_nov_prec_timed = [x + y for x, y in zip(avg_doc_nov_prec_timed, timed_scores['doc']['nove']['prec'])]

    avg_doc_rel_rec_timed = [x + y for x, y in zip(avg_doc_rel_rec_timed, timed_scores['doc']['rele']['rec'])]
    avg_doc_nov_rec_timed = [x + y for x, y in zip(avg_doc_nov_rec_timed, timed_scores['doc']['nove']['rec'])]

    avg_key_rel_prec_timed = [x + y for x, y in zip(avg_key_rel_prec_timed, timed_scores['key']['rele']['prec'])]
    avg_key_spec_prec_timed = [x + y for x, y in zip(avg_key_spec_prec_timed, timed_scores['key']['speci']['prec'])]

    avg_key_rel_rec_timed = [x + y for x, y in zip(avg_key_rel_rec_timed, timed_scores['key']['rele']['rec'])]
    avg_key_spec_rec_timed = [x + y for x, y in zip(avg_key_spec_rec_timed, timed_scores['key']['speci']['rec'])]

def write_values_to_a_file(values, filename):
    # If the file does not yet exist, create it and write the parameters used in the simulations on the first line.
    if not os.path.isfile(filename):
        file = open(filename, 'a')
        file.write("STEPS " + str(STEPS) + " SIMULATIONS " + str(RUNS) + "\n")
    else:
        file = open(filename, 'a')
    for value in values:
        file.write(str(value) + " ")
    file.write("\n")
    file.close()

# Just add these to a method. Isn't it enough to reset for example just keywords_data, which is then
# used to reset keywords_datas, keywords_data_cumul and keywords_datas_cumul?
def reset_parameters():
    global clicked_words
    global clicked_weights
    global keyword_datas
    global documents_datas
    global documents_datas_cumul
    global keywords_data
    global keywords_datas
    global keywords_data_cumul
    global keywords_datas_cumul
    global keywords_all
    global linrel
    global cumul_documents
    clicked_words = []
    clicked_weights = []
    keyword_datas = []
    documents_datas = []
    documents_datas_cumul = []
    keywords_data = []
    keywords_datas = []
    keywords_data_cumul = []
    keywords_datas_cumul = []
    keywords_all = []
    linrel = LinRel()
    cumul_documents = []

# Click on a keyword from a given list
def click_keyword(search_word, keywords, scores, clicked_words, clicked_weights, context):
    keyword_to_click = KeywordChooser.choose(keywords, context, [])
    index_of_keyword = keywords.index(keyword_to_click)
    score_of_keyword = scores[index_of_keyword]

    # A safeguard against problem-causing words in the URL. Replace all the reserved characters with
    # spaces. Make into a method??
    reserved_characters = [':', '/', '?', '#', '[', ']', '@', '!', '$', '&', '\'', '(', ')', '*', '+', ',', ';', '=',
                           '%']
    while any(elem in keyword_to_click for elem in reserved_characters):
        for ch in reserved_characters:
            if ch in keyword_to_click:
                keyword_to_click = keyword_to_click.replace(ch, " ")

    clicked_words.append(keyword_to_click)
    clicked_weights.append(score_of_keyword)
    unparsed_data = data_extractor.get_data(search_word, clicked_words, clicked_weights)
    data = data_extractor.parse_data(unparsed_data)
    return data, clicked_words, clicked_weights

# Type a new query for the search engine
def type_query(context):
    if (context == "semantic"):
        search_word_file = semantic_searchwords
    else:
        search_word_file = robotics_searchwords
    # Choose a random search word from the user-inputted search words
    rand_index = random.sample(range(len(search_word_file)), 1)[0]
    search_word = search_word_file[rand_index]
    search_word = search_word.strip()
    # The variables clicked_words and weights are empty
    # because we are starting again with a new query
    unparsed_data = data_extractor.get_data(search_word, [], [])
    data = data_extractor.parse_data(unparsed_data)
    return data, search_word

def combine_lists_remove_duplicates(list1, list2):
    set1 = set(list1)
    set2 = set(list2)
    set3 = set1 | set2
    return set3

def simulate_one_run_with_query_then_keywords(c, context):
    # Choose the search word file to use based on the given context
    if (context == "semantic"):
        search_word_file = semantic_searchwords
    else:
        search_word_file = robotics_searchwords

    # Choose a random search word from the user-inputted search words
    rand_index = random.sample(range(len(search_word_file)), 1)[0]
    search_word = search_word_file[rand_index]
    search_word = search_word.strip()

    # Debug code, set the search word to a default one
    if DEBUG:
        search_word = "robotics"
    print("First search word: " + search_word)

    keywords_datas_cumul = []
    documents_datas_cumul = []

    for i in range(0, STEPS):
        keywords = []
        words_not_allowed_in_url = []
        # Do the search
        # First is a check to see if we get viable data with the given clicked words. If not,
        # the last clicked word in the search is replaced with a new one.
        data = 0
        while 1:
            data = data_extractor.get_data(search_word, clicked_words, clicked_weights)
            if data == 0:
                error_causing_word = clicked_words[len(clicked_words) - 1]
                words_not_allowed_in_url.append(error_causing_word)
                new_word = clicker.choose(keywords[0:10], context, words_not_allowed_in_url)
                clicked_words[len(clicked_words) - 1] = new_word
            else:
                break

        results = data_extractor.parse_data(data)
        # Get and collect the data for the documents using the CSV file.
        # Before this we only have the names of the docs.
        documents_data = docu_key_extractor.get_document_data(results['documents'])
        documents_datas.append(documents_data)

        keywords_data = docu_key_extractor.get_keyword_data(results['keywords'])
        keywords_datas.append(keywords_data)


        # Returns the keyword scores given by LinRel, list of keywords ordered by score, and the documents.
        # Keywords and documents are added to the previously found ones.
        scores, keywords, cumul_documents = linrel.get_keyword_scores(results['keywords'], results['documents'],
                                                                results["resultmatrix"], clicked_words, clicked_weights, c)

        # Get and collect the cumulative data for the documents using the CSV file.
        # Before this we only have the names of the docs.
        # documents_data_cumul contains the data for all the documents found during this run.
        documents_data_cumul = docu_key_extractor.get_document_data(cumul_documents)
        # documents_datas_cumul contains the datas for all the documents found during each step of the run.
        documents_datas_cumul.append(documents_data_cumul)

        # Get and collect the cumulative data for the keywords using the CSV file.
        keywords_data_cumul = docu_key_extractor.get_keyword_data(keywords)
        keywords_datas_cumul.append(keywords_data_cumul)

        keywords = list(keywords)
        scores = list(scores)

        for clicked_word in clicked_words:
            if clicked_word in keywords:
                index = keywords.index(clicked_word)
                keywords.remove(clicked_word)
                del scores[index]

        print("Clicked words and scores:")
        print(clicked_words)
        print(clicked_weights)
        print("Top keywords and scores")
        print(keywords[0:10])
        print(scores[0:10])
        print("")

        # Choosing the word to click
        clicked_word = clicker.choose(keywords[0:10], context, words_not_allowed_in_url)
        word_index = keywords.index(clicked_word)
        clicked_word = clicked_word.strip()
        if clicked_word == None:
            hallo = 5
        # Always click the first suggested word instead, for debugging
        if DEBUG:
            clicked_word = keywords[0]

        # A safeguard against problem-causing words in the URL. Replace all the reserved characters with
        # spaces.
        reserved_characters = [':','/','?','#','[',']','@','!','$','&','\'','(',')','*','+',',',';','=','%']
        while any(elem in clicked_word for elem in reserved_characters):
            for ch in reserved_characters:
                if ch in clicked_word:
                    clicked_word = clicked_word.replace(ch, " ")
        clicked_words.append(clicked_word)
        clicked_weights.append(scores[word_index])
    return documents_datas, keywords_datas, documents_datas_cumul, keywords_datas_cumul

# A run with the user only typing queries. Context is provided beforehand because if it would be random
# documents would be sampled from both contexts and the recall would be unusually high. Also it is not a
# realistic use case where the subject area would change back and forth.
def simulate_one_run_only_queries(context):

    global cumul_documents

    if (context == "semantic"):
        search_word_file = semantic_searchwords
    else:
        search_word_file = robotics_searchwords

    for i in range(0, STEPS):

        # Choose a random search word from the user-inputted search words
        rand_index = random.sample(range(len(search_word_file)), 1)[0]
        search_word = search_word_file[rand_index]
        search_word = search_word.strip()

        # Debug code, set the search word to a default one
        if DEBUG:
            search_word = "robotics"
        print("Search word: " + search_word)

        keywords = []
        # Do the search
        data = data_extractor.get_data(search_word, clicked_words, clicked_weights)

        results = data_extractor.parse_data(data)
        # Get and collect the data for the documents using the CSV file.
        # Before this we only have the names of the docs.
        documents_data = docu_key_extractor.get_document_data(results['documents'])
        documents_datas.append(documents_data)

        keywords_datas.append(keywords_data)

        # Add the new-found documents to the previously found ones.
        # In the method using keywords linrel takes care of this.
        cumul_documents = combine_lists_remove_duplicates(cumul_documents, results['documents'])

        # Get and collect the cumulative data for the documents using the CSV file.
        # Before this we only have the names of the docs.
        documents_data_cumul = docu_key_extractor.get_document_data(cumul_documents)
        documents_datas_cumul.append(documents_data_cumul)

        # Get and collect the cumulative data for the keywords using the CSV file.
        keywords_data_cumul = docu_key_extractor.get_keyword_data(keywords)
        keywords_datas_cumul.append(keywords_data_cumul)

        print("Clicked words and scores:")
        print(clicked_words)
        print(clicked_weights)
        print("")
    return documents_datas, keywords_datas, documents_datas_cumul, keywords_datas_cumul

# Run a simulation with the user switching between writing queries and clicking keywords.
# There is always a roughly 60% chance to click a keyword and a 40% chance to write a query.
def simulate_one_run_with_switching_tasks(c, context):
    percentages = UserdataParser.calc_task_switching_percentages()
    clicked_words = []
    clicked_weights = []

    # First task is always a query
    curr_task = "first"
    data, search_word_used = type_query(context)
    scores, keywords, cumul_documents = linrel.get_keyword_scores(data['keywords'], data['documents'],
                                                                  data['resultmatrix'], clicked_words,
                                                                  clicked_weights, c)

    # We do this part STEPS - 1 times because we already did a typed query in the beginning.
    for i in range(0, STEPS):

        # Pick a random real number from 0 to 1. Used to pick the next task.
        task_choice = random.uniform(0, 1)
        if curr_task == "query" or curr_task == "first":
            if task_choice <= percentages['query_keyword_chance'] and curr_task != "first":
                curr_task = "keyword"
                # Click on a keyword, get the data and the updated clicked_words and clicked_weights
                data, clicked_words, clicked_weights = click_keyword(search_word_used,
                                        keywords[0:10], scores[0:10], clicked_words, clicked_weights,
                                                                     context)
                print("Clicked a keyword, clicked keywords are: " + str(clicked_words))
            else:
                curr_task = "query"
                data, search_word_used = type_query(context)
                print("Typed query with search word: " + search_word_used)
        else:
            if task_choice <= percentages['keyword_keyword_chance']:
                curr_task = "keyword"
                # Click on a keyword, get the data and the updated clicked_words and clicked_weights
                data, clicked_words, clicked_weights = click_keyword(search_word_used,
                                                                     keywords[0:10], scores[0:10], clicked_words,
                                                                     clicked_weights,
                                                                     context)
            else:
                curr_task = "query"
                data, search_word_used = type_query(context)

        scores, keywords, cumul_documents = linrel.get_keyword_scores(data['keywords'], data['documents'],
                                                                          data["resultmatrix"], clicked_words,
                                                                          clicked_weights, c)

        # Get and collect the data for the documents using the CSV file.
        # Before this we only have the names of the docs.
        documents_data = docu_key_extractor.get_document_data(data['documents'])
        documents_datas.append(documents_data)

        keywords_data = docu_key_extractor.get_keyword_data(data['keywords'])
        keywords_datas.append(keywords_data)

        # Get and collect the cumulative data for the documents using the CSV file.
        # Before this we only have the names of the docs.
        # documents_data_cumul contains the data for all the documents found during this run.
        documents_data_cumul = docu_key_extractor.get_document_data(cumul_documents)
        # documents_datas_cumul contains the datas for all the documents found during each step of the run.
        documents_datas_cumul.append(documents_data_cumul)

        # Get and collect the cumulative data for the keywords using the CSV file.
        keywords_data_cumul = docu_key_extractor.get_keyword_data(keywords)
        keywords_datas_cumul.append(keywords_data_cumul)

    return documents_datas, keywords_datas, documents_datas_cumul, keywords_datas_cumul

# Run a simulation where the user starts with a query, then has certain percentage chances to switch from one task
# to another, and each task takes a certain amount of time to do.
def simulate_one_run_time_based_switching_tasks(c, context):
    percentages = UserdataParser.calc_task_switching_percentages()
    clicked_words = []
    clicked_weights = []
    scores = []
    keywords = []
    cumul_documents = []

    # First task is always a query
    curr_task = "first"
    data, search_word_used = type_query(context)
    scores, keywords, cumul_documents = linrel.get_keyword_scores(data['keywords'], data['documents'],
                                                                  data['resultmatrix'], clicked_words,
                                                                  clicked_weights, c)
    task_time_matrix = data_parser.calc_task_times_from_files()

    total_time = 0
    times = []
    while total_time <= TIMELIMIT:

        # Pick a random real number from 0 to 1. Used to pick the next task.
        task_choice = random.uniform(0, 1)
        if curr_task == "query" or curr_task == "first":
            data, search_word_used = type_query(context)
            if task_choice <= percentages['query_keyword_chance'] and curr_task != "first":
                curr_task = "keyword"
                total_time = total_time + task_time_matrix[1, 0]
                times.append(task_time_matrix[1, 0])
                # Click on a keyword, get the data and the updated clicked_words and clicked_weights
                data, clicked_words, clicked_weights = click_keyword(search_word_used,
                                                                     keywords[0:10], scores[0:10], clicked_words,
                                                                     clicked_weights,
                                                                     context)
                print("Clicked a keyword, clicked keywords are: " + str(clicked_words))
            else:
                curr_task = "query"
                total_time = total_time + task_time_matrix[1, 1]
                times.append(task_time_matrix[1, 1])
                data, search_word_used = type_query(context)
                print("Typed query with search word: " + search_word_used)
        else:
            if task_choice <= percentages['keyword_keyword_chance']:
                curr_task = "keyword"
                total_time = total_time + task_time_matrix[0, 0]
                times.append(task_time_matrix[0, 0])
                # Click on a keyword, get the data and the updated clicked_words and clicked_weights
                data, clicked_words, clicked_weights = click_keyword(search_word_used,
                                                                     keywords[0:10], scores[0:10], clicked_words,
                                                                     clicked_weights,
                                                                     context)
            else:
                curr_task = "query"
                total_time = total_time + task_time_matrix[0, 1]
                times.append(task_time_matrix[0, 1])
                data, search_word_used = type_query(context)

        scores, keywords, cumul_documents = linrel.get_keyword_scores(data['keywords'], data['documents'],
                                                                        data["resultmatrix"], clicked_words,
                                                                        clicked_weights, c)

        # Get and collect the data for the documents using the CSV file.
        # Before this we only have the names of the docs.
        documents_data = docu_key_extractor.get_document_data(data['documents'])
        documents_datas.append(documents_data)

        keywords_data = docu_key_extractor.get_keyword_data(data['keywords'])
        keywords_datas.append(keywords_data)

        # Get and collect the cumulative data for the documents using the CSV file.
        # Before this we only have the names of the docs.
        # documents_data_cumul contains the data for all the documents found during this run.
        documents_data_cumul = docu_key_extractor.get_document_data(cumul_documents)
        # documents_datas_cumul contains the datas for all the documents found during each step of the run.
        documents_datas_cumul.append(documents_data_cumul)

        # Get and collect the cumulative data for the keywords using the CSV file.
        keywords_data_cumul = docu_key_extractor.get_keyword_data(keywords)
        keywords_datas_cumul.append(keywords_data_cumul)

    return documents_datas, keywords_datas, documents_datas_cumul, keywords_datas_cumul, times

# Function to do several runs with switching tasks and time taken into account.
def simulate_runs_time_based_switching_tasks(c_values):

    global avg_doc_rel_prec_timed
    global avg_doc_nov_prec_timed
    global avg_doc_rel_rec_timed
    global avg_doc_nov_rec_timed
    global avg_key_rel_prec_timed
    global avg_key_spec_prec_timed
    global avg_key_rel_rec_timed
    global avg_key_spec_rec_timed

    for c in c_values:
        # The run averages are reset before starting a new simulation.
        avg_doc_rel_prec_timed = [0]*TIMELIMIT
        avg_doc_nov_prec_timed = [0]*TIMELIMIT
        avg_doc_rel_rec_timed = [0]*TIMELIMIT
        avg_doc_nov_rec_timed = [0]*TIMELIMIT
        avg_key_rel_prec_timed = [0]*TIMELIMIT
        avg_key_spec_prec_timed = [0]*TIMELIMIT
        avg_key_rel_rec_timed = [0]*TIMELIMIT
        avg_key_spec_rec_timed = [0]*TIMELIMIT
        for i in range(0, RUNS):
            print("c = " + str(c) + ", run number = " + str(i+1))
            reset_parameters()
            # Choose the context for the simulation. Is the user looking for something related to
            # robotics or semantic search?
            context = random.choice(contexts)
            # Do one run, get results
            documents_datas, keywords_datas, documents_datas_cumul, keywords_datas_cumul, times = \
                simulate_one_run_time_based_switching_tasks(c, context)

            # Convert the results to time-based vectors, from task-based ones.
            timed_scores = convert_results_to_time_format(documents_datas, keywords_datas, documents_datas_cumul,
                                                                keywords_datas_cumul, context, times)
            # Change path to the new folder we made for writing the data in files.
            os.chdir(saving_path)
            # Write the newly formatted results to files
            write_timed_results_to_files(timed_scores)
            # Change the directory back to the one the project is in.
            os.chdir(os.path.dirname(os.getcwd()))

            # Add the statistics of the results to the averages over the runs.
            add_timed_results_to_averages(timed_scores)

        avg_doc_rel_prec_timed = [x / RUNS for x in avg_doc_rel_prec_timed]
        avg_doc_nov_prec_timed = [x / RUNS for x in avg_doc_nov_prec_timed]

        avg_doc_rel_rec_timed = [x / RUNS for x in avg_doc_rel_rec_timed]
        avg_doc_nov_rec_timed = [x / RUNS for x in avg_doc_nov_rec_timed]

        avg_key_rel_prec_timed = [x / RUNS for x in avg_key_rel_prec_timed]
        avg_key_spec_prec_timed = [x / RUNS for x in avg_key_spec_prec_timed]

        avg_key_rel_rec_timed = [x / RUNS for x in avg_key_rel_rec_timed]
        avg_key_spec_rec_timed = [x / RUNS for x in avg_key_spec_rec_timed]

        avg_doc_rel_precs_timed.append(avg_doc_rel_prec_timed)
        avg_doc_nov_precs_timed.append(avg_doc_nov_prec_timed)
        avg_doc_rel_recs_timed.append(avg_doc_rel_rec_timed)
        avg_doc_nov_recs_timed.append(avg_doc_nov_rec_timed)
        avg_key_rel_precs_timed.append(avg_key_rel_prec_timed)
        avg_key_spec_precs_timed.append(avg_key_spec_prec_timed)
        avg_key_rel_recs_timed.append(avg_key_rel_rec_timed)
        avg_key_spec_recs_timed.append(avg_key_spec_rec_timed)

    # Change path to the new folder we made for writing the data in files.
    os.chdir(saving_path)
    write_values_to_a_file(avg_doc_rel_precs_timed, "avg_doc_rel_precs_timed.txt")
    write_values_to_a_file(avg_doc_nov_precs_timed, "avg_doc_nov_precs_timed.txt")
    write_values_to_a_file(avg_doc_rel_recs_timed, "avg_doc_rel_recs_timed.txt")
    write_values_to_a_file(avg_doc_nov_recs_timed, "avg_doc_nov_recs_timed.txt")
    write_values_to_a_file(avg_key_rel_precs_timed, "avg_key_rel_precs_timed.txt")
    write_values_to_a_file(avg_key_spec_precs_timed, "avg_key_spec_precs_timed.txt")
    write_values_to_a_file(avg_key_rel_recs_timed, "avg_key_rel_recs_timed.txt")
    write_values_to_a_file(avg_key_spec_recs_timed, "avg_key_spec_recs_timed.txt")

    # Change the directory back to the one the project is in.
    os.chdir(os.path.dirname(os.getcwd()))

    plotter.plot_values(avg_doc_rel_precs_timed, "Time in seconds", "Document relevancy precision", 1)
    plotter.plot_values(avg_doc_nov_precs_timed, "Time in seconds", "Document novelty precision", 1)
    plotter.plot_values(avg_doc_rel_recs_timed, "Time in seconds", "Document relevancy recall", 0.2)
    plotter.plot_values(avg_doc_nov_recs_timed, "Time in seconds", "Document novelty recall", 0.2)
    plotter.plot_values(avg_key_rel_precs_timed, "Time in seconds", "Keyword relevancy precision", 1)
    plotter.plot_values(avg_key_spec_precs_timed, "Time in seconds", "Keyword specificity precision", 1)
    plotter.plot_values(avg_key_rel_recs_timed, "Time in seconds", "Keyword relevancy recall", 0.2)
    plotter.plot_values(avg_key_spec_recs_timed, "Time in seconds", "Keyword specificity recall", 0.2)

# Run a number of simulations for each c value. Store the average values of those runs, and then plot them.
#  The values for different c-values for each attribute are plotted on the same graph.
def simulate_runs_with_query_then_keywords(c_values):
    global avg_doc_rel_prec
    global avg_doc_nov_prec
    global avg_doc_rel_rec
    global avg_doc_nov_rec
    global avg_key_rel_prec
    global avg_key_spec_prec
    global avg_key_rel_rec
    global avg_key_spec_rec

    for c in c_values:
        avg_doc_rel_prec = [0] * STEPS
        avg_doc_nov_prec = [0] * STEPS
        avg_doc_rel_rec = [0] * STEPS
        avg_doc_nov_rec = [0] * STEPS
        avg_key_rel_prec = [0] * STEPS
        avg_key_spec_prec = [0] * STEPS
        avg_key_rel_rec = [0] * STEPS
        avg_key_spec_rec = [0] * STEPS
        for i in range(0, RUNS):
            print("c = " + str(c) + ", run number = " + str(i+1))
            reset_parameters()
            # Choose the context for the simulation. Is the user looking for something related to
            # robotics or semantic search?
            context = random.choice(contexts)
            # Do one run, get results
            documents_datas, keywords_datas, documents_datas_cumul, keywords_datas_cumul = \
                simulate_one_run_with_query_then_keywords(c, context)
            # Change path to the new folder we made for writing the data in files.
            os.chdir(saving_path)
            # Write the results to files.
            write_results_to_files(documents_datas, keywords_datas, documents_datas_cumul, keywords_datas_cumul,
                                   context)
            # Add the statistics of the results to the averages over the runs.
            add_results_to_averages(documents_datas, documents_datas_cumul, keywords_datas, keywords_datas_cumul,
                                    context)

            # Change the directory back to the one the project is in.
            os.chdir(os.path.dirname(os.getcwd()))

        avg_doc_rel_prec = [x / RUNS for x in avg_doc_rel_prec]
        avg_doc_nov_prec = [x / RUNS for x in avg_doc_nov_prec]

        avg_doc_rel_rec = [x / RUNS for x in avg_doc_rel_rec]
        avg_doc_nov_rec = [x / RUNS for x in avg_doc_nov_rec]

        avg_key_rel_prec = [x / RUNS for x in avg_key_rel_prec]
        avg_key_spec_prec = [x / RUNS for x in avg_key_spec_prec]

        avg_key_rel_rec = [x / RUNS for x in avg_key_rel_rec]
        avg_key_spec_rec = [x / RUNS for x in avg_key_spec_rec]

        avg_doc_rel_precs.append(avg_doc_rel_prec)
        avg_doc_nov_precs.append(avg_doc_nov_prec)
        avg_doc_rel_recs.append(avg_doc_rel_rec)
        avg_doc_nov_recs.append(avg_doc_nov_rec)
        avg_key_rel_precs.append(avg_key_rel_prec)
        avg_key_spec_precs.append(avg_key_spec_prec)
        avg_key_rel_recs.append(avg_key_rel_rec)
        avg_key_spec_recs.append(avg_key_spec_rec)

    write_values_to_a_file(avg_doc_rel_precs, "avg_doc_rel_precs.txt")
    write_values_to_a_file(avg_doc_nov_precs, "avg_doc_nov_precs.txt")
    write_values_to_a_file(avg_doc_rel_recs, "avg_doc_rel_recs.txt")
    write_values_to_a_file(avg_doc_nov_recs, "avg_doc_nov_recs.txt")
    write_values_to_a_file(avg_key_rel_precs, "avg_key_rel_precs.txt")
    write_values_to_a_file(avg_key_spec_precs, "avg_key_spec_precs.txt")
    write_values_to_a_file(avg_key_rel_recs, "avg_key_rel_recs.txt")
    write_values_to_a_file(avg_key_spec_recs, "avg_key_spec_recs.txt")

    plotter.plot_values(avg_doc_rel_precs, "Iteration", "Document relevancy precision", 1)
    plotter.plot_values(avg_doc_nov_precs, "Iteration", "Document novelty precision", 1)
    plotter.plot_values(avg_doc_rel_recs, "Iteration", "Document relevancy recall", 0.2)
    plotter.plot_values(avg_doc_nov_recs, "Iteration", "Document novelty recall", 0.2)
    plotter.plot_values(avg_key_rel_precs, "Iteration", "Keyword relevancy precision", 1)
    plotter.plot_values(avg_key_spec_precs, "Iteration", "Keyword specificity precision", 1)
    plotter.plot_values(avg_key_rel_recs, "Iteration", "Keyword relevancy recall", 0.2)
    plotter.plot_values(avg_key_spec_recs, "Iteration", "Keyword specificity recall", 0.2)

def simulate_runs_with_switching_tasks(c_values):
    global avg_doc_rel_prec
    global avg_doc_nov_prec
    global avg_doc_rel_rec
    global avg_doc_nov_rec
    global avg_key_rel_prec
    global avg_key_spec_prec
    global avg_key_rel_rec
    global avg_key_spec_rec

    for c in c_values:
        # The run averages are reset before starting a new simulation.
        avg_doc_rel_prec = [0] * STEPS
        avg_doc_nov_prec = [0] * STEPS
        avg_doc_rel_rec = [0] * STEPS
        avg_doc_nov_rec = [0] * STEPS
        avg_key_rel_prec = [0] * STEPS
        avg_key_spec_prec = [0] * STEPS
        avg_key_rel_rec = [0] * STEPS
        avg_key_spec_rec = [0] * STEPS
        for i in range(0, RUNS):
            print("c = " + str(c) + ", run number = " + str(i+1))
            reset_parameters()
            # Choose the context for the simulation. Is the user looking for something related to
            # robotics or semantic search?
            context = random.choice(contexts)
            # Do one run, get results
            documents_datas, keywords_datas, documents_datas_cumul, keywords_datas_cumul = \
                simulate_one_run_with_switching_tasks(c, context)
            # Change path to the new folder we made for writing the data in files.
            os.chdir(saving_path)
            # Write the calculated numbers from the results to files.
            write_results_to_files(documents_datas, keywords_datas, documents_datas_cumul, keywords_datas_cumul, context)
            # Add the statistics of the results to the averages over the runs.
            add_results_to_averages(documents_datas, documents_datas_cumul, keywords_datas, keywords_datas_cumul,
                                    context)

            # Change the directory back to the one the project is in.
            os.chdir(os.path.dirname(os.getcwd()))

        avg_doc_rel_prec = [x / RUNS for x in avg_doc_rel_prec]
        avg_doc_nov_prec = [x / RUNS for x in avg_doc_nov_prec]

        avg_doc_rel_rec = [x / RUNS for x in avg_doc_rel_rec]
        avg_doc_nov_rec = [x / RUNS for x in avg_doc_nov_rec]

        avg_key_rel_prec = [x / RUNS for x in avg_key_rel_prec]
        avg_key_spec_prec = [x / RUNS for x in avg_key_spec_prec]

        avg_key_rel_rec = [x / RUNS for x in avg_key_rel_rec]
        avg_key_spec_rec = [x / RUNS for x in avg_key_spec_rec]

        avg_doc_rel_precs.append(avg_doc_rel_prec)
        avg_doc_nov_precs.append(avg_doc_nov_prec)
        avg_doc_rel_recs.append(avg_doc_rel_rec)
        avg_doc_nov_recs.append(avg_doc_nov_rec)
        avg_key_rel_precs.append(avg_key_rel_prec)
        avg_key_spec_precs.append(avg_key_spec_prec)
        avg_key_rel_recs.append(avg_key_rel_rec)
        avg_key_spec_recs.append(avg_key_spec_rec)

    write_values_to_a_file(avg_doc_rel_precs, "avg_doc_rel_precs.txt")
    write_values_to_a_file(avg_doc_nov_precs, "avg_doc_nov_precs.txt")
    write_values_to_a_file(avg_doc_rel_recs, "avg_doc_rel_recs.txt")
    write_values_to_a_file(avg_doc_nov_recs, "avg_doc_nov_recs.txt")
    write_values_to_a_file(avg_key_rel_precs, "avg_key_rel_precs.txt")
    write_values_to_a_file(avg_key_spec_precs, "avg_key_spec_precs.txt")
    write_values_to_a_file(avg_key_rel_recs, "avg_key_rel_recs.txt")
    write_values_to_a_file(avg_key_spec_recs, "avg_key_spec_recs.txt")

    plotter.plot_values(avg_doc_rel_precs, "Iteration", "Document relevancy precision", 1)
    plotter.plot_values(avg_doc_nov_precs, "Iteration", "Document novelty precision", 1)
    plotter.plot_values(avg_doc_rel_recs, "Iteration", "Document relevancy recall", 0.2)
    plotter.plot_values(avg_doc_nov_recs, "Iteration", "Document novelty recall", 0.2)
    plotter.plot_values(avg_key_rel_precs, "Iteration", "Keyword relevancy precision", 1)
    plotter.plot_values(avg_key_spec_precs, "Iteration", "Keyword specificity precision", 1)
    plotter.plot_values(avg_key_rel_recs, "Iteration", "Keyword relevancy recall", 0.2)
    plotter.plot_values(avg_key_spec_recs, "Iteration", "Keyword specificity recall", 0.2)

from pprint import pprint
import time
from time import gmtime, strftime
import DataExtractor
import numpy as np
from LinRel import LinRel
import math
import KeywordChooser
import DataPlotter
import csv
import random
import UserdataParser
import DocuKeyDataExtractor
import AttributeCalculator
from time import strftime
import os

data_extractor = DataExtractor
# A class for mimicking a user clicking on the keywords in the list
# NOTE: One simulation for 15 iterations takes about 3 minutes.
clicker = KeywordChooser
linrel = LinRel()
plotter = DataPlotter
docu_key_extractor = DocuKeyDataExtractor
data_parser = UserdataParser
KEYWORD_AMOUNT = 1325
STEPS = 15
RUNS = 500
TIMELIMIT = 1800
DEBUG = 0

clicked_words = []
clicked_weights = []
keyword_datas = []
documents_datas = []
documents_datas_cumul = []
keywords_data = []
keywords_datas = []
keywords_data_cumul = []
keywords_datas_cumul = []
keywords_all = []
semantic_searchwords = []
robotics_searchwords = []
calc = AttributeCalculator
start_time = time.time()
cumul_documents = []

avg_doc_rel_prec = [0] * STEPS
avg_doc_nov_prec = [0] * STEPS
avg_doc_rel_rec = [0] * STEPS
avg_doc_nov_rec = [0] * STEPS
avg_key_rel_prec = [0] * STEPS
avg_key_spec_prec = [0] * STEPS
avg_key_rel_rec = [0] * STEPS
avg_key_spec_rec = [0] * STEPS

avg_doc_rel_precs = []
avg_doc_nov_precs = []
avg_doc_rel_recs = []
avg_doc_nov_recs = []
avg_key_rel_precs = []
avg_key_spec_precs = []
avg_key_rel_recs = []
avg_key_spec_recs = []

avg_doc_rel_prec_timed = [0] * TIMELIMIT
avg_doc_nov_prec_timed = [0] * TIMELIMIT
avg_doc_rel_rec_timed = [0] * TIMELIMIT
avg_doc_nov_rec_timed = [0] * TIMELIMIT
avg_key_rel_prec_timed = [0] * TIMELIMIT
avg_key_spec_prec_timed = [0] * TIMELIMIT
avg_key_rel_rec_timed = [0] * TIMELIMIT
avg_key_spec_rec_timed = [0] * TIMELIMIT

avg_doc_rel_precs_timed = []
avg_doc_nov_precs_timed = []
avg_doc_rel_recs_timed = []
avg_doc_nov_recs_timed = []
avg_key_rel_precs_timed = []
avg_key_spec_precs_timed = []
avg_key_rel_recs_timed = []
avg_key_spec_recs_timed = []

# Extract the search words used by the test users from the relevant files
# and compile them.
if not data_parser.check_user_files_exist():
    data_parser.write_searchwords_to_files()

# Put all the searchwords users have used in the tests into two lists.
semantic_file = open("semanticsearchwords.txt", "r")
for line in semantic_file:
    semantic_searchwords.append(line)
semantic_file.close()
robotics_file = open("roboticssearchwords.txt", "r")
for line in robotics_file:
    robotics_searchwords.append(line)
robotics_file.close()

contexts = ['semantic', 'robotics']

saving_path = strftime("%Y%m%d %H%M%S")
if not os.path.exists(saving_path):
    os.makedirs(saving_path)

# simulate_runs_with_query_then_keywords([0, 1, 2, 4, 8])

# simulate_runs_with_changing_tasks([0, 1, 2, 4, 8])

simulate_runs_time_based_switching_tasks([0, 1, 2, 4, 8])


# Show how long the program took to run
print("--- %s seconds ---" % (time.time() - start_time))
plotter.show_plots()
# simulate_moving_between_tasks(c = 2)