import json
import rdflib
import glob
from rdflib import Literal, BNode, Graph
from string import capitalize
from pprint import pprint
from rdflib.namespace import XSD
import re


## Author: @gatemezing ##
## This script is intended to transform XBRL data in JSON to RDF ##
## It is compatible with Python 2.7 ####
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
TPLE = rdflib.Namespace("http://data.mondeca.com/id/tuple/")
SCEN = rdflib.Namespace("http://data.mondeca.com/id/scenario/")
DIM = rdflib.Namespace("http://data.mondeca.com/id/dimension/")
PERS = rdflib.Namespace("http://data.mondeca.com/id/xbrl/person/")
ENT = rdflib.Namespace("http://data.mondeca.com/id/entity/")
XBRLL = rdflib.Namespace("https://w3id.org/vocab/xbrll#")
ROV = rdflib.Namespace("http://www.w3.org/ns/regorg#")
VCARD = rdflib.Namespace("http://www.w3.org/2006/vcard/ns#")
FRPT = rdflib.Namespace("http://data.mondeca.com/id/report/")
DBR = rdflib.Namespace("http://dbpedia.org/resource/")



# Namespaces declaration
# are all added in the IPPENC namespace below
IPP = rdflib.Namespace("http://www.cnmv.es/ipp/taxonomia/2008-01-01/ipp-gen-2008-01-01/")
#IPPENC = rdflib.Namespace("http://data.mondeca.com/id/skos/ipp/")
IPPSCH = rdflib.Namespace("http://data.mondeca.com/id/scheme/ipp")

# Here in the case of using the IPP namespaces in the XBRL scheme
IPPCOM = rdflib.Namespace("http://www.cnmv.es/ipp/com/1-2008/2008-01-01/") 
IPPGEN = rdflib.Namespace("http://www.cnmv.es/ipp/gen/1-2008/2008-01-01/")

# here we put legacy es-be-fs and ifrs-gp
IFRSGPS = rdflib.Namespace("http://data.mondeca.com/id/scheme/ifrsgp")
IFRSGP = rdflib.Namespace("http://xbrl.iasb.org/int/fr/ifrs/gp/2005-05-15/")
ESBEFS = rdflib.Namespace("http://www.bde.es/es/fr/ifrs/basi/bde/4-2004/2006-01-01/")

# here we put legacy dgi-est-gen, dgi-lc-es and dgi-lc-int namespaces
DGI = rdflib.Namespace("http://www.xbrl.org.es/es/2007/dgi/gp/est-gen/2007-05-30/")
DGILCINT = rdflib.Namespace("http://www.xbrl.org.es/es/2007/dgi/gp/lc-int/2007-05-30/")
DGILCES = rdflib.Namespace("http://www.xbrl.org.es/es/2007/dgi/gp/lc-es/2007-05-30/")
DGIS = rdflib.Namespace("http://data.mondeca.com/id/scheme/dgi")


#RDF graphe preparation 
gxbrl = rdflib.ConjunctiveGraph()


# ----- opening the json file --
json_data = open('/Users/gatemezing/Dropbox/Ghislain - Maria/01. Data/03. SPARQL data/CNMV_2013.json')
data = json.load(json_data)

#pprint(data) % for printing the dataset if it's not so huge
facts = data[u'facts']  
prefixes = data[u'prefixes'] 
header = data[u'dtsReferences']

# here I take the code of the entity from the prefixes
# should check if it is always 9 chars
# This helps for metadata information in the dataset
#TODO: implement strafter the last /
suri = prefixes[u'scheme']
code = suri[-10:]

#print it
#print (len(facts))
#print(prefixes)
f1 = data[u'facts'][0]
idf = f1[u'id']
c = f1[u'oim:concept']

t= c.find(":")
sc = c[t+1:len(c)]
#time to split camalcase string 
splitsc = re.sub('(?!^)([A-Z][a-z0-9]+)', r' \1', sc).split()
sclabel = " ".join(splitsc)

gxbrl.add((TPLE[idf], RDF["type"], XBRLL["Tuple"]))
gxbrl.add((TPLE[idf], SKOS["inScheme"], IPPSCH[""]))
gxbrl.add((TPLE[idf], XBRLL["concept"], IPP[sc]))
gxbrl.add((TPLE[idf], RDFS["label"], Literal(sclabel)))
#gxbrl.add((TPLE[idf], XBRLL["hasTuple"], IPPENC["TupleFact"]))


#f2 = data[u'facts'][1]
#print t 
#print f1, f1[u'id']
#print f2, f2[u'id']

## some useful declarations here
bn1 = BNode()
bn2 = BNode()
v3 = ""

#fentity = Graph()


for i in range(1,len(facts)) :
	tuple = data[u'facts'][i]
	#print(tuple)
	# here we start to generate facts  and their "parents"
	for j in tuple:
		if j == u'id':
			v = tuple[j]
			gxbrl.add((TPLE[v], RDF["type"], XBRLL["Tuple"]))

			sbj1= tuple[u'oim:concept']
			t = sbj1.find(":")
			s = sbj1[t+1:len(sbj1)]
			# spliting s to have labels 
			splits = re.sub('(?!^)([A-Z][a-z0-9]+)', r' \1', s).split()
			slabel = " ".join(splits)
			l = sbj1[0:t]
			#print l
			if l == "dgi-lc-int":
				gxbrl.add((TPLE[v], XBRLL["concept"], DGILCINT[s]))
				gxbrl.add((TPLE[v], RDFS["label"], Literal(slabel)))
				gxbrl.add((TPLE[v], SKOS["inScheme"], DGIS[""]))

			if l == "dgi-est-gen":
				gxbrl.add((TPLE[v], XBRLL["concept"], DGI[s]))
				gxbrl.add((TPLE[v], RDFS["label"], Literal(slabel)))
				gxbrl.add((TPLE[v], SKOS["inScheme"], DGIS[""]))

			if l == "dgi-lc-es":
				gxbrl.add((TPLE[v], XBRLL["concept"], DGILCES[s]))
				gxbrl.add((TPLE[v], RDFS["label"], Literal(slabel)))
				gxbrl.add((TPLE[v], SKOS["inScheme"], DGIS[""]))

			#if l == "dgi-lc-int":
			#	gxbrl.add((TPLE[v], XBRLL["concept"], DGI[s]))
			#	gxbrl.add((TPLE[v], RDFS["label"], Literal(slabel)))
			#	gxbrl.add((TPLE[v], SKOS["inScheme"], DGIS[""]))
			if l == "ipp-com":
				gxbrl.add((TPLE[v], XBRLL["concept"], IPPCOM[s]))
				gxbrl.add((TPLE[v], SKOS["inScheme"], IPPSCH[""]))
				gxbrl.add((TPLE[v], RDFS["label"], Literal(slabel)))

			if l == "ipp-enc":
				gxbrl.add((TPLE[v], XBRLL["concept"], IPP[s]))
				gxbrl.add((TPLE[v], SKOS["inScheme"], IPPSCH[""]))
				gxbrl.add((TPLE[v], RDFS["label"], Literal(slabel)))

			if l == "ipp-gen":
				gxbrl.add((TPLE[v], XBRLL["concept"], IPPGEN[s]))
				gxbrl.add((TPLE[v], SKOS["inScheme"], IPPSCH[""]))
				gxbrl.add((TPLE[v], RDFS["label"], Literal(slabel)))

			#gxbrl.add((TPLE[v], XBRLL["concept"], IPP[s]))
	


			obj = tuple[u'oim:tupleParent']
			gxbrl.add((FCT[v], XBRLL["hasTuple"], TPLE[obj]))

			#od= tuple[u'oim:tupleOrder']
			#gxbrl.add((FCT[v], xbrll["tupleOrder"], Literal(od)))

		# case j != u'id  - facts

		if j == u'oim:concept': # here for the entity
			w = tuple[j]

			
			if w == "dgi-est-gen:IdentifierValue":
				b = tuple[u'value']
				if code == b:

					cif = "CIF-" + b  #CIF + code for Spanish if not just use b in registration
					gxbrl.add((ENT[b], RDF["type"], XBRLL["Entity"]))  # use of the more generic Entity
					gxbrl.add((ENT[b], ROV["registration"], Literal(cif)))
					e = tuple[u'oim:entity']
					a = e.find(":")
					s1 = e[a+1:len(e)]
					gxbrl.add((ENT[b], ROV["legalName"], Literal(s1)))

		if j == u'baseType':
			r = tuple[j]
			if r == "xs:decimal":
				#st = b + str(i) # code + rang i for creating uris of facts
				b1 = b.find("-")
				b2 = b[b1+1:len(b)]
				st = "f"+ b2 + str(i) # f + partofEntity + rang i
				

				gxbrl.add((FCT[st], RDF["type"], XBRLL["Fact"]))
				d = tuple[u'accuracy']

				# accuracy is replaced by xbrll:decimals
				gxbrl.add((FCT[st], XBRLL["decimals"], Literal(d)))
				e = tuple[u'numericValue']
				gxbrl.add((FCT[st], XBRLL["value"], Literal(e, datatype=XSD.decimal))) #todo: add decimal datatype
				e1 = tuple[u'oim:unit']
				tm = e1.find(":")
				tm1 = e1[tm+1:len(e1)]
				gxbrl.add((FCT[st], XBRLL["unitRef"], DBR[tm1])) #added code currency from DBpedia
				e2 = tuple[u'oim:tupleParent']
				gxbrl.add((FCT[st], XBRLL["hasTuple"], TPLE[e2]))

				e3 = BNode() # bNode for the start/end period

				gxbrl.add((FCT[st], XBRLL["period"], e3))
				e4 = tuple[u'oim:period'][u'start']
				gxbrl.add((e3, XBRLL["startPeriod"], Literal(e4, datatype=XSD.date)))
				e5 = tuple[u'oim:period'][u'end']
				gxbrl.add((e3, XBRLL["endPeriod"], Literal(e5, datatype=XSD.date)))

				e6 = tuple[u'oim:concept']
				a1 = e6.find(":")
				s2 = e6[a1+1:len(e6)]
				s3 = e6[0:a1]

				# add uri for the concepts here.. Not a simple task, 
				# since it depends on the different types of existing concepts
				if s3 == "ifrs-gp":
					gxbrl.add((FCT[st], XBRLL["concept"], IFRSGP[s2]))
				if s3 == "ipp-enc":
					gxbrl.add((FCT[st], XBRLL["concept"], IPP[s2]))
				if s3 == "ipp-com":
					gxbrl.add((FCT[st], XBRLL["concept"], IPPCOM[s2]))
				if s3 == "ipp-gen":
					gxbrl.add((FCT[st], XBRLL["concept"], IPPGEN[s2]))

				gxbrl.add((FCT[st], XBRLL["hasEntity"], ENT[b])) # link to the entity 

				#e7 = tuple[u'oim:tupleOrder']
				#gxbrl.add((FCT[st], OIM["tupleOrder"], Literal(e7)))

			if r == "xs:string":
				h = tuple[u'oim:concept']
				h1 = tuple[u'value']

				if h == "dgi-est-gen:AddressLine":  # metadata and  report
					gxbrl.add((ENT[code], VCARD["street-address"], Literal(h1)))
					gxbrl.add((FRPT[code], RDF["type"], XBRLL["Report"])) # more generic report used
					gxbrl.add((FRPT[code], DCT["publisher"], ENT[code]))
					gxbrl.add((FRPT[code], RDFS["label"], Literal("Report", lang=u'en'))) #more generic
					gxbrl.add((FRPT[code], RDFS["label"], Literal("Informe ", lang=u'es')))

					bn = BNode()

					h2 = tuple[u'oim:period']
					gxbrl.add((FRPT[code], XBRLL["period"], bn))
					ps = tuple[u'oim:period'][u'start']
					gxbrl.add((bn, XBRLL["startPeriod"], Literal(ps, datatype=XSD.date)))
					pe = tuple[u'oim:period'][u'end']
					gxbrl.add((bn, XBRLL["endPeriod"], Literal(pe, datatype=XSD.date)))

					pass

				#create an URI for person entity

				
				if h =="dgi-est-gen:IdentifierValue":
					v3 = tuple[u'value']
					if len(v3) > 0:

						gxbrl.add((FRPT[code], XBRLL["contactPerson"], PERS[v3]))
						gxbrl.add((PERS[v3], RDF["type"], FOAF["Person"]))
						gxbrl.add((PERS[v3], DCT["identifier"], Literal(v3)))

						pass


				if h =="dgi-lc-es:Xcode_IDC.CIF":
					v4 = tuple[u'value']
					if len(v3) > 0:
						gxbrl.add((FRPT[code], XBRLL["contactPerson"], PERS[v3]))
						gxbrl.add((PERS[v3], XBRLL["codeID"], Literal(v4)))




				if h == "dgi-est-gen:FormattedName":
					v= tuple[u'value']
					gxbrl.add((FRPT[code], XBRLL["contactPerson"], PERS[v3]))
					gxbrl.add((PERS[v3], FOAF["name"], Literal(v)))
					
					pass


				if h == "dgi-est-gen:PositionType":
					v1 = tuple[u'value']
					gxbrl.add((PERS[v3], ORG["role"], Literal(v1)))

					pass

				if h =="dgi-est-gen:CommunicationValue":
					v2= tuple[u'value']
					v21 = v2.find("@")  # we test only valid email in the string
					if v21 > 0:
						gxbrl.add((PERS[v3], SCHEMA["email"], Literal(v2)))

					pass 
				
				

				
				





			


json_data.close()


# ----- OUTPUT FILES -----

print "Length of gxbrl : " + str(len(gxbrl))

print "Nb of tuple facts  in dataset : " + str(len(list(gxbrl.triples((None, RDF["type"], XBRLL["Tuple"])))))
print "Nb of facts  in dataset : " + str(len(list(gxbrl.triples((None, RDF["type"], XBRLL["Fact"])))))
print "Nb of report in dataset : " + str(len(list(gxbrl.triples((None, RDF["type"], XBRLL["Report"])))))
outfile = open("/Users/gatemezing/Dropbox/Ghislain - Maria/01. Data/03. SPARQL data/CNMV_2013.rdf", "w")
#outfile.write(gxbrl.serialize())
gxbrl.serialize(destination='/Users/gatemezing/Dropbox/Ghislain - Maria/01. Data/03. SPARQL data/CNMV_2013.ttl', format='turtle')
outfile.close()

"""json file dump
#outfile = open("webint.json", "w")
#outfile.write(json.dumps(webintCourses, sort_keys=True, indent=4))
#outfile.close()
"""
