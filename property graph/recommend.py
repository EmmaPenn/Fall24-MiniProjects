'''
Filename: recommendation.py

A Recommendation system to use on a property graph database. Hardcodes in a Property Graph and Generates Some Book Recommendations
based on relationships within the property graph
'''

from propertygraph import Node
from propertygraph import Relationship
from propertygraph import PropertyGraph
'''

Original Property Graph: 
{Node(Emily:Person): [(Node(Spencer:Person), Relationship(known)), (Node(Database Design:Book     {'Price': 195.0}), Relationship(bought))],
Node(Spencer:Person): [(Node(Emily:Person), Relationship(known)), (Node(Brendan:Person), Relationship(known)), (Node(Cosmos:Book     {'Price': 17.0}), Relationship(bought)), (Node(Database Design:Book     {'Price': 195.0}), Relationship(bought))], 
Node(Brendan:Person): [(Node(DNA and You:Book     {'Price': 11.5}), Relationship(bought)), (Node(Database Design:Book     {'Price': 195.0}), Relationship(bought))], 
Node(Database Design:Book     {'Price': 195.0}): [], 
Node(Cosmos:Book     {'Price': 17.0}): [], 
Node(DNA and You:Book     {'Price': 11.5}): [], 
Node(Trevor:Person): [(Node(Cosmos:Book     {'Price': 17.0}), Relationship(bought)), (Node(Database Design:Book     {'Price': 195.0}), Relationship(bought))], 
Node(Paxtyn:Person): [(Node(Database Design:Book     {'Price': 195.0}), Relationship(bought)), (Node(The Life of Cronkite:Book     {'Price': 29.95}), Relationship(bought))], 
Node(The Life of Cronkite:Book     {'Price': 29.95}): []}


Spencer's Recommendation subgraph: 
{Node(Spencer:Person): [(Node(DNA and You:Book     {'Price': 11.5}), Relationship(Recommendation))], 
Node(DNA and You:Book     {'Price': 11.5}): []}


Added Recommendation to the Property Graph: 
{Node(Emily:Person): [(Node(Spencer:Person), Relationship(known)), (Node(Database Design:Book     {'Price': 195.0}), Relationship(bought))], 
Node(Spencer:Person): [(Node(Emily:Person), Relationship(known)), (Node(Brendan:Person), Relationship(known)), (Node(Cosmos:Book     {'Price': 17.0}), Relationship(bought)), (Node(Database Design:Book     {'Price': 195.0}), Relationship(bought)), (Node(DNA and You:Book     {'Price': 11.5}), Relationship(Recommendation))], 
Node(Brendan:Person): [(Node(DNA and You:Book     {'Price': 11.5}), Relationship(bought)), (Node(Database Design:Book     {'Price': 195.0}), Relationship(bought))], 
Node(Database Design:Book     {'Price': 195.0}): [],
 Node(Cosmos:Book     {'Price': 17.0}): [], 
 Node(DNA and You:Book     {'Price': 11.5}): [], 
 Node(Trevor:Person): [(Node(Cosmos:Book     {'Price': 17.0}), Relationship(bought)), (Node(Database Design:Book     {'Price': 195.0}), Relationship(bought))], 
 Node(Paxtyn:Person): [(Node(Database Design:Book     {'Price': 195.0}), Relationship(bought)), (Node(The Life of Cronkite:Book     {'Price': 29.95}), Relationship(bought))], 
 Node(The Life of Cronkite:Book     {'Price': 29.95}): []}

Process finished with exit code 0



'''

def recommend(og_person, og_graph, rel):
    '''

    A Function that will create a subgraph of a specified person and their book recommendations, returns both the subgraph
    and the book recommendations
    '''
    subgraph = og_graph.subgraph([og_person])
    relationship_knows = og_graph.adjacent(node=og_person, node_category="Person", rel_category="known")

    bought_books = og_graph.adjacent(node=og_person, node_category="Book")

    book_recs = []
    for person in relationship_knows:
        person_node = person[0]
        books = og_graph.adjacent(node=person_node, node_category="Book", rel_category="bought")
        # filter out the books that the person already has
        for book in books:
            if book in bought_books:
                continue
            else:
                subgraph.add_relationship(og_person, book[0], rel = rel)
                book_recs.append(book[0])
        return subgraph, book_recs

def add_recommendations_to_og(og_graph, source, book_recs, rel):
    '''
    Takes in the original graph and new book recs and adds the relationships to the source person in the original subgraph
    '''
    for book in book_recs:
        og_graph.add_relationship(source, book, rel)

    return og_graph


def main():


    # person nodes
    emily = Node("Emily", "Person")

    spencer = Node("Spencer", "Person")

    brendan = Node("Brendan", "Person")

    trevor = Node("Trevor", "Person")

    paxtyn = Node("Paxtyn", "Person")

    # Book Nodes
    cosmos = Node("Cosmos", "Book", ("Price", 17.00))


    database_design = Node("Database Design", "Book", ("Price", 195.00))

    the_life_of_cronkite = Node("The Life of Cronkite", "Book", ("Price", 29.95))

    dna = Node("DNA and You", "Book", ("Price", 11.50))

    # Relationship Objects
    known = Relationship("known")
    bought = Relationship("bought")

    # Constructing the Property Graph
    og_graph = PropertyGraph()

    # adding known relationships
    og_graph.add_relationship(emily, spencer, known)

    og_graph.add_relationship(spencer, emily, known)

    og_graph.add_relationship(spencer, brendan, known)

    # adding book relationships
    og_graph.add_relationship(emily, database_design, bought)

    og_graph.add_relationship(spencer, cosmos, bought)

    og_graph.add_relationship(spencer, database_design, bought)

    og_graph.add_relationship(brendan, dna, bought)

    og_graph.add_relationship(trevor, cosmos, bought)

    og_graph.add_relationship(trevor, database_design, bought)

    og_graph.add_relationship(paxtyn, database_design, bought)

    og_graph.add_relationship(paxtyn, the_life_of_cronkite, bought)

    og_graph.add_relationship(brendan, database_design, bought)

    # Printing out the first property graph

    print(og_graph.propertyGraph)


    recommendation_relationship = Relationship("Recommendation")

    subgraph_recommendation, book_recs = recommend(spencer, og_graph, recommendation_relationship)

    # Get Spencer's recommendations
    print(subgraph_recommendation.propertyGraph)


    # add the recommendation relationships to the new graph
    new_propertygraph = add_recommendations_to_og(og_graph, spencer, book_recs, recommendation_relationship)

    print(new_propertygraph.propertyGraph)










if __name__ == "__main__":
    main()
