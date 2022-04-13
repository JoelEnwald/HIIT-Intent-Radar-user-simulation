TIME_LIMIT = 1800
FOLDER_NAME = "20180412 035716"
BLINE_FOLDER_NAME = "20180412 210838"
c_values_amount = 5
c_values = c(0,1,2,4,8)[1:c_values_amount]
colours1 = rainbow(c_values_amount, start = 3/6, end = 4/6, alpha = 1)
colours2 = "orange"

# Package all the pieces of the file names neatly
file_names <- list(doc = list(rel = list('prec', 'rec'), nov = list('prec', 'rec')),
                   key = list(rel = list('prec', 'rec'), spec = list('prec', 'rec')))

avg_values <- list(doc = list(rel = list(prec = matrix(0, nrow = TIME_LIMIT, ncol = c_values_amount),
                                         rec = matrix(0, nrow = TIME_LIMIT, ncol = c_values_amount)),
                              nov = list(prec = matrix(0, nrow = TIME_LIMIT, ncol = c_values_amount),
                                         rec = matrix(0, nrow = TIME_LIMIT, ncol = c_values_amount))),
                   key = list(rel = list(prec = matrix(0, nrow = TIME_LIMIT, ncol = c_values_amount),
                                         rec = matrix(0, nrow = TIME_LIMIT, ncol = c_values_amount)),
                              spec = list(prec = matrix(0, nrow = TIME_LIMIT, ncol = c_values_amount),
                                          rec = matrix(0, nrow = TIME_LIMIT, ncol = c_values_amount))))
avg_values <- list(doc = list(rel = list(prec = matrix(0, nrow = TIME_LIMIT, ncol = c_values_amount),
                                         rec = matrix(0, nrow = TIME_LIMIT, ncol = c_values_amount)),
                              nov = list(prec = matrix(0, nrow = TIME_LIMIT, ncol = c_values_amount),
                                         rec = matrix(0, nrow = TIME_LIMIT, ncol = c_values_amount))),
                   key = list(rel = list(prec = matrix(0, nrow = TIME_LIMIT, ncol = c_values_amount),
                                         rec = matrix(0, nrow = TIME_LIMIT, ncol = c_values_amount)),
                              spec = list(prec = matrix(0, nrow = TIME_LIMIT, ncol = c_values_amount),
                                          rec = matrix(0, nrow = TIME_LIMIT, ncol = c_values_amount))))

# Compile all the file names from the package one by one.
readValuesFromFolder <- function(folder_name, bline){
  # Change the working directory to the folder given. Might need admin rights?
  setwd(paste("/home/local/enwald/Python/HIIT-Intent-Radar-user-simulation/Intent Radar User Simulator/"
              , "/", folder_name, sep = ""))
  for (data_type in names(file_names)) {
    for (attribute in names(file_names[[data_type]])) {
      for (measure in file_names[[data_type]][[attribute]]) {
        # The file name is a bit different depending on if we are reading from a baseline folder or not.
        if (bline == TRUE) {
          file_name = paste(data_type, attribute, measure, 'avgs', 'bline', 'timed.txt', sep = '_')
        } else {
          file_name = paste(data_type, attribute, measure, 'avgs', 'timed.txt', sep = '_')
        }
        # Read the file
        file_as_table = read.csv2(header = FALSE, file_name, sep = " ", dec = ".")
        # Format the file correctly, make it a vector. Surprisingly the function as.vector
        # keeps it as a list.
        file_as_vector = unlist(file_as_table)
        offset = 4
        file_as_vector = file_as_vector[(offset+1):(TIME_LIMIT*c_values_amount+offset)]
        # Cut the file into a number of pieces corresponding to the different
        # c-values. Store these as separate lists in avg_values.
        for (i in c(0:(c_values_amount-1))) {
          avg_values[[data_type]][[attribute]][[measure]][1:TIME_LIMIT, i+1] =
            file_as_vector[(TIME_LIMIT*i+1):(TIME_LIMIT*(i+1))]
        }
      }
    }
  }
  return(avg_values)
}

# #TASK: precision of obvious
# precision_obvious_baseline <- read.table("./obvious_precision_baseline_20.dat", header=FALSE, sep=";")
# precision_obvious_baseline <-t(precision_obvious_baseline)
# #precision_obvious_baseline
# nrow(precision_obvious_baseline)
# ncol(precision_obvious_baseline)
# #ColBL <- colMeans(precision_obvious_baseline [,])
# ColBL <- precision_obvious_baseline[nrow(precision_obvious_baseline),]
# ColBL
# NROW(ColBL)
# NCOL(ColBL)
# 
# precision_obvious_stash <- read.table("./obvious_precision_stash_20.dat", header=FALSE, sep=";")
# precision_obvious_stash <-t(precision_obvious_stash)
# #precision_obvious_stash
# nrow(precision_obvious_stash)
# ncol(precision_obvious_stash)
# ColIN <- precision_obvious_stash[nrow(precision_obvious_stash),]
# NROW(ColIN)
# NCOL(ColIN)
# ColIN
# 
# mean(ColIN)
# mean(ColBL)
# 
# wilcox.test(ColIN, ColBL, paired=FALSE) 
# 
# #PLOT DATA
# NROW(precision_obvious_baseline)
# NCOL(precision_obvious_baseline)
#   
# 
# precision_relevant<- data.frame(rowMeans(precision_obvious_baseline [,]),rowMeans(precision_obvious_stash [,]))
# nrow(precision_relevant)
# ncol(precision_relevant)
# names(precision_relevant) <- c("baseline","intent")
# #print(precision_relevant)

plot_values_from_folders <- function(folder_name, c_values, bline_folder_name) {
  file_names <- list(doc = list(rel = list('prec', 'rec'), nov = list('prec', 'rec')),
                     key = list(rel = list('prec', 'rec'), spec = list('prec', 'rec')))
  avg_values <- readValuesFromFolder(folder_name, bline = FALSE)
  bline_avg_values <- readValuesFromFolder(bline_folder_name, bline = TRUE)
  for (data_type in names(file_names)) {
    for (attribute in names(file_names[[data_type]])) {
      for (measure in file_names[[data_type]][[attribute]]) {
        bline_values_for_one_c = bline_avg_values[[data_type]][[attribute]][[measure]][1:TIME_LIMIT]
        # Go through the c-values for the keyword model.
        for (i in c(1:c_values_amount)) {
          #PLOT
          par(mar=c(4.2, 3.8, 0.2, 0.2))
          if (measure == "prec") {
            if (attribute == "rel") {
              ylim = c(0.15, 0.5)
            } else {
              ylim = c(0.25, 0.65)
            }
          } else {
            if (data_type == "doc") {
              ylim = c(0, 0.025)
            } else {
              ylim = c(0, 0.1)
            }
          }
          
          # The first plot is done using plot(), the next ones are done using lines().
          # There is probably a better solution to this.
          if (i == 1) {
            plot(avg_values[[data_type]][[attribute]][[measure]][1:TIME_LIMIT, i],
                 type="l", col = colours1[i], 
                 ylim=ylim, axes=F, ann=T, xlab="Time (s)",
                 ylab = paste(data_type, attribute, measure, sep = "_"), cex.lab=0.8, lwd=2)
          } else {
            lines(avg_values[[data_type]][[attribute]][[measure]][1:TIME_LIMIT, i],
                  type = "l", lty = 1, lwd = 2, col = colours1[i])
          }
          # ylim=range(precision_relevant)
          # Make x axis tick marks without labels
          axis(1, lab=F, cex.axis=0.8)
          # Plot x axis with smaller horizontal labels
          axis(1, las=1, cex.axis=0.8)
          # Plot y axis with smaller horizontal labels
          axis(2, las=1, cex.axis=0.8)
          # Create box around plot
          box()
        }
        # Plot the baseline curve, to the same plot as the previous curves for the different
        # c-values in the keyword model. Only do this for documents, since baseline does not
        # have keywords.
        if (data_type == "doc"){
          lines(bline_values_for_one_c, type = 'l', lty = 1, lwd = 2, col = "orange")
        }
        legend_names = c()
        # Add the different c-values to legend names
        for (c in c_values){
          legend_names = c(legend_names, paste("c = ", c, sep = ""))
        }
        # add baseline to legend names
        legend_names = c(legend_names, "baseline")
        # Create a legend in the top-left corner.
        legend("top", legend_names, cex=0.5, col=c(colours1, colours2), 
               lty=1:1, lwd=2, bty="n");
      }
    }
  }
}
  
plot_values_from_folders(FOLDER_NAME, c_values, BLINE_FOLDER_NAME)
setwd("/home/local/enwald/Python/HIIT-Intent-Radar-user-simulation/Intent Radar User Simulator/")

# # Graph suvs with thicker green dotted line
# lines(precision_relevant$baseline, type="l", lty=1, lwd=2, 
#       col=plot_colors[1])
# lines(precision_relevant$intent, type="l", lty=1, lwd=2, 
#       col=plot_colors[2])
# 
# # Create a legend in the top-left corner that is slightly  
# # smaller and has no border
# legend("top", names(precision_relevant), cex=0.8, col=plot_colors, 
#        lty=1:1, lwd=2, bty="n");
# 
# # Turn off device driver (to flush output to PDF)
# #dev.off()
# 
# # Restore default margins
# par(mar=c(5, 4, 4, 2) + 0.1)
# 
# #TASK: recall of obvious
# 
# recall_obvious_baseline <- read.table("./obvious_recall_baseline_20.dat", header=FALSE, sep=";")
# recall_obvious_baseline <-t(recall_obvious_baseline)
# #precision_obvious_baseline
# nrow(recall_obvious_baseline)
# ncol(recall_obvious_baseline)
# ColBL <-  recall_obvious_baseline[nrow(recall_obvious_baseline),]
# ColBL
# 
# recall_obvious_stash <- read.table("./obvious_recall_stash_20.dat", header=FALSE, sep=";")
# recall_obvious_stash <-t(recall_obvious_stash)
# #precision_obvious_baseline
# nrow(recall_obvious_stash)
# ncol(recall_obvious_stash)
# ColIN <-  recall_obvious_stash[nrow(recall_obvious_stash),]
# ColIN
# 
# wilcox.test(ColIN, ColBL, paired=FALSE) 
# 
# #PLOT DATA
# NROW(recall_obvious_baseline)
# NCOL(recall_obvious_baseline)
# mean(ColIN)
# mean(ColBL)
# 
# #mean(rowMeans(recall_obvious_baseline [,]))
# 
# #mean(rowMeans(recall_obvious_stash [,]))
# 
# 
# recall_relevant<- data.frame(rowMeans(recall_obvious_baseline [,]),rowMeans(recall_obvious_stash [,]))
# nrow(recall_relevant)
# ncol(recall_relevant)
# names(recall_relevant) <- c("baseline","intent")
# #print(precision_relevant)
# summary(recall_relevant)
# 
# #PLOT
# plot_colors <- c( "orange", "black")
# par(mar=c(4.2, 3.8, 0.2, 0.2))
# plot(recall_relevant$intent, type="l", col=plot_colors[1], 
#      ylim=c(0, 0.05), axes=F, ann=T, xlab="Time (s)",
#      ylab="Recall obvious", cex.lab=0.8, lwd=2)
# 
# # Make x axis tick marks without labels
# axis(1, lab=F, cex.axis=0.8)
# # Plot x axis with smaller horizontal labels 
# axis(1, las=1, cex.axis=0.8)
# # Plot y axis with smaller horizontal labels 
# axis(2, las=1, cex.axis=0.8)
# # Create box around plot
# box()
# # Graph suvs with thicker green dotted line
# 
# lines(recall_relevant$baseline, type="l", lty=1, lwd=2, 
#       col=plot_colors[1])
# lines(recall_relevant$intent, type="l", lty=1, lwd=2, 
#       col=plot_colors[2])
# # Create a legend in the top-left corner that is slightly  
# # smaller and has no border
# legend("top", names(recall_relevant), cex=0.8, col=plot_colors, 
#        lty=1:1, lwd=2, bty="n");
# 
# # Turn off device driver (to flush output to PDF)
# #dev.off()
# 
# # Restore default margins
# par(mar=c(5, 4, 4, 2) + 0.1)
# 
# #TASK F1 of obvious
# 
# f1_obvious_baseline <- read.table("./obvious_f1_baseline_20.dat", header=FALSE, sep=";")
# f1_obvious_baseline <-t(f1_obvious_baseline)
# #precision_obvious_baseline
# nrow(f1_obvious_baseline)
# ncol(f1_obvious_baseline)
# 
# ColBL <- f1_obvious_baseline[nrow(f1_obvious_baseline),]
# ColBL
# 
# f1_obvious_stash <- read.table("./obvious_f1_stash_20.dat", header=FALSE, sep=";")
# f1_obvious_stash <-t(f1_obvious_stash)
# #precision_obvious_baseline
# nrow(f1_obvious_stash)
# ncol(f1_obvious_stash)
# ColIN <- f1_obvious_stash[nrow(f1_obvious_stash),]
# ColIN
# 
# wilcox.test(ColIN, ColBL, paired=FALSE) 
# 
# #PLOT DATA
# NROW(f1_obvious_baseline)
# NCOL(f1_obvious_baseline)
# 
# 
# f1_relevant<- data.frame(rowMeans(f1_obvious_baseline [,]),rowMeans(f1_obvious_stash [,]))
# nrow(f1_relevant)
# ncol(f1_relevant)
# names(f1_relevant) <- c("baseline","intent")
# #print(precision_relevant)
# 
# #PLOT
# plot_colors <- c( "orange", "black")
# par(mar=c(4.2, 3.8, 0.2, 0.2))
# plot(f1_relevant$intent, type="l", col=plot_colors[1], 
#      ylim=c(0, 0.07), axes=F, ann=T, xlab="Time (s)",
#      ylab="F1 obvious", cex.lab=0.8, lwd=2)
# 
# # Make x axis tick marks without labels
# axis(1, lab=F, cex.axis=0.8)
# # Plot x axis with smaller horizontal labels 
# axis(1, las=1, cex.axis=0.8)
# # Plot y axis with smaller horizontal labels 
# axis(2, las=1, cex.axis=0.8)
# # Create box around plot
# box()
# # Graph suvs with thicker green dotted line
# 
# lines(f1_relevant$baseline, type="l", lty=1, lwd=2, 
#       col=plot_colors[1])
# lines(f1_relevant$intent, type="l", lty=1, lwd=2, 
#       col=plot_colors[2])
# # Create a legend in the top-left corner that is slightly  
# # smaller and has no border
# legend("top", names(f1_relevant), cex=0.8, col=plot_colors, 
#        lty=1:1, lwd=2, bty="n");
# 
# # Turn off device driver (to flush output to PDF)
# #dev.off()
# 
# # Restore default margins
# par(mar=c(5, 4, 4, 2) + 0.1)