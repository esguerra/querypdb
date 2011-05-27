# If you want to run this from the command line as a script
# Do
# R CMD BATCH filename.R >& filename.log &

# We are including some statistics of RNA Structures
# emphasizing the preponderance of ribosomal
# structure information.

#Read data
numbases <- read.table("yearlydata.dat")

#Get number of rows
m <- dim(numbases)[1]
n <- m/10

#Use only data greater than or equal to year 2000
x <- numbases[,2][numbases[,4] >= 2000]

ribobases <- sum(numbases[,2][numbases[,2] >= 1000])
totbases <- sum(numbases[,2])
per_ribo <- (ribobases/totbases)*100


#Send Histogram output to postscript image
postscript("Histogram.ps")

a <- hist(x,breaks=n,col="light blue",border="black",
     xlim=range(0:3050),ylim=range(0:140),xlab="Number of RNA Bases",
     axes=FALSE, main="Number of bases in RNA's in PDB")
axis(1, xaxp=c(0,3100,31), pos=0.0)
axis(2, yaxp=c(0,270,27), pos=0.0)
#box(pos=1.0)
#dev.off() 


#xl <- 0 ; xu <- 3100;
#rnahist <- hist(x, breaks=seq(xl,xu,by=1), plot=FALSE)
#barplot(rnahist$counts, axes=FALSE, ylim=c(0,140), space=0.001, col="skyblue3")
#axis(1, cex.axis=1.0)
#axis(2, cex.axis=1.0)
#box()
