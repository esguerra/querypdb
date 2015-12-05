# README  

querypdb.py is a pymol script to automatically download RNA structures from the
PDB given specific query parameters and perform analysis using the original
information and derived information computed with the 3DNA software package.


## Setup  

1. Clone the repository  

    git clone https://github.com/esguerra/querypdb.git


## Usage  

To run the program just call it from the prompt:

    bash-4.0$ ./querypdb.py

And it will download all structures and organize them in their
correspoding folders, and also run them through 3DNA.


## Examples  

To perform common maintenance tasks which do not necessarily have to go through
the more costly step of querying the whole online database some scripts are
provided, for example, the toquery.py and tograph.py scripts.

With the toquery.py script we can check if the numbers of downloaded pdb
structures, find_pair output files, and striped of protein onlyrna files,
match in their counts using the consistency module.

    python toquery.py

Or to produce only the graphs  

    python tographs.py

The scripts are easy to modify so that the user can easily use the objects and
modules that constitute the query and graph packages.


CAUTION: THE DOWNLOADED INFORMATION CAN USE A LARGE AMOUNT OF DISK SPACE.


Thanks for your interest!

Mauricio
