#!/usr/bin/python
#####################################################################
## File:        querypdb.py
## Authors:     Mauricio Esguerra
## Date:        February 15, 2012
## Version:     1.0
## Email:       mauricio.esguerra@gmail.com
##
## Description:
## With this script we wish to reduce many tasks to one:
## -1- Query the pdb to get a list of RNA structures with resolution
##     less than or equal to 3.5 Angstrom.
## -2- Download such structures.
## -3- Run them through 3DNA to get the right number of bases.
## -4- Plot Number of Bases vs. Year
##     Plot Number of RNA Molecules vs. Year
##
## Note:
## Perhaps this process can never be fully automated since it
## needs a human checking to see when 3DNA fails due to new
## modified bases.
#####################################################################
import os
from query import queryrna
queryrna()



orig_pdb  = int(os.system("ls data/Pdb/ | wc -l"))
rna_pdb   = int(os.system("ls data/OnlyNA/ | wc -l"))
inp_pdb   = int(os.system("ls data/Inp/ | wc -l"))

def consistency(x,y,z):
    if (x==y and y==z):
        print "All files have been processed by find_pair"
        print "There is no need of baselist.dat editing"
    else:
        print "WARNING! You migth need to edit baselist.dat"
        print "There might be new modified bases in the pdb."    

consistency(orig_pdb,rna_pdb,inp_pdb)

#def grep(string,list):
#    expr = re.compile(string)
#    return filter(expr.search,list)

os.system('grep "date_original" data/Xml/* | grep -v "nil" > t1')
os.system("awk -F '>' '{print substr($2,1,4)}' t1 > c1")
os.system('grep "number of bases" data/Inp/*.inp > t1')
os.system("awk '{print substr($1,5,4)\",\"$2}' t1 > c2")
os.system("paste -d ',' c1 c2 > rnaonly.csv ")
os.system("rm t1 c1 c2")

#####################################################################
## -4-
## Plot number of bases vs. year
## This script automatically generates plots after subsetting the 
## relevant information.
## The aim is to produce plots like the ones in Figure 2.1 (page 22 )
## of the authors thesis which were created in a more manual, 
## non-fully automated fashion.
##    
#####################################################################

import graphs
graphs.plots(1)
