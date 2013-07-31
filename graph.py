import sys,os,copy,pdb
import networkx as nx

def match_graphs(nh,H,ng,G):
	"""Determines whether the node nh in H can be matched with the node ng in G, i.e. if ng is a distractor of nh."""
#	if ng doesn't have the same loops as nh, it can't be a match
#	print "matching node",nh,"in H to node",ng,"in G"
	for n in H[nh]:	
		if n==nh:
			for e in H[nh][n]:
				if H[nh][n][e] not in G[ng][ng].values():
					return False
#	if ng does have the same loops as nh, all other edges and nodes in H have to be matched to edges and nodes in G				
	H_neighbours = get_neighbour_nodes(nh,H)
#	print H.edges(data=True)
	ToBeMatched = zip(H_neighbours,[nh]*len(H_neighbours)) # the list of neighbour nodes to be matched, each in a pair with its neighbour that just got matched
	mapping = {nh:ng}		
	return match_helper(mapping,ToBeMatched,H,G)

def match_helper(mapping,ToBeMatched,H,G):
#	if all nodes in H have been mapped
	if len(mapping.keys()) == len(H.nodes()):
		return True
#	if no mapping has been found yet, but there are no more nodes to be matched
	if len(ToBeMatched) == 0:
		return False
#	choose a new, unmatched y from ToBeMatched 
## 	choose the first one to make sure that nodes closer to the intended referent are mentioned before nodes further away (i.e. avoid strings of relations)
	y = ToBeMatched[0][0]
	introducer = ToBeMatched[0][1]
#	get candidate matches for y in G (G-nodes that are neighbours of the mapping of the H-node that introduced y to ToBeMatched (introducer) and are not in the mapping yet)
	Candidates = get_neighbour_nodes(mapping[introducer],G)
	for z in Candidates:	
#		check if all edges starting or ending at y in H also hold for z in G and if the other node in the edge is consistent with the mapping
		yz_match = True
		for e in H.edges(data=True):
			e_data = e[2]
#			if e starts at y
			if y == e[0]:
				other_node = e[1]
#				if the other node in e is already matched
				if other_node in mapping:
					other_match = mapping[other_node]
#					if there is no edge in G from z to the other node's match that has e_data
					if (z,other_match,e_data) not in G.edges(data=True):
						yz_match = False
#				if the other node in e is not yet matched
				else:
					yz_match = False
#					unless there is an edge in G starting at z, ending in an unmatched node and with e_data:
					for f in G.edges(data=True):
						if f[0] == z and f[1] not in mapping.values() and f[2] == e_data:
							yz_match = True
#			if e ends in y
			if y == e[1]:
				other_node = e[0]
#				if the other node in e is already matched
				if other_node in mapping:
					other_match = mapping[other_node]
#					if there is no edge in G from the other node's match to z that has e_data
					if (other_match,z,e_data) not in G.edges(data=True):
						yz_match = False
#				is the other node in e is not yet matched
				else:
					yz_match = False
#					unless there is an edge in G ending in z, starting at an unmatched node and with e_data:
					for f in G.edges(data=True):
						if f[1] == z and f[0] not in mapping.values() and f[2] == e_data:
							yz_match = True
						
		if yz_match:
#			extend the mapping with y->z	
			mapping[y] = z
#			print "old ToBeMatched", ToBeMatched
#			remove y from ToBeMatched
			del ToBeMatched[0]
#			add y's neighbours (in a pair with y to record the introducing node) to ToBeMatched
#			print "y",y
			all_y_neighbours = get_neighbour_nodes(y,H)
#			I think I have to remove those nodes from y-neighbours that are already in mapping
			y_neighbours = []
			for x in all_y_neighbours:
				if x not in mapping:
					y_neighbours.append(x)
			
#			print "new y_neighbours", y_neighbours
			ToBeMatched.extend(zip(y_neighbours,[y]*len(y_neighbours)))
#			print "new ToBeMatched", ToBeMatched
#			check if the remaining nodes in HNS (neighbours of the orignal node in H) can be matched to someting in G		
			return match_helper(mapping,ToBeMatched,H,G)
	return False					


def get_neighbour_nodes(n,G):
	"""Given a node n and a graph G, returns all neighbour nodes of n in G."""
	N = []
	for e in G.edges():
		n2 = None
		if n == e[0]:
			n2 = e[1]
		elif n == e[1]:
			n2 = e[0]
		if n2 and n2 != n and not n2 in N:
			N.append(n2)
	return N


def get_new_neighbour_edges(G,H,n):
	"""Given a graph G a subgraph H of G, and a node n in H and G, returns n's edges in G that are not yet in H.
	each edge is a tuple containing the two nodes it connects and the dictionary with the edge data."""

	E = []
	for e in G.edges(data=True):
		if e[0] == n: # or e[1] == n:
			if not e in H.edges(data=True):
				E.append(e)
	return E


def preferred(p1,p2,PO):
	"""Determines whether p1 is preferred over p2 according to the preference order PO"""
	for p in [p1,p2]:
		if p not in PO:
			print "\nERROR! Property", p, "was not found in the preference order file.\n"
			sys.exit()
	for p in PO:
		if p == p1:
			return True
		if p == p2:
			return False			
	

def order_edges(E,PO):
	"""Returns the list of edges E ordered according to the preference order PO."""
	ordered = [E[0]]
	del E[0]
	while E:
		inserted = False
		for e in ordered:
			if preferred(E[0][2]["att"]+"."+E[0][2]["val"],e[2]["att"]+"."+e[2]["val"],PO):
				ordered.insert(ordered.index(e),E[0])
				inserted = True
				break
		if not inserted:
			ordered.append(E[0])
		del E[0]
	return ordered

def get_graph_cost(G):
	"""returns the cost of the graph G as the sum of the costs of all edges in it."""

	if G:
		c = 0.0
	#	for n in G.nodes_iter():
	#		c += G[n]["cost"] # nx nodes seem not be allowed to have a cost. Hm... might be useful for defining an object's salience
		for e in G.edges_iter(data=True):
			c += e[2]["cost"]	
		return c
	else: return 100000

reciprocal = {"below":"on-top-of","on-top-of":"below","in-front-of":"behind","behind":"in-front-of","left-of":"right-of","right-of":"left-of",
			"northeast":"southwest","southwest":"northeast","southeast":"northwest","northwest":"southeast","in":"have","have":"in","near-to":"near-to"}
def rec_already_in(e,H):
	if (e[1],e[0],{'att':'rel_location','cost':e[2]['cost'],'val':reciprocal[e[2]['val']]}) in H.edges(data=True):
		return True
	else: return False	

#	print e
##	print H.edges(data=True)
#	if ('obj3', 'tg', {'att': 'rel_location', 'cost': 0.0, 'val': 'left-of'}) in [('obj3', 'tg', {'att': 'rel_location', 'cost': 0.0, 'val': 'left-of'})]:
#		print "yes"
	
			
#graphs_found = 0

def find_RE_Graph(targetid,bestG,H,G,PO,edges_to_try,maxlen):
	"""Returns the first found longest cheapest subgraph of G that fully distinguishes the target from all other objects in the scene up to a maximum length."""
	
#	if the cost of the current graph is bigger than that of bestG, abandon the current graph
	bestcost = get_graph_cost(bestG)
	if bestG and (bestcost < get_graph_cost(H) or len(H.edges()) > int(maxlen)):
		return bestG
#	find the set D of distractor nodes that the current graph H could also describe
	D = []
#	print H.edges()	
	for n in (x for x in G.nodes() if x != targetid):
		if match_graphs(targetid,H,n,G):
			D.append(n)
#	if no distractors are left, and (H is cheaper than bestG or (they're equal and H is longer)) return H
	if len(D) == 0 and (bestcost > get_graph_cost(H) or (bestcost == get_graph_cost(H) and len(H.edges()) > len(bestG.edges()))):
		return H			
#	otherwise try adding more edges	in order of preference
	for e in edges_to_try:
#		unless this is a relation and the reciprocal relation is already in H
		if not (e[0] != e[1] and rec_already_in(e,H)):
#			add e to (a new copy of) H (so that we can try extending H with other edges later)
			new_H = copy.deepcopy(H)
			new_H.add_edge(e[0],e[1],attr_dict=e[2])
			new_edges_to_try = copy.deepcopy(edges_to_try)
#			if the new edge introduces a new node, add the *new* edges of the new node to the edges_to_try list
			if e[0] != e[1] and e[1] not in H.nodes():	
				new_edges_to_try.extend(order_edges(get_new_neighbour_edges(G,H,e[1]),PO))	
#			remove the new edge from the edges_to_try_list
			new_edges_to_try.remove(e)
#			find the best graph including all the edges chosen so far
			I = find_RE_Graph(targetid,bestG,new_H,G,PO,new_edges_to_try,maxlen)
#			if this is the first distinguishing graph found so far OR the new graph is cheaper than the best graph so far OR it is equally cheap AND HAS MORE EDGES, it becomes the new best graph
			if not bestG or get_graph_cost(I) < bestcost or (get_graph_cost(I) == bestcost and len(I.edges()) > len(bestG.edges())):
				bestG = I
	return bestG


def add_type_for_all(RE,G):
	"""Adds the "type" attribute to each object in the referring graph RE."""
	for n in RE:	
		RE_has_type = False
		if n in RE[n]:
			for e in RE[n][n]:
				if RE[n][n][e]["att"] == "type":
					RE_has_type = True
		if not RE_has_type:
			for e in G[n][n]:
				if G[n][n][e]["att"] == "type":
					type_data = G[n][n][e]
			RE.add_edge(n,n,att=type_data["att"],val=type_data["val"],cost=type_data["cost"])	

def add_target_type(RE,G,targetid):
	"""Adds the "type" attribute to each object in the referring graph RE."""
	for n in RE:
		RE_has_target_type = False
		if n == targetid and n in RE[n]:
			for e in RE[n][n]:
				if RE[n][n][e]["att"] == "type":
					RE_has_target_type = True
			if not RE_has_target_type:
				for e in G[n][n]:
					if G[n][n][e]["att"] == "type":
						type_data = G[n][n][e]
				RE.add_edge(n,n,att=type_data["att"],val=type_data["val"],cost=type_data["cost"])

def scenedict_to_graph(scenedict,Costs):
	"""Turns the standard input format (JSON) into a networkx.MultiDiGraph (a directed multigraph)"""
	G = nx.MultiDiGraph()
	for n in scenedict:
		G.add_node(n)
		for att in scenedict[n]:
			if not scenedict[n][att] in scenedict.keys():
				try:
					G.add_edge(n,n,att=att,val=scenedict[n][att],cost=Costs[att][scenedict[n][att]])
				except KeyError: 
					print "\n ERROR: Property <"+att+","+scenedict[n][att]+"> not found in cost function file.\n"
					sys.exit()
			else:
				try:
					G.add_edge(n,scenedict[n][att],att="rel_location",val=att,cost=Costs["rel_location"][att])
				except KeyError: 
					print "\n ERROR: Property <relation,"+scenedict[n][att]+"> not found in cost function file.\n"
					sys.exit()
	return G

def scenedict_to_graph_version2(scenedict,Costs):
	"""Turns the standard input format (JSON) into a networkx.MultiDiGraph (a directed multigraph)"""
	G = nx.MultiDiGraph()
	for n in scenedict:
		G.add_node(n)
		for att in scenedict[n]:
			for element in scenedict[n][att]:
				if not element in scenedict.keys():
					try:
						G.add_edge(n,n,att=att,val=element,cost=Costs[att][element])
					except KeyError: 
						print "\n ERROR: Property <"+att+","+element+"> not found in cost function file.\n"
						sys.exit()
				else:
					try:
						G.add_edge(n,element,att="rel_location",val=att,cost=Costs["rel_location"][att])
					except KeyError: 
						print "\n ERROR: Property <relation,"+element+"> not found in cost function file.\n"
						sys.exit()
	return G

def make_short_RE(RE):
	"""Takes a list of edge triples, such as returned by the nx.MultiDiGraph.edges(data=True) method of a nx graph, and
	returns a list of (entity,attribute,value) triples."""

	short_RE = []
	for e in RE:
		if e[0] == e[1]:
			short_RE.append((e[0],e[2]["att"],e[2]["val"]))
		else:
			short_RE.append((e[0],e[2]["val"],e[1]))
	return short_RE
	

def main(args):	
	if len(args) != 7:
		print "\nWrong number of arguments!\n"
		print "Usage: python",args[0],"input targetid prefcostfile outfolder force-type maxlen\n"
		print "Example: python",args[0],'../input/GRE3D7-2 tg ../PrefAndCosts.txt ../data/output/ yes 4OR:'
		print "Example: python",args[0],'../input/ tg ../PrefAndCosts.txt ../data/output/ yes 4\n'
		print '"input" can be a single scenefile or a directory of scenefiles.\n'
		print 'With the "force-type" parameter you can specify whether the "type" attribute should always be added for all objects mentioned in the description. Use "yes" or "no".\n'
		sys.exit()

	input_para = args[1] # a text file (or a folder containing a number of text files) containing a scene in json format. This is equivalent to a Python disctionary. Each key of the dictionary is the id for an object and its value is another dictionary specifying the attribute-value pairs for this object
	targetid = args[2] # a string specifying the id of the object in scenefile which should be described
	prefcostfile = open(args[3],"r") # a txt file listing attribute value pairs in the order of preference and with their associated costs
	outfolder = args[4] # the path to the folder where the output files should be saved
	force_type = args[5] # "yes" or "no"
	maxlen = args[6] # an integer
	
	if not os.path.exists(input_para):
		print "\nERROR! Input file or folder not found!\n"
		sys.exit()
	if not os.path.exists(outfolder):
		os.makedirs(outfolder)
	
	PO = []
	Costs = {}
	for line in prefcostfile.readlines():
		if line != "\n":
			listed = line.split('\t')
			if not listed[0] in Costs:
				Costs[listed[0]] = {}
			Costs[listed[0]][listed[1]] = float(listed[2])
			PO.append(listed[0]+"."+listed[1])

	scenelist = []
	if os.path.isfile(input_para):
		scenelist.append(input_para)	
	elif os.path.isdir(input_para):
		for file in os.listdir(input_para):
			scenelist.append(os.path.join(input_para,file))	

	for scene in scenelist:
		H = nx.MultiDiGraph()
		H.add_node(targetid) # the initial description graph containing only the target node

		scenefile = open(scene,"r")	
		scenedict = eval(scenefile.read())
		scenefile.close()
		G = scenedict_to_graph_version2(scenedict,Costs) # the domain (aka scene) graph
			
		bestG = None
		
		edges_to_try = order_edges(get_new_neighbour_edges(G,H,targetid),PO)	
		
		RE = find_RE_Graph(targetid,bestG,H,G,PO,edges_to_try,maxlen)

#		ALWAYS ADD TYPE?
		if force_type == "all" or force_type == "a":
			add_type_for_all(RE,G)
		elif force_type == "target" or force_type =="t":
			add_target_type(RE,G,targetid)
		elif force_type == "none" or force_type =="n":
			pass
		else:
			print '\nPlease use "all", "none", OR "target" to specify whether type should be force-added for all objects, no objects, or only the target. (the last paramter)\n'
			sys.exit()
		
		outfile = open(os.path.join(outfolder,os.path.split(scene)[1]),"w")
		outfile.write(str(make_short_RE(RE.edges(data=True))))
		outfile.close()
