#!/usr/bin/python
import fileinput
import re
import json
import urllib

user_input_gene_name = raw_input('Please type your gene name, all caps, and press enter: ')

matched=False
gene_id_str=""

for line in fileinput.input(['/data/Homo_sapiens.GRCh37.75.gtf']):
    text_in_columns = re.split('\t',line)
    text_to_match ='gene_name \"'+user_input_gene_name+'\";'
    gene_name = re.findall(text_to_match,line)
    if len(gene_name)>0:
        gene_id = re.findall('gene_id \"(.*?)\";',line)
        gene_id_str=gene_id[0]
        matched=True

if matched:
    print("The variants within the gene " + user_input_gene_name + " " + gene_id_str + " are:")

data = urllib.urlopen("http://rest.ensembl.org/overlap/id/"+gene_id_str+".json?feature=variation").read()
text = json.loads(data)

for i in text:
    variant_id = i["id"]
    consequence_type_with_underscore = i["consequence_type"]
    consequence_type_with_space = consequence_type_with_underscore.replace("_", " ")
    clinical_significance = i["clinical_significance"]
    if len(clinical_significance) == 0:
        print("Variant " + variant_id + " is a " + consequence_type_with_space)
    else:
        print("Variant " + variant_id + " is a " + consequence_type_with_space + ", and is clinically PATHOGENIC")
