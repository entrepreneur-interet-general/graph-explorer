import org.janusgraph.core.JanusGraphFactory
import org.janusgraph.core.Cardinality
import org.apache.tinkerpop.gremlin.structure.Vertex

// define the schema 
graph = JanusGraphFactory.open('janusgraph.properties')
mgmt = graph.openManagement()

mgmt.makeVertexLabel('person').make()
mgmt.makeEdgeLabel('sends_money').make()

entity = mgmt.makePropertyKey('entity').dataType(String.class).cardinality(Cardinality.SINGLE).make()
prenom = mgmt.makePropertyKey('prenom').dataType(String.class).cardinality(Cardinality.SINGLE).make()
nom = mgmt.makePropertyKey('nom').dataType(String.class).cardinality(Cardinality.SINGLE).make()
prenomnom = mgmt.makePropertyKey('prenomnom').dataType(String.class).cardinality(Cardinality.SINGLE).make()
date_naissance = mgmt.makePropertyKey('date_naissance').dataType(String.class).cardinality(Cardinality.SINGLE).make()
pays_code = mgmt.makePropertyKey('pays_code').dataType(String.class).cardinality(Cardinality.SINGLE).make()
code_postal = mgmt.makePropertyKey('code_postal').dataType(String.class).cardinality(Cardinality.SINGLE).make()
star = mgmt.makePropertyKey('star').dataType(Boolean.class).cardinality(Cardinality.SINGLE).make()
date_operation = mgmt.makePropertyKey('date_operation').dataType(String.class).cardinality(Cardinality.SINGLE).make()
valeur_euro = mgmt.makePropertyKey('valeur_euro').dataType(Double.class).cardinality(Cardinality.SINGLE).make()
degree = mgmt.makePropertyKey('degree').dataType(Integer.class).cardinality(Cardinality.SINGLE).make()
in_degree_weighted = mgmt.makePropertyKey('in_degree_weighted').dataType(Double.class).cardinality(Cardinality.SINGLE).make()
out_degree_weighted = mgmt.makePropertyKey('out_degree_weighted').dataType(Double.class).cardinality(Cardinality.SINGLE).make()

mgmt.buildIndex('vertexByPrenomNom', Vertex.class).addKey(mgmt.getPropertyKey('prenomnom')).buildMixedIndex('search')
mgmt.buildIndex('vertexByEntity', Vertex.class).addKey(entity).buildCompositeIndex()
mgmt.commit()

graph.close()
