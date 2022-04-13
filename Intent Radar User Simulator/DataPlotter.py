import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import csv
import seaborn as sns
import pandas
import AttributeCalculator


keywords_all = []
documents_all = []
RELEVANT_DOC_AMOUNT = 3551
NOVEL_DOC_AMOUNT = 2672
DOC_CSV_SIZE = 5794
portion_of_relevant_docs = RELEVANT_DOC_AMOUNT/DOC_CSV_SIZE
portion_of_novel_docs = NOVEL_DOC_AMOUNT/DOC_CSV_SIZE
RELEVANT_KEY_AMOUNT = 985
SPECIFIC_KEY_AMOUNT = 758
KEY_CSV_SIZE = 1440
portion_of_relevant_keys = RELEVANT_KEY_AMOUNT/ KEY_CSV_SIZE
portion_of_specific_keys = SPECIFIC_KEY_AMOUNT/KEY_CSV_SIZE
global calc
calc = AttributeCalculator
global subplot_counter
subplot_counter = 1

plt.subplot(2, 4, subplot_counter)

# I want to plot all the different plots into one grid of plots. For that I use
# a 2-by-4 subplot table in which I increase the counter for where the next plot
# comes every time I call the method plot_values.
def increment_counter():
    global subplot_counter
    subplot_counter = min(subplot_counter + 1, 8)
    plt.subplot(2, 4, subplot_counter)

def show_plots():
    plt.show()

# Plots two graphs, with a parameter for having the y-axis go from 0 to 1
def plot_values(valuelists, xlabel, ylabel, ylimit):
    palette = sns.color_palette("coolwarm", n_colors=len(valuelists))
    hi = len(valuelists)
    i = 0
    for values in valuelists:
        axes = sns.pointplot(x = list(range(1, len(values) + 1)), y = values, color = palette[i])
        axes.set(xlabel = xlabel, ylabel = ylabel)
        ticks = list(range(0, len(values)+1, 50))
        axes.set_xticks(ticks)
        axes.set_ylim(0, ylimit)
        i = i + 1
    increment_counter()

# Plot the PRECISION of novel and relevant documents.
def plot_document_precision(documents_datas):
    novel_shares = []
    novel_amounts = []
    relevant_shares = []
    relevant_amounts = []
    for data in documents_datas:
        novel_amounts.append(calc.count_novel_documents(data))
        relevant_amounts.append(calc.count_relevant_documents(data))

    for i in range(0, len(documents_datas)):
        relevant_shares.append(relevant_amounts[i] / len(documents_datas[i]))
        novel_shares.append(novel_amounts[i] / relevant_amounts[i])

    plt.subplot(1, 2, 1)
    axes = sns.pointplot(x = list(range(1, len(documents_datas) + 1)), y = novel_shares)
    axes.set(xlabel = "Iteration", ylabel = "Document novelty precision")
    # Plot the line showing the proportion of documents in the CSV file that are novel
    plt.plot([0, len(documents_datas)], [portion_of_novel_docs,
                                         portion_of_novel_docs], linewidth = 2)
    axes.text(0, portion_of_novel_docs + 0.01,
              "Portion of all documents that are novel")
    axes.set_ylim(0, 1)

    plt.subplot(1, 2, 2)
    axes = sns.pointplot(x = list(range(1, len(documents_datas) + 1)), y = relevant_shares)
    axes.set(xlabel = "Iteration", ylabel = "Document relevancy precision")
    # Plot the line showing the proportion of documents in the CSV file that are relevant
    plt.plot([0, len(documents_datas)], [portion_of_relevant_docs,
                                         portion_of_relevant_docs], linewidth=2)
    axes.text(0, portion_of_relevant_docs + 0.01,
              "Portion of all documents that are relevant")
    axes.set_ylim(0, 1)
    plt.show()

# Plot the RECALL of novel and relevant documents.
def plot_document_relevancy_novelty_recall(documents_datas_cumul):
    novel_amounts = []
    relevant_amounts = []
    for data in documents_datas_cumul:
        novel_amounts.append(calc.count_novel_documents(data))
        relevant_amounts.append(calc.count_relevant_documents(data))
    # Create the new lists which contain the relevant and novel amounts as proportions.
    # In other words, recall.
    novel_amounts_prop = [x / NOVEL_DOC_AMOUNT for x in novel_amounts]
    relevant_amounts_prop = [x / RELEVANT_DOC_AMOUNT for x in relevant_amounts]
    plt.subplot(1, 2, 1)
    axes = sns.pointplot(x = list(range(1, len(documents_datas_cumul) + 1)),
                                  y = novel_amounts_prop)
    axes.set(xlabel = "Iteration", ylabel = "Novelty recall")

    plt.subplot(1, 2, 2)
    axes = sns.pointplot(x = list(range(1, len(documents_datas_cumul) + 1)),
                                  y = relevant_amounts_prop)
    axes.set(xlabel = "Iteration", ylabel = "Relevancy recall")
    plt.show()

# Plot the PRECISION of relevant and specific keywords
def plot_keyword_relevancy_specificity_precision(keywords_datas):
    relevant_shares = []
    relevant_amounts = []
    specific_shares = []
    specific_amounts = []
    for data in keywords_datas:
        relevant_amounts.append(calc.count_relevant_keywords(data))
        specific_amounts.append(calc.count_specific_keywords(data))
    for i in range(0, len(keywords_datas)):
        relevant_shares.append(relevant_amounts[i] / len(keywords_datas[i]))
        specific_shares.append(specific_amounts[i] / len(keywords_datas[i]))

    plt.subplot(1, 2, 1)
    axes = sns.pointplot(x = list(range(1, len(keywords_datas) + 1)), y = relevant_shares)
    axes.set(xlabel = "Iteration", ylabel = "Keyword relevancy precision")
    axes.set_ylim(0, 1)
    axes.text(0, portion_of_relevant_keys + 0.01, "Portion of all keywords that are relevant")

    # Line showing the proportion of keywords in the CSV file that are relevant
    plt.plot([0, len(keywords_datas)], [portion_of_relevant_keys,
                                        portion_of_relevant_keys], linewidth = 2)
    plt.subplot(1, 2, 2)
    axes = sns.pointplot(x = list(range(1, len(keywords_datas) + 1)), y = specific_shares)
    axes.set(xlabel = "Iteration", ylabel = "Keyword specificity precision")
    axes.set_ylim(0, 1)
    axes.text(0, portion_of_specific_keys + 0.01, "Portion of all keywords that are specific")

    # Line showing the proportion of keywords in the CSV file that are specific
    plt.plot([0, len(keywords_datas)], [portion_of_specific_keys,
                                        portion_of_specific_keys], linewidth = 2)
    plt.show()

# Plot the RECALL of relevant and specific keywords
def plot_keyword_relevancy_specificity_recall(keywords_datas_cumul):
    relevant_amounts = []
    specific_amounts = []
    for data in keywords_datas_cumul:
        relevant_amounts.append(calc.count_relevant_keywords(data))
        specific_amounts.append(calc.count_specific_keywords(data))
    relevant_amounts_prop = [x / RELEVANT_KEY_AMOUNT for x in relevant_amounts]
    specific_amounts_prop = [x / SPECIFIC_KEY_AMOUNT for x in specific_amounts]
    plt.subplot(1, 2, 1)
    axes = sns.pointplot(x = list(range(1, len(keywords_datas_cumul) + 1)),
                         y = relevant_amounts_prop)
    axes.set(xlabel = "Iteration", ylabel = "Relevancy recall")
    plt.subplot(1, 2, 2)
    axes = sns.pointplot(x = list(range(1, len(keywords_datas_cumul) + 1)),
                         y = specific_amounts_prop)
    plt.show()

