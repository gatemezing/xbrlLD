import json
import rdflib
import glob
from rdflib import Literal, BNode, Graph
from string import capitalize
from pprint import pprint
from rdflib.namespace import XSD

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

FCT= rdflib.Namespace("http://data.cdp.net/id/fact/")
ENT = rdflib.Namespace("http://data.cdp.net/id/entity/")
FRPT = rdflib.Namespace("http://data.cdp.net/id/financialreport/")
XBRLL = rdflib.Namespace("http://data.cdp.net/def/xbrll#")
ROV = rdflib.Namespace("http://www.w3.org/ns/regorg#")
VCARD = rdflib.Namespace("http://www.w3.org/2006/vcard/ns#")
FRPT = rdflib.Namespace("http://data.cdp.net/id/financialreport/")

# all the entities ipp-enc and ipp-com from the legacy data
# are all added in the IPPENC namespace below

IPPENC = rdflib.Namespace("http://data.cdp.net/id/skos/ipp/")
IPPSCH = rdflib.Namespace("http://data.cdp.net/id/scheme/ipp")

# here we put legacy es-be-fs and ifrs-gp
IFRSGPS = rdflib.Namespace("http://data.cdp.net/id/scheme/ifrsgp")
IFRSGP = rdflib.Namespace("http://data.cdp.net/id/skos/ifrsgp/")

# here we put legacy dgi-est-gen, dgi-lc-es and dgi-lc-int namespaces
DGI = rdflib.Namespace("http://data.cdp.net/id/skos/dgi/")
DGIS = rdflib.Namespace("http://data.cdp.net/id/scheme/dgi")


OIM = rdflib.Namespace("http://data.cdp.net/def/oim#")



#RDF graphe preparation 
gxbrl = rdflib.ConjunctiveGraph()


# ----- opening the json file --
json_data = open('abanca-report.json')
data = json.load(json_data)

#pprint(data) % for printing the dataset if it's not so huge
facts = data[u'facts']  
prefixes = data[u'prefixes'] 
header = data[u'dtsReferences']

# here I take the code of the entity from the prefixes
# should check if it is always 9 chars
# This helps for metadata information in the dataset
suri = prefixes[u'scheme']
code = suri[-9:]

#print it
#print (len(facts))
#print(prefixes)
f1 = data[u'facts'][0]
idf = f1[u'id']
c = f1[u'oim:concept']

t= c.find(":")
sc = c[t+1:len(c)]
#print sc 
gxbrl.add((FCT[idf], RDF["type"], OIM["TupleFact"]))
gxbrl.add((FCT[idf], SKOS["inScheme"], IPPSCH[""]))
gxbrl.add((FCT[idf], OIM["concept"], IPPENC[sc]))
gxbrl.add((FCT[idf], RDFS["label"], Literal(sc, lang=u'es')))
#gxbrl.add((FCT[idf], OIM["concept"], IPPENC["TupleFact"]))


#f2 = data[u'facts'][1]
#print t 
#print f1, f1[u'id']
#print f2, f2[u'id']

## some useful declarations here

#fentity = Graph()

for i in range(1,len(facts)) :
	tuple = data[u'facts'][i]
	#print(tuple)
	# here we start to generate tuple facts and their "parents"
	for j in tuple:
		if j == u'id':
			v = tuple[j]
			gxbrl.add((FCT[v], RDF["type"], OIM["TupleFact"]))

			sbj1= tuple[u'oim:concept']
			t = sbj1.find(":")
			s = sbj1[t+1:len(sbj1)]
			l = sbj1[0:t]
			#print l
			if l == "dgi-lc-int":
				gxbrl.add((FCT[v], OIM["concept"], DGI[s.lower()]))
				gxbrl.add((FCT[v], RDFS["label"], Literal(s)))
				gxbrl.add((FCT[v], SKOS["inScheme"], DGIS[""]))

			if l == "dgi-est-gen":
				gxbrl.add((FCT[v], OIM["concept"], DGI[s.lower()]))
				gxbrl.add((FCT[v], RDFS["label"], Literal(s)))
				gxbrl.add((FCT[v], SKOS["inScheme"], DGIS[""]))

			if l == "dgi-lc-es":
				gxbrl.add((FCT[v], OIM["concept"], DGI[s.lower()]))
				gxbrl.add((FCT[v], RDFS["label"], Literal(s)))
				gxbrl.add((FCT[v], SKOS["inScheme"], DGIS[""]))

			if l == "dgi-lc-int":
				gxbrl.add((FCT[v], OIM["concept"], DGI[s.lower()]))
				gxbrl.add((FCT[v], RDFS["label"], Literal(s)))
				gxbrl.add((FCT[v], SKOS["inScheme"], DGIS[""]))
			if l == "ipp-com":
				gxbrl.add((FCT[v], OIM["concept"], IPPENC[s.lower()]))
				gxbrl.add((FCT[v], SKOS["inScheme"], IPPSCH[""]))
				gxbrl.add((FCT[v], RDFS["label"], Literal(s)))

			if l == "ipp-enc":
				gxbrl.add((FCT[v], OIM["concept"], IPPENC[s.lower()]))
				gxbrl.add((FCT[v], SKOS["inScheme"], IPPSCH[""]))
				gxbrl.add((FCT[v], RDFS["label"], Literal(s)))

			#gxbrl.add((FCT[v], OIM["concept"], IPPENC[s]))
	


			obj = tuple[u'oim:tupleParent']
			gxbrl.add((FCT[v], OIM["tupleParent"], FCT[obj]))

			od= tuple[u'oim:tupleOrder']
			gxbrl.add((FCT[v], OIM["tupleOrder"], Literal(od)))

		# case j != u'id  - facts

		if j == u'oim:concept': # here for the entity
			w = tuple[j]

			#w1 = w.lower()
			#print w1
			#gxbrl.add((ENT[w1], RDF["type"], XBRLL["FinancialEntity"]))
			#gxbrl.add((ENT[w1], ROV["registration"], Literal(w)))

			#b= tuple[u'oim:concept']
			#a = w.find(":")
			#s1 = w[a+1:len(w)]
			#print s1
			if w == "dgi-est-gen:IdentifierValue":
				b = tuple[u'value']
				gxbrl.add((ENT[b.lower()], RDF["type"], XBRLL["FinancialEntity"]))
				#gxbrl.add((ENT[b.lower()], ROV["legalName"], Literal(s1)))
				gxbrl.add((ENT[b.lower()], ROV["registration"], Literal(b)))

				e = tuple[u'oim:entity']
				a = e.find(":")
				s1 = e[a+1:len(e)]
				gxbrl.add((ENT[b.lower()], ROV["legalName"], Literal(s1)))

		if j == u'baseType':
			r = tuple[j]
			if r == "xs:decimal":
				st = b.lower() + str(i) # code + rang i for creating uris of facts
				gxbrl.add((FCT[st], RDF["type"], OIM["Fact"]))
				d = tuple[u'accuracy']

				# accuracy is replaced by xbrll:decimals
				gxbrl.add((FCT[st], XBRLL["decimals"], Literal(d)))
				e = tuple[u'numericValue']
				gxbrl.add((FCT[st], OIM["value"], Literal(e, datatype=XSD.decimal))) #todo: add decimal datatype
				e1 = tuple[u'oim:unit']
				gxbrl.add((FCT[st], OIM["unitRef"], Literal (e1)))
				e2 = tuple[u'oim:tupleParent']
				gxbrl.add((FCT[st], OIM["tupleParent"], FCT[e2]))

				e3 = BNode() # bNode for the start/end period

				gxbrl.add((FCT[st], OIM["period"], e3))
				e4 = tuple[u'oim:period'][u'start']
				gxbrl.add((e3, OIM["startPeriod"], Literal(e4, datatype=XSD.date)))
				e5 = tuple[u'oim:period'][u'end']
				gxbrl.add((e3, OIM["endPeriod"], Literal(e5, datatype=XSD.date)))

				e6 = tuple[u'oim:concept']
				a1 = e6.find(":")
				s2 = e6[a1+1:len(e6)]
				s3 = e6[0:a1]

				# add uri for the concepts here.. Not a simple task, 
				# since it depends on the different types of existing concepts
				if s3 == "ifrs-gp":
					gxbrl.add((FCT[st], OIM["concept"], IFRSGP[s2.lower()]))
				if s3 == "ipp-enc":
					gxbrl.add((FCT[st], OIM["concept"], IPPENC[s2.lower()]))
				if s3 == "ipp-com":
					gxbrl.add((FCT[st], OIM["concept"], IPPENC[s2.lower()]))

				gxbrl.add((FCT[st], OIM["entity"], ENT[b.lower()])) # link to the entity 

				e7 = tuple[u'oim:tupleOrder']
				gxbrl.add((FCT[st], OIM["tupleOrder"], Literal(e7)))

			if r == "xs:string":
				h = tuple[u'oim:concept']
				h1 = tuple[u'value']

				if h == "dgi-est-gen:AddressLine":  # metadata and financial report
					gxbrl.add((ENT[code.lower()], VCARD["street-address"], Literal(h1)))
					gxbrl.add((FRPT[code.lower()], RDF["type"], XBRLL["FinancialReport"]))
					gxbrl.add((FRPT[code.lower()], DCT["publisher"], ENT[code.lower()]))
					gxbrl.add((FRPT[code.lower()], RDFS["label"], Literal("Financial report", lang=u'en')))
					gxbrl.add((FRPT[code.lower()], RDFS["label"], Literal("Informe financiero", lang=u'es')))

					bn = BNode()

					h2 = tuple[u'oim:period']
					gxbrl.add((FRPT[code.lower()], OIM["period"], bn))
					ps = tuple[u'oim:period'][u'start']
					gxbrl.add((bn, OIM["startPeriod"], Literal(ps, datatype=XSD.date)))
					pe = tuple[u'oim:period'][u'end']
					gxbrl.add((bn, OIM["endPeriod"], Literal(pe, datatype=XSD.date)))

					pass

				if h == "dgi-est-gen:FormattedName":
					v= tuple[u'value']
					bn1 = BNode()
					gxbrl.add((FRPT[code.lower()], XBRLL["contactPerson"], bn1))
					gxbrl.add((bn1, RDF["type"], FOAF["Person"]))
					gxbrl.add((bn1, FOAF["name"], Literal(v)))
					
					pass


				if h == "dgi-est-gen:PositionType":
					v1 = tuple[u'value']
					#bn2 = BNode()
					gxbrl.add((FRPT[code.lower()], XBRLL["contactPerson"], bn1))
					gxbrl.add((bn1, ORG["role"], Literal(v1)))

				if h =="dgi-est-gen:CommunicationValue":
					v2= tuple[u'value']
					v21 = v2.find("@")  # we test only valid email in the string
					if v21 > 0:
						gxbrl.add((FRPT[code.lower()], XBRLL["contactPerson"], bn1))
						gxbrl.add((bn1, SCHEMA["email"], Literal(v2)))



			


json_data.close()


# ----- OUTPUT FILES -----

print "Length of gxbrl : " + str(len(gxbrl))

print "Nb of tuple facts  in dataset : " + str(len(list(gxbrl.triples((None, RDF["type"], OIM["TupleFact"])))))
print "Nb of facts  in dataset : " + str(len(list(gxbrl.triples((None, RDF["type"], OIM["Fact"])))))
print "Nb of financial report in dataset : " + str(len(list(gxbrl.triples((None, RDF["type"], XBRLL["FinancialReport"])))))
outfile = open("gxbrl.rdf", "w")
#outfile.write(gxbrl.serialize())
gxbrl.serialize(destination='gxbrl.ttl', format='turtle')
outfile.close()

"""json file dump
#outfile = open("webint.json", "w")
#outfile.write(json.dumps(webintCourses, sort_keys=True, indent=4))
#outfile.close()
"""
