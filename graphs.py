class Plots(object):
     """
     #####################################################################
     ## graphs.py
     ## Date: February 15, 2012
     ## This module automatically generates plots after subsetting the 
     ## relevant information.
     ## The aim is to produce plots like the ones in Figure 2.1 (page 22 )
     ## of the authors thesis which were created in a more manual, 
     ## non-fully automated fashion.
     #####################################################################
     """
     @staticmethod
     def pdb_stats():
          import csv
          from numpy import *
          from pylab import *
          
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

          numrna      = []   # Number of RNA structures per year
          totalnumrna = []   # Total number of RNA structures in PDB
          for i in range(begin,end+1):
               numrna.append(len(data[data['years']==i]['years']))
               totalnumrna.append(sum(numrna))
     #len(data[data['years']==2001]['years'])

          subplot(1,2,1)    
          plot(year, totalnb,'bo')
          title('Number of RNA Bases in PDB vs. Year')
          xlabel('Year')
          ylabel('Total Number of RNA Bases in PDB')
     #yscale('log')
          grid(True,which="both")
          xlim(2000, 2011)
     #rasterized(True)
     #savefig("num_of_rna_bases.png", dpi=200, format="png")
     #close()

          subplot(1,2,2)
          plot(year, totalnumrna,'ro')
          title('Number of RNA Files in PDB vs. Year')
          xlabel('Year')
          ylabel('Total Number of RNA Files in PDB')
     #xticks(year)
     #yscale('log')
          grid(True,which="both")
          xlim(2000, 2011)
     #rasterized(True)
          savefig("graphs/num_of_rna_files.png", dpi=300, format="png")
          show()
          close()

     @staticmethod
     def hel_stats():
          import csv
          from numpy import *
          from pylab import *
          
          helix_size = recfromcsv('helices/size.dat', delimiter='', names=['size'])
          hist(helix_size['size'], len(helix_size['size']))
          xticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], rotation=0 )
          xlim(0,20)
          grid(True,which="both")
          print helix_size
          show()
     





