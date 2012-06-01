#!/usr/bin/python
import csv
from numpy import *
from pylab import *
from matplotlib import *

# It seems like recfromcsv is analog to pylabs csv2rec
data = recfromcsv('../rnaonly.csv', delimiter=',',
                  names=['years','pdbid','nofbp'])

begin = min(data['years'])
end   = max(data['years'])

year = []
nb   = []      # Number of bases per year
totalnb = []   # Total number of bases in pdb
for i in range(begin,end+1):
     nb.append(sum(data[data['years']==i]['nofbp']))
     totalnb.append(sum(nb))
     year.append(i)

wrdata = c_[year,nb,totalnb]
f = open('yearly.csv', 'wb')
wr = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
wr.writerows(wrdata)

numrna      = []   # Number of RNA structures per year
totalnumrna = []   # Total number of RNA structures in PDB
for i in range(begin,end+1):
     numrna.append(len(data[data['years']==i]['years']))
     totalnumrna.append(sum(numrna))
#len(data[data['years']==2001]['years'])


rcParams['figure.figsize'] = 14, 10
subplot(1,2,1)
plot(year, totalnb,'bo')
#subplots_adjust(left=0.0, bottom=0.0, right=0.1, top=0.1, wspace=0.0, hspace=0.0)
#http://stackoverflow.com/questions/6541123/improve-subplot-size-spacing-with-many-subplots-in-matplotlib
#         subplots_adjust(wspace=2.0, hspace=0.1)
title('Total Number of Base-Paired RNA Bases in PDB vs. Year')
xlabel('Year')
ylabel('Total Number of RNA Bases in PDB')
#xticks([2000, 2002, 2004, 2006, 2008, 2010, 2012], rotation=0 )
yscale('log')
grid(True,which="both")
xlim(1970, 2012)

subplot(1,2,2)
plot(year, totalnumrna,'ro')     
title('Number of RNA Files in PDB vs. Year')
xlabel('Year')
ylabel('Total Number of RNA Files in PDB')
#xticks(year)
yscale('log')
grid(True,which="both")
xlim(1970, 2012)
savefig("graphs/num_of_rna_files.png", dpi=300, format="png")
#     show()
close()
