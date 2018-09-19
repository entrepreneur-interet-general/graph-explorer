
graph = JanusGraphFactory.open('janusgraph.properties') 
mgmt = graph.openManagement() 
instances = mgmt.getOpenInstances()

instances.iterator().findAll {
  !it.contains('current')
}.each { 
  mgmt.forceCloseInstance(it)
}

mgmt.commit()
