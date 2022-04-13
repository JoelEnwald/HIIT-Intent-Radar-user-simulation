import os
import re
import platform
from datetime import datetime
import numpy as np

semantic_users = ['sigir2', 'sigir4', 'sigir6', 'sigir8', 'sigir31',
                      'iuitest11', 'iuitest12', 'iuitest13', 'iuitest14', 'iuitest15']
robotics_users = ['sigir12', 'sigir14', 'sigir16', 'sigir18', 'sigir20',
                      'iuitest1', 'iuitest2', 'iuitest3', 'iuitest4', 'iuitest5']

slash = "/"
# Windows uses different separators in file paths than other operating systems.
if platform.system() == "Windows":
    slash = '\\'

def check_user_files_exist():
    if os.path.isfile("three-systems-logs" + slash + "roboticssearchwords.txt") and os.path.isfile("three-system_logs" + slash + "semanticsearchwords.txt"):
        return True
    return False

def write_word_to_file(word, filename):
    with open(filename, 'w') as target_file:
        target_file.write(word + "\n")

# Get all the user-inputted search words from the relevant files
# This was used to make the files semanticsearchwords.txt and roboticssearchwords.txt
def write_searchwords_to_files():
    global semantic_users
    global robotics_users
    path = "three-systems-logs"
    # Get a list of all the filenames as strings to go through
    filelist = os.listdir(path)
    semantic_words = []
    robotics_words = []
    list_users = [2, 12, 4, 14, 6, 16, 8, 18, 31, 20]
    # Go through only the necessary files, recognising the right ones using regex and the names.
    with open("semanticsearchwords.txt", "w") as semantic_file, open("roboticssearchwords.txt", "w") as robotics_file:
        for user_file in filelist:
            if user_file == "usertable.txt":
                continue
            number_in_filename = int(re.findall(r'\d+', user_file)[0])
            # Checks that the file contains search words from tests using the list system or baseline.
            if ("queries" in user_file) and \
                    (("iui" in user_file) or ("sigir" in user_file and number_in_filename in list_users)):
                # Extract the user-inputted search words from the file.
                searchwords = extract_searchwords(user_file)
                with open(user_file[:-4] + "_as_strings.txt", 'w') as queries_file:
                    # Checks whether file belongs to the semantic or robotics files
                    # and splits the search words in those to two different files.
                    if any(semantic_user_file == user_file.split("_")[0] for semantic_user_file in semantic_users):
                        for word in searchwords:
                            queries_file.write(word + "\n")
                            semantic_file.write(word + "\n")
                    else:
                        for word in searchwords:
                            queries_file.write(word + "\n")
                            robotics_file.write(word + "\n")

    semantic_file.close()
    robotics_file.close()

def extract_searchwords(user_file):
    search_words = []
    file = open("three-systems-logs" + slash + user_file, 'r')
    for line in file:
        if line.startswith("\""):
            search_words = search_words + [line.split("\"")[1]]
    return search_words

# Extract the times it takes to do different tasks (taking into account which task was done
# previously) from the user data ("_allactions" files).
def calc_task_times_from_files():
    keyword_system_filelist = ["sigir2", "sigir4", "sigir6", "sigir8", "sigir31",
                "sigir12", "sigir14", "sigir16", "sigir18", "sigir20"]
    baseline_system_filelist = ["iuitest1", "iuitest2", "iuitest3", "iuitest4", "iuitest5",
                                "iuitest11", "iuitest12", "iuitest13", "iuitest14", "iuitest15"]
    total_task_times_matrix = np.zeros((2, 2))
    total_task_counts_matrix = np.zeros((2, 2))
    total_query_time = 0
    total_query_count = 0
    for i in range(0, len(keyword_system_filelist)):
        keyword_filename = keyword_system_filelist[i]
        baseline_filename = baseline_system_filelist[i]
        keyword_filename = keyword_filename + "_allactions.txt"
        baseline_filename = baseline_filename + "_allactions.txt"
        time_sum_matrix, count_matrix = calc_switching_task_times_from_file(keyword_filename)
        query_times, query_counts = calc_baseline_query_time_from_file(baseline_filename)
        total_task_times_matrix = total_task_times_matrix + time_sum_matrix
        total_task_counts_matrix = total_task_counts_matrix + count_matrix
        total_query_time += query_times
        total_query_count += query_counts
    for i in range(0, np.shape(total_task_times_matrix)[0]):
        for j in range(0, np.shape(total_task_times_matrix)[1]):
            total_task_times_matrix[i, j] = total_task_times_matrix[i, j]/total_task_counts_matrix[i, j]
    total_query_time /= total_query_count

    # total_query_time currently not returned
    return total_task_times_matrix

# Calculate how long making a query took for the users, on average, from the baseline
# system user files.
def calc_baseline_query_time_from_file(filename):
    file = open("three-systems-logs" + slash + filename, 'r')
    file_as_lines = []
    time0 = time1 = None
    # Two queries and times are needed to calculate differences. When we only have the first one,
    # nothing can be done yet.
    first_query = True
    sum_of_times = 0
    query_count = 0
    for line in file:
        file_as_lines.append(line)
        split_line = line.split()
        # Go through the queries, and calculate and save the time differences between them
        if split_line[2] == "query-type":
            time0 = time1
            time1 = datetime.strptime(split_line[0] + " " + split_line[1], "%Y-%m-%d %H:%M:%S")
            # If this is the first task we are checking, do nothing. We can't do comparisons yet.
            if first_query == True:
                first_query = False
            else:
                time_diff = (time1 - time0).total_seconds()
                sum_of_times += time_diff
                query_count += 1
    return sum_of_times, query_count

# Extract the times it takes for a user to do a task (taking into account what task was done
# before that one) from a user file. Also return the counts of how many times a task-pair was done.
def calc_switching_task_times_from_file(filename):
    file = open("three-systems-logs" + slash + filename, 'r')
    file_as_lines = []
    time0 = time1 = None
    task0 = task1 = None
    # Two tasks and times are needed to calculate differences. When we only have the first one,
    # nothing can be done yet.
    first_task = True
    # Create matrices to store the sum of the task switching times and
    # counts on how many times a task pair was counted.
    time_sum_matrix = np.zeros((2, 2))
    count_matrix = np.zeros((2, 2))

    for line in file:
        file_as_lines.append(line)
        split_line = line.split()
        # Go through the relevant tasks, note the time differences between them and mark them down.
        if split_line[2] == "keyword-selection" or split_line[2] == "query-type":
            time0 = time1   # time0 = previous time, time1 = current time
            task0 = task1   # task0 = previous task, task1 = current task
            time1 = datetime.strptime(split_line[0] + " " + split_line[1], "%Y-%m-%d %H:%M:%S")

            # If this is the first task we are checking, do nothing. We can't do comparisons yet.
            if first_task == True:
                first_task = False
            else:
                # Add the times and counts to the arrays in the spots corresponding to what task is done
                # and what was done.
                time_diff = (time1 - time0).total_seconds()
                if split_line[2] == "keyword-selection":
                    task1 = "keyword"
                    if task0 == "keyword":
                        time_sum_matrix[0, 0] = time_sum_matrix[0, 0] + time_diff
                        count_matrix[0, 0] = count_matrix[0, 0] + 1
                    elif task0 == "query":
                        time_sum_matrix[1, 0] = time_sum_matrix[1, 0] + time_diff
                        count_matrix[1, 0] = count_matrix[1, 0] + 1
                if split_line[2] == "query-type":
                    task1 = "query"
                    if task0 == "keyword":
                        time_sum_matrix[0, 1] = time_sum_matrix[0, 1] + time_diff
                        count_matrix[0, 1] = count_matrix[0, 1] + 1
                    elif task0 == "query":
                        time_sum_matrix[1, 1] = time_sum_matrix[1, 1] + time_diff
                        count_matrix[1, 1] = count_matrix[1, 1] + 1
    return time_sum_matrix, count_matrix

# I bet there is a more elegant way of doing this. oh well.
def calc_task_switching_percentages():
    task_lists = extract_tasks_from_allfiles()
    query_query = 0
    query_keyword = 0
    keyword_keyword = 0
    keyword_query = 0
    for task_list in task_lists:
        if len(task_list) < 2:
            continue
        # Let's look at two tasks at a time and count the types of switches the user does
        i = 0; j = 1
        while j < len(task_list):
            if task_list[i] == "query":
                if task_list[j] == "query":
                    query_query += 1
                else:
                    query_keyword += 1
            else:
                if task_list[j] == "query":
                    keyword_query += 1
                else:
                    keyword_keyword += 1
            i += 1; j += 1
    percentages = {"query_query_chance" : query_query/(query_query + query_keyword),
               "query_keyword_chance" : query_keyword/(query_query + query_keyword),
               "keyword_keyword_chance" : keyword_keyword/(keyword_keyword + keyword_query),
               "keyword_query_chance" : keyword_query/(keyword_keyword + keyword_query)}
    return percentages

# Get the lists of tasks the users did from the "_queries" files.
def extract_tasks_from_allfiles():
    tasks = []
    filelist = ["sigir2", "sigir4", "sigir6", "sigir8", "sigir31",
                "sigir12", "sigir14", "sigir16", "sigir18", "sigir20"]
    for i in range(0, len(filelist)):
        filename = filelist[i]
        filename = filename + "_queries.txt"
        filelist[i] = filename
        file_tasks = extract_tasks_from_a_file(filename)
        tasks.append(file_tasks)
    return tasks

# Get a list of the tasks from a single queries file
def extract_tasks_from_a_file(filename):
    file_tasks = []
    try: file = open("three-systems-logs" + slash + filename, 'r')
    except FileNotFoundError:
        print("User data not found.")

    keyword_actions_numbers = []
    for line in file:
        # Check that the line starts with " to skip the first line.
        if (line[0] != "\""):
            continue
        words = line.split()
        keyword_actions_numbers.append(int(words[len(words)-2]))
    # The numbers in the queries-files are one too large because the
    # nKeywordActionsBetweenThisQueryAndTheNext also counts the query apparently.
    for i in range(0, len(keyword_actions_numbers)):
        keyword_actions_numbers[i] = keyword_actions_numbers[i] - 1
    i = 0
    # The tasks always start with a query
    file_tasks.append("query")
    while i < len(keyword_actions_numbers):
        # If there are no more keyword_actions (clicking keywords) between queries, the user made
        # a query next. Unless it is the last task.
        if keyword_actions_numbers[i] <= 0:
            if not i == len(keyword_actions_numbers) - 1:
                file_tasks.append("query")
            i = i + 1
        # Add a keyword_selection to the tasks and reduce their amount by one.
        else:
            keyword_actions_numbers[i] = keyword_actions_numbers[i] - 1
            file_tasks.append("keyword_selection")
    return file_tasks

hallo = calc_task_times_from_files()
hello = 5