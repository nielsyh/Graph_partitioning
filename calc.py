import struct
import random
import networkx as nx
# import matplotlib.pyplot as plt

def read_file(file):
    g = nx.Graph()

    with open(file, 'rb') as inh:
        data = inh.read()
    for i in range(0, len(data), 8):
        edge_0 = struct.unpack('i', data[i:i+4])[0]
        edge_1 = struct.unpack('i', data[i+4:i+8])[0]

        # print(edge_0,edge_1)

        g.add_node(edge_0)
        g.add_node(edge_1)
        g.add_edge(edge_0,edge_1)


    # nx.draw(g,with_labels=True)
    # plt.show()
    print('file read done...')
    return g

def edge_cut(k,g, output):
    partitions = []
    for i in range(k):
        tmp = nx.Graph()
        partitions.append(tmp)

    vertex_list = list(g.nodes())
    random.shuffle(vertex_list)
    
    #divide nodes to partitions evenly
    while(len(vertex_list) > 0):

        #some monitoring, because its slow..
        l = len(vertex_list)
        if(l % 10000 == 0):
            print('len: ', str(l))

        for i in partitions:
            if(len(vertex_list) > 0):

                #random node
                rnd = vertex_list[-1]
                i.add_node(rnd)

                #added random node, now add its edges to neighbors in original graph. 
                
                n = list(g.neighbors(rnd))

                for neig in n:
                    if(i.has_node(neig)):
                        i.add_edge(neig,rnd)

                #TODO to time consuming...
                # current_nodes = list(i.nodes())
                # max = len(current_nodes)
                # added = 0
                # for u in current_nodes:
                #     if(added == max):
                #         continue
                #     if(g.has_edge(u,rnd)):
                #         i.add_edge(u, rnd)
                #         added += 1

                del vertex_list[-1]

    #add copy neighbors and save results
    for i in partitions:

        normal_edges = len(i.edges())
        nodes = list(i.nodes())
        
        print('partition: ' + str(partitions.index(i)))
        output.write('partition: ' + str(partitions.index(i))+ '\n')
        print('master vertices: ', str(len(nodes)))
        # print(i.nodes())
        output.write(str(len(nodes))+ '\n')
        
        for v in nodes:
            n = list(g.neighbors(v))
            i.add_nodes_from(n)

            for w in n:
                i.add_edge(v,w)


        print('total vertices: ', str(len(list(i.nodes))))
        # print(i.nodes())
        output.write(str(len(list(i.nodes)))+ '\n')

        print('number of replicated edges in this partition: ', str(len(i.edges()) - normal_edges))
        output.write(str(len(i.edges()) - normal_edges)+ '\n')

        print('number of edges in this partition: ', str(len(i.edges())))
        output.write(str(len(i.edges()))+ '\n')
        

                
        


        # <number of master vertices> 
    # <number of total vertices (include master and mirror vertices)> 
    # <number of edges in this partition>
def vertex_cut(k,g, output):

    master  = nx.Graph()
    partitions = []
    master_vertices = []

    for i in range(k):
        tmp = nx.Graph()
        partitions.append(tmp)
        master_vertices.append(0)

    edge_list = list(g.edges())
    # random.shuffle(edge_list)
    
    #divide nodes to partitions evenly
    while(len(edge_list) > 0):
         l = len(edge_list)
         
         if(l % 10000 == 0):
            print('len: ', str(l))
        
         for i in partitions:            

            idx = partitions.index(i)

            if(len(edge_list) > 0):
                rnd = edge_list[-1]

                v = rnd[0]
                w = rnd[1]

                if(not master.has_node(v)):
                    master.add_node(v)
                    master_vertices[idx] += 1
                if(not master.has_node(w)):
                    master.add_node(w)
                    master_vertices[idx] += 1

                i.add_node(v)
                i.add_node(w)
                i.add_edge(v,w)

                #delete edge from todo list
                del edge_list[-1]

    # <number of master vertices> 
    # <number of total vertices (include master and mirror vertices)> 
    # <number of edges in this partition>
    
    for i in partitions:
        idx = partitions.index(i)
        print('partition: ', str(idx))
        output.write('partition: ' + str(idx) + '\n')
        print('number of total vetices: ', str(len(i.nodes())))
        # print(i.nodes())
        # print(len(i.nodes()))
        output.write(str(len(i.nodes()))+ '\n')
        print('number of master vertices: ', str(master_vertices[idx]))
        # print(str(master_vertices[idx]))
        # print(master_vertices[idx])
        output.write(str(master_vertices[idx])+ '\n')
        print('total edges: ', str(len(i.edges())))
        # print(i.edges())
        
        output.write(str(len(i.edges()))+ '\n')
        # nx.draw(i,with_labels=True)
        # plt.show()
                
       # <number of master vertices> 
    # <number of total vertices (include master and mirror vertices)> 
    # <number of edges in this partition>


def greedy_vertex_cut(k,g, output):

    master  = nx.Graph()
    partitions = []
    master_vertices = []

    for i in range(k):
        tmp = nx.Graph()
        partitions.append(tmp)
        master_vertices.append(0)

    edge_list = list(g.edges())
    random.shuffle(edge_list)
    
    #divide nodes to partitions evenly
    while(len(edge_list) > 0):

        l = len(edge_list)
         
        if(l % 10000 == 0):
            print('len: ', str(l))

        rnd = edge_list[-1]
        v = rnd[0]
        w = rnd[1]

        assigned_v = False
        assigned_w = False
        machine_v = 9
        machine_w = 9
        #check if assigned
        
        
        if(v in master_vertices or w in master_vertices):
            #TODO speed this up
            for i in partitions:
                if(assigned_v and assigned_w):
                    continue
                for vertex in list(i.nodes()):
                    if(assigned_v and assigned_w):
                        continue
                    if(vertex == v):
                        assigned_v = True
                        machine_v = partitions.index(i)
                    if(w == vertex):
                        assigned_w = True    
                        machine_w = partitions.index(i)

        if(assigned_v and assigned_w):
            partitions[machine_v].add_node(v)
            partitions[machine_w].add_node(w)
            if(machine_v == machine_w):
                i.add_edge(v,w)
        if(assigned_v or assigned_w):
            if(assigned_v):
                master_vertices.append(w)
                partitions[machine_v].add_node(w)
                partitions[machine_v].add_edge(v,w)
            if(assigned_w):
                master_vertices.append(v)
                partitions[machine_w].add_node(v)
                partitions[machine_w].add_edge(v,w)
        else:
            lowest = 9
            score = 999999
            for i in partitions:
                if(len(i.edges()) < score):
                    score = len(i.edges())
                    lowest = partitions.index(i)

            master_vertices.append(v)
            master_vertices.append(w)
            partitions[lowest].add_node(v)
            partitions[lowest].add_node(w)
            partitions[lowest].add_edge(v,w)

        del edge_list[-1]
        
    # <number of master vertices> 
    # <number of total vertices (include master and mirror vertices)> 
    # <number of edges in this partition>
    
    for i in partitions:
        idx = partitions.index(i)
        print('partition: ', str(idx))
        output.write('partition: ' + str(idx) + '\n')
        print('number of total vetices: ', str(len(i.nodes())))
        # print(i.nodes())
        output.write(str(len(i.nodes()))+ '\n')
        print('number of master vertices: ', str(master_vertices[idx]))
        # print(master_vertices[idx])
        output.write(str(master_vertices[idx])+ '\n')
        print('total edges: ', str(len(i.edges())))
        # print(i.edges())
        
        output.write(str(len(i.edges()))+ '\n')


k = [2]
# k = [2,3,4,8]
# file  = 'small-5.graph'
file  = 'roadNet-PA.graph'
# file = 'synthesized-1b.graph'
# file = '/mnt/data/hw7/synthesized-1b.graph'
# file = '/mnt/data/hw7/roadNet-PA.graph'
# file = '/mnt/data/hw7/twitter-2010.graph'
name = 'small-5.graph'

g = read_file(file)
output = open('results_greedy' + str(name),'w')
 
print(file)
output.write('results_' + str(file) + '\n')

for i in k:
    print('amount of partitions: ' + str(i))
    output.write('amount of partitions: ' + str(i) + '\n')
    
    print('edge cut:')
    output.write('edge cut:\n')
    edge_cut(i,g, output)

    print('greede vertex cut:')
    output.write('vertex cut:\n')
    vertex_cut(i,g, output)
    
    print('greedy vertex cut:')
    output.write('vertex cut:\n')
    greedy_vertex_cut(i,g, output)

output.close() 