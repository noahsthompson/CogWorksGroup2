def plot_graph(graph, adj):
    """ Use the package networkx to produce a diagrammatic plot of the graph, with
        the nodes in the graph colored according to their current labels.

        Note that only 20 unique colors are available for the current color map,
        so common colors across nodes may be coincidental.

        Parameters
        ----------
        graph : Tuple[Node, ...]
            The graph to plot
            
        adj : numpy.ndarray, shape=(N, N)
            The adjacency-matrix for the graph. Nonzero entries indicate
            the presence of edges.

        Returns
        -------
        Tuple[matplotlib.fig.Fig, matplotlib.axis.Axes]
            The figure and axes for the plot."""
    import networkx as nx
    import numpy as np
    import matplotlib.cm as cm
    import matplotlib.pyplot as plt

    g = nx.Graph()
    for n, node in enumerate(graph):
        g.add_node(n)

    g.add_edges_from(zip(*np.where(np.triu(adj) > 0)))
    pos = nx.spring_layout(g)

    color = list(iter(cm.Vega20b(np.linspace(0, 1, len(set(i.label for i in graph))))))
    color_map = dict(zip(sorted(set(i.label for i in graph)), color))
    colors = [color_map[i.label] for i in graph]
    fig, ax = plt.subplots()
    nx.draw_networkx_nodes(g, pos=pos, ax=ax, nodelist=range(len(graph)), node_color=colors)
    nx.draw_networkx_edges(g, pos, ax=ax, edgelist=g.edges())
    return fig, ax
class whisperNode():
    """Whisper node:
            Feilds:
                label- (str) :
                    The label of the image
                ID- (np.array, shape (128,)):
                    The image description vector of the image
                neighbors-([whisperNode]):
                    The neighbors of the node as determined by the findNeighbor function
                neighborsWeights-([float]):
                    The weights associated with each neighbor
                wasUpdate- (bool):
                    Boolean to determine if the whisperNode was updated in last updateLabel iteration.
                    If all wasUpdate's in a whisper graph are false, then iteration halts.
                KnownLabel- (bool):
                    Boolean to determine if the given label should not be overriden in updateLabel, ie if 
                    the image has already been correctly labeled. Default false"""
                
    def __init__(self, imageLabel,imageDescrip,kName=False):
        """ __init__
            Params:
                imageLabel-(str):
                    Current label for image
                imageDescrip-(np.array, shape (128,)):
                    image description of image
                kName-(bool (optional, default false)):
                    If true, will make Node not update during updateLabel. Used when inputed label is correct label""""
        self.label=imageLabel
        self.ID=imageDescrip
        self.neighbors=[]
        self.neighborsWeights=[]
        self.wasUpdated=True
        self.KnownLabel=kName
    def __repr__(self):
        return self.label
    def findNeighbors(self, nodes):
        """findNeighbors:
                Takes a list of nodes(the other nodes in the graph) and finds the ones that are similar enough to be neighbors
                Params:
                    nodes:list of potencial neighbors
                Returns: Updated self.neighbors"""
        edges=[]
        for node in nodes:
            l2dist=np.sqrt(np.sum((self.ID - node.ID)**2))
            if(l2dist<5):
                edges.append(1)
                self.neighbors.append(node)
                weight=1/(l2dist**2)
                self.neighborsWeights.append(weight)
            else:
                edges.append(0)

        return edges
    def getLabel(self):
        """getLabel:
                returns: Nodes current label"""
        return self.label
    def updateLabel(self):
        """updateLabel:
                Looks at all current neighbors, updates label
            return:
                updated self.label"""
        if(self.KnownLabel):
            return self.label
        labelWeights=dict()
        for i in range(len(self.neighbors)):
            label=self.neighbors[i].getLabel()
            weight=self.neighborsWeights[i]
            if(self.neighbors[i].getLabel() in labelWeights.keys()):
                labelWeights[label]+=weight
            else:
                labelWeights[label]=weight
        maxlabel=self.getLabel()
        maxweight=-1
        for label in labelWeights:
            if(labelWeights[label]>maxweight):
                maxweight=labelWeights[label]
                maxlabel=label
        if(self.label==maxlabel):
            self.wasUpdated=False
        self.label=maxlabel
        return self.label
    
        
class whisperGraph():
    """A full graph of Whisper Nodes
        Feilds: List of whisper nodes"""
    def __init__(self,imageDescriptors,TrustName=True):
        """ __init__:
                Initailizes whisperGraph
            Params:
                imageDescriptors:
                    Image decriptors either in the form of a list of (label,descriptor), or just a list of decriptors,
                    where decriptors are np.array of shape (128,)
                TrustName(bool (optional, default= True)): 
                    If labels have already been given in imageDescriptors, determines if the node graph will "trust"
                    these names as correct for each image. If true, the node graph will not update the label on any
                    node where the label has been passed in
                """
        self.nodes=[]
        self.edges=[]
        
        if(imageDescriptors != None):
            for i in range(len(imageDescriptors)):
                if(isinstance(imageDescriptors[i],tuple)):
                    self.nodes.append(whisperNode(imageDescriptors[i][0],imageDescriptors[i][1],TrustName))
                else:
                    self.nodes.append(whisperNode(str(i),imageDescriptors[i]))
        else:
            for i in range(len(imageDescriptors)):
                self.nodes.append(whisperNode(str(i),imageDescriptors[i]))
    def add(self,imageDescriptor,name=None,TrustName=True):
        """add:
            Adds new node to graph. Note: you will need to run cluster again once adding a new node.
            Params:
                image descriptor-(np.array shape=(128,)):   
                    Array of image descriptors
                Name-(str (optional)):
                    Label for node
                TrustName(bool, (optional, default=True)):
                    Determines whether label is correct(true), or should be changed by labelUpdate(false).
                    If True, the new node will not update its label in updateLabel
                """
        if(name == None):
            self.nodes.append(whisperNode(str(len(nodes)),imageDescriptor))
        else
            self.nodes.append(whisperNode(name,imageDescriptor,TrustName))
    def cluster(self,verificationLevel=500):
        """cluster:
                Finds neighbors of nodes and clusters them using updateLabel. All nodes of the same label
                make up a cluster.
                Params:
                    verificationLevel(int (optional, default=500)):
                        The number of iterations through updateLabel done while the number of clusters remains constant
                        before quitting.
                        """
        for i in range(len(self.nodes)):
            nodesCopy=self.nodes.copy()
            del nodesCopy[i]
            edge=self.nodes[i].findNeighbors(nodesCopy)
            edge.insert(i,0)
            self.edges.append(edge)
        iterate=True
        labelNumber=len(self.nodes)
        verification=0
        while(iterate):
            cont=False
            labels=[]
            for node in self.nodes:
                labels.append(node.getLabel())
                node.updateLabel()
                cont=(cont or node.wasUpdated)
            cnt=collections.Counter(labels)
            labelN=len(cnt)
            if(labelN==labelNumber):
                verification+=1
            labelNumber=labelN
            iterate=(cont and verification<verificationLevel)
  
    def getLabels(self):
        """getLabels:
                Returns the label of each node"""
        labels=[]
        for node in self.nodes:
            labels.append(node.getLabel())
        return labels
    
    def plot(self):
        """plot:
                plots node graph"""
        plot_graph(tuple(self.nodes),self.edges)

    
