#TASK: precision of relevant
precision_relevant_baseline <- read.table("./relevant_precision_baseline_noncumulative_20.dat", header=FALSE, sep=";")
precision_relevant_baseline <-t(precision_relevant_baseline)
#precision_relevant_baseline
nrow(precision_relevant_baseline)
ncol(precision_relevant_baseline)
#ColBL <- colMeans(precision_relevant_baseline [,])
ColBL <- precision_relevant_baseline[nrow(precision_relevant_baseline),]
ColBL
NROW(ColBL)
NCOL(ColBL)

precision_relevant_stash <- read.table("./relevant_precision_stash_noncumulative_20.dat", header=FALSE, sep=";")
precision_relevant_stash <-t(precision_relevant_stash)
#precision_relevant_stash
nrow(precision_relevant_stash)
ncol(precision_relevant_stash)
ColIN <- precision_relevant_stash[nrow(precision_relevant_stash),]
NROW(ColIN)
NCOL(ColIN)
ColIN

mean(ColIN)
mean(ColBL)

wilcox.test(ColIN, ColBL, paired=FALSE) 

#PLOT DATA
NROW(precision_relevant_baseline)
NCOL(precision_relevant_baseline)
  

precision_relevant<- data.frame(rowMeans(precision_relevant_baseline [,]),rowMeans(precision_relevant_stash [,]))
nrow(precision_relevant)
ncol(precision_relevant)
names(precision_relevant) <- c("baseline","intent")
#print(precision_relevant)

#PLOT
plot_colors <- c( "orange", "black")
plot_colors
plot_colors[1]
plot_colors[2]
par(mar=c(4.2, 3.8, 0.2, 0.2))
plot(precision_relevant$intent, type="l", col=plot_colors[1], 
     ylim=c(0, 1), axes=F, ann=T, xlab="Time (s)",
     ylab="Precision relevant", cex.lab=0.8, lwd=2)
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

#TASK: recall of relevant

recall_relevant_baseline <- read.table("./relevant_recall_baseline_noncumulative_20.dat", header=FALSE, sep=";")
recall_relevant_baseline <-t(recall_relevant_baseline)
#precision_relevant_baseline
nrow(recall_relevant_baseline)
ncol(recall_relevant_baseline)
ColBL <-  recall_relevant_baseline[nrow(recall_relevant_baseline),]
ColBL

recall_relevant_stash <- read.table("./relevant_recall_stash_noncumulative_20.dat", header=FALSE, sep=";")
recall_relevant_stash <-t(recall_relevant_stash)
#precision_relevant_baseline
nrow(recall_relevant_stash)
ncol(recall_relevant_stash)
ColIN <-  recall_relevant_stash[nrow(recall_relevant_stash),]
ColIN

mean(ColIN)
mean(ColBL)

wilcox.test(ColIN, ColBL, paired=FALSE) 

#PLOT DATA
NROW(recall_relevant_baseline)
NCOL(recall_relevant_baseline)
mean(recall_relevant_baseline [nrow(recall_relevant_baseline),])
NROW(recall_relevant_stash)
NCOL(recall_relevant_stash)
mean(recall_relevant_stash [nrow(recall_relevant_stash),])
#mean(rowMeans(recall_relevant_baseline [,]))

#mean(rowMeans(recall_relevant_stash [,]))


recall_relevant<- data.frame("baseline"=rowMeans(recall_relevant_baseline [,]),"intent"=rowMeans(recall_relevant_stash [,]))
nrow(recall_relevant)
ncol(recall_relevant)
#names(recall_relevant) <- c("baseline","intent")
#print(precision_relevant)
summary(recall_relevant)

#PLOT
plot_colors <- c( "orange", "black")
par(mar=c(4.2, 3.8, 0.2, 0.2))
plot(recall_relevant$intent, type="l", col=plot_colors[1], 
     ylim=c(0, 0.025), axes=F, ann=T, xlab="Time (s)",
     ylab="Recall relevant", cex.lab=0.8, lwd=2)

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
legend("top", names(recall_relevant), cex=0.8, col=plot_colors[], 
       lty=1:1, lwd=2, bty="n");
plot_colors[]
names(recall_relevant)
plot_colors[1]
plot_colors[2]
names(recall_relevant)[1]
names(recall_relevant)[2]
# Turn off device driver (to flush output to PDF)
#dev.off()

# Restore default margins
par(mar=c(5, 4, 4, 2) + 0.1)

#TASK F1 of relevant

f1_relevant_baseline <- read.table("./relevant_f1_baseline_noncumulative_20.dat", header=FALSE, sep=";")
f1_relevant_baseline <-t(f1_relevant_baseline)
#precision_relevant_baseline
nrow(f1_relevant_baseline)
ncol(f1_relevant_baseline)

ColBL <- f1_relevant_baseline[nrow(f1_relevant_baseline),]
ColBL

f1_relevant_stash <- read.table("./relevant_f1_stash_noncumulative_20.dat", header=FALSE, sep=";")
f1_relevant_stash <-t(f1_relevant_stash)
#precision_relevant_baseline
nrow(f1_relevant_stash)
ncol(f1_relevant_stash)
ColIN <- f1_relevant_stash[nrow(f1_relevant_stash),]
ColIN

wilcox.test(ColIN, ColBL, paired=FALSE) 

#PLOT DATA
NROW(f1_relevant_baseline)
NCOL(f1_relevant_baseline)


f1_relevant<- data.frame(rowMeans(f1_relevant_baseline [,]),rowMeans(f1_relevant_stash [,]))
nrow(f1_relevant)
ncol(f1_relevant)
names(f1_relevant) <- c("baseline","intent")
#print(precision_relevant)

#PLOT
plot_colors <- c( "orange", "black")
par(mar=c(4.2, 3.8, 0.2, 0.2))
plot(f1_relevant$intent, type="l", col=plot_colors[1], 
     ylim=c(0, 0.025), axes=F, ann=T, xlab="Time (s)",
     ylab="F1 relevant", cex.lab=0.8, lwd=2)

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