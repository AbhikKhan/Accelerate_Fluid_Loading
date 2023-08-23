
from drawgrid import *
import numpy as np
from matplotlib import pyplot
from save_frame import *
import pprint # prints good
import pydot
import LAFCA_DFL as lafca
pp = pprint.PrettyPrinter(indent=4)

from drawtree import *

# PARAMETERS FOR TABLE
TIME=0
OPR=0
WASTE=0
IND_LOAD=0
OPT_LOAD=0
FP=0



mxr=[]
treevec=[]
nodecount=0


# <<<<<<<<<<<<<<<<===========================>>>>>>>>>>>>>...
def findBendings(path):
    b = 0
    # print(path)
    for i in range(2, len(path)):
        if (path[i][0] != path[i-2][0]) & (path[i][1] != path[i-2][1]):
            b+=1

    return b


# FIND LEVELWISE NODES##############################################################################
from collections import deque

def level_wise_nodes(adjacency_list):
    visited = set()
    queue = deque([(1, 0)])  # Start from node 1 with level 0
    result = []

    while queue:
        node, level = queue.popleft()
        if node not in visited:
            visited.add(node)
            if level == len(result):
                result.append([])
            result[level].append(node)
            neighbors = adjacency_list.get(node, [])
            for neighbor in neighbors:
                if neighbor not in visited:
                    queue.append((neighbor, level + 1))

    return result


# GENERATE DOT FILE FROM TREEVEC#####################################################################################
from graphviz import Digraph

def generate_tree_dot(treevec):
    node_ids = {}
    dot_file_content = 'digraph Tree {\n'

    for edge in treevec:
        edge_value, u, v = edge

        if u not in node_ids:
            node_ids[u] = 'M' + str(len(node_ids) + 1)

        if v not in node_ids:
            node_ids[v] = 'R' + str(len(node_ids) + 1)

        dot_file_content += '  "{}" -> "{}" [label="{}"];\n'.format(node_ids[u], node_ids[v], edge_value)

    for node, node_id in node_ids.items():
        dot_file_content += '  "{}" [label="{}"];\n'.format(node_id, node)

    dot_file_content += '}\n'

    with open('tree.dot', 'w') as dot_file:
        dot_file.write(dot_file_content)






def get_frequency(my_list):
    frequency = {}
    for element in my_list:
        if element in frequency:
            frequency[element] += 1
        else:
            frequency[element] = 1
    return [[key, value] for key, value in frequency.items()]

def find_leaf_nodes(nodereagents):
    leaf_nodes = []
    # print("in find leaf nodes",nodereagents)
    index=0
    for r in nodereagents:
        
        if len(r)==4:
            # print("in leaf find--->",r)
            leaf_nodes.append(index)
        index=index+1
            
    return leaf_nodes


from collections import Counter
from itertools import chain
from collections import Counter
from itertools import chain

def rearrange_list(lst):
    # Count the frequency of each element
    counts = Counter(lst)

    # Sort the elements based on their frequency in descending order
    sorted_elements = sorted(lst, key=lambda x: counts[x], reverse=True)

    # Create a list to store the rearranged elements
    rearranged_list = []

    # Group the elements based on their frequency
    grouped_elements = [[k] * v for k, v in counts.items()]

    # Find the maximum group length
    max_group_length = max(map(len, grouped_elements)) if grouped_elements else 0

    # Helper function to check if a group has consecutive same elements
    def has_consecutive_elements(group):
        for i in range(len(group) - 1):
            if group[i] == group[i+1]:
                return True
        return False

    # Iterate until all elements are processed
    while grouped_elements:
        # Sort the groups based on their length and check for consecutive same elements
        grouped_elements.sort(key=len, reverse=True)

        # Get the largest group
        largest_group = grouped_elements[0]

        # Check if the largest group has consecutive same elements
        if has_consecutive_elements(largest_group):
            # If so, take the first element from the largest group and move it to the end
            element = largest_group.pop(0)
            largest_group.append(element)

            # Sort the groups again
            grouped_elements.sort(key=len, reverse=True)

        # Remove and append elements from each group to the rearranged list
        grouped_elements = [group for group in grouped_elements if group]
        for i in range(len(grouped_elements)):
            rearranged_list.append(grouped_elements[i].pop(0))

    # Extend the rearranged list with remaining elements
    rearranged_list.extend(chain.from_iterable(grouped_elements))

    return rearranged_list


# def rearrange_list(lst):
#     # Count the frequency of each element
#     counts = Counter(lst)

#     # Sort the elements based on their frequency in descending order
#     sorted_elements = sorted(lst, key=lambda x: counts[x], reverse=True)

#     # Create a list to store the rearranged elements
#     rearranged_list = []

#     # Group the elements based on their frequency
#     grouped_elements = [[k] * v for k, v in counts.items()]

#     # Find the maximum group length
#     max_group_length = max(map(len, grouped_elements)) if grouped_elements else 0

#     # Iterate until all elements are processed
#     while grouped_elements:
#         # Sort the groups based on their length in descending order
#         grouped_elements.sort(key=len, reverse=True)

#         # Remove and append elements from each group to the rearranged list
#         grouped_elements = [group for group in grouped_elements if group]
#         for i in range(len(grouped_elements)):
#             rearranged_list.append(grouped_elements[i].pop(0))

#     # Extend the rearranged list with remaining elements
#     rearranged_list.extend(chain.from_iterable(grouped_elements))

#     return rearranged_list





def makeworse(level,nodereagents,adj_list,mxr):
    
    ll=len(level)
    for l in range(len(level)):
        # print("level-->",l)
        lst=[]
        for e in ((level[l])):
            # print("node-->",e)
            lst.extend(nodereagents[e])
       
        
       
        sorted_list = rearrange_list(lst)
        
        # print("REASSIGN-------------------------------")
        c1=0
        c2=0
        for el in ((level[l])):
            # print("for-->",el)
            
            if l!=0 and l<ll-1:
                
                nodereagents[el]=sorted_list[0:0+len(nodereagents[el])]
                del sorted_list[c1:c1+len(nodereagents[el])]
                # c1=c1+len(nodereagents[el])
                
                sorted_list = rearrange_list(sorted_list)
                # print("after del+SORTING R-->",sorted_list)
                
            elif l==ll-1:
                
                nodereagents[el]=sorted_list[0:0+len(nodereagents[el])]
                del sorted_list[c2:c2+len(nodereagents[el])]
                # c2=c2+len(nodereagents[el]) 
                
                sorted_list = rearrange_list(sorted_list)
                # print("after del+SORTING R-->",sorted_list)
   
    # print("\n\nPermuted--LEVELWISE_NodeR--->")#STILL SWAP TO LESSSEN THE CYCLES...
    # pprint.pprint(nodereagents) 
    # for lv in range(len(level)):
    #     for ell in ((level[lv])):    
    #         print(ell,"-->",nodereagents[ell])
    #     print("\n")
   
    #modifying the tree 
    nodetoremove=-1
    ret=1 #IF NO CHANGES FOUND RETURN 1
    # print("NODE_REAGENTS BEFORE FIND LEAVES-->",)
    
    leaf_nodes = find_leaf_nodes(nodereagents)
    # leaf_nodes = list(set(leaf_nodes))
    # print("LEAF_NODES-->",leaf_nodes)
    
    # for m in leaf_nodes:
    #     if all(element == nodereagents[m][0] for element in nodereagents[m])==1:
    #         ret=-1
    #         r=nodereagents[m][0]
    #         #add r in that m's parent node
    #         for u in range(nodecount+1):
                
    #             if u in adj_list:
    #                 if m in adj_list[u] :
    #                     adj_list[u].remove(m)#delet node from adj_list
    #                     nodereagents[u].append(r)#append R in that parents node
    #                     nodereagents[m]=[]
    #                     level=level_wise_nodes(adj_list)
                        
    #                     # print("afer change-->")
    #                     # print("ADJ_LIST-->",adj_list)
    #                     # print("LEVEL-->",level)
    #                     # print("NodeR-->")
    #                     # pprint.pprint(nodereagents) 
    #change treevec
    temp_treevec=[]
    for u in range(nodecount+1):
        lstt=[]
        if u in adj_list and len(adj_list[u])!=0:
            
            for v in adj_list[u] :
                
                # print(v,"in-",u)
                
                lstt=[1,"M"+str(u),"M"+str(v)] 
                # print("lstt-->",lstt)
                temp_treevec.append([1,"M"+str(u),"M"+str(v)]) 
            
            for rr in range(len(nodereagents[u])):
                lstt=[1,"M"+str(u),nodereagents[u][rr]] 
                temp_treevec.append(lstt)
            # print("\n")
    #add leafs also
    for u in leaf_nodes:
        for rr in range(len(nodereagents[u])):
            lstt=[1,"M"+str(u),nodereagents[u][rr]] 
            temp_treevec.append(lstt)
            
            
    # print("Changed_treevec---->")
    # temp_treevec=list(set(map(tuple, temp_treevec)))
    # print(temp_treevec)
    global treevec
    treevec=temp_treevec
    # permute(level, nodereagents, adj_list, mxr,ret)       



def permute(level,nodereagents,adj_list,mxr,ret):
    
    if ret==1:
        return
    
    ll=len(level)
    for l in range(len(level)):
        # print("level-->",l)
        lst=[]
        for e in ((level[l])):
            # print("node-->",e)
            lst.extend(nodereagents[e])
       
        
        #sort according to the freq of element    
        from collections import Counter
        frequency_counter = Counter(lst)
        sorted_list = sorted(lst, key=lambda x: (-frequency_counter[x], x))
        # print("after SORTING R-->",sorted_list)
        
        # reassign the reagents
        # print("REASSIGN-------------------------------")
        c1=0
        c2=0
        for el in ((level[l])):
            # print("for-->",el)
            
            if l!=0 and l<ll-1:
                
                nodereagents[el]=sorted_list[0:0+len(nodereagents[el])]
                del sorted_list[c1:c1+len(nodereagents[el])]
                # c1=c1+len(nodereagents[el])
                frequency_counter = Counter(sorted_list)
                sorted_list = sorted(sorted_list, key=lambda x: (-frequency_counter[x], x))
                # print("after del+SORTING R-->",sorted_list)
                
            elif l==ll-1:
                
                nodereagents[el]=sorted_list[0:0+len(nodereagents[el])]
                del sorted_list[c2:c2+len(nodereagents[el])]
                # c2=c2+len(nodereagents[el]) 
                frequency_counter = Counter(sorted_list)
                sorted_list = sorted(sorted_list, key=lambda x: (-frequency_counter[x], x))
                # print("after del+SORTING R-->",sorted_list)
   
    # print("\n\nPermuted--LEVELWISE_NodeR--->")#STILL SWAP TO LESSSEN THE CYCLES...
    # pprint.pprint(nodereagents) 
    # for lv in range(len(level)):
    #     for ell in ((level[lv])):    
    #         print(ell,"-->",nodereagents[ell])
    #     print("\n")
   
    #modifying the tree 
    nodetoremove=-1
    ret=1 #IF NO CHANGES FOUND RETURN 1
    # print("NODE_REAGENTS BEFORE FIND LEAVES-->",)
    
    leaf_nodes = find_leaf_nodes(nodereagents)
    # leaf_nodes = list(set(leaf_nodes))
    # print("LEAF_NODES-->",leaf_nodes)
    
    for m in leaf_nodes:
        if all(element == nodereagents[m][0] for element in nodereagents[m])==1:
            ret=-1
            r=nodereagents[m][0]
            #add r in that m's parent node
            for u in range(nodecount+1):
                
                if u in adj_list:
                    if m in adj_list[u] :
                        adj_list[u].remove(m)#delet node from adj_list
                        nodereagents[u].append(r)#append R in that parents node
                        nodereagents[m]=[]
                        level=level_wise_nodes(adj_list)
                        
                        # print("afer change-->")
                        # print("ADJ_LIST-->",adj_list)
                        # print("LEVEL-->",level)
                        # print("NodeR-->")
                        # pprint.pprint(nodereagents) 
    #change treevec
    temp_treevec=[]
    for u in range(nodecount+1):
        lstt=[]
        if u in adj_list and len(adj_list[u])!=0:
            
            for v in adj_list[u] :
                
                # print(v,"in-",u)
                
                lstt=[1,"M"+str(u),"M"+str(v)] 
                # print("lstt-->",lstt)
                temp_treevec.append([1,"M"+str(u),"M"+str(v)]) 
            
            for rr in range(len(nodereagents[u])):
                lstt=[1,"M"+str(u),nodereagents[u][rr]] 
                temp_treevec.append(lstt)
            # print("\n")
    #add leafs also
    for u in leaf_nodes:
        for rr in range(len(nodereagents[u])):
            lstt=[1,"M"+str(u),nodereagents[u][rr]] 
            temp_treevec.append(lstt)
            
            
    # print("Changed_treevec---->")
    # temp_treevec=list(set(map(tuple, temp_treevec)))
    # print(temp_treevec)
    global treevec
    treevec=temp_treevec
    
    permute(level, nodereagents, adj_list, mxr,ret)       
            
        
# FOR GENMIX_HDA
##########################################from  G to adj list
adj_list = {} #to save the tree from G in easy form
mylist = [] #temp list to save nodes

def add_node(node):
  if node not in mylist:
    mylist.append(node)
  # else:
  #   print("Node ",node," already exists!")
  
def add_edge(node1, node2):
  temp = []
  if node1 in mylist and node2 in mylist:
    if node1 not in adj_list:
      temp.append(node2)
      adj_list[node1] = temp
   
    elif node1 in adj_list:
      temp.extend(adj_list[node1])
      temp.append(node2)
      adj_list[node1] = temp
       
  else:
    print("Nodes don't exist!")
    

GRID=15 #grid size

m=np.random.randint(2, size=(GRID, GRID))# matrix to repesent the grid
nodereagents=[[] for _ in range(50)]
X=GRID/2
Y=GRID/2    
c=0
parcoord=[[None,None]]*1000 #list to save coordinates of parent node [x,y] 
coordinates=[[[None,None],[None,None],[None,None],[None,None]]]*30 #[tree_node,c1,c2,c3,c4],c1-c4-->coordinates of the  form (x,y) in the grid
discard=[[] for _ in range(30)]# saving the nodes to discard--WASTE
coordinates[1]=[[X,Y],[X+1,Y],[X,Y+1],[X+1,Y+1]]#root node coordinates


def footprint(treelist,mxx):
    
    global discard
    discard=[[] for _ in range(30)]#
    [discard[1].extend(inner_list) for inner_list in coordinates[1] ]
    global mxr
    mxr=mxx
    # print("MIXTUE==>",mxr)
    number_of_rows = GRID
    number_of_columns = GRID
   
    #MAKING COORDINATES TO ALL 0
    for x in range(number_of_rows):
       # column_elements=[]
       for y in range(number_of_columns):
           m[x][y]=0
           
    
    #COORDINATES OF ROOT NODE#######
    i=number_of_rows/2
    j=number_of_columns/2
    m[i][j]=1
    m[i+1][j+1]=1
    m[i+1][j]=1
    m[i][j+1]=1
    ################################



    #CONVERT Genmix list-->ADJ LIST ##################################################################################
    
    treevec_temp=[]
    for e in range(len(treelist[1])):
        if type(treelist[1][e][1][1])!=str:
            list=[1,treelist[1][e][0][1],"R"+str(treelist[1][e][1][1])]#[edgeValue,u,v]
            
            global IND_LOAD
            IND_LOAD=IND_LOAD+1  #reagents leaf nodes
        else:
             
            list=[1,treelist[1][e][0][1],(treelist[1][e][1][1])]#[edgeValue,u,v]
        treevec_temp.append(list)
    
        
    global treevec
    treevec=[] #[edgeValue,u,v] and it contains tree directly from genmix(hda(root))
    treevec=treevec_temp
    # [treevec.append(x) for x in treevec_temp if x not in treevec]
    # print("TREEVEC")
    # print(treevec)
    
    mxnode=0
    
    global nodecount
    # find max node number
    for x in treevec:
        if int(x[1][1])>mxnode:
            mxnode=int(x[1][1])
        if len(x[1])==3 and int(x[1][1]+x[1][2])>=mxnode:
             # print("lenth--->",3)
             nodecount=int(x[1][1]+x[1][2])
             mxnode=max(nodecount,mxnode)
    
    # print("maxnode-->",mxnode)
    
    for y in treevec:
        if y[1][0] == "m":
            y[1]="M"+ str(int(y[1][1])+mxnode+1)
        if y[2][0] == "m":
            y[2]="M"+ str(int(y[2][1])+mxnode+1)            
    
    # print("TREEVEC AFTER CHANGE")
    # print(treevec) #after making m-->M
    
    
    
    
    nodereagents=[[] for _ in range(50)]
    for ee in range(len(treevec)):
        if (treevec[ee][2][0])=="R":
            # list=[1,treelist[1][e][0][1],"R"+str(treelist[1][e][1][1])]#[edgeValue,u,v]
            if len(treevec[ee][1])!=3:
                # global nodereagents
                nodereagents[int(treevec[ee][1][1])].append(treevec[ee][2])
            elif len(treevec[ee][1])==3:
                # global nodereagents
                nodereagents[int(treevec[ee][1][1] + treevec[ee][1][2])].append(treevec[ee][2])
    
    
    # print("nodeR-->",nodereagents)
            
    # # COUNT IND_cycles
    # r_count=[0 for _ in range(len(mxr)+1)]
    # # print(r_count)
    # for s in nodereagents:
    #     # print("s-->",s)
    #     if len(s)!=0:
    #         for rg in range(len(mxr)+1):
    #             # print("rg-->",rg)
    #             if rg!=0 and ("R"+str(rg)) in s:
    #                r_count[rg]=r_count[rg]+1 
    #                # print("r_count-->",r_count)
                
    # global IND_LOAD
    # IND_LOAD=sum(r_count)
    
    
    # print("Ind load-->",IND_LOAD)
    #count nodes
    # mxnode=-1
    # global nodecount
    nodecount=0
    mxnode=0
    for xy in range(len(treevec)):
        if int(treevec[xy][1][1]) >= mxnode:
            # global nodecount
            nodecount=int(treevec[xy][1][1])
            mxnode=max(nodecount,mxnode)
        if len(treevec[xy][1])==3 and int(treevec[xy][1][1]+treevec[xy][1][2])>=mxnode:
            # print("lenth--->",3)
            nodecount=int(treevec[xy][1][1]+treevec[xy][1][2])
            mxnode=max(nodecount,mxnode)
            
            # print("# of nodes-->",nodecount)
    
    
    nodecount=mxnode
    # print("# of nodes-->",nodecount)##########################
    
    # print("Node-reagents-->")
    # print(nodereagents)#######################################
    
    
    visited=[]
    for u in range(nodecount+2):
        visited.append(0)
        add_node(u+1)
        # print("added",u)
    
    
    global adj_list
    adj_list={}
    # print("before-->",adj_list)
    # treevec.sort(reverse = True) # Sort according to edgeValue decending   
    for i in treevec:
        if i[2][0]!="R":
            if len(i[1])!=3 and len(i[2])!=3:
                add_edge(int(i[1][1]),int(i[2][1]))
            if len(i[1])==3 and len(i[2])!=3:
                add_edge(int(i[1][1]+i[1][2]),int(i[2][1]))
            if len(i[1])!=3 and len(i[2])==3:
                add_edge(int(i[1][1]),int(i[2][1]+i[2][2]))
            if len(i[1])==3 and len(i[2])==3:
                add_edge(int(i[1][1]+i[1][2]),int(i[2][1]+i[2][2]))
            
    #     # print("\n")
    
    
    # for node in adj_list:
    #     print(node, " ---> ", [i for i in adj_list[node]])
    
    # print(adj_list)#contins only the mixing nodes######################################<-----
    # print("LEVEL WISE NODES-->")
    # print(level_wise_nodes(adj_list))
    level=level_wise_nodes(adj_list)
    # level, nodereagents, adj_list =  
    #####################################################################################
    makeworse(level, nodereagents, adj_list, mxr)
    
    # COUNT IND_cycles
    r_count=[0 for _ in range(len(mxr)+1)]
    # print(r_count)
    for s in nodereagents:
        # print("s-->",s)
        if len(s)!=0:
            for rg in range(len(mxr)+1):
                # print("rg-->",rg)
                if rg!=0 and ("R"+str(rg)) in s:
                   r_count[rg]=r_count[rg]+1 
                   # print("r_count-->",r_count)
                
    global IND_LOAD
    IND_LOAD=sum(r_count)
    global treevec
    dtree(treevec)
    dot_file_path = 'modified_graph.dot'
    output_png_path = 'output_wgenmix.png'
    generate_png_from_dot(dot_file_path, output_png_path)
    
    #####################################################################################
    permute(level,nodereagents,adj_list,mxr,-1)
    
    #####################################################################################
    global treevec
    dtree(treevec)
    dot_file_path = 'modified_graph.dot'
    output_png_path = 'output2.png'
    generate_png_from_dot(dot_file_path, output_png_path)
    image1_path = 'output_wgenmix.png'
    image2_path = 'output2.png'
    output_path = 'connected_trees.png'
    connect_images(image1_path, image2_path, output_path)
    import pydot
    image_path = 'connected_trees.png'
    # image = display_image(image_path)
    # image.show()
    ###################################################################################        
        
   
    u=1 #root node
    i=number_of_rows/2 
    j=number_of_columns/2 
    dfs(adj_list,u,i,j,visited) # TO MARK POSITION OF EACH NODE ON GRID
    
    g=0 # NO OF CELLS OCCUPIED IN THE MIXING PROCESS OF A SAMPLE RATIO##################
    for x in range(number_of_rows):
        for y in range(number_of_columns):
            if m[x][y]==1:
                g=g+1
               
    # print('No of cells =' ,g)
    global FP
    FP=g
    #####################################################################################
    # print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in m]))
    # main2(m) #GRAPHICAL REPRESENTATION OF THE FOOTPRINT (drawgrid.py)
    
    
    

def dfs(adj_list,u,i,j,visited):
    
    
    
    # print("i  j  => ",i,j)
    # print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in m]))
   
    if(u not in adj_list):
        return
    
    # print("node=",u,"\t")
    
    for v in adj_list[u]:
        # print("parcoor",v)
        parcoord[v+1]=([i,j])
        
    # print(parcoord)
    # G.nodes[u]['visited']=1;
    # print("in dfs")
    count_2=0 #for the combination of (2,2) for a node
    count_1=0 #for the combination of (1,1) ,(1 1 1) or (1 1 1 1) for a node
    for v in adj_list[u]:
        # print(v)
        
        count_1=count_1+1
        
        if count_1==4 and visited[v]==0:
            # print("for count_1=4")
            # m[i-1][j]=1
            m[parcoord[v+1][0]-1][parcoord[v+1][1]+1]=1
            
            # m[i][j-1]=1
            m[parcoord[v+1][0]-1][parcoord[v+1][1]+2]=1
            
            # m[i-1][j-1]=1
            m[parcoord[v+1][0]][parcoord[v+1][1]+2]=1
            
            # i=i-1
            i=(parcoord[v+1][0]-1)
            
            # j=j-1
            j=(parcoord[v+1][1]+1)
            
            visited[v]=1
            
            #saving the coordinates of a node
            coordinates[v]=[ [parcoord[v+1][0],parcoord[v+1][1]+2],
                             [parcoord[v+1][0]-1,parcoord[v+1][1]+2],
                             [parcoord[v+1][0],parcoord[v+1][1]+1],
                             [parcoord[v+1][0]-1,parcoord[v+1][1]+1] 
                           ]
            coordinates[v].sort()
            # print("for node",v,coordinates[v])
            #saving the discarding coordinates of a node
            discard[v]=([parcoord[v+1][0]-1,parcoord[v+1][1]+1,
                               parcoord[v+1][0]-1,parcoord[v+1][1]+2,
                               parcoord[v+1][0],parcoord[v+1][1]+2])
            # discard[v].sort()
            # print(discard[v])
            # print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in m]))
            
            
        if count_1==2 and visited[v]==0:
            # print("for count_1=2")
            # m[i-1][j]=1
            m[parcoord[v+1][0]+1][parcoord[v+1][1]-1]=1
            
            # m[i][j-1]=1
            m[parcoord[v+1][0]+2][parcoord[v+1][1]-1]=1
            
            # m[i-1][j-1]=1
            m[parcoord[v+1][0]+2][parcoord[v+1][1]]=1
            
            # i=i-1
            i=parcoord[v+1][0]+1
            
            # j=j-1
            j=parcoord[v+1][1]-1
            
            visited[v]=1
            
            #saving the coordinates of a node
            coordinates[v]=[ [parcoord[v+1][0]+1,parcoord[v+1][1]],#1
                             [parcoord[v+1][0]+2,parcoord[v+1][1]],#2
                             [parcoord[v+1][0]+2,parcoord[v+1][1]-1],#3  
                             [parcoord[v+1][0]+1,parcoord[v+1][1]-1] 
                           ]
            coordinates[v].sort()
            # print("for node",v,coordinates[v])
            #saving the discarding coordinates of a node
            discard[v]=([parcoord[v+1][0]+1,parcoord[v+1][1]-1,
                               parcoord[v+1][0]+2,parcoord[v+1][1]-1,
                               parcoord[v+1][0]+2,parcoord[v+1][1]])
            # discard[v].sort()
            # print(discard[v])
            # print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in m]))
            
        
        if count_1==3 and visited[v]==0:
            # print("for count_1=3")
            # m[i-1][j]=1
            m[parcoord[v+1][0]+1][parcoord[v+1][1]+2]=1
            
            # m[i][j-1]=1
            m[parcoord[v+1][0]+2][parcoord[v+1][1]+2]=1
            
            # m[i-1][j-1]=1
            m[parcoord[v+1][0]+2][parcoord[v+1][1]+1]=1
            
            # i=i-1
            i=parcoord[v+1][0]+1
            
            # j=j-1
            j=parcoord[v+1][1]+1
            
            visited[v]=1
            
            #saving the coordinates of a node
            coordinates[v]=[ [parcoord[v+1][0]+1,parcoord[v+1][1]+1],
                             [parcoord[v+1][0]+2,parcoord[v+1][1]+1], 
                             [parcoord[v+1][0]+2,parcoord[v+1][1]+2],
                             [parcoord[v+1][0]+1,parcoord[v+1][1]+2]
                           ]
            coordinates[v].sort()
            # print("for node",v,coordinates[v])
            #saving the discarding coordinates of a node
            discard[v]=([parcoord[v+1][0]+1,parcoord[v+1][1]+2,
                               parcoord[v+1][0]+2,parcoord[v+1][1]+2,
                               parcoord[v+1][0]+2,parcoord[v+1][1]+1])
            # discard[v].sort()
            # print(discard[v])
            # print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in m]))
        
        if count_1==1 and visited[v]==0:
            # print("for count_1=1")
            # m[i-1][j]=1
            m[parcoord[v+1][0]-1][parcoord[v+1][1]]=1
            
            # m[i][j-1]=1
            m[parcoord[v+1][0]][parcoord[v+1][1]-1]=1
            
            # m[i-1][j-1]=1
            m[parcoord[v+1][0]-1][parcoord[v+1][1]-1]=1
            
            # i=i-1
            i=parcoord[v+1][0]-1
            
            # j=j-1
            j=parcoord[v+1][1]-1
            
            visited[v]=1
            
            #saving the coordinates of a node
            coordinates[v]=[ [parcoord[v+1][0],parcoord[v+1][1]],
                             [parcoord[v+1][0]-1,parcoord[v+1][1]],
                             [parcoord[v+1][0],parcoord[v+1][1]-1],  
                             [parcoord[v+1][0]-1,parcoord[v+1][1]-1] 
                           ]
            coordinates[v].sort()
            # print("for node",v,coordinates[v])
            #saving the discarding coordinates of a node
            discard[v]=([parcoord[v+1][0]-1,parcoord[v+1][1],
                         parcoord[v+1][0]-1,parcoord[v+1][1]-1,
                               parcoord[v+1][0],parcoord[v+1][1]-1
                                   ])
            # discard[v].sort()
            # print(discard[v])
            # print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in m]))
            
        # print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in m]))
        # main2(m)
        ########
        # if G[u][v]['edgeVar'][1] == str(3) and  visited[v]==0:
        #     print("")
        #     coordinates[v]=coordinates[u]
        #     print("for node",v,coordinates[v])
        #     discard[v]=([parcoord[v+1][0],parcoord[v+1][1]])
        #     # discard[v].sort()
        #     print(discard[v])
        #     visited[v]=1
            
        #     # i=i-1
        #     i=parcoord[v+1][0]
            
        #     # j=j-1
        #     j=parcoord[v+1][1]
            
       
        dfs(adj_list,v,i,j,visited)
    
 
    
 
n=mylist.__len__()              
 #this will contains the nodes seq to run

mix_u=[[] for _ in range(20)] #list  contains mixing components 
mix_u[0]=['M1', 'M1', 'M1', 'M1']

def find_seq(height = 0):
    
    
    TIME=0
    OPR=0
    WASTE=0
    # IND_LOAD=0
    OPT_LOAD=0
    
    #############to save every nodes childrens reagents or mixing nodes####
    numReagents = len(mxr)
    # for u in range(numReagents+1) :
    #     lst=[]
        
    #     if u in adj_list:
    #         for v in adj_list[u]:
    #             # l=G[u][v]['edgeVar'][1]
    #             for p in range(1):
    #                 lst.append("M"+str(v))
        
        # l=G[u][v]['edgeVar'][1]           
        # for i in range(numReagents):
        #     if G.node[u]['reagent'][i][1]!= '0':
        #         rg_count=G.node[u]['reagent'][i][1]
        #         rg=G.node[u]['reagent'][i][0]
        #         rg=rg[0].upper()+rg[6]
                
        #         for k in range(int(rg_count)):
        #             lst.append(rg)
    # global treevec
    # unique_lst = list(set(map(tuple, treevec)))

    # # Convert back to a list of lists
    
    # treevec = [list(t) for t in unique_lst]
    global mix_u
    mix_u=[[] for _ in range(20)] #list  contains mixing components 
    mix_u[0]=['M1', 'M1', 'M1', 'M1']
    
    # print("TREEVEC BEFORE MIXU-->",treevec)
    # print("TREEVEC BEFORE MIXU-->",mix_u)
    for u in treevec:
        
        # mix_u[int(u[1][1])].append(u[2])
        if u[2][0]=="R":
            if len(u[1])!=3 :
                mix_u[int(u[1][1])].append(u[2])
            if len(u[1])==3 :
                mix_u[int(u[1][1]+u[1][2])].append(u[2])
        elif u[2][0]=="M":
            if len(u[1])!=3 :
                mix_u[int(u[1][1])].append(u[2])
            if len(u[1])==3 :
                mix_u[int(u[1][1]+u[1][2])].append(u[2])
        
        
        # lst.sort()
        # mix_u[u]=(lst)
    
    # mix_u=list(filter(lambda x: x, mix_u))# delete empty list
    # mix_u = [elem for elem in mix_u if elem != []]
    # print(mix_u)
        # print("\n")
        
    # print("COORDINATES:")
    # pprint.pprint(coordinates)
    # print("MIX UNITS:")
    # pprint.pprint(mix_u)
    ######################################################################
    run_seq=[]#[[] for _ in range(11+1)]
    run_seq.append([1]) 
    parts=[]  
    run_3=[]
    run_it=[]
    
    #find by level
    leaves=[]
    traverse=[]
    
    
    
    rs=level_wise_nodes(adj_list)
    # print("LEVEL FOR RUNNING-->",rs)
    rs.reverse()
    for e in rs:
        e.reverse()
        for ee in e:
            run_it.append(ee)

    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>      
    allFlow, allBendings, allLengths = 0, 0, 0
    for parallelMixtures in rs:
        parallelLoadingCells = []
        reagents = []
        blockageList = [] # stores all the blockages and the coordinates in which they can be places.
        '''
            As only one unit is being shared between parent and child so there is no need to keep track of
            number of same blockages as only one blockage of a particular kind will be taken into consideration.
        '''

        for mix in parallelMixtures:
            mixture = [[element - 1 for element in sublist] for sublist in coordinates[mix][:]]
            parallelLoadingCells.append(mixture[:])

            # Child information to place blockages
            blockages = dict()
            if mix in adj_list:
                for child in adj_list[mix]:
                    for cell in coordinates[child]:
                        if cell in coordinates[mix]:
                            interFluid = 'M'+str(child)
                            if interFluid not in blockages: # Check wheather the blockage is present in the list or not
                                blockages[interFluid] = [[x-1 for x in cell]]
                            else:
                                blockages[interFluid].append([x-1 for x in cell])
                blockageList.append(blockages)

            # Get all the reagents for the current mixture
            reagents.append(mix_u[mix])

        totalPathLength, totalBendings = 0, 0
        loadingPaths = lafca.getPlacementAndLoading(parallelLoadingCells, blockageList, reagents)
        for order in loadingPaths:
            totalBendings += order[1]
            totalPathLength += len(order[2])
            print(order[0], 'Bendings:', order[1], 'Path Length:', len(order[2]))
        
        print('Flow:', len(loadingPaths), ',Total Bendings:', totalBendings, ',Total Path Length:', totalPathLength)
        allFlow += len(loadingPaths)
        allBendings += totalBendings
        allLengths += totalPathLength
    
    print('K', allFlow, 'B', allBendings, 'L', allLengths)


    # save the data
    data = [{'Ratio':mxr, 'Height':height, 'Loading Cycles (K)': allFlow, 'Bendings (B)': allBendings,
            'Path Length (L)': allLengths}]
    file_path = 'genmix_NTM_best_modified.xlsx'
    
    save_data_to_excel(data, file_path)
