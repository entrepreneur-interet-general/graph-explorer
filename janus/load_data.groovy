

graph = JanusGraphFactory.open('janusgraph.properties')
g = graph.traversal()


new File('data/nodes.csv').eachLine {
  if (!it.startsWith("#")){
    node = it.split(',')
    (entity_id,
    prenom,
    nom,
    date_naissance,
    telephone,
    numero_piece_identite,
    pays,
    pays_code,
    code_postal,
    star) = node 

    g.addV('person')
      .property('entity', entity_id)
      .property('nom', nom)
      .property('prenom', prenom)
      .property('prenomnom', "${prenom} ${nom}")
      .property('date_naissance', date_naissance)
      .property('numero_piece_identite', numero_piece_identite)
      .property('pays_code', pays_code)
      .property('pays', pays)
      .property('code_postal', code_postal)
      .property('star', (star == "true") ? true : false)
      .next()
  }
}

new File('data/links.csv').eachLine {
  if (!it.startsWith("#")){ 
    link = it.split(',')
    (don_entity,
    ben_entity,
    date_operation,
    valeur_euro) = link 
    fromVertex = g.V().has('entity', don_entity).next()
    toVertex = g.V().has('entity', ben_entity).next()
    g.V(fromVertex).addE('sends_money').to(g.V(toVertex))
      .property('date_operation', date_operation)
      .property('valeur_euro', Double.parseDouble(valeur_euro))
      .next()
  }
}


graph.tx().commit()
graph.close()




