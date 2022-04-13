import seaborn as sns
from time import strftime
import os
import UserdataParser
import numpy as np

parser = UserdataParser
task_lists = parser.extract_tasks_from_allfiles()
parser.calc_task_times_from_files()
pass