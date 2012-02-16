# If you want to run this from the command line as a script
# Do
# R CMD BATCH filename.R >& filename.log &

peryear <- read.table("yearlydata.dat")
x <- peryear[,4]
y1 <- peryear[,2]
y2 <- peryear[,2]

m <- nrow(peryear)

cull <- function(i){
if (peryear[i,4] >= 2000 & peryear[i,4] <=  2009) peryear[i,]
else matrix(NA,1,4)
}

A <- sapply(1:m,cull)

write.table(t(A),"2000_2001.tab",sep="\t",col.names=FALSE,row.names=FALSE)


postscript("rna_per_year.ps")
par( mfrow= c(1, 2), lwd=0.1 )

# Total RNA Molecules per year
#
plot(x, y1, 
     main="Total RNA Molecules per Year", 
     xlab="Year", ylab="Total number of RNA molecules")
points(x, y1, pch=21, cex=3, bg="red")
lines(x, y1)
# Total RNA bases per year
#
plot(x, y2,
     main="Total RNA Bases per Year", 
     xlab="Year", ylab="Total number of RNA bases")
points(x, y2, pch=21, cex=3, bg="blue")
lines(x, y2)
dev.off()
