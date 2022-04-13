setwd("/home/local/enwald/Python/HIIT-Intent-Radar-user-simulation/tuukka-analysis")

#TASK: precision of obvious
precision_obvious_baseline <- read.table("./obvious_precision_baseline_20.dat", header=FALSE, sep=";")
precision_obvious_baseline <-t(precision_obvious_baseline)
#precision_obvious_baseline
nrow(precision_obvious_baseline)
ncol(precision_obvious_baseline)
#ColBL <- colMeans(precision_obvious_baseline [,])
ColBL <- precision_obvious_baseline[nrow(precision_obvious_baseline),]
ColBL
NROW(ColBL)
NCOL(ColBL)

precision_obvious_stash <- read.table("./obvious_precision_stash_20.dat", header=FALSE, sep=";")
precision_obvious_stash <-t(precision_obvious_stash)
#precision_obvious_stash
nrow(precision_obvious_stash)
ncol(precision_obvious_stash)
ColIN <- precision_obvious_stash[nrow(precision_obvious_stash),]
NROW(ColIN)
NCOL(ColIN)
ColIN

mean(ColIN)
mean(ColBL)

wilcox.test(ColIN, ColBL, paired=FALSE) 

#PLOT DATA
NROW(precision_obvious_baseline)
NCOL(precision_obvious_baseline)
  

precision_relevant<- data.frame(rowMeans(precision_obvious_baseline [,]),rowMeans(precision_obvious_stash [,]))
nrow(precision_relevant)
ncol(precision_relevant)
names(precision_relevant) <- c("baseline","intent")
#print(precision_relevant)

#PLOT
plot_colors <- c( "orange", "black")
par(mar=c(4.2, 3.8, 0.2, 0.2))
plot(precision_relevant$intent, type="l", col=plot_colors[1], 
     ylim=c(0, 1), axes=F, ann=T, xlab="Time (s)",
     ylab="Precision obvious", cex.lab=0.8, lwd=2)
# ylim=range(precision_relevant)
# Make x axis tick marks without labels
axis(1, lab=F, cex.axis=0.8)
# Plot x axis with smaller horizontal labels 
axis(1, las=1, cex.axis=0.8)
# Plot y axis with smaller horizontal labels 
axis(2, las=1, cex.axis=0.8)
# Create box around plot
box()
# Graph suvs with thicker green dotted line
lines(precision_relevant$baseline, type="l", lty=1, lwd=2, 
      col=plot_colors[1])
lines(precision_relevant$intent, type="l", lty=1, lwd=2, 
      col=plot_colors[2])

# Create a legend in the top-left corner that is slightly  
# smaller and has no border
legend("top", names(precision_relevant), cex=0.8, col=plot_colors, 
       lty=1:1, lwd=2, bty="n");

# Turn off device driver (to flush output to PDF)
#dev.off()

# Restore default margins
par(mar=c(5, 4, 4, 2) + 0.1)

#TASK: recall of obvious

recall_obvious_baseline <- read.table("./obvious_recall_baseline_20.dat", header=FALSE, sep=";")
recall_obvious_baseline <-t(recall_obvious_baseline)
#precision_obvious_baseline
nrow(recall_obvious_baseline)
ncol(recall_obvious_baseline)
ColBL <-  recall_obvious_baseline[nrow(recall_obvious_baseline),]
ColBL

recall_obvious_stash <- read.table("./obvious_recall_stash_20.dat", header=FALSE, sep=";")
recall_obvious_stash <-t(recall_obvious_stash)
#precision_obvious_baseline
nrow(recall_obvious_stash)
ncol(recall_obvious_stash)
ColIN <-  recall_obvious_stash[nrow(recall_obvious_stash),]
ColIN

wilcox.test(ColIN, ColBL, paired=FALSE) 

#PLOT DATA
NROW(recall_obvious_baseline)
NCOL(recall_obvious_baseline)
mean(ColIN)
mean(ColBL)

#mean(rowMeans(recall_obvious_baseline [,]))

#mean(rowMeans(recall_obvious_stash [,]))


recall_relevant<- data.frame(rowMeans(recall_obvious_baseline [,]),rowMeans(recall_obvious_stash [,]))
nrow(recall_relevant)
ncol(recall_relevant)
names(recall_relevant) <- c("baseline","intent")
#print(precision_relevant)
summary(recall_relevant)

#PLOT
plot_colors <- c( "orange", "black")
par(mar=c(4.2, 3.8, 0.2, 0.2))
plot(recall_relevant$intent, type="l", col=plot_colors[1], 
     ylim=c(0, 0.05), axes=F, ann=T, xlab="Time (s)",
     ylab="Recall obvious", cex.lab=0.8, lwd=2)

# Make x axis tick marks without labels
axis(1, lab=F, cex.axis=0.8)
# Plot x axis with smaller horizontal labels 
axis(1, las=1, cex.axis=0.8)
# Plot y axis with smaller horizontal labels 
axis(2, las=1, cex.axis=0.8)
# Create box around plot
box()
# Graph suvs with thicker green dotted line

lines(recall_relevant$baseline, type="l", lty=1, lwd=2, 
      col=plot_colors[1])
lines(recall_relevant$intent, type="l", lty=1, lwd=2, 
      col=plot_colors[2])
# Create a legend in the top-left corner that is slightly  
# smaller and has no border
legend("top", names(recall_relevant), cex=0.8, col=plot_colors, 
       lty=1:1, lwd=2, bty="n");

# Turn off device driver (to flush output to PDF)
#dev.off()

# Restore default margins
par(mar=c(5, 4, 4, 2) + 0.1)

#TASK F1 of obvious

f1_obvious_baseline <- read.table("./obvious_f1_baseline_20.dat", header=FALSE, sep=";")
f1_obvious_baseline <-t(f1_obvious_baseline)
#precision_obvious_baseline
nrow(f1_obvious_baseline)
ncol(f1_obvious_baseline)

ColBL <- f1_obvious_baseline[nrow(f1_obvious_baseline),]
ColBL

f1_obvious_stash <- read.table("./obvious_f1_stash_20.dat", header=FALSE, sep=";")
f1_obvious_stash <-t(f1_obvious_stash)
#precision_obvious_baseline
nrow(f1_obvious_stash)
ncol(f1_obvious_stash)
ColIN <- f1_obvious_stash[nrow(f1_obvious_stash),]
ColIN

wilcox.test(ColIN, ColBL, paired=FALSE) 

#PLOT DATA
NROW(f1_obvious_baseline)
NCOL(f1_obvious_baseline)


f1_relevant<- data.frame(rowMeans(f1_obvious_baseline [,]),rowMeans(f1_obvious_stash [,]))
nrow(f1_relevant)
ncol(f1_relevant)
names(f1_relevant) <- c("baseline","intent")
#print(precision_relevant)

#PLOT
plot_colors <- c( "orange", "black")
par(mar=c(4.2, 3.8, 0.2, 0.2))
plot(f1_relevant$intent, type="l", col=plot_colors[1], 
     ylim=c(0, 0.07), axes=F, ann=T, xlab="Time (s)",
     ylab="F1 obvious", cex.lab=0.8, lwd=2)

# Make x axis tick marks without labels
axis(1, lab=F, cex.axis=0.8)
# Plot x axis with smaller horizontal labels 
axis(1, las=1, cex.axis=0.8)
# Plot y axis with smaller horizontal labels 
axis(2, las=1, cex.axis=0.8)
# Create box around plot
box()
# Graph suvs with thicker green dotted line

lines(f1_relevant$baseline, type="l", lty=1, lwd=2, 
      col=plot_colors[1])
lines(f1_relevant$intent, type="l", lty=1, lwd=2, 
      col=plot_colors[2])
# Create a legend in the top-left corner that is slightly  
# smaller and has no border
legend("top", names(f1_relevant), cex=0.8, col=plot_colors, 
       lty=1:1, lwd=2, bty="n");

# Turn off device driver (to flush output to PDF)
#dev.off()

# Restore default margins
par(mar=c(5, 4, 4, 2) + 0.1)