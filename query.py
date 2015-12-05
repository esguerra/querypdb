#!/usr/bin/env python
"""
================================================================================
 File:        query.py
 Authors:     Mauricio Esguerra
 Date:        February 16, 2012
 Version:     1.0
 Email:       mauricio.esguerra@gmail.com

 This module takes care of querying the pdb directly from the
 online repository.
================================================================================
"""
import urllib2
import urllib
import os


def queryrna():
    url = 'http://www.rcsb.org/pdb/rest/search'
    xmlquery = open('queryrna.xml', 'r')
    # print "query:\n", queryText
    print "querying PDB...\n"
    req = urllib2.Request(url, data=xmlquery.read())
    f = urllib2.urlopen(req)
    # Note how result is defined global to be able to call it from
    # other modules.
    global result
    result = f.readlines()  # Read as a list
    # result = f.read()     # Read as a string
    nstr = len(result)
    # nstr = result.count('\n')  #Use for counting if reading as a string
    # print result

    if result:
        print "Number of PDB entries found matching query:", nstr
    else:
        print "No data in your query"


def makedirs():
    """
    Create Folders to organize data
    """
    if not os.path.exists("data"):
        os.system("mkdir data")
    if not os.path.exists("data/Pdb"):
        os.system("mkdir data/Pdb")
    if not os.path.exists("data/Xml"):
        os.system("mkdir data/Xml")
#    if not os.path.exists("data/Cif"):
#        os.system("mkdir data/Cif")
    if not os.path.exists("data/OnlyNA"):
        os.system("mkdir data/OnlyNA")
    if not os.path.exists("data/Inp"):
        os.system("mkdir data/Inp")
    if not os.path.exists("helices"):
        os.system("mkdir helices")


def download():
    i = 0
    while i <= len(result)-1:
        filename = result[i].rstrip().lower()
        print filename
        # Download ONLY if pdb file does not exist
        if not os.path.exists("data/Pdb/"+filename+".pdb"):
            pdbname = '%s.pdb.gz' % filename
            xmlname = '%s.xml' % filename.upper()
            # cifname = '%s.cif.gz' % filename
            url = 'ftp://ftp.wwpdb.org/pub/pdb/data/structures/all/pdb/pdb'\
                  + filename + ".ent.gz"
            # urlxml='ftp://ftp.wwpdb.org/pub/pdb/data/structures/all/pdb/xml'
            # + filename + ".xml.gz"
            urlxml = 'http://www.pdb.org/pdb/files/'+filename.upper()+".xml"
            # urlcif='ftp://ftp.wwpdb.org/pub/pdb/data/structures/all/mmCIF/'
            # + filename + ".cif.gz"
            print "Downloading: "+url
            print "Downloading: "+urlxml
            # print "Downloading: "+urlcif
            try:
                urllib.urlretrieve(url, pdbname)
                print "Uncompressing ", pdbname
                os.system("gunzip "+pdbname)
                os.system("mv "+filename+".pdb data/Pdb/")
                urllib.urlretrieve(urlxml, xmlname)
                os.system("mv "+filename+".xml data/Xml/")
#                urllib.urlretrieve(urlcif, cifname)
#                print "Uncompressing ", cifname
#                os.system("gunzip "+cifname)
#                os.system("mv "+filename+".cif data/Cif/")
            except:
                print "Error retrieving ", url
        else:
            print "PDB file already exists"
        i = i+1


def analysis():
    """
    -3-
    Running 3DNA on all files and extracting the information we need.
    Note: The following commands assumes you've installed and configured 3DNA
    in your computer.
    """
    j=0
    while j <= len(result)-1:
        filename = result[j].rstrip().lower()
        # Only do 3DNA processing if it doesn't exist
        if not os.path.exists("data/Inp/"+filename+".inp"):
            os.system("get_part data/Pdb/%s.pdb data/OnlyNA/%s.onlyNA.pdb"
                      % (filename, filename))
            os.system("find_pair -st data/OnlyNA/%s.onlyNA.pdb data/Inp/%s.inp"
                      % (filename, filename))
    #    os.system("seq_num %s.onlyNA.pdb" % (filename))
        else:
            print "INP file already exists"
        j = j+1
    os.system("x3dna_utils dcmnfile")


def consistency(x,y,z):
    """
    -4-
    Module to check that all pdb files have gone through find_pair
    """
    if (x==y and y==z):
        print "All files have been processed by find_pair"
        print "There is no need of baselist.dat editing"
    else:
        print "WARNING! You migth need to edit baselist.dat"
        print "There might be new modified bases in the pdb."


def getdata():
    """
    -5-
    Module that assambles the data for new rnas against year.
    """
    os.system('grep "date_original" data/Xml/* | grep -v "nil" > t1')
    os.system("awk -F '>' '{print substr($2,1,4)}' t1 > c1")
    os.system('grep "number of base-pairs" data/Inp/*.inp > t1')
    os.system("awk '{print substr($1,5,4)\",\"$2}' t1 > c2")
    os.system("paste -d ',' c1 c2 > rnaonly.csv ")

# Thw following code became obsolete with newer versions of python as it cannot read via os.system as a variable.
#    os.system("grep \"REVDAT\" data/Pdb/*.pdb | awk '{ if ($5 ~ /^0/) print \"\"substr($3,8,2)\",\"substr($4,0,4)}' > t1")
#    os.system("awk -F ',' '{if ($1 >= 70) print \"19\"$1\",\"$2; else print \"20\"$1\",\"$2}' t1 > c1")
#    os.system("grep \"number of base-pairs\" data/Inp/*.inp | awk '{print $2}' > c2")

#    year=subprocess.check_output("grep \"REVDAT\" data/Pdb/*.pdb | awk '{ if ($5 ~ /^0/) print substr($3,8,2)}'", shell=True)
#    print "two digit year = %d" % float(year)
# This is a really bad patch for y2k style issue. At some point having a two digit year will break again.
#    os.system("awk -F ',' '{if ($1 >= 70) print \"19\"$1\",\"$2; else print \"20\"$1\",\"$2}' t1 > c1")
#    os.system("grep \"number of base-pairs\" data/Inp/*.inp | awk '{print $2}' > c2")
##grep -L "number of base-pairs" *.inp  #To find if there are any without number of base-pairs
#    os.system("paste -d ',' c1 c2 > rnaonly.csv ")
#    os.system("rm t1 c1 c2")
    # IT's ONLY MISSING adding 19XX and 20XX in years

# Gives a number smaller than it should.
#awk '{ if ($1 ~ /^1$/ && $NF ~  /^0$/) print $0}' *.cif | wc -l

# Not all records of release date are in row 23rd
#for i in *.cif; do; awk 'NR==23' $i ; done

# The record which seems to work always is in the bulky Xml's.
#grep "<PDBx:date_original>" Xml/*.xml | wc -l
#ls -l Xml/* | wc -l


def helices():
    j=0
    while j <= len(result)-1:
        filename = result[j].rstrip().lower()
        if not os.path.exists("data/Inp/"+filename+".inp"): #Only do 3DNA processing if it doesn't exist
            os.system("get_part data/Pdb/%s.pdb data/OnlyNA/%s.onlyNA.pdb" % (filename, filename))
            os.system("find_pair data/OnlyNA/%s.onlyNA.pdb data/Inp/%s.inp" % (filename, filename))
        #    os.system("seq_num %s.onlyNA.pdb" % (filename))
        else:
            print "INP file already exists"
        j = j+1
    os.system("x3dna_utils dcmnfile")
    os.system('grep " helices " data/Inp/* | awk \'{print $6}\' > helices/size.dat')


#queryrna()
#orig_pdb=subprocess.check_output("ls data/Pdb/ | wc -l",shell=True)
#print "total number of pdb files = %d" % int(orig_pdb)
#rna_pdb=subprocess.check_output("ls data/OnlyNA/ | wc -l",shell=True)
#print "rna pdbs = %d" % int(rna_pdb)
#inp_pdb=subprocess.check_output("ls data/Inp/ | wc -l",shell=True)
#print "inp pdbs = %d" % int(inp_pdb)
#consistency(orig_pdb,rna_pdb,inp_pdb)