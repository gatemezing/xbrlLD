import json
import rdflib
import glob
from rdflib import Literal, BNode, Graph
from string import capitalize
from pprint import pprint
from rdflib.namespace import XSD
import re
import random


## Author: @gatemezing ##
## This script is intended to transform XBRL data + dimensions in JSON to RDF ##
## It is compatible with Python 2.7 - v3 ####
## Copyright: 2016 ### 


#-- namespaces declaration here -##
## ------------------------------##

RDF = rdflib.Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
RDFS = rdflib.Namespace("http://www.w3.org/2000/01/rdf-schema#")
OWL = rdflib.Namespace("http://www.w3.org/2002/07/owl#")
SKOS = rdflib.Namespace("http://www.w3.org/2004/02/skos/core#")
DCT = rdflib.Namespace("http://purl.org/dc/terms/")
FOAF = rdflib.Namespace("http://xmlns.com/foaf/0.1/")
ORG = rdflib.Namespace("http://www.w3.org/ns/org#")
SCHEMA = rdflib.Namespace("http://schema.org/")

FCT= rdflib.Namespace("http://data.mondeca.com/id/fact/")
PERS = rdflib.Namespace("http://data.mondeca.com/id/xbrl/person/")
ENT = rdflib.Namespace("http://data.mondeca.com/id/entity/")
XBRLL = rdflib.Namespace("https://w3id.org/vocab/xbrll#")
ROV = rdflib.Namespace("http://www.w3.org/ns/regorg#")
VCARD = rdflib.Namespace("http://www.w3.org/2006/vcard/ns#")
DIM = rdflib.Namespace("http://data.mondeca.com/id/dimension/")

CDP =rdflib.Namespace("http://www.cdp.net/xbrl/cdp/cdp-cor/")
CDPENUM=rdflib.Namespace("http://www.cdp.net/xbrl/cdp/cdp-enum/")

DTS=rdflib.Namespace("http://data.mondeca.com/id/dataset/")
SDMXAT=rdflib.Namespace("http://purl.org/linked-data/sdmx/2009/measure#")
QB=rdflib.Namespace("http://purl.org/linked-data/cube#")
SDMXMEASURE=rdflib.Namespace("http://purl.org/linked-data/sdmx/2009/measure#")

# all the entities ipp-enc and ipp-com from the legacy data
# are all added in the IPPENC namespace below

IPPENC = rdflib.Namespace("http://data.mondeca.com/id/skos/ipp/")
IPPSCH = rdflib.Namespace("http://data.mondeca.com/id/scheme/ipp")

# Here in the case of using the IPP namespaces in the XBRL scheme
IPPCOM = rdflib.Namespace("http://www.cnmv.es/ipp/com/1-2008/") 
IPPGEN = rdflib.Namespace("http://www.cnmv.es/ipp/gen/1-2008/")

# here we put legacy es-be-fs and ifrs-gp
IFRSGPS = rdflib.Namespace("http://data.mondeca.com/id/scheme/ifrsgp")
IFRSGP = rdflib.Namespace("http://data.mondeca.com/id/skos/ifrsgp/")

# here we put legacy dgi-est-gen, dgi-lc-es and dgi-lc-int namespaces
DGI = rdflib.Namespace("http://data.mondeca.com/id/skos/dgi/")
DGIS = rdflib.Namespace("http://data.mondeca.com/id/scheme/dgi")
RSOURCE = rdflib.Namespace("http://dbpedia.org/resource/")






#RDF graphe preparation 
data = rdflib.ConjunctiveGraph()


# ----- opening the json file --###
###################################

json_data = open('/Users/gatemezing/Dropbox/Ghislain - Maria/01. Data/03. SPARQL data/CDP_2015.json')
jdata = json.load(json_data)

#pprint(jdata) 

facts = jdata[u'facts']  
prefixes = jdata[u'prefixes'] 
header = jdata[u'dtsReferences']


## some useful declarations here
bn1 = BNode()
bn2 = BNode()
v3 = ""

#fentity = Graph()

for i in range(1,len(facts)) :
	tuple = jdata[u'facts'][i]
	v = "f"+str(random.randint(1000,1000000)) #todo: find sth more generic
	#print(v)
	#print(tuple)
	# here we start to generate facts and dimensions
	for j in tuple:
		if j == u'baseType':

			#v = tuple[j]
			data.add((FCT[v], RDF["type"], XBRLL["Fact"]))
       
			sbj1= tuple[u'oim:concept']
			data.add((FCT[v], XBRLL["concept"], Literal(sbj1)))  #handle as literal/string
			v1 = tuple[j]
			print v1

			if v1 == u'xs:decimal':
				# accuracy is replaced by xbrll:decimals

				e = tuple[u'numericValue']
				data.add((FCT[v], XBRLL["value"], Literal(e, datatype=XSD.decimal))) #todo: add decimal datatype
				e1 = tuple[u'oim:unit']
				data.add((FCT[v], XBRLL["unitRef"], Literal(e1)))


			if v1 in {u'xs:string', u'xs:QName'}:

				obj = tuple[u'value']
				data.add((FCT[v], XBRLL["value"], Literal(obj)))    #handle as literal/string

			od = tuple[u'oim:entity']
			# creating the uri part of the entity
			od1 = od.find(":")
			od2 = od[od1+1:len(od)]
			data.add((FCT[v], XBRLL["hasEntity"], ENT[od2]))
			
			#d = tuple[u'accuracy']

			

			#e1 = tuple[u'oim:unit']
			#data.add((FCT[v], XBRLL["unitRef"], Literal (e1)))

			pde = tuple[u'oim:period'] 

			e3 = BNode() # bNode for the start/end period

			data.add((FCT[v], XBRLL["period"], e3))
			e4 = tuple[u'oim:period'][u'start']
			data.add((e3, XBRLL["startPeriod"], Literal(e4, datatype=XSD.date)))
			e5 = tuple[u'oim:period'][u'end']
			data.add((e3, XBRLL["endPeriod"], Literal(e5, datatype=XSD.date)))
        
		if j == u'accuracy':
			d = tuple[u'accuracy']
			data.add((FCT[v], XBRLL["decimals"], Literal(d)))

			bn1 = BNode()   # for dimensionsionalItem

		if j in {u'cdp:GreenhouseInventoryBoundariesAxis', u'cdp:TotalEmissionDataAxis'} :
			d1 = tuple[j]
			st = v
			data.add((FCT[v], XBRLL["hasDimension"], DIM[st]))
			data.add((DIM[st], RDF["type"], XBRLL["Dimension"]))
			data.add((DIM[st], XBRLL["dimension"], bn1))
			data.add((bn1, XBRLL["axis"], Literal(j)))
			data.add((bn1, XBRLL["member"], Literal(d1)))

		

    


json_data.close()


# ----- OUTPUT FILES -----

print "Length of data : " + str(len(data))

print "Nb of facts  in dataset : " + str(len(list(data.triples((None, RDF["type"], XBRLL["Fact"])))))
outfile = open("/Users/gatemezing/Dropbox/Ghislain - Maria/01. Data/03. SPARQL data/CDP_2015.rdf", "w")
#outfile.write(gxbrl.serialize())
data.serialize(destination='/Users/gatemezing/Dropbox/Ghislain - Maria/01. Data/03. SPARQL data/CDP_2015.ttl', format='turtle')
outfile.close()



