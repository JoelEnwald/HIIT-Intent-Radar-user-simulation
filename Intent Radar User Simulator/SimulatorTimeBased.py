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
from collections import namedtuple

# Write the result vectors with the slots representing seconds to files.
def write_timed_results_to_files(timed_scores, bline):
    if bline == True:
        bline_add = "_bline"
    else:
        bline_add = ""
    for counted_documents_amount_scores in timed_scores:
        hallo = 5
        for data_type in counted_documents_amount_scores:
            for attribute in counted_documents_amount_scores[data_type]:
                for measure in counted_documents_amount_scores[data_type][attribute]:
                    write_values_to_a_file(counted_documents_amount_scores[data_type][attribute][measure],
                                           data_type + "_" + attribute + "_" + measure + bline_add + "_timed.txt")

def calculate_results_in_time_format(documents_datas, keywords_datas, documents_datas_cumul, keywords_datas_cumul,
                                     context, times):
    # Create an empty array to save the scores in with given dimensions.
    scores_array = np.zeros((2, 2, 2, len(COUNTED_DOCUMENT_AMOUNTS), TIMELIMIT))
    scores_dict_list = []

    # Do this for each different amount of counted documents we want to run the simulation on.
    for counted_document_amount in COUNTED_DOCUMENT_AMOUNTS:
        scores_dict = dict(doc=dict(rel=dict(prec=[0] * TIMELIMIT, rec=[0] * TIMELIMIT),
                                    nov=dict(prec=[0] * TIMELIMIT, rec=[0] * TIMELIMIT)),
                           key=dict(rel=dict(prec=[0] * TIMELIMIT, rec=[0] * TIMELIMIT),
                                    spec=dict(prec=[0] * TIMELIMIT, rec=[0] * TIMELIMIT)))
        doc_rele_prec, doc_nove_prec =\
                    calc.calc_document_relevancy_novelty_precision(documents_datas, context, counted_document_amount)
        doc_rele_rec, doc_nove_rec =\
                    calc.calc_document_relevancy_novelty_recall(documents_datas_cumul, context, counted_document_amount)
        key_rele_prec, key_speci_prec =\
                    calc.calc_keyword_relevancy_specificity_precision(keywords_datas, context)
        key_rele_rec, key_speci_rec =\
                    calc.calc_keyword_relevancy_specificity_recall(keywords_datas_cumul, context)

        # Change the precision and recall scores from being listed by task to being listed by second of time.
        sum_of_times = 0
        for t in range(0, len(times)):
            i = math.ceil(sum_of_times)
            while i < sum_of_times + times[t] and i < TIMELIMIT:

                scores_dict['doc']['rel']['prec'][i] += doc_rele_prec[t]
                scores_dict['doc']['nov']['prec'][i] += doc_nove_prec[t]
                scores_dict['doc']['rel']['rec'][i] += doc_rele_rec[t]
                scores_dict['doc']['nov']['rec'][i] += doc_nove_rec[t]

                scores_dict['key']['rel']['prec'][i] += key_rele_prec[t]
                scores_dict['key']['spec']['prec'][i] += key_speci_prec[t]
                scores_dict['key']['rel']['rec'][i] += key_rele_rec[t]
                scores_dict['key']['spec']['rec'][i] += key_speci_rec[t]

                i = i + 1
            sum_of_times = sum_of_times + times[t]

        keys1 = ['doc', 'key']
        keys2a = ['nov', 'rel']
        keys2b = ['rel', 'spec']
        keys3 = ['prec', 'rec']


        for i in range(0, 2):
            for j in range(0, 2):
                for k in range(0, 2):
                    for c in range(0, len(C_VALUES)):
                        for m in range(0, TIMELIMIT):
                            if i == 0:
                                keys2 = keys2a
                            else:
                                keys2 = keys2b
                            # l is current index
                            l = COUNTED_DOCUMENT_AMOUNTS.index(counted_document_amount)
                            try: scores_array[i][j][k][l][m] = scores_dict[keys1[i]][keys2[j]][keys3[k]][m]
                            except IndexError:
                                hallo = 5

    # scores_dict_list.append(scores_dict)

    return scores_array

def add_timed_results_to_averages(timed_scores_array, timed_avgs_array):

    for i in [0, 2]:
        for j in [0, 2]:
            for k in [0, 2]:
                for l in [0, len(COUNTED_DOCUMENT_AMOUNTS)]:
                    timed_avgs_array[i][j][k][l] = [x + y for x,y in zip(timed_avgs_array[i][j][k][l],
                                                                        timed_scores_array[i][j][k][l])]

    # Go through all the objects (document, key), attributes and measures in a loop,
    # and add each combination to the right spot in timed_avgs_dict.
    # for documents_counted in timed_avgs_dict:
    #     for data_type in timed_avgs_dict[documents_counted]:
    #         for attribute in timed_avgs_dict[documents_counted][data_type]:
    #             for measure in timed_avgs_dict[documents_counted][data_type][attribute]:
    #                 try: timed_avgs_dict[documents_counted][data_type][attribute][measure] = [x + y for x,y in
    #                                             zip(timed_avgs_dict[documents_counted][data_type][attribute][measure],
    #                                                 timed_scores[documents_counted][data_type][attribute][measure])]
    #                 except TypeError:
    #                     hallo = 5
    return timed_avgs_array

# Write the given values to a file, that is located outside the git repository. This is to avoid large data files
# being added to the repository.
def write_values_to_a_file(values, filename):
    # Get the current working directory upon arriving in this function
    original_dir = os.getcwd()
    timestamp_folder = strftime("%Y%m%d %H%M%S")
    data_folder_name = "Intent Radar simulation data files"
    # If the directory for saving the data folders does not exist, create it.
    if not os.path.exists(os.path.join(GIT_PROJECT_DIR, data_folder_name)):
        hallo = os.path.join(GIT_PROJECT_DIR, data_folder_name)
        os.makedirs(os.path.join(GIT_PROJECT_DIR, data_folder_name))
    os.chdir(os.path.join(GIT_PROJECT_DIR, data_folder_name))
    # If the folder for saving the data for this run does not exist, create it.
    if not os.path.exists(timestamp_folder):
        os.makedirs(timestamp_folder)
    os.chdir(os.path.join(GIT_PROJECT_DIR, data_folder_name, timestamp_folder))
    # If the file does not yet exist, create it and write the parameters used in the simulations on the first line.
    if not os.path.isfile(filename):
        file = open(filename, 'a')
        file.write("TIME_LIMIT " + str(TIMELIMIT) + " SIMULATIONS " + str(RUNS) + " ")
    else:
        file = open(filename, 'a')
    for value in values:
        file.write(str(value) + " ")
    file.close()
    # Change the directory back to the original one
    os.chdir(original_dir)

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
    keyword_to_click = KeywordChooser.choose(keywords, context)
    index_of_keyword = keywords.index(keyword_to_click)
    score_of_keyword = scores[index_of_keyword]

    # A safeguard against problem-causing characters in the URL. Replace all the reserved characters with
    # spaces. Make into a method??
    reserved_characters = [':','/','?','#','[',']','@','!','$','&','\'','(',')','*','+',',',';','=','%']
    while any(elem in keyword_to_click for elem in reserved_characters):
        for ch in reserved_characters:
            if ch in keyword_to_click:
                keyword_to_click = keyword_to_click.replace(ch, " ")

    clicked_words.append(keyword_to_click)
    clicked_weights.append(score_of_keyword)
    unparsed_data = data_extractor.get_data(search_word, clicked_words, clicked_weights)
    data = data_extractor.parse_data(unparsed_data)
    return data, clicked_words, clicked_weights

# Type a new query for the search engine.
# If global_queries is set to True, then all queries sample search words from all the search words the users
# have used. If it is false, then for each run a random user is picked and the search words are sampled from the
# search words that user has used.
def type_query(context, search_word_file_name):

    # If any search words can be used, just use the ready lists
    if (GLOBAL_SEARCHWORDS == True):
        if (context == "semantic"):
            search_word_list = semantic_searchwords
        else:
            search_word_list = robotics_searchwords
    else:
        # Is the type of simulation a mix of keywords and queries, or is it just queries (baseline)?
        with open(search_word_file_name, "r") as search_word_file:
            search_word_list = []
            for word in search_word_file:
                search_word_list.append(word)

        search_word_file.close()
    # Choose a random search word from the user-inputted search words
    rand_index = random.sample(range(len(search_word_list)), 1)[0]
    search_word = search_word_list[rand_index]
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

# A run with the user only typing queries. Context is provided beforehand because if it would be random
# documents would be sampled from both contexts and the recall would be unusually high. Also it is not a
# realistic use case where the subject area would change back and forth.
def simulate_one_run_only_queries(c, context):
    clicked_words = []
    clicked_weights = []

    # Choose a random file from which the search words can be sampled from.
    if (context == "semantic"):
        user_query_files = ["iuitest11", "iuitest12", "iuitest13", "iuitest14", "iuitest15"]
    else:
        user_query_files = ["iuitest1", "iuitest2", "iuitest3", "iuitest4", "iuitest5"]
    user_query_files = [s + "_queries_as_strings.txt" for s in user_query_files]
    # Choose a random user query file
    rand_file_index = random.sample(range(len(user_query_files)), 1)[0]
    search_word_file = user_query_files[rand_file_index]

    # First task is a query
    curr_task = "first"
    data, search_word_used = type_query(context, search_word_file)
    scores, keywords, cumul_documents = linrel.get_keyword_scores(data['keywords'], data['documents'],
                                                                  data['resultmatrix'], clicked_words,
                                                                  clicked_weights, c)

    total_time = 0
    # The vector into which we will put the amount of seconds used for each individual action taken.
    times = []

    while total_time <= TIMELIMIT:

        curr_task = "query"
        total_time = total_time + QUERY_TIME
        times.append(QUERY_TIME)

        data, search_word_used = type_query(context, search_word_file)
        print("Typed query with search word: " + search_word_used)

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


def simulate_runs_only_queries(c_values):

    global abbreviation_map

    timed_avgs_dict = None

    c_values_timed_avgs_array = np.zeros((len(C_VALUES), 2, 2, 2, len(COUNTED_DOCUMENT_AMOUNTS), TIMELIMIT))

    timed_avgs_dict_compiled = dict(doc = dict(rel = dict(prec = [], rec = []),
                                                nov = dict(prec = [], rec = [])),
                                    key = dict(rel = dict(prec = [], rec = []),
                                                spec = dict(prec = [], rec = [])))

    for c in c_values:
        # The run averages are reset before starting a new simulation.
        timed_avgs_array = np.zeros(2, 2, 2, len(COUNTED_DOCUMENT_AMOUNTS), TIMELIMIT)
        timed_avgs_dict = dict(doc=dict(rel=dict(prec=[0] * TIMELIMIT, rec=[0] * TIMELIMIT),
                                        nov=dict(prec=[0] * TIMELIMIT, rec=[0] * TIMELIMIT)),
                               key=dict(rel=dict(prec=[0] * TIMELIMIT, rec=[0] * TIMELIMIT),
                                        spec=dict(prec=[0] * TIMELIMIT, rec=[0] * TIMELIMIT)))
        # The list of dictionaries for saving the results for different amounts of documents counted.
        timed_avgs_dict_list = []

        for i in range(0, RUNS):
            print("c = " + str(c) + ", run number = " + str(i + 1))
            reset_parameters()
            # Choose the context for the simulation. Is the user looking for something related to
            # robotics or semantic search?
            context = random.choice(contexts)
            # Do one run, get results
            documents_datas, keywords_datas, documents_datas_cumul, keywords_datas_cumul, times = \
                simulate_one_run_only_queries(c, context)

            # Convert the results to time-based vectors. Previously the results were listed for each action,
            # instead of each second.
            timed_scores = calculate_results_in_time_format(documents_datas, keywords_datas, documents_datas_cumul,
                                                            keywords_datas_cumul, context, times)
            # Change path to the new folder we made for writing the data in files.
            os.chdir(saving_path)

            # Add the statistics of the results to the averages over the runs.
            for documents_counted in timed_scores:
                timed_avgs_array = add_timed_results_to_averages(timed_scores, timed_avgs_array)

            # Write the newly formatted results to files
            write_timed_results_to_files(timed_scores, bline = True)
            # Change the directory back to the one the project is in.
            os.chdir(os.path.dirname(os.getcwd()))

        for data_type in timed_avgs_dict:
            for attribute in timed_avgs_dict[data_type]:
                for measure in timed_avgs_dict[data_type][attribute]:
                    # Divide the sums of the scores by the number of runs to get the averages.
                    timed_avgs_dict[data_type][attribute][measure] = \
                        [x / RUNS for x in timed_avgs_dict[data_type][attribute][measure]]
                    # Add the averages to the end of the list of compiled averages for all the c values.
                    timed_avgs_dict_compiled[data_type][attribute][measure].append(
                        timed_avgs_dict[data_type][attribute][measure])

    # Change path to the new folder we made for writing the data in files.
    os.chdir(saving_path)
    for data_type in timed_avgs_dict:
        for attribute in timed_avgs_dict[data_type]:
            for measure in timed_avgs_dict[data_type][attribute]:
                for i in range(0, len(c_values)):
                    write_values_to_a_file(timed_avgs_dict_compiled[data_type][attribute][measure][i],
                                           data_type + "_" + attribute + "_" + measure + "_avgs_bline" + "_timed.txt")
                if PLOTTING == True:
                    # Plot the averages, retrieve the full names for the abbreviations such as rec, nov etc.
                    # Show the full words on the x-axis of the plot.
                    x_axis_label = abbreviation_map[data_type]+" "+abbreviation_map[attribute] +" "+abbreviation_map[measure]
                    # The default scale for the y-axis should be different for precision and recall measures
                    if measure == "prec":
                        y_axis_scale = 1
                    else:
                        y_axis_scale = 0.2
                    print("Only plotting left")
                    plotter.plot_values(timed_avgs_dict_compiled[data_type][attribute][measure],
                                       "Time in seconds", x_axis_label, y_axis_scale)

    # Change the directory back to the one the project is in.
    os.chdir(os.path.dirname(os.getcwd()))

# Run a simulation where the user starts with a query, then has certain percentage chances to switch from one task
# to another, and each task takes a certain amount of time to do.
def simulate_one_run_time_based_switching_tasks(c, context):
    hallo = os.getcwd()
    percentages = UserdataParser.calc_task_switching_percentages()
    clicked_words = []
    clicked_weights = []

    # Choose a random file from which the search words can be sampled from.
    if (context == "semantic"):
        user_query_files = ["sigir2", "sigir4", "sigir6", "sigir8", "sigir31"]
    else:
        user_query_files = ["sigir12", "sigir14", "sigir16", "sigir18", "sigir20"]
    user_query_files = [s + "_queries_as_strings.txt" for s in user_query_files]
    # Choose a random user query file
    rand_file_index = random.sample(range(len(user_query_files)), 1)[0]
    search_word_file = user_query_files[rand_file_index]

    # First task is always a query
    curr_task = "first"
    data, search_word_used = type_query(context, search_word_file)
    scores, keywords, cumul_documents = linrel.get_keyword_scores(data['keywords'], data['documents'],
                                                                  data['resultmatrix'], clicked_words,
                                                                  clicked_weights, c)
    task_time_matrix = data_parser.calc_task_times_from_files()

    total_time = 0
    # The vector into which we will put the amount of seconds used for each individual action taken.
    times = []

    while total_time <= TIMELIMIT:

        # Pick a random real number from 0 to 1. Used to pick the next task.
        task_choice = random.uniform(0, 1)
        if curr_task == "query" or curr_task == "first":
            data, search_word_used = type_query(context, search_word_file)
            if task_choice <= percentages['query_keyword_chance'] and curr_task != "first":
                curr_task = "keyword"
                total_time = total_time + task_time_matrix[1, 0]
                times.append(task_time_matrix[1, 0])
                data, clicked_words, clicked_weights = click_keyword(search_word_used,
                                                                     keywords[0:SHOWN_KEYWORDS], scores[0:SHOWN_KEYWORDS],
                                                                     clicked_words, clicked_weights, context)
                print("Clicked a keyword, clicked keywords are: " + str(clicked_words))
            else:
                curr_task = "query"
                total_time = total_time + task_time_matrix[1, 1]
                times.append(task_time_matrix[1, 1])
                data, search_word_used = type_query(context, search_word_file)
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
                data, search_word_used = type_query(context, search_word_file)

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

    timed_avgs_dict = None

    timed_avgs_dict_compiled = dict(doc = dict(rel = dict(prec = [], rec = []),
                                nov = dict(prec = [], rec = [])),
                    key = dict(rel = dict(prec = [], rec = []),
                                spec = dict(prec = [], rec = [])))

    for c in c_values:
        # The run averages are reset before starting a new simulation.
        timed_avgs_array = np.zeros((2, 2, 2, 3, 1800))
        timed_avgs = dict(doc=dict(rel=dict(prec=[0] * TIMELIMIT, rec=[0] * TIMELIMIT),
                                        nov=dict(prec=[0] * TIMELIMIT, rec=[0] * TIMELIMIT)),
                               key=dict(rel=dict(prec=[0] * TIMELIMIT, rec=[0] * TIMELIMIT),
                                        spec=dict(prec=[0] * TIMELIMIT, rec=[0] * TIMELIMIT)))
        timed_avgs_dict = []

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
            timed_scores = calculate_results_in_time_format(documents_datas, keywords_datas, documents_datas_cumul,
                                                            keywords_datas_cumul, context, times)
            # Change path to the new folder we made for writing the data in files.
            os.chdir(saving_path)

            # Add the statistics of the results to the averages over the runs.
            timed_avgs_array = add_timed_results_to_averages(timed_scores, timed_avgs_dict)

            # Write the newly formatted results to files
            write_timed_results_to_files(timed_scores, bline = False)
            # Change the directory back to the one the project is in.
            os.chdir(os.path.dirname(os.getcwd()))

        for data_type in timed_avgs_dict:
            for attribute in timed_avgs_dict[data_type]:
                for measure in timed_avgs_dict[data_type][attribute]:
                    # Divide the sums of the scores by the number of runs to get the averages.
                    timed_avgs_dict[data_type][attribute][measure] =\
                        [x / RUNS for x in timed_avgs_dict[data_type][attribute][measure]]
                    # Add the averages to the end of the list of compiled averages for all the c values.
                    timed_avgs_dict_compiled[data_type][attribute][measure].append(
                        timed_avgs_dict[data_type][attribute][measure])

    # Change path to the new folder we made for writing the data in files.
    os.chdir(saving_path)
    for data_type in timed_avgs_dict:
        for attribute in timed_avgs_dict[data_type]:
            for measure in timed_avgs_dict[data_type][attribute]:
                for i in range(0, len(C_VALUES)):
                    write_values_to_a_file(timed_avgs_dict_compiled[data_type][attribute][measure][i],
                                           data_type + "_" + attribute + "_" + measure + "_avgs_timed.txt")
                # Plot the averages, retrieve the full names for the abbreviations such as rec, nov etc.
                # Show the full words on the x-axis of the plot.
                # x_axis_label = abbreviation_map[data_type]+" "+abbreviation_map[attribute] +" "+abbreviation_map[measure]
                # The default scale for the y-axis should be different for precision and recall measures
                # if measure == "prec":
                #     y_axis_scale = 1
                # else:
                #     y_axis_scale = 0.2
                # print("Only plotting left")
                # plotter.plot_values(timed_avgs_dict_compiled[data_type][attribute][measure],
                #                    "Time in seconds", x_axis_label, y_axis_scale)

    # Change the directory back to the one the project is in.
    os.chdir(os.path.dirname(os.getcwd()))

data_extractor = DataExtractor
# A class for mimicking a user clicking on the keywords in the list
# NOTE: 3 runs with a time limit of 300 and 5 different c values takes about 2 minutes.
clicker = KeywordChooser
linrel = LinRel()
plotter = DataPlotter
docu_key_extractor = DocuKeyDataExtractor
data_parser = UserdataParser
KEYWORD_AMOUNT = 1325
RUNS = 3
TIMELIMIT = 300
SHOWN_KEYWORDS = 10
DEBUG = 0
C_VALUES = [0, 1, 2, 4, 8]
PLOTTING = True
QUERY_TIME = 174.22857 # Calculated from user data
GLOBAL_SEARCHWORDS = True
COUNTED_DOCUMENT_AMOUNTS = [1, 10, 20]
GIT_PROJECT_DIR = os.path.dirname(os.path.dirname(os.getcwd()))

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

abbreviation_map = dict(doc = "document", key = "keyword", rel = "relevancy", nov = "novelty",
                                                    spec = "specificity", rec = "recall", prec = "precision")

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



# simulate runs where the user switches between keywords and queries
simulate_runs_time_based_switching_tasks(C_VALUES)
# simulate runs with only queries
simulate_runs_only_queries([2])


# Show how long the program took to run
print("--- %s seconds ---" % (time.time() - start_time))
if PLOTTING == True:
    plotter.show_plots()
