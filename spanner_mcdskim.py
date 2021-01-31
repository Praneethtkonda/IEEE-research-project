import itertools as it
import networkx as nx
import math
import time
import networkx.algorithms.approximation as nxaa
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
# Pre- Requisites to be installed a new environment(ANACONDA)

# Initializations

#G = nx.florentine_families_graph()
G = nx.Graph()
G.add_path([0, 1, 2, 3, 4])
'''
G.add_path([1,5,4,3,2,1])
G.add_path([1,6])
G.add_path([5,7])
G.add_path([4,8])
G.add_path([3,9]) 
G.add_path([2,10])
G.add_path([6,9])
G.add_path([6,8])
G.add_path([7,10])
G.add_path([7,9])
G.add_path([8,10])
'''

'''
G.add_path([1,2,3,6,11])
G.add_path([1,2,3,12])
G.add_path([1,2,4,5,3])
G.add_path([4,7,8,9])
G.add_path([4,7,8,10])
G.add_path([6,8])
G.add_path([5,7])
'''
n = G.number_of_nodes()
test = list(G.nodes)
color_map = []  # Assigning color to the nodes
hops = []
whis = []  # Vertex Sets list of lists
I = []
B = []
fin = 0
start_time = 0
finalB = []
# Initialize all the colors of the vertex to white
def colorInitializer():
    i = 0
    while i < n:
        color_map.append('W')
        i+=1
    print(color_map)
# Finds you the root node from the graph and selects the node with the maximum degree
def rootFinder():
    global n
    i = 0
    temp=0
    max = 0
    while i < n:
        if G.degree[test[i]] > max:
            max = G.degree[test[i]]
            temp = i
        i += 1
    return test[temp]
# Gives You the hop distances from root to all other nodes
def hopGiver(root):
    global hops
    i=0
    while i < n:
        hops += [nx.shortest_path_length(G, root, test[i])]
        i += 1

# Generates a list of vertices with particular hops used to generate I for Kmax
def hopEquilizer(value):
    global hops
    temp = []
    i = 0
    while i < n:
        if value == hops[i]:
            temp += [test[i]]
        i+=1
    return temp

def VlistGenerator(kmax):
    global whis
    i=0
    while i <= kmax:
        whis.append(hopEquilizer(i))
        i += 1
    print(whis)
def gen(a):
    # Generate maximal independent set each time for a graph as argument in this function to avoid getting the wrong thing
    Arial = G
    temp = nx.Graph()
    temp = Arial.subgraph(a)
    lis = []
    lis = nx.maximal_independent_set(temp)
    return lis
# Generating I list with union of maximal independent sets of each Ik
def IGenerator(kmax):
    global I
    lis = []
    i = 0
    while i <= kmax:
        lis.clear()
        lis = gen(whis[i])
        I += lis
        i+=2
    I = list(set(I))
    print(I)
# Check if the neighbour list has already black ones if it has Black leave it, otherwise make it GRAY
def makeAdjaGray(neigh):
    global test
    te = []
    for element in neigh:
        te.append(test.index(element))
    i = 0
    while i < len(te):
        color_map[te[i]] = 'G'
        i += 1

def colorInodes():
    global I, color_map,te
    temp = list(G.nodes)
    x = len(I)
    i = 0
    while i < n:
        j=0
        while j<x:
            if I[j] == temp[i]:
                color_map[i] = 'B'
                neigh=nx.neighbors(G,temp[i]) # Returns a Dictonary so need to iterate through each key
                makeAdjaGray(neigh)
            j+=1
        i+=1
    print(color_map)

# If the blacked element consists of any white neighbours we make them Gray
def doCheckExtension(val):
    global test
    neigh = nx.neighbors(G,test[val])
    for element in neigh:
        index = test.index(element)
        if color_map[index] == 'W':
            color_map[index] = 'G'

#Check Whether any white nodes exist in the graph if exists it makes them Black and runs the inner function
def doCheckWhiteNodes():
    global color_map
    i = 0
    while i < len(color_map):
        if color_map[i] == 'W':
            color_map[i] = 'B'
            doCheckExtension(i)
        i+=1
def Blist():
    global color_map,test
    j = 0
    while j < n:
        if color_map[j] == 'B':
            B.append(test[j])
        j += 1
    print(B)

def parentNode(node): # Do check for the root node
    global test,hops,whis
    parents = []
    temp = whis[hops[test.index(node)] - 1]
    j = 0
    while j < len(temp):
        if G.has_edge(node,temp[j]):
            parents.append(temp[j])
        j += 1
    k = 0
    max = 0
    deg = []
    while k < len(parents):
        curr = G.degree(parents[k])
        deg.append(curr)
        if curr > max:
            max = curr
        k += 1
    return parents[deg.index(max)]
def parentNodeTwo(node): # Do check for the root node
    global test,hops,fin,whis
    parents = []
    flag = 0
    count = 0
    temp = whis[hops[test.index(node)] - 1]
    j = 0
    while j < len(temp):
        if G.has_edge(node,temp[j]):
            parents.append(temp[j])
            if (color_map[test.index(temp[j])] == 'B') and (count == 0):
                flag = 1
                count += 1
        j += 1
    if flag == 0:  # That means no black nodes
        k = 0
        max = 0
        deg = []
        while k < len(parents):
            curr = G.degree(parents[k])
            deg.append(curr)
            if curr > max:
                max = curr
            k += 1
        fin =  parents[deg.index(max)]
        return True
    else:  # There is black node
        return False
def Finalloop(istar):
    global B,test,whis
    j = 1
    while j < istar:
        # First Loop
        inde = j * 2
        temp = whis[inde]
        temp = list(set(temp) & set(B))
        i = 0
        while i < len(temp):
            y = parentNode(temp[i])
            z = parentNode(y)
            color_map[test.index(y)] = 'B'
            color_map[test.index(z)] = 'B'
            i += 1

        # Second Loop
        inde1 = (j * 2) - 1
        temp2 = whis[inde1]
        temp2 = list(set(temp2) & set(B))
        h = 0
        while h < len(temp2):
            if parentNode(temp2[i]):  # If there are no black parent nodes color the parent node with highest degree as Black
                color_map[test.index(fin)] = 'B'
            h += 1
        j += 1
def lastStep():
    i = 0
    while i < len(color_map):
        if color_map[i] == 'B':
            finalB.append(test[i])
        i += 1
    print(finalB)
def removeUnwantedEdges():
    temp = list(set(test) - set(finalB))
    ebu = []
    i = 0
    while i < len(temp)-1:
        j = i+1
        while j < len(temp):
            if G.has_edge(temp[i], temp[j]):
                G.remove_edge(temp[i], temp[j])
            j += 1
        i += 1


# CDS with bounded diameter algorithm
def Algo():
    global start_time
    start_time=time.clock()
    print("Number of nodes:")
    print(G.number_of_nodes())
    print("Number of edges:")
    print(G.number_of_edges())
    root = rootFinder()
    hopGiver(root)
    print("This is the hops list: ")
    print(hops)
    kmax = max(hops)
    print("These are the vertices list of lists Eg: [v1, v2,....vkmax]: ")
    VlistGenerator(kmax)
    print("These gives us the I list that is the union of all the independent MIS of each I1,I2.. Ikmax: ")
    IGenerator(kmax)
    print("Initialized color for each vertex:")
    colorInitializer()
    print("Coloring Nodes wrt Nodes in I list: ")
    colorInodes()
    doCheckWhiteNodes()
    print("The Black colored vertices are:")
    Blist()
    istar = math.ceil(kmax/2)
    Finalloop(istar)
    print("The Diameter of the graph:")
    print(nx.diameter(G))
    print("The Minimum Connected Dominating set is:")
    lastStep()
    removeUnwantedEdges()
    nx.draw(G, with_labels=True, node_color='white')
    print("Diameter of the CDS :")
    print(nx.diameter(G))
    pp = PdfPages('finale.pdf')
    pp.savefig()
    pp.close()
    print(G.edges())
Algo()
print (time.clock() - start_time, "seconds")
'''nx.draw(G,with_labels=True)
pp= PdfPages('test.pdf')
pp.savefig()
pp.close()
print(nx.diameter(G))'''
#print(nxaa.min_edge_dominating_set(G))

