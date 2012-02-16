#!/usr/bin/python
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
<orgPdbCompositeQuery version="1.0">
 <queryRefinement>
  <queryRefinementLevel>0</queryRefinementLevel>
  <orgPdbQuery>
    <queryType>org.pdb.query.simple.ChainTypeQuery</queryType>
    <description>Chain Type: there is a RNA chain</description>
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
    <queryType>org.pdb.query.simple.ResolutionQuery</queryType>
    <description>Resolution is between 0.0 and 3.5 </description>
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
nstr=len(result)


if result:
    print "Found number of PDB entries:", len(result)    
else:
    print "Failed to retrieve results"


j=0    
while j <= len(result)-2:
    filename = result[j].rstrip().lower()
    print filename
#    os.system("find_pair -st OnlyNA/%s.onlyNA.pdb Inp/%s.inp" % (filename, filename))    
    j = j+1

