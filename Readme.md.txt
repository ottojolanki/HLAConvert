#Description:


This program converts the HLA coding from NMDP allele codes to the new nomenclature coding based on the CWD 2.0.0 list of alleles.


##File formats: 


The program takes comma-separated input files that have column names. The first column should be individual identifiers marked as ID. Other columns are named locus:name, for example A:harry, DQB1:sweden etc. where the locus is the locus used for the column, and name after that can be anything.
Values marked by *X are filled from cell on the left from the marked value. Use 99:99 for now for NaNs.


##Usage: 


python HLAConvert <your datafile> <NMDP allele code file> <CWD2.0 file> <output filename>
Examples of file formats are provided in the repo.