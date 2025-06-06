from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Iterable
from rdflib import RDF, Graph, Node, URIRef, Literal, IdentifiedNode

@dataclass
class GraphNavigator:
    """
    Wraps an RDF graph and provides methods to navigate through it using URIs.
    """
    graph: Graph

    def __getitem__(self, uri: IdentifiedNode) -> UriNode:
        "Traverses to a given node"
        return UriNode(self.graph, uri)

    def subjects(self, predicate: URIRef, object: URIRef) -> Iterable[UriNode]:
        """
        Yields navigator objects for all nodes that are subjects of the given predicate and object
        """
        for subj in self.graph.subjects(predicate, object):
            yield UriNode(self.graph, subj)
    
    def subject(self, predicate: URIRef, object: URIRef) -> UriNode:
        """
        Yields a single navigator object for the subject of the given predicate and object.
        Raises an error if there are is not exactly one such subject.
        """
        subjects = list(self.subjects(predicate, object))
        if len(subjects) == 0:
            raise ValueError(f"Subject not found for {predicate} {object}")
        elif len(subjects) > 1:
            raise ValueError(f"Multiple subjects found for {predicate} {object}")
        return subjects[0]

    def instances(self, type_uri: URIRef) -> Iterable[UriNode]:
        """
        Yields navigator objects for all instances of the given type URI.
        """
        return self.subjects(predicate=RDF.type, object=type_uri)
    
    def instance(self, type_uri: URIRef) -> UriNode:
        """
        Returns a single navigator object for an instance of the given type URI.
        """
        instances = self.instances(type_uri)
        return exactly_one(instances)


def exactly_one[T](items: Iterable[T]) -> T:
    """
    Helper function to ensure that exactly one item is returned from an iterable.
    Raises ValueError if there are no items or more than one item.
    """
    items_list = list(items)
    if len(items_list) == 0:
        raise ValueError("No items found")
    elif len(items_list) > 1:
        raise ValueError("Multiple items found")
    return items_list[0]

@dataclass
class UriNode:
    """
    Navigation helper for a single node in the RDF graph, identified by a URI.
    Typically this is created by the `GraphNavigator` class.
    """
    graph: Graph
    iri: Node

    @property
    def suffix(self) -> str:
        "Returns the suffix of the URI, which is the last part after the last slash or hash."
        return self.graph.namespace_manager.compute_qname(str(self.iri))[2]

    def ref_objs(self, predicate: URIRef) -> Iterable[UriNode]:
        """
        Yields navigator objects for all nodes that can be reached from the current object using `predicate`.
        """
        for obj in self.graph.objects(subject=self.iri, predicate=predicate):
            if not isinstance(obj, IdentifiedNode):
                raise ValueError(f"Object is not a URI for {self.iri} {predicate}")
            yield UriNode(self.graph, obj)
    
    def ref_obj(self, predicate: URIRef) -> UriNode:
        """
        Yields one `UriNode` that can be reached from the current object using `predicate`.
        Fails if there are no objects or more than one object.
        """
        objs = self.ref_objs(predicate)
        return exactly_one(objs)

    def lit_objs(self, predicate: URIRef) -> Iterable[Any]:
        """
        Yields all literals that can be reached from the current object using `predicate`.
        """
        for obj in self.graph.objects(subject=self.iri, predicate=predicate):
            if not isinstance(obj, Literal):
                raise ValueError(f"Object is not a Literal for {self.iri} {predicate}")
            yield obj.value
    
    def lit_obj(self, predicate: URIRef) -> Any:
        """
        Returns one literal that can be reached from the current object using `predicate`.
        Fails if there are no objects or more than one object.
        """
        objs = self.lit_objs(predicate)
        return exactly_one(objs)

    def ref_subjs(self, predicate: URIRef) -> Iterable[UriNode]:
        """
        Yields all URIs that can reach the current object using `predicate`, as `UriNode` instances.
        """
        for subj in self.graph.subjects(predicate=predicate, object=self.iri):
            if not isinstance(subj, IdentifiedNode):
                raise ValueError(f"Subject is not a URI or BNode for {subj} {predicate}")
            yield UriNode(self.graph, subj)
    
    def ref_subj(self, predicate: URIRef) -> UriNode:
        """
        Yields one `UriNode` that can reach the current object using `predicate`.
        Fails if there are no subjects or more than one subject.
        """
        subjs = self.ref_subjs(predicate)
        return exactly_one(subjs)

    def subgraph(self) -> Graph:
        """
        Returns a subgraph containing only the current node and anything traversable from it.
        """
        if not isinstance(self.iri, IdentifiedNode):
            raise ValueError(f"Cannot create subgraph for non-URI node {self.iri}")

        result = self.graph.query("""
            CONSTRUCT {
                ?s ?p ?o .
            }
            WHERE {
                # Find any subject that can be reached from the root node via any number of any predicate
                ?root !<>* ?s .
                # Then return all triples whose subject is that node
                ?s ?p ?o . 
            }
        """, initBindings={'root': self.iri})
        if result.graph is None:
            raise ValueError("Subgraph query did not return a Graph")
        return result.graph

    # def navigate(self, predicate: URIRef) -> 'Subject':
    #     obj = self.graph.value(subject=self.uri, predicate=predicate)
    #     if obj is None:
    #         raise ValueError(f"Object not found for {self.uri} {predicate}")
    #     if not isinstance(obj, URIRef):
    #         raise ValueError(f"Object is not a URI for {self.uri} {predicate}")
        
    #     return Subject(self.graph, obj)

    # def literal(self, predicate: URIRef) -> Any:
    #     obj = self.graph.value(subject=self.uri, predicate=predicate)
    #     if obj is None:
    #         raise ValueError(f"Object not found for {self.uri} {predicate}")
    #     if not isinstance(obj, Literal):
    #         raise ValueError(f"Object is not a Literal for {self.uri} {predicate}")
        
    #     return obj.value
