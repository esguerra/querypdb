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

import urllib, urllib2, os, sys, time, re


url = 'http://www.rcsb.org/pdb/rest/search'

#####################################################################
## -1-
## The next part of the script makes a query to the
## Protein Data Bank with the query we want using XML.
##
#####################################################################
queryText = """
<?xml version="1.0" encoding="UTF-8"?>
<orgPdbCompositeQuery version="1.0">
 <queryRefinement>
  <queryRefinementLevel>0</queryRefinementLevel>
  <orgPdbQuery>
    <version>head</version>
    <queryType>org.pdb.query.simple.ChainTypeQuery</queryType>
    <description>Chain Type Search : , Contains RNA=Y</description>
    <containsProtein>?</containsProtein>
    <containsDna>?</containsDna>
    <containsRna>Y</containsRna>
    <containsHybrid>?</containsHybrid>
  </orgPdbQuery>
 </queryRefinement>
 <queryRefinement>
  <queryRefinementLevel>1</queryRefinementLevel>
  <conjunctionType>and</conjunctionType>
  <orgPdbQuery>
    <version>head</version>
    <queryType>org.pdb.query.simple.ResolutionQuery</queryType>
    <description>ResolutionQuery: refine.ls_d_res_high.comparator=between refine.ls_d_res_high.min=0.0 refine.ls_d_res_high.max=3.5 </description>
    <refine.ls_d_res_high.comparator>between</refine.ls_d_res_high.comparator>
    <refine.ls_d_res_high.min>0.0</refine.ls_d_res_high.min>
    <refine.ls_d_res_high.max>3.5</refine.ls_d_res_high.max>
  </orgPdbQuery>
 </queryRefinement>
</orgPdbCompositeQuery>
"""

#print "query:\n", queryText
print "querying PDB...\n"

req = urllib2.Request(url, data=queryText)
f = urllib2.urlopen(req)
result = f.readlines() #Read as a list
#result = f.read()     #Read as a string
nstr=len(result)
#nstr = result.count('\n')  #Use for counting if reading as a string

if result:
    print "Found number of PDB entries:", len(result)    
else:
    print "No data in your query" 


## Create Folders to organize data

if not os.path.exists("Pdb"):
    os.system("mkdir Pdb")
if not os.path.exists("Xml"):
    os.system("mkdir Xml")        
if not os.path.exists("OnlyNA"):
    os.system("mkdir OnlyNA")
if not os.path.exists("Inp"):
    os.system("mkdir Inp")
    
    
#####################################################################
## -2-
## This part takes care of downloading and uncompressing all
## the files which came from the XML query.    
##
#####################################################################


i=0
while i <= len(result)-1:
    filename = result[i].rstrip().lower()
    if not os.path.exists("Pdb/"+filename+".pdb"): #Download ONLY if pdb file does not exist
        pdbname = '%s.pdb.gz' % filename
        xmlname = '%s.xml.gz' % filename
        url='ftp://ftp.wwpdb.org/pub/pdb/data/structures/all/pdb/pdb'+filename+".ent.gz"
        urlxml='ftp://ftp.wwpdb.org/pub/pdb/data/structures/all/XML-noatom/'+filename+"-noatom.xml.gz"
        print "Downloading: "+url
        print "Downloading: "+urlxml
        try:
            urllib.urlretrieve(url, pdbname)
            print "Uncompressing ", pdbname
            os.system("gunzip "+pdbname)
            os.system("mv "+filename+".pdb Pdb/")            
            urllib.urlretrieve(urlxml, xmlname)
            print "Uncompressing ", xmlname            
            os.system("gunzip "+xmlname)
            os.system("mv "+filename+".xml Xml/")                        
        except:
            print "Error retrieving ", url
    else:
        print "PDB file already exists" 
    i = i+1

#####################################################################
## -3-
## Running 3DNA on all files and extracting the information
## we need.
##
## Note: The following commands assume that you have installed
##       and configured correctly 3DNA in your computer.
##
#####################################################################

j=0    
while j <= len(result)-1:
    filename = result[j].rstrip().lower()
    if not os.path.exists("Inp/"+filename+".inp"): #Only do 3DNA processing if it doesn't exist
        os.system("get_part Pdb/%s.pdb OnlyNA/%s.onlyNA.pdb" % (filename, filename))
        os.system("find_pair -st OnlyNA/%s.onlyNA.pdb Inp/%s.inp" % (filename, filename))    
#    os.system("seq_num %s.onlyNA.pdb" % (filename))
    else:
        print "INP file already exists"     
    j = j+1
os.system("dcmnfile")

orig_pdb  = int(os.system("ls Pdb/ | wc -l"))
rna_pdb   = int(os.system("ls OnlyNA/ | wc -l"))
inp_pdb   = int(os.system("ls Inp/ | wc -l"))

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

os.system('grep "date_original" Xml/* | grep -v "nil" > t1')
os.system("awk -F '>' '{print substr($2,1,4)}' t1 > c1")
os.system('grep "number of bases" Inp/*.inp > t1')
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
