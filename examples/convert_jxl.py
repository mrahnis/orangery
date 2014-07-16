#!/usr/bin/python

"""
Applies an XSLT stylesheet to a JobXML
	# variable name : String
	# prompt : String
	# variable type : Double, Integer, String and StringMenu

"""
from __future__ import print_function

from collections import OrderedDict
import json
from lxml import etree

from orangery.tools.console import *

def read_xml(filename, parser):
	xml = open(filename).read().encode('utf-8')
	xmlRoot = etree.fromstring(xml, parser=parser)

	return xmlRoot

def get_fields(xslRoot):
	fields = OrderedDict()

	# xpath 1.0
	for element in xslRoot.xpath("//xsl:variable[starts-with(@name, 'userField')]", namespaces={'xsl':'http://www.w3.org/1999/XSL/Transform'}):
	# xpath 2.0
	#for field in xslRoot.xpath("/variable[matches(@name, 'userField*')]"):
		select = element.attrib['select'].strip("'")
		properties = select.split('|')
		fields[properties[0]] = properties[1:]

	return fields

def get_options(xslRoot, options):
	settings = OrderedDict()

	for option in options:
		setting = xslRoot.xpath("//xsl:variable[@name = '{0}']".format(option), namespaces={'xsl':'http://www.w3.org/1999/XSL/Transform'})
		settings[setting[0].attrib['name']] = setting[0].attrib['select'].strip("'")
	return settings

def set_options(xslRoot, options):
	for option in options:
		current = xslRoot.xpath("//xsl:variable[@name = '{0}']".format(option), namespaces={'xsl':'http://www.w3.org/1999/XSL/Transform'})
		current[0].set('select', options[option])
	return xslRoot

def get_input(xslRoot):
	options = OrderedDict()
	fields = get_fields(xslRoot)
	for field in fields:
		props = fields[field]
		label = "{0}?".format(props[0])
		if props[1].lower()=='stringmenu':
			n = int(props[2])
			value = choice_prompt(props[-n:], label=label)
		elif props[1].lower()=='double':
			value = double_prompt(props[2], props[3], label=label)
		elif props[1].lower()=='integer':
			value = integer_prompt(props[2], props[3], label=label)
		elif props[1].lower()=='string':
			value = string_prompt(label=label)
		else:
			print('Unexpected field type: ', props[1])
		options[field] = "'{0}'".format(value)
	return options

def transform(xmlRoot, xslRoot, options=None):

	fields = get_fields(xslRoot)

	if options is not None:
		xslRoot = set_options(xslRoot, options)
		print('Using Options:')
	else:
		print('Using Defaults:')
	
	print(json.dumps(get_options(xslRoot, fields)))
	print()

	transform = etree.XSLT(xslRoot)
	transRoot = transform(xmlRoot)

	return transRoot

if __name__ == '__main__':
	import argparse

	# python .\convert_jxl.py './data/Topo-20100331.jxl' './xslt/Comma Delimited with dates.xsl' -o text.csv --includeAttributes='No' --no-prompt

	parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')

	argparser = argparse.ArgumentParser()
	argparser.add_argument('xml_path', help="input JobXML path")
	argparser.add_argument('xsl_path', help="input XSLT stylesheet path"),
	argparser.add_argument('-o', '--output', dest='output', type=argparse.FileType('wb', 0), help="output file name")
	
	argparser.add_argument('--prompt', dest='prompt', action='store_true', help="show user prompts for stylesheet options")
	argparser.add_argument('--no-prompt', dest='prompt', action='store_false', help="do not show user prompts for stylesheet options")
	argparser.set_defaults(prompt=True)

	args = argparser.parse_known_args()

	xmlRoot = read_xml(args[0].xml_path, parser)
	xslRoot = read_xml(args[0].xsl_path, parser)

	fields = get_fields(xslRoot)
	for field in fields:
		props = fields[field]
		argparser.add_argument('--{0}'.format(field), help=props[0])

	args = argparser.parse_args()

	if args.prompt is True:
		options = get_input(xslRoot)
	else:
		options = get_options(xslRoot, fields)
		arguments = (vars(args))
		for field in fields:
			if arguments[field] is not None:
				 options[field] = arguments[field]

	#print(json.dumps(options))

	result = transform(xmlRoot, xslRoot, options=options)

	if args.output is not None:
		args.output.write(result)
	else:
		print(result)
