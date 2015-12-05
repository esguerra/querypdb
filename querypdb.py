#!/usr/bin/python
"""
================================================================================
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
================================================================================
"""
import subprocess
import query
# from query import analysis
# from query import consistency

query.queryrna()

orig_pdb = subprocess.check_output('ls data/Pdb/ | wc -l', shell=True)
print "total number of pdb files = %d" % int(orig_pdb)
rna_pdb = subprocess.check_output('ls data/OnlyNA/ | wc -l', shell=True)
print "rna pdbs = %d" % int(rna_pdb)
inp_pdb = subprocess.check_output('ls data/Inp/ | wc -l', shell=True)
print "inp pdbs = %d" % int(inp_pdb)
query.consistency(orig_pdb, rna_pdb, inp_pdb)

query.makedirs()

query.download()

# query.analysis()
# query.helices()
# query.getdata()

#####################################################################
# -4-
# Plot number of bases vs. year
# This module automatically generates plots after subsetting the
# relevant information.
# The aim is to produce plots like the ones in Figure 2.1 (page 22 )
# of the authors thesis which were created in a more manual,
# non-fully automated fashion.
#####################################################################

# import graphs
# graphs.Plots.plot()
# graphs.Plots.hel_stats()
# graphs.Plots.rnadimerplot()
