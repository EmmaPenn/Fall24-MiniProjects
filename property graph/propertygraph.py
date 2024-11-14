"""
File: propertygraph.py
Description: An implementation of a PropertyGraph consisting of
Node and Relationship objects.  Nodes and Relationships carry
properties.  Property graphs are used to represent connected knowledge.

"""


class Node:

    def __init__(self, name, category, props=None):
        """ Class constructor """
        self.name = name
        self.category = category
        self.props = {}
        if props:
            self.props[props[0]] = props[1]

    def __getitem__(self, key):
        """ Fetch a property from the node using []
         return None if property doesn't exist """
        if key in self.props.keys():
            return self.props[key]
        else:
            return None

    def __setitem__(self, key, value):
        """ Set a node property with a specified value using [] """
        self.props[key] = value


    def __eq__(self, other):
        """ Two nodes are equal if they have the same
        name and category irrespective of their properties """
        if isinstance(other, Node):
            return self.name == other.name and self.category == other.category
        else:
            return None


    def __hash__(self):
        """ By making Nodes hashable we can now
        store them as keys in a dictionary! """
        return hash((self.name, self.category))

    def __repr__(self):
        """ Output the node as a string in the following format:
        name:category<tab>properties.
        Note: __repr__ is more versatile than __str__ """
        if self.props:
             return f'Node({self.name}:{self.category}     {self.props})'
        else:
            return f'Node({self.name}:{self.category})'



class Relationship:

    def __init__(self, category, props=None):
        """ Class constructor """
        self.category = category
        self.props = {}
        if props:
            self.props[props[0]] = props[1]

    def __getitem__(self, key):
        """ Fetch a property from the node using []
         return None if property doesn't exist """
        if key in self.props.keys():
            return self.props[key]
        else:
            return None

    def __setitem__(self, key, value):
        """ Set a node property with a specified value using [] """
        self.props[key] = value

    def __repr__(self):
        """ Output the relationship as a string in the following format:
        :category<space>properties.
        Note: __repr__ is more versatile than __str__ """

        if self.props:
            return f'Relationship(:{self.category} {self.props})'
        else:
            return f'Relationship({self.category})'



class PropertyGraph:

    def __init__(self):
        """ Construct an empty property graph """
        self.propertyGraph = {}

    def add_node(self, node):
        """ Add a node to the property graph """
        self.propertyGraph[node] = []

    def add_relationship(self, src, targ, rel):
        """ Connect src and targ nodes via the specified directed relationship.
        If either src or targ nodes are not in the graph, add them.
        Note that there can be many relationships between two nodes! """
        if src not in self.propertyGraph.keys():
            self.propertyGraph[src] = []
        if targ not in self.propertyGraph.keys():
            self.propertyGraph[targ] = []
        list_src = self.propertyGraph[src]
        tup = (targ, rel)
        list_src.append(tup)

        self.propertyGraph[src] = list_src



    def get_nodes(self, name=None, category=None, key=None, value=None):
        """ Return the SET of nodes matching all the specified criteria.
        If the criterion is None it means that the particular criterion is ignored. """
        nodes = []
        for node in self.propertyGraph.keys():
            if name:
                if node.name != name:
                    continue
            if category:
                if node.category != category:
                    continue
            if key:
                if key in node.props.keys():
                    if node.props[key] != value:
                        continue
                else:
                    continue
            nodes.append(node)
        return set(nodes)


    def adjacent(self, node, node_category=None, rel_category=None):
        """ Return a set of all nodes that are adjacent to node.
        If specified include only adjacent nodes with the specified node_category.
        If specified include only adjacent nodes connected via relationships with
        the specified rel_category """
        related_nodes = []
        for relationship in self.propertyGraph[node]:
            node_adjacent = relationship[0]
            relationship_adjacent = relationship[1]
            if node_category:
                if node_adjacent.category != node_category:
                    continue
            if rel_category:
                if relationship_adjacent.category != rel_category:
                    continue
            related_nodes.append((node_adjacent, relationship_adjacent))
        return set(related_nodes)


    def subgraph(self, nodes):
        """ Return the subgraph as a PropertyGraph consisting of the specified
        set of nodes and all interconnecting relationships """
        subgraph = PropertyGraph()
        for node in nodes:
            subgraph.propertyGraph[node]= []
        return subgraph


    def __repr__(self):
        """ A string representation of the property graph
        Properties are not displaced.

        Node
            Relationship Node
            Relationship Node
            .
            .
            etc.
        Node
            Relationship Node
            Relationship Node
            .
            .
            etc.
        .
        .
        etc.
        """
        list_nodes = list(self.propertyGraph.keys())
        for src in list_nodes:
            information = self.propertyGraph[src]
            grouped_info = (src, information)


        return f'({grouped_info})'






