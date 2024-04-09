#!/usr/bin/python3
# SKOS to Excel
# By Ash Smith, MarEA project, University of Southampton
# Based on PO2Excel, by Thomas Huet and Ash Smith

import os, re, csv, sys, argparse, json
from deep_translator import GoogleTranslator
from deep_translator.exceptions import NotValidPayload
from progress.bar import IncrementalBar as progressbar
from openpyxl import Workbook
from rdflib import Graph, URIRef, Literal
from rdflib.namespace import RDF, RDFS, XSD, SKOS, DCTERMS as DCT
from hashlib import md5

print("Run...")

argp = argparse.ArgumentParser()
argp.add_argument('SKOSFile', metavar='skos_file', type=str, help='The SKOS file to convert')
argp.add_argument('CSVFile', metavar='csv_file', type=str, help='The CSV file to write')
argp.add_argument('-lang', '--language', action='store', type=str, help='The 2-letter code for the language to use', default='')
argp.add_argument('-f', '--format', action='store', type=str, help='The file format to export, xlsx or csv (default is csv)', default='csv')
args = argp.parse_args()

target_language = args.language
target_format = args.format
path_fold = os.getcwd()
input_file = args.SKOSFile
output_file = args.CSVFile

g = Graph()
with open(input_file, 'r') as fp:
	data = fp.read()
g.parse(data=data, format='xml')

target_format = target_format.lower()
if target_format == 'xls':
	target_format = 'xlsx'
if target_format != 'xlsx':
	target_format = 'csv'

ret = []

ret.append(['id', 'language', 'text'])

print("...start loops")
g_len = len(g)
print(g[0])
