#!/usr/bin/python
"""
File:        simple.py
Authors:     Mauricio Esguerra
Date:        January 28, 2010
Email:       mauricio.esguerra@gmail.com

Description:
This is a simple example script for querying directly to the statically served
xml's in the PDB.
"""
import urllib, urllib2, os, sys, time, re

url = 'http://www.rcsb.org/pdb/files/1ehz.xml'
f = urllib2.urlopen(url)
xml_string = f.read()

date = re.findall('date_original',xml_string)
print date


from xml.parsers import expat

class Parser:
    def __init__(self):
        self._parser = expat.ParserCreate()
        self._parser.StartElementHandler = self.start
        self._parser.EndElementHandler = self.end
        self._parser.CharacterDataHandler = self.data
    def feed(self, data):
        self._parser.Parse(data, 0)
    def close(self):
        self._parser.Parse("", 1) # end of data
        del self._parser # get rid of circular references
    def start(self, tag, attrs):
        print "START", repr(tag), attrs
    def end(self, tag):
        print "END", repr(tag)
    def data(self, data):
        print "DATA", repr(data)

p = Parser()
p.feed(xml_string)
p.close()

