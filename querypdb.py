#!/usr/bin/python
#####################################################################
## File:        querypdb.py
## Authors:     Mauricio Esguerra
## Date:        September 2, 2011
## Email:       mauricio.esguerra@gmail.com
##
## Description:
## With this code we wish to do various task in one script:
## -1- Query the pdb to get a list of RNA structures with resolution
##     less than or equal to 3.5 Angstrom.
## -2- Download said structures.
## -3- Run them through 3DNA to get the right number of bases.
## -4- Plot Number of Bases vs. Year
## -5- Plot Number of RNA Molecules vs. Year
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
    os.system("get_part Pdb/%s.pdb OnlyNA/%s.onlyNA.pdb" % (filename, filename))
    os.system("find_pair -st OnlyNA/%s.onlyNA.pdb Inp/%s.inp" % (filename, filename))    
#    os.system("seq_num %s.onlyNA.pdb" % (filename))
    j = j+1
os.system("dcmnfile")    
#grep "date_original" Xml/* | grep -v "nil" | awk -F '>' '{print substr($2,1,4)}'
#grep "number of bases" Inp/*.inp | awk '{print substr($1,5,4), $2}'

# Bug with number of Inps
# The bug comes from an incomplete baselist.dat file
# To check which files are failing the find_pair do:
# ls -l OnlyNA/ | awk {'print substr($8,1,4)'}  > t1
# ls -l Inp/ | awk {'print substr($8,1,4)'}  > t2
# diff -y t1 t2 | grep "<"



