from cmath import inf
from collections import defaultdict
from array import *
from glob import glob
from turtle import color
import numpy as np
from matplotlib.pyplot import connect
from operator import contains, eq
from genericpath import isdir
from operator import eq
from matplotlib.style import use
import networkx as nx
import matplotlib.pyplot as plt 
import warnings

with warnings.catch_warnings():
    warnings.filterwarnings('ignore', r'All-NaN (slice|axis) encountered')

visited = set()
visitedBfs = []
visitedConnected = set()
queue = []
INF = 9999999

def dfs(visited,graph,node,lookedForNode):
    ##EXEMPLE OF GRAPH STRUCTURE
    ## { 0:[1,2] 1:[0]}
    if node not in visited:
        print ("Visitei", node, end=" ")
        visited.add(node)
        if(eq(int(node),int(lookedForNode))):
            resultToReturn = True
            return resultToReturn
        for neighbour in graph[node]:
            dfs(visited, graph, neighbour,lookedForNode)

def bfs(visitedBfs, graph, node,lookedForNode): 
  visitedBfs.append(node)
  queue.append(node)
  if(eq(int(node),int(lookedForNode))):
    resultToReturn = True
    return resultToReturn
  while queue:          # Creating loop to visit each node
    m = queue.pop(0) 
    print (m, end = " ") 
    for neighbour in graph[m]:
      if neighbour not in visitedBfs:
        visitedBfs.append(neighbour)
        queue.append(neighbour)
    

 

class Graph(object):
    def __init__(self, vertices, directed):
        self.vertices = int(vertices)
        self.directed = directed
        self.arr = self.createArray()


    def primsAlg(self):
        ##FOR MOCK
        ##mockedArr = ([[0,0,0,0,0,0,0,0,0,0,0],[3,0,0,0,0,0,0,0,0,0,0],[0,16,0,0,0,0,0,0,0,0,0],[0,0,11,0,0,0,0,0,0,0,0],[0,0,3,3,0,0,0,0,0,0,0],[0,0,20,0,14,0,0,0,0,0,0],[0,0,0,0,0,12,0,0,0,0,0],[0,0,0,0,0,0,10,0,0,0,0],[0,9,19,0,0,0,6,8,0,0,0],[9,0,0,0,0,0,0,3,6,0,0],[0,0,11,0,0,5,2,0,5,0,0]])
        ##arrayForPrims = np.tril(mockedArr)
        ##Making the lower triangle
        arrayForPrims = np.tril(self.arr)
        ##Changing 0 to nan
        arrayForPrims=[[_el if _el != 0 else np.nan for _el in _ar] for _ar in arrayForPrims]
        linesAndColumns = []
        print(arrayForPrims)
        ##Getting tuple of the lowest value
        lowest =(np.argwhere(arrayForPrims== np.nanmin(arrayForPrims)))
        value = np.nanmin(arrayForPrims)
        ##transforming into 1d array
        lowest = lowest.flatten()
        print(value)
        resultArray = (self.vertices,self.vertices)
        resultArray = np.zeros((resultArray),dtype=int)
        linesAndColumns.append(lowest[0])
        linesAndColumns.append(lowest[1])
        resultArray[lowest[0]][lowest[1]] =  value
        ## -2 because I already made one above and matrix should return arr -1 vertices by default
        for i in range(self.vertices-2):
            print("Lines and columns", linesAndColumns)
            ##Max number possible of float
            lowerNum = 9223372036854775807.00
            for x in linesAndColumns:
            ##Grabbing lowest from current line and column and it needs to be not crossed by line and column stated in "linesandcollumns"
                for j in range(self.vertices):
                    
                    if (np.nanmin(arrayForPrims[j][x]))<lowerNum and (j not in linesAndColumns):
                        lowerNum = np.nanmin(arrayForPrims[j][x])
                        lowest = [j,x]
                    if (np.nanmin(arrayForPrims[x][j]))<lowerNum and (j not in linesAndColumns):
                        lowerNum = np.nanmin(arrayForPrims[x][j])
                        lowest = [x,j]
            print("lowerNum = ", lowerNum)
            print("index = ", lowest)

            linesAndColumns.append(lowest[0])
            linesAndColumns.append(lowest[1])
            value = arrayForPrims[lowest[0]][lowest[1]]
            resultArray[lowest[0]][lowest[1]] =  value
            ##removing duplicates
            linesAndColumns = list(dict.fromkeys(linesAndColumns))

        sum = np.sum(resultArray)
        print(resultArray)
        print("Caminho", sum)
        self.printArray()
        ##self.printArray(mockedArr)
        self.printArray(resultArray)




    def graphToDict(self):
        ##TURNS THE MATRIX OF 1 AND 0 INTO A DICTONARY OF THE INDEXES
        graph = {}
        for i in range(self.arr.shape[0]):
            graph[i]=[]
            for j in range(self.arr.shape[0]):
                if(self.arr[i][j]!=0):
                    graph[i].append(j)
        print(graph)
        return graph
    def helperFunction(self):
        arrayOfIndexes = []
        for i in range(self.arr.shape[0]):
            arrayOfIndexes.append(i)
        return arrayOfIndexes


    
    def depthSearch(self):
        print("Qual vertice voce esta procurando?")
        searchVertice = int(input())
        print("Qual o ponto inicial de busca?")
        initialPoint = int(input())
        if(initialPoint>self.arr.shape[0] or initialPoint<0):
            return "Erro, digite um vertice valido"

        graph = self.graphToDict()
        node = initialPoint
        result = dfs(visited,graph,node,searchVertice)
        if(eq(result,True)):
            print("\nEncontrado")
            return
        if(len(visited)!=self.arr.shape[0]):
            remainingNodes = set(visited) ^ set(self.helperFunction())
            remainingNodes= list(remainingNodes)
            print("Ainda faltam vertices... ",remainingNodes)
            for i in range(len(remainingNodes)):
                result = dfs(visited,graph,remainingNodes[i],searchVertice)
                if(searchVertice in visited):
                    print("\nEncontrei, foram encontrados ", visited)
                    return
            print("\nNao encontrado, foram encontrados ", visited)
            return

    def breadthSearch(self):          
        print("Busca por largura")
        print("Qual vertice voce esta procurando?")
        searchVertice = int(input())
        print("Qual o ponto inicial de busca?")
        initialPoint = int(input())
        if(initialPoint>self.arr.shape[0] or initialPoint<0):
            return "Erro, digite um vertice valido"

        graph = self.graphToDict()
        node = initialPoint
        result = bfs(visitedBfs,graph,node,searchVertice)
        if(eq(result,True)):
            print("\nEncontrado")
            return
        if(len(visitedBfs)!=self.arr.shape[0]):
            remainingNodes = set(visitedBfs) ^ set(self.helperFunction())
            remainingNodes= list(remainingNodes)
            print("Ainda faltam vertices... ",remainingNodes)
            for i in range(len(remainingNodes)):
                result = bfs(visitedBfs,graph,remainingNodes[i],searchVertice)
                if(searchVertice in visitedBfs):
                    print("\nEncontrei, foram encontrados ", visitedBfs)
                    return
            print("\nNao encontrado, foram encontrados ", visitedBfs)
            return



    def printEdges(self):
        print(self.edges)

    def insertVertice(self):
        ##SHAPE = (1,1) - (2,2)
        self.arr=np.insert(self.arr,self.arr.shape[0],0,axis=0)
        self.arr=np.insert(self.arr, self.arr.shape[1], 0, axis=1)
        self.vertices = self.vertices +1


                
    def removeVertice(self):
        print("Qual vertice voce deseja excluir?")
        vertice = int(input())
        if(self.arr.shape[1]>=vertice and self.arr.shape[0]>=vertice):
            self.arr = np.delete(self.arr,vertice,1)
            self.arr = np.delete(self.arr,vertice,0)
            self.vertices = self.vertices -1
        else:
            print("Erro, vertice inexistente")        
        
    def insertOrRemoveConnection(self, insert):
        print("Numero do primeiro item:")
        x = int(input())
        y= 999
        while(not eq(y,-1)):
            print("LOOP: Selecione os itens que fazem relacao com o PRINCIPAL - Digite -1 para cancelar")
            y = int(input())
            if(eq(x,y) or y>self.arr.shape[0] or x>self.arr.shape[1]):
                print("O vertice nao pode ser e deve ser menor que a quantidade de linhas;colunas")
            elif((x<=self.arr.shape[0] or y<=self.arr.shape[0]) and not(eq(y,-1))):
                print("Insira o valor da relacao")
                conexionValue = int(input())
                if(eq(insert, True)):
                    print("Conexao gerada")
                    self.arr[x][y] = conexionValue
                    if(eq(self.directed,False)):
                        self.arr[y][x] = conexionValue
                else:
                    print("Conexao removida")
                    self.arr[x][y] =0
                    if(eq(self.directed,False)):
                        self.arr[y][x] = 0
            else:
                print("Vertice inexistente")


    def createArray(self):
        s = (self.vertices,self.vertices)
        s = np.zeros((s),dtype=int)
        return s

    def printArray(self,arr=np.array([])):
        selfArrayCopy = np.copy(self.arr)
        if len(arr)!=0:
            selfArrayCopy = arr
        print(selfArrayCopy)
        printTuple = ()
        arrayOfTuples = []
        if(self.directed==True):
            G = nx.MultiDiGraph()
        if(self.directed==False):
            G = nx.MultiGraph()
        ##Creating nodes
        for x in range(self.vertices):
            G.add_node(x)
        ##adding connections
        for i in range(self.vertices):
            for j in range(self.vertices):
                if(not eq(selfArrayCopy[i][j],0)):
                    t=(i,j)
                    arrayOfTuples.append(t)
        printTuple = (arrayOfTuples)                 
        print(printTuple)
        G.add_edges_from(printTuple)
        plt.figure(figsize=(8,8))
        pos = nx.spring_layout(G)
        nx.draw(  G, pos, edge_color='black', width=1, linewidths=1,
    node_size=500, node_color='green', alpha=0.9,
    labels={node: node for node in G.nodes()})

        labels = {}
        for i in printTuple:
            labels[i] = selfArrayCopy[i[0]][i[1]]
        nx.draw_networkx_edge_labels(
        G, pos,
        edge_labels=labels,
        font_color='black'
        )
        plt.axis('off')
        plt.show()  # pause before exiting


