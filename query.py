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
import subprocess


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
                os.system("gunzip " + pdbname)
                os.system("mv " + filename + ".pdb data/Pdb/")
                urllib.urlretrieve(urlxml, xmlname)
                os.system("mv " + filename + ".xml data/Xml/")
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
            subprocess.call("get_part data/Pdb/%s.pdb data/OnlyNA/%s.onlyNA.pdb"
                      % (filename, filename), shell=True)
            subprocess.call("find_pair -st data/OnlyNA/%s.onlyNA.pdb data/Inp/%s.inps"
                      % (filename, filename), shell=True)
            subprocess.call("find_pair data/OnlyNA/%s.onlyNA.pdb data/Inp/%s.inp"
                      % (filename, filename), shell=True)
    #    os.system("seq_num %s.onlyNA.pdb" % (filename))
        else:
            print "INP file already exists"
        j = j+1
    subprocess.call("x3dna_utils dcmnfile", shell=True)


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
    """ -5-
    Module that assambles the data for new rnas against year.
    rnaonly.csv  year, pdbid, numberofbases
    """
    subprocess.call("grep date_original data/Xml/* | grep -v \"nil\" > xmldate", shell=True)
    subprocess.call("awk -F '>' '{print substr($2,1,4)}' xmldate > year", shell=True)
    subprocess.call("awk '{print substr($0,10,4)}' xmldate > pdbid", shell=True)
    subprocess.call("grep \"number of bases\" data/Inp/*.inps | awk '{print $2}' > numbases", shell=True)
    subprocess.call("paste -d ',' year pdbid numbases > rnaonly.csv", shell=True)


def helices():
    j=0
    while j <= len(result)-1:
        filename = result[j].rstrip().lower()
        # Only do 3DNA processing if it doesn't exist
        if not os.path.exists("data/Inp/"+filename+".inp"):
            subprocess.call("get_part data/Pdb/%s.pdb data/OnlyNA/%s.onlyNA.pdb"
                      % (filename, filename), shell=True)
            subprocess.call("find_pair data/OnlyNA/%s.onlyNA.pdb data/Inp/%s.inp"
                      % (filename, filename), shell=True)
        #    os.system("seq_num %s.onlyNA.pdb" % (filename))
        else:
            print "INP file already exists"
        j = j+1
    subprocess.call("x3dna_utils dcmnfile", shell=True)
    subprocess.call('grep " helices " data/Inp/*.inp | awk \'{print $6}\' > helices/size.dat',
                    shell=True)


#queryrna()
#orig_pdb=subprocess.check_output("ls data/Pdb/ | wc -l",shell=True)
#print "total number of pdb files = %d" % int(orig_pdb)
#rna_pdb=subprocess.check_output("ls data/OnlyNA/ | wc -l",shell=True)
#print "rna pdbs = %d" % int(rna_pdb)
#inp_pdb=subprocess.check_output("ls data/Inp/ | wc -l",shell=True)
#print "inp pdbs = %d" % int(inp_pdb)
#consistency(orig_pdb,rna_pdb,inp_pdb)
