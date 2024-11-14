'''
Filenmae: test_propertygraphy.py
A testfile using pytest for the propertygraph.py file that checks if the functions are working properly
'''

import pytest

from propertygraph import Node
from propertygraph import Relationship
from propertygraph import PropertyGraph


# Setting up the testing fixtures

@pytest.fixture
def node_a():
    return Node("Little Women", "Literary Fiction")

@pytest.fixture
def node_b():
    return Node("Little Women", "Drama")

@pytest.fixture
def node_c():
    return Node("Little Women", "Literary Fiction", ("price", 4))

@pytest.fixture
def node_d():
    return Node("Of Mice and Men", "Drama")
@pytest.fixture
def node_e():
    return Node("Of Mice and Men", "Drama", ("sold", 2))

# setting up relationship fixtures for testing
@pytest.fixture
def rel_a():
    return Relationship("Genre")

@pytest.fixture
def rel_b():
    return Relationship("Media")

@pytest.fixture
def rel_c():
    return Relationship("Type", ("Added", "Months Ago"))

@pytest.fixture
def rel_d():
    return Relationship("Type", ("Added", "Weeks Ago"))

# set up the propertygraph fixture
@pytest.fixture
def pgraph():
    return PropertyGraph()
# Setting up the Python tests

def test_constructor(node_a, node_c, rel_a, pgraph):
    # setting up the test for the init function
    assert isinstance(node_a, Node),"Did not set up nodes to be intitiated with no properties"
    assert isinstance(node_c, Node),"Did not set up Nodes properly"
    assert isinstance(rel_a, Relationship), "Did not set up Relationship Properly"
    assert isinstance(pgraph, PropertyGraph), "Did not Set up PropertyGraph Properly"

def test_equals(node_a, node_c, node_b, node_d):
    # test for equals function AND Hash function
    assert node_a != node_b, "Equality does not include category "
    assert node_a == node_c, "Equality takes into account the properties"
    assert node_b != node_d, "Equality does not take into account"

def test_getitem(node_a, node_c, node_e, rel_a, rel_c):
    # test for the get_item function
    assert node_a["price"] == None, "Retrieves a Property with a key that does not exist"
    assert node_c["price"] == 4, "Retrieves a value from the key that is not accurate"
    assert node_e["price"] == None, "Does Not retrieve Values Based On Keys"
    assert rel_a["Price"] == None, "Retrieves properties where non exist"
    assert rel_c["Added"] == "Months Ago", "Does Not Retrieve Properties for Relationships"

def test_setitem(node_a, node_c, node_e, rel_a, rel_c, rel_d):
    # test for set item function
    node_a["price"] = 5
    node_c["price"] = 10
    node_e["price"] = 0
    rel_a["prior"] = "Strangers"
    rel_c["Added"] = "Weeks Ago"
    rel_d["Price"] = 15
    assert node_a.props == {"price" : 5}, "Does not Update the Dictionary"
    assert node_c.props == {"price": 10}, "Does not Update existing keys"
    assert node_e.props == {"sold" : 2, "price": 0}, "Overrides Current Property Values With Different Keys"
    assert rel_a.props == {"prior" : "Strangers"}, "Does not Add Keys"
    assert rel_c.props == {"Added": "Weeks Ago"}, "Does not Update Existing keys"
    assert rel_d.props == {"Added": "Weeks Ago", "Price": 15}, "Overrides Current Property Values With Different Keys "


def test_add_node(pgraph, node_b):
    # test to add a node
    pgraph.add_node(node_b)
    assert pgraph.propertyGraph == {node_b: []}, "Does not initiate a node with an empty list"

def test_add_relationship(pgraph, node_b, node_d, node_e, rel_a):
    # test to add a directed relationship
    pgraph.add_node(node_b)
    pgraph.add_node(node_d)
    pgraph.add_relationship(node_b, node_d, rel_a)

    assert pgraph.propertyGraph[node_b] == [(node_d, rel_a)], "Add Relationship does not add the proper relationship to node b"
    assert pgraph.propertyGraph[node_d] == [], "Add Relationship adds the directed relationship to both nodes when it is only meant to one node"

    pgraph.add_relationship(node_b, node_e, rel_a)
    assert pgraph.propertyGraph[node_b] == [(node_d, rel_a), (node_e, rel_a)], "Add Relationship does not add multiple nodes to the list and/or overrides current list and does not add when the target node doesn't exist"

    node_z = Node("Frankenstein", "Drama")
    pgraph.add_relationship(node_z, node_b, rel_a)
    assert pgraph.propertyGraph[node_z] == [(node_b, rel_a)], "Property Graph does not add a new node/relationship if the target node does not exist"


def test_get_nodes(pgraph, node_b, node_d, node_a, node_e):
    # test to filter out and return certain nodes
    pgraph.add_node(node_b)
    pgraph.add_node(node_d)
    pgraph.add_node(node_a)
    pgraph.add_node(node_e)
    drama_nodes = pgraph.get_nodes(category = "Drama")
    lw_nodes = pgraph.get_nodes(name = "Little Women")
    assert drama_nodes == {node_b,node_d, node_e}, "Does not return by category only"
    assert lw_nodes == {node_b,node_a}, "Does not return by name only"
    assert pgraph.get_nodes(name = "Dracula") == set(), "Returns nodes when none fit the filter"
    assert pgraph.get_nodes(category = "Thriller")  == set(), "Returns nodes when none fit the filter"
    assert pgraph.get_nodes(name = "Little Women", category = "Drama") == {node_b}, "Does not filter on multiple filters"
    assert pgraph.get_nodes(key = "price", value = 4) == set(), "Returns key/value pairs not in the property graph"

def test_adjacent(pgraph, node_a, node_e, node_d, rel_a, rel_b):
    # test to get all the adjacent nodes function
    pgraph.add_node(node_a)
    pgraph.add_node(node_e)
    pgraph.add_node(node_d)

    pgraph.add_relationship(node_a, node_e, rel_a)
    pgraph.add_relationship(node_a, node_d, rel_b)

    assert pgraph.adjacent(node_a) == {(node_e, rel_a), (node_d, rel_b)}, "Does Not Return All Relationship Types for Adjacent Nodes"
    assert pgraph.adjacent(node_d) == set(), "Adds Nodes to Adjacency where there is none"

def test_subgraph(pgraph, node_a, node_b, node_c):
    # test to get the subgraph property graph
    pgraph.add_node(node_a)
    pgraph.add_node(node_b)
    pgraph.add_node(node_c)

    assert pgraph.subgraph([node_a]).propertyGraph == {node_a: []}, "Does not initiate Subgraph Dictionary Properly"
    assert pgraph.subgraph([node_a, node_b]).propertyGraph == {node_a: [], node_b: []}, "Does not Add multiple nodes to the Subgraph"










