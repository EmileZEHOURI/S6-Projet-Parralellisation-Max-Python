import networkx as nx
import matplotlib.pyplot as plt

edge_list=[(1,2), (6,3), (2,4), (2,3), (2,4),(3,4)]

edge_list_prece=[(1,2),(3,2),(2,4),(2,5)]

G = nx.Graph() #nonOrienté
G2 = nx.DiGraph() #orienté
# G = nx.MultiGraph() #posibilitéPlusieursArête
# G = nx.MultiDiGraph()

G.add_edges_from(edge_list)




nx.draw_spring(G, with_labels=True)
plt.show()



#nx.draw_circular(G, with_labels=True)
#plt.show()

# nx.draw_shell(G, with_labels=True)
# plt.show()

# nx.draw_spectral(G, with_labels=True)
# plt.show()

# nx.draw_random(G, with_labels=True)
# plt.show()

# nx.draw_planar(G, with_labels=True)
# plt.show()

print(dict(G.degree)[2])