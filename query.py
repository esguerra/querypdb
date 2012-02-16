#!/usr/bin/python
#####################################################################
## File:        query.py
## Authors:     Mauricio Esguerra
## Date:        February 16, 2012
## Version:     1.0
## Email:       mauricio.esguerra@gmail.com
##
## This module takes care of querying the pdb directly from the 
## online repository.
#####################################################################

def queryrna():
    import urllib
    import urllib2
    import os
    import sys
    import time
    import re
    url = 'http://www.rcsb.org/pdb/rest/search'

    queryText = """
<?xml version="1.0" encoding="UTF-8"?>
<orgPdbCompositeQuery version="1.0">

<queryRefinement>
<queryRefinementLevel>0</queryRefinementLevel>
<orgPdbQuery>
<version>head</version>
<queryType>org.pdb.query.simple.ChainTypeQuery</queryType>
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


<!--
<queryRefinement>
<queryRefinementLevel>1</queryRefinementLevel>
<conjunctionType>and</conjunctionType>
<orgPdbQuery>
<version>head</version>
<queryType>org.pdb.query.simple.ReleaseDateQuery</queryType>
<database_PDB_rev.date.comparator>between</database_PDB_rev.date.comparator>
<database_PDB_rev.date.min>2010-01-01</database_PDB_rev.date.min>
<database_PDB_rev.date.max>2011-01-01</database_PDB_rev.date.max>
<database_PDB_rev.mod_type.comparator><![CDATA[<]]></database_PDB_rev.mod_type.comparator>
<database_PDB_rev.mod_type.value>1</database_PDB_rev.mod_type.value>
</orgPdbQuery>
</queryRefinement>
-->

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
    #print result

    if result:
        print "Number of PDB entries found matching query:", nstr 
    else:
        print "No data in your query"
    
    
  ## Create Folders to organize data
    if not os.path.exists("data"):
        os.system("mkdir data")
    if not os.path.exists("data/Pdb"):
        os.system("mkdir data/Pdb")
    if not os.path.exists("data/Xml"):
        os.system("mkdir data/Xml")        
    if not os.path.exists("data/OnlyNA"):
        os.system("mkdir data/OnlyNA")
    if not os.path.exists("data/Inp"):
        os.system("mkdir data/Inp")


    i=0
    while i <= len(result)-1:
        filename = result[i].rstrip().lower()
        if not os.path.exists("data/Pdb/"+filename+".pdb"): #Download ONLY if pdb file does not exist
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
                os.system("mv "+filename+".pdb data/Pdb/")            
                urllib.urlretrieve(urlxml, xmlname)
                print "Uncompressing ", xmlname            
                os.system("gunzip "+xmlname)
                os.system("mv "+filename+".xml data/Xml/")                        
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
        if not os.path.exists("data/Inp/"+filename+".inp"): #Only do 3DNA processing if it doesn't exist
            os.system("get_part data/Pdb/%s.pdb OnlyNA/%s.onlyNA.pdb" % (filename, filename))
            os.system("find_pair -st data/OnlyNA/%s.onlyNA.pdb data/Inp/%s.inp" % (filename, filename))    
    #    os.system("seq_num %s.onlyNA.pdb" % (filename))
        else:
            print "INP file already exists"     
        j = j+1
    os.system("dcmnfile")