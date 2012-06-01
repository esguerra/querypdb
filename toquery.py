import os
from query import consistency
from query import getdata
#from query import queryrna
#queryrna()

orig_pdb  = int(os.system("ls data/Pdb/ | wc -l"))
rna_pdb   = int(os.system("ls data/OnlyNA/ | wc -l"))
inp_pdb   = int(os.system("ls data/Inp/ | wc -l"))
rel_date  = int(os.system("grep \"REVDAT\" data/Pdb/*.pdb | awk '{ if ($5 ~ /^0/) print $0}' | wc -l"))

consistency(orig_pdb,rna_pdb,inp_pdb)

#Uncomment to check that the release dates match
#consistency(orig_pdb,rna_pdb,rel_date)

getdata()