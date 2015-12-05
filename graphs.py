#!/usr/bin/env python
"""
================================================================================
 File:        graphs.py
 Authors:     Mauricio Esguerra
 Date:        February 15, 2012
 Email:       mauricio.esguerra@gmail.com

Description:
This module automatically generates plots after subsetting the relevant
information.
The aim is to produce plots like the ones in Figure 2.1 (page 22 ) of the
authors thesis which were created in a more manual, non-fully automated fashion.

================================================================================
"""
import csv
from numpy import *
from pylab import *
from matplotlib import *

class Plots(object):
     """
     Class to plot statistical data parsed from the output of x3dna on a set
     of select downloaded pdb files from the PDB.
     """
     @staticmethod
     def pdb_stats():
     # It seems like recfromcsv is analog to pylabs csv2rec
          data = recfromcsv('rnaonly.csv', delimiter=',',
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
          f = open('data/yearly_nb.csv', 'wb')
          wr = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
          wr.writerows(wrdata)

#writer = csv.writer(ofile, delimiter='\t', quotechar='"', quoting=csv.QUOTE_ALL)

          numrna      = []   # Number of RNA structures per year
          totalnumrna = []   # Total number of RNA structures in PDB
          for i in range(begin,end+1):
               numrna.append(len(data[data['years']==i]['years']))
               totalnumrna.append(sum(numrna))
     #len(data[data['years']==2001]['years'])
  
          wrdata = c_[year,numrna,totalnumrna]
          f = open('data/yearly_numrna.csv', 'wb')
          wr = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
          wr.writerows(wrdata)     
     
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
          xlim(1970, 2014)
          
          subplot(1,2,2)
          plot(year, totalnumrna,'ro')     
          title('Number of RNA Files in PDB vs. Year')
          xlabel('Year')
          ylabel('Total Number of RNA Files in PDB')
     #xticks(year)
          yscale('log')
          grid(True,which="both")
          xlim(1970, 2014)
          savefig("graphs/num_of_rna_files.png", dpi=300, format="png")
     #     show()
          close()

     @staticmethod
     def hel_stats():
          import csv
          from numpy import *
          from pylab import *
          
          helix_size = recfromcsv('helices/size.dat', delimiter='', names=['size'])
          hist(helix_size['size'], len(helix_size['size']))
          title('Frequency vs Size of Helical Regions in RNA\'s')
          xlabel('Helix size (number of base-pairs)')
          ylabel('Frequency')
          xticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16], rotation=0 )
          xlim(0,20)
          grid(True,which="both")
          print helix_size
          savefig("graphs/helices_dist.png", dpi=300, format="png")
     #    show()
          close()
     
     @staticmethod
     def plot():
         import os
         from numpy import *
         import csv
         from matplotlib.figure import Figure
     
         rna     = open('rnaonly.csv', 'r');
         dna     = open('dnaonly.csv', 'r');
         protein = open('proteins.csv','r');
     
         readrna = csv.reader(rna)        
         rnadata = []
         for row in readrna:
             rnadata.append(row)
         
         rna_arr = array(rnadata)
         
         readdna = csv.reader(dna)        
         dnadata = []
         for row in readdna:
             dnadata.append(row)
         
         dna_arr = array(dnadata)
     
         readprotein = csv.reader(protein)        
         proteindata = []
         for row in readprotein:
             proteindata.append(row)
         
         protein_arr = array(proteindata)
                 
         
         fig=Figure()
         ax=fig.add_subplot(111)
         year = rna_arr[1:,0]
         yearly_rna = rna_arr[1:,1]
         yearly_dna = dna_arr[1:,1]
         yearly_protein = protein_arr[1:,1]    
     #    yearlyfit = polyfit(year, yearly, 1)
         ax.set_yscale('log')
         ax.plot(year, yearly_rna,'o', color='red')
         leg1=ax.plot(year, yearly_rna,'b-', color='red')
         ax.plot(year, yearly_dna,'o', color='blue')
         leg2=ax.plot(year, yearly_dna,'b-', color='blue')
         ax.plot(year, yearly_protein,'o', color='green')
         leg3=ax.plot(year, yearly_protein,'b-', color='green')
         ax.grid(True,which="both")
         ax.set_xlim(1995, 2014)
         ax.set_rasterized(True)
         ax.set_xlabel('Year')
         ax.set_ylabel('Number of Yearly Added Structures')    
         ax.set_title('Structures in PDB per Year')
         ax.legend((leg1,leg2,leg3),('RNA','DNA','Protein'), loc=4)
         
         plt.savefig("graphs/rnagraph.png")
         close()
         
     @staticmethod
     def rnadimerplot():
          import os
          homies = '/Users/esguerra'
          static = '/development/python/querypdb'
          os.environ['HOME']=homies+static
          from numpy import *
          import csv
          from matplotlib.figure import Figure
      
          rna     = open(homies+static+'/rnaonly.csv', 'r');
          dna     = open(homies+static+'/dnaonly.csv', 'r');
          protein = open(homies+static+'/proteins.csv','r');
      
          readrna = csv.reader(rna)
          rnadata = []
          for row in readrna:
               rnadata.append(row)
      
               rna_arr = array(rnadata)
      
          readdna = csv.reader(dna)
          dnadata = []
          for row in readdna:
               dnadata.append(row)
      
               dna_arr = array(dnadata)
      
          readprotein = csv.reader(protein)
          proteindata = []
          for row in readprotein:
               proteindata.append(row)
      
          protein_arr = array(proteindata)
      
      
          fig=Figure()
          ax=fig.add_subplot(111)
          year = rna_arr[1:,0]
          yearly_rna = rna_arr[1:,1]
          yearly_dna = dna_arr[1:,1]
          yearly_protein = protein_arr[1:,1]
     #    yearlyfit = polyfit(year, yearly, 1)
          ax.set_yscale('log')
          ax.plot(year, yearly_rna,'o', color='red')
          leg1=ax.plot(year, yearly_rna,'b-', color='red')
          ax.plot(year, yearly_dna,'o', color='blue')
          leg2=ax.plot(year, yearly_dna,'b-', color='blue')
          ax.plot(year, yearly_protein,'o', color='green')
          leg3=ax.plot(year, yearly_protein,'b-', color='green')
          ax.grid(True,which="both")
          ax.set_xlim(1995, 2014)
          ax.set_rasterized(True)
          ax.set_xlabel('Year')
          ax.set_ylabel('Number of Yearly Added Structures')
          ax.set_title('Structures in PDB per Year')
          ax.legend((leg1,leg2,leg3),('RNA','DNA','Protein'), loc=4)
      
          plt.savefig("graphs/aswww.png")
          close()


Plots.pdb_stats()
#Plots.plot()
#Plots.hel_stats()
