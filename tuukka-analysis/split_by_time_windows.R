#TASK: split OBVIOUS to first 100s

recall_obvious_baseline <- read.table("./obvious_recall_stash-only-query_20.dat", header=FALSE, sep=";")
recall_obvious_baseline <-t(recall_obvious_baseline)
#precision_obvious_baseline
recall_obvious_baseline<-head(recall_obvious_baseline,100)
nrow(recall_obvious_baseline)
ncol(recall_obvious_baseline)
ColBL <-  recall_obvious_baseline[nrow(recall_obvious_baseline),]
ColBL

recall_obvious_stash <- read.table("./obvious_recall_stash-only-intent_20.dat", header=FALSE, sep=";")
recall_obvious_stash <-t(recall_obvious_stash)
#precision_obvious_baseline

recall_obvious_stash<-head(recall_obvious_stash,100)
nrow(recall_obvious_stash)
ncol(recall_obvious_stash)
ColIN <-  recall_obvious_stash[nrow(recall_obvious_stash),]
ColIN

wilcox.test(ColIN, ColBL, paired=FALSE) 
print("First 100s recall obvious")
mean(ColIN)
mean(ColBL)

#TASK: split to last 1900s 
recall_obvious_baseline <- read.table("./obvious_recall_stash-only-query_20.dat", header=FALSE, sep=";")
recall_obvious_baseline <-t(recall_obvious_baseline)
#precision_obvious_baseline
recall_obvious_baseline<-tail(recall_obvious_baseline,1900)
nrow(recall_obvious_baseline)
ncol(recall_obvious_baseline)
ColBL <-  recall_obvious_baseline[nrow(recall_obvious_baseline),]
ColBL

recall_obvious_stash <- read.table("./obvious_recall_stash-only-intent_20.dat", header=FALSE, sep=";")
recall_obvious_stash <-t(recall_obvious_stash)
#precision_obvious_baseline

recall_obvious_stash<-tail(recall_obvious_stash,1900)
nrow(recall_obvious_stash)
ncol(recall_obvious_stash)
ColIN <-  recall_obvious_stash[nrow(recall_obvious_stash),]
ColIN

wilcox.test(ColIN, ColBL, paired=FALSE) 
print("Last 1900s recall obvious")
mean(ColIN)
mean(ColBL)

#### Precision
#TASK: split to first 100s

recall_obvious_baseline <- read.table("./obvious_precision_stash-only-query_20.dat", header=FALSE, sep=";")
recall_obvious_baseline <-t(recall_obvious_baseline)
#precision_obvious_baseline
recall_obvious_baseline<-head(recall_obvious_baseline,100)
nrow(recall_obvious_baseline)
ncol(recall_obvious_baseline)
ColBL <-  recall_obvious_baseline[nrow(recall_obvious_baseline),]
ColBL

recall_obvious_stash <- read.table("./obvious_precision_stash-only-intent_20.dat", header=FALSE, sep=";")
recall_obvious_stash <-t(recall_obvious_stash)
#precision_obvious_baseline

recall_obvious_stash<-head(recall_obvious_stash,100)
nrow(recall_obvious_stash)
ncol(recall_obvious_stash)
ColIN <-  recall_obvious_stash[nrow(recall_obvious_stash),]
ColIN

wilcox.test(ColIN, ColBL, paired=FALSE) 
print("First 100s precision obvious")
mean(ColIN)
mean(ColBL)

#TASK: split to last 1900s 
recall_obvious_baseline <- read.table("./obvious_precision_stash-only-query_20.dat", header=FALSE, sep=";")
recall_obvious_baseline <-t(recall_obvious_baseline)
#precision_obvious_baseline
recall_obvious_baseline<-tail(recall_obvious_baseline,1900)
nrow(recall_obvious_baseline)
ncol(recall_obvious_baseline)
ColBL <-  recall_obvious_baseline[nrow(recall_obvious_baseline),]
ColBL

recall_obvious_stash <- read.table("./obvious_precision_stash-only-intent_20.dat", header=FALSE, sep=";")
recall_obvious_stash <-t(recall_obvious_stash)
#precision_obvious_baseline

recall_obvious_stash<-tail(recall_obvious_stash,1900)
nrow(recall_obvious_stash)
ncol(recall_obvious_stash)
ColIN <-  recall_obvious_stash[nrow(recall_obvious_stash),]
ColIN

wilcox.test(ColIN, ColBL, paired=FALSE) 
print("Last 1900s precision obvious")
mean(ColIN)
mean(ColBL)


#TASK: split RELEVANT to first 100s

recall_obvious_baseline <- read.table("./relevant_recall_stash-only-query_20.dat", header=FALSE, sep=";")
recall_obvious_baseline <-t(recall_obvious_baseline)
#precision_obvious_baseline
recall_obvious_baseline<-head(recall_obvious_baseline,100)
nrow(recall_obvious_baseline)
ncol(recall_obvious_baseline)
ColBL <-  recall_obvious_baseline[nrow(recall_obvious_baseline),]
ColBL

recall_obvious_stash <- read.table("./relevant_recall_stash-only-intent_20.dat", header=FALSE, sep=";")
recall_obvious_stash <-t(recall_obvious_stash)
#precision_obvious_baseline

recall_obvious_stash<-head(recall_obvious_stash,100)
nrow(recall_obvious_stash)
ncol(recall_obvious_stash)
ColIN <-  recall_obvious_stash[nrow(recall_obvious_stash),]
ColIN

wilcox.test(ColIN, ColBL, paired=FALSE) 
print("First 100s recall relevant")
mean(ColIN)
mean(ColBL)

#TASK: split to last 1900s 
recall_obvious_baseline <- read.table("./relevant_recall_stash-only-query_20.dat", header=FALSE, sep=";")
recall_obvious_baseline <-t(recall_obvious_baseline)
#precision_obvious_baseline
recall_obvious_baseline<-tail(recall_obvious_baseline,1900)
nrow(recall_obvious_baseline)
ncol(recall_obvious_baseline)
ColBL <-  recall_obvious_baseline[nrow(recall_obvious_baseline),]
ColBL

recall_obvious_stash <- read.table("./relevant_recall_stash-only-intent_20.dat", header=FALSE, sep=";")
recall_obvious_stash <-t(recall_obvious_stash)
#precision_obvious_baseline

recall_obvious_stash<-tail(recall_obvious_stash,1900)
nrow(recall_obvious_stash)
ncol(recall_obvious_stash)
ColIN <-  recall_obvious_stash[nrow(recall_obvious_stash),]
ColIN

wilcox.test(ColIN, ColBL, paired=FALSE) 
print("Last 1900s recall relevant")
mean(ColIN)
mean(ColBL)

#### Precision
#TASK: split to first 100s

recall_obvious_baseline <- read.table("./relevant_precision_stash-only-query_20.dat", header=FALSE, sep=";")
recall_obvious_baseline <-t(recall_obvious_baseline)
#precision_obvious_baseline
recall_obvious_baseline<-head(recall_obvious_baseline,100)
nrow(recall_obvious_baseline)
ncol(recall_obvious_baseline)
ColBL <-  recall_obvious_baseline[nrow(recall_obvious_baseline),]
ColBL

recall_obvious_stash <- read.table("./relevant_precision_stash-only-intent_20.dat", header=FALSE, sep=";")
recall_obvious_stash <-t(recall_obvious_stash)
#precision_obvious_baseline

recall_obvious_stash<-head(recall_obvious_stash,100)
nrow(recall_obvious_stash)
ncol(recall_obvious_stash)
ColIN <-  recall_obvious_stash[nrow(recall_obvious_stash),]
ColIN

wilcox.test(ColIN, ColBL, paired=FALSE) 
print("First 100s precision relevant")
mean(ColIN)
mean(ColBL)

#TASK: split to last 1900s 
recall_obvious_baseline <- read.table("./relevant_precision_stash-only-query_20.dat", header=FALSE, sep=";")
recall_obvious_baseline <-t(recall_obvious_baseline)
#precision_obvious_baseline
recall_obvious_baseline<-tail(recall_obvious_baseline,1900)
nrow(recall_obvious_baseline)
ncol(recall_obvious_baseline)
ColBL <-  recall_obvious_baseline[nrow(recall_obvious_baseline),]
ColBL

recall_obvious_stash <- read.table("./relevant_precision_stash-only-intent_20.dat", header=FALSE, sep=";")
recall_obvious_stash <-t(recall_obvious_stash)
#precision_obvious_baseline

recall_obvious_stash<-tail(recall_obvious_stash,1900)
nrow(recall_obvious_stash)
ncol(recall_obvious_stash)
ColIN <-  recall_obvious_stash[nrow(recall_obvious_stash),]
ColIN

wilcox.test(ColIN, ColBL, paired=FALSE) 
print("Last 1900s precision relevant")
mean(ColIN)
mean(ColBL)

