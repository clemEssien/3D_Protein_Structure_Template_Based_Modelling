import os
from os.path import dirname, abspath
import sys
import textwrap
DIRECTORY = dirname(dirname(abspath(__file__)))
sys.path.append(DIRECTORY)
from lib import library 
from Bio.Blast import NCBIWWW
from Bio.Blast import NCBIXML
from Bio import SeqIO
from Alignment import Alignment

TARGET_DIR = "../data/target/" #place target fasta files here i.e. one fasta file per target protein
OUTPUT_DIR = "../data/msa/"


def parse_result(msa_xml_file,file_no):
	result=open(msa_xml_file,"r")
	output= OUTPUT_DIR+"msa"+str(file_no)+".fasta";
	records= NCBIXML.parse(result)
	item=next(records)
	for alignment in item.alignments:
		for hsp in alignment.hsps:
			library.write_to_file(output, ">"+alignment.accession[0:4]+":"+alignment.accession[5]+"|PDBID|CHAIN|SEQUENCE","a")
			library.write_to_file(output, hsp.query, "a")
			library.write_to_file(output, hsp.match,"a")
			library.write_to_file(output, hsp.sbjct, "a")
		library.write_to_file(output, "", "a")
	print(str(file_no)+" msa fasta file has been generated")

def gen_alignment_obj(msa_xml_file):
	result=open(msa_xml_file,"r")
	records= NCBIXML.parse(result)
	alignment_obj_list = []
	item=next(records)
	for alignment in item.alignments:
		for hsp in alignment.hsps:
			hit_id = alignment.accession[0:4]+"_"+alignment.accession[5]
			query_range = (hsp.query_start,hsp.query_end)
			hit_range = (hsp.sbjct_start,hsp.sbjct_end)
			query_hit_dict = None   #Jeff your code goes in here
			alignment_obj = Alignment(hit_id, query_range,hit_range,query_hit_dict)
			alignment_obj_list.append(alignment_obj)
	return alignment_obj_list;

def main():
	library.create_dir(TARGET_DIR)
	for filename in os.listdir(TARGET_DIR):
		file_no =0; 
		if filename.endswith(".fasta") :
	    	 file_no +=1;
	    	 target_file = TARGET_DIR+filename;
	    	 msa_file = OUTPUT_DIR+"msa.xml";
	    	 record = SeqIO.read(target_file, format="fasta")
	    	 result_handle = NCBIWWW.qblast("blastp", "pdbaa", record.seq)
	    	 library.create_dir(OUTPUT_DIR)
	    	 library.write_stream(msa_file, result_handle)
	    	 parse_result(msa_file, file_no)
		else:
	        	continue

main()