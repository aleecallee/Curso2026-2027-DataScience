from rdflib import Graph, Namespace
from rdflib.namespace import RDF, RDFS
from oeg_sw_class import Report

github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2026-2027-Datascience/refs/heads/master/Assignment4/course_materials"
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.parse(github_storage + "/rdf/data07.ttl", format="turtle")
report = Report()

#task 7.1.a
result = [(cls, parent) for cls in g.subjects(RDF.type, RDFS.Class)
          for parent in (list(g.objects(cls, RDFS.subClassOf)) or [None])]
for item in result:
    print(item)
report.validate_07_1a(result)

#task 7.1b
query = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?c ?sc
WHERE {
    ?c a rdfs:Class .
    OPTIONAL { ?c rdfs:subClassOf ?sc }
}
"""
for row in g.query(query):
    print(row.c, row.sc)
report.validate_07_1b(query, g)

#task 7.2a
ns = Namespace("http://oeg.fi.upm.es/def/people#")
classes = {ns.Person}
frontier = [ns.Person]
while frontier:
    parent = frontier.pop()
    for child in g.subjects(RDFS.subClassOf, parent):
        if child not in classes:
            classes.add(child)
            frontier.append(child)
individuals = list({subject for cls in classes for subject in g.subjects(RDF.type, cls)})
for individual in individuals:
    print(individual)
report.validate_07_02a(individuals)

#task 7.2b
query = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX people: <http://oeg.fi.upm.es/def/people#>
SELECT DISTINCT ?ind
WHERE {
    ?ind a ?class .
    ?class rdfs:subClassOf* people:Person .
}
"""
for row in g.query(query):
    print(row.ind)
report.validate_07_02b(g, query)

#task 7.3
query = """
PREFIX people: <http://oeg.fi.upm.es/def/people#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT DISTINCT ?name ?type
WHERE {
    ?someone people:knows people:Curry ;
             rdfs:label ?name ;
             rdf:type ?type .
}
"""
for row in g.query(query):
    print(row.name, row.type)
report.validate_07_03(g, query)

#task 7.4
query = """
PREFIX people: <http://oeg.fi.upm.es/def/people#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT DISTINCT ?name
WHERE {
    ?entity rdfs:label ?name ;
            people:hasColleague/people:hasColleague? ?colleague .
    ?colleague people:ownsPet ?dog .
    ?dog a people:Animal .
}
"""
for row in g.query(query):
    print(row.name)
report.validate_07_04(g, query)
report.save_report("_Task_07")
