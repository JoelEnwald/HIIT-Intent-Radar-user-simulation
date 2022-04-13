#TASK: typed queries amount
typed_queries_baseline <- read.table("./typed_queries_baseline.dat", header=FALSE, sep=";")
typed_queries_baseline<-t(typed_queries_baseline)
#precision_obvious_baseline
nrow(typed_queries_baseline)
ncol(typed_queries_baseline)
#ColBL <- colMeans(precision_obvious_baseline [,])
ColBL <- typed_queries_baseline[nrow(typed_queries_baseline),]
ColBL
NROW(ColBL)
NCOL(ColBL)
typed_queries_stash <- read.table("./typed_queries_stash.dat", header=FALSE, sep=";")
typed_queries_stash<-t(typed_queries_stash)
#precision_obvious_baseline
nrow(typed_queries_stash)
ncol(typed_queries_stash)
#ColBL <- colMeans(precision_obvious_baseline [,])
ColIN <- typed_queries_stash[nrow(typed_queries_stash),]

NROW(ColIN)
NCOL(ColIN)
ColIN

mean(ColIN)
mean(ColBL)


intent_queries_stash <- read.table("./intent_interactions.dat", header=FALSE, sep=";")
intent_queries_stash<-t(intent_queries_stash)
#precision_obvious_baseline
all_queries_stash <-intent_queries_stash + typed_queries_stash 
nrow(intent_queries_stash)
ncol(intent_queries_stash)
#ColBL <- colMeans(precision_obvious_baseline [,])
ColIN2 <- intent_queries_stash[nrow(intent_queries_stash),]

NROW(ColIN2)
NCOL(ColIN2)
ColIN2

ColALLIN <-all_queries_stash[nrow(all_queries_stash),]

mean(ColIN2)
mean(ColIN)
mean(ColALLIN)
mean(ColBL)

wilcox.test(ColIN, ColBL, paired=FALSE) 
wilcox.test(ColIN2, ColBL, paired=FALSE) 
wilcox.test(ColALLIN, ColBL, paired=FALSE) 

#PLOT DATA
NROW(typed_queries_baseline)
NCOL(typed_queries_baseline)
NROW(typed_queries_stash)
NCOL(typed_queries_stash) 

typed_queries<- data.frame(rowMeans(typed_queries_baseline [,]),rowMeans(typed_queries_stash [,]))
nrow(typed_queries)
ncol(typed_queries)
names(typed_queries) <- c("baseline","intent")
#print(precision_relevant)

#PLOT
plot_colors <- c( "orange", "black")
par(mar=c(4.2, 3.8, 0.2, 0.2))
plot(typed_queries$intent, type="l", col=plot_colors[1], 
     ylim=c(0, 25), axes=F, ann=T, xlab="Time (s)",
     ylab="Typed queries", cex.lab=0.8, lwd=2)
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
lines(typed_queries$baseline, type="l", lty=1, lwd=2, 
      col=plot_colors[1])
lines(typed_queries$intent, type="l", lty=1, lwd=2, 
      col=plot_colors[2])

# Create a legend in the top-left corner that is slightly  
# smaller and has no border
legend("top", names(typed_queries), cex=0.8, col=plot_colors, 
       lty=1:1, lwd=2, bty="n");

# Turn off device driver (to flush output to PDF)
#dev.off()

# Restore default margins
par(mar=c(5, 4, 4, 2) + 0.1)

#TASK: query reformulation
typed_queries_baseline <- read.table("./query_repetition_baseline.dat", header=FALSE, sep=";")
typed_queries_baseline<-t(typed_queries_baseline)
#precision_obvious_baseline
nrow(typed_queries_baseline)
ncol(typed_queries_baseline)
#ColBL <- colMeans(precision_obvious_baseline [,])
ColBL <- typed_queries_baseline[nrow(typed_queries_baseline),]
ColBL
NROW(ColBL)
NCOL(ColBL)
typed_queries_stash <- read.table("./query_repetition_stash.dat", header=FALSE, sep=";")
typed_queries_stash<-t(typed_queries_stash)
#precision_obvious_baseline
nrow(typed_queries_stash)
ncol(typed_queries_stash)
#ColBL <- colMeans(precision_obvious_baseline [,])
ColIN <- typed_queries_stash[nrow(typed_queries_stash),]

NROW(ColIN)
NCOL(ColIN)
ColIN

mean(ColIN)
mean(ColBL)

wilcox.test(ColIN, ColBL, paired=FALSE) 

#PLOT DATA
NROW(typed_queries_baseline)
NCOL(typed_queries_baseline)
NROW(typed_queries_stash)
NCOL(typed_queries_stash) 

typed_queries<- data.frame(rowMeans(typed_queries_baseline [,]),rowMeans(typed_queries_stash [,]))
nrow(typed_queries)
ncol(typed_queries)
names(typed_queries) <- c("baseline","intent")
#print(precision_relevant)

#PLOT
plot_colors <- c( "orange", "black")
par(mar=c(4.2, 3.8, 0.2, 0.2))
plot(typed_queries$intent, type="l", col=plot_colors[1], 
     ylim=c(0, 25), axes=F, ann=T, xlab="Time (s)",
     ylab="Typed query reformulation", cex.lab=0.8, lwd=2)
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
lines(typed_queries$baseline, type="l", lty=1, lwd=2, 
      col=plot_colors[1])
lines(typed_queries$intent, type="l", lty=1, lwd=2, 
      col=plot_colors[2])

# Create a legend in the top-left corner that is slightly  
# smaller and has no border
legend("top", names(typed_queries), cex=0.8, col=plot_colors, 
       lty=1:1, lwd=2, bty="n");

# Turn off device driver (to flush output to PDF)
#dev.off()

# Restore default margins
par(mar=c(5, 4, 4, 2) + 0.1)

#ALL INTERACTIONS PLOT

all_interactions<- data.frame(rowMeans(typed_queries_baseline [,]),rowMeans(all_queries_stash [,]))

names(all_interactions) <- c("baseline","intent")
#print(precision_relevant)

#PLOT
plot_colors <- c( "orange", "black")
par(mar=c(4.2, 3.8, 0.2, 0.2))
plot(all_interactions$intent, type="l", col=plot_colors[1], 
     ylim=c(0, 25), axes=F, ann=T, xlab="Time (s)",
     ylab="All interactions", cex.lab=0.8, lwd=2)
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
lines(all_interactions$baseline, type="l", lty=1, lwd=2, 
      col=plot_colors[1])
lines(all_interactions$intent, type="l", lty=1, lwd=2, 
      col=plot_colors[2])

# Create a legend in the top-left corner that is slightly  
# smaller and has no border
legend("top", names(all_interactions), cex=0.8, col=plot_colors, 
       lty=1:1, lwd=2, bty="n");

# Turn off device driver (to flush output to PDF)
#dev.off()

# Restore default margins
par(mar=c(5, 4, 4, 2) + 0.1)


