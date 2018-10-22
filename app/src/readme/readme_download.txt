Le dossier contient trois fichiers:

* transactions.csv: contient l'ensemble des transactions brutes. 
Ce fichier est utile lorsque l'on veut connaitre le détail des 
transactions entre deux noeuds.  

* noeuds.csv: contient l'ensemble des noeuds du graphe avec leurs
attributs. Un noeud est le regroupement de différents enregistrements 
donneur/benéficiaire. 

* liens.csv: contient les liens du graphe et leurs attributs. 
L'attribut `valeur_euro` est la somme de tous les envois entre
deux noeuds. 

Les fichiers noeuds.csv et liens.csv constitue une représentation 
standard d'un graphe. Ils peuvent être utilisés conjointement pour 
recréer le graphe dans un logiciel tierce (ex: Gephi, Cytoscape, 
Analyst Notebook, etc).