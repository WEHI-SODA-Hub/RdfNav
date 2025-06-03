from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Iterable
from rdflib import Graph, Node, URIRef, Literal

@dataclass
class GraphNavigator:
    graph: Graph

    def __getitem__(self, uri: URIRef) -> UriNode:
        return UriNode(self.graph, uri)

    def subjects(self, predicate: URIRef, object: URIRef) -> Iterable[UriNode]:
        for subj in self.graph.subjects(predicate, object):
            yield UriNode(self.graph, subj)
    
    def subject(self, predicate: URIRef, object: URIRef) -> UriNode:
        subjects = list(self.subjects(predicate, object))
        if len(subjects) == 0:
            raise ValueError(f"Subject not found for {predicate} {object}")
        elif len(subjects) > 1:
            raise ValueError(f"Multiple subjects found for {predicate} {object}")
        return subjects[0]

@dataclass
class UriNode:
    graph: Graph
    iri: Node

    @property
    def suffix(self) -> str:
        return self.graph.namespace_manager.compute_qname(str(self.iri))[2]

    def ref_objs(self, predicate: URIRef) -> Iterable[UriNode]:
        """
        Yields all URIs that can be reached from the current object using `predicate`, as `UriNode` instances.
        """
        for obj in self.graph.objects(subject=self.iri, predicate=predicate):
            if not isinstance(obj, URIRef):
                raise ValueError(f"Object is not a URI for {self.iri} {predicate}")
            yield UriNode(self.graph, obj)
    
    def ref_obj(self, predicate: URIRef) -> UriNode:
        """
        Yields one `UriNode` that can be reached from the current object using `predicate`.
        Fails if there are no objects or more than one object.
        """
        objs = list(self.ref_objs(predicate))
        if len(objs) == 0:
            raise ValueError(f"Object not found for {self.iri} {predicate}")
        elif len(objs) > 1:
            raise ValueError(f"Multiple objects found for {self.iri} {predicate}")
        return objs[0]

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
        objs = list(self.lit_objs(predicate))
        if len(objs) == 0:
            raise ValueError(f"Object not found for {self.iri} {predicate}")
        elif len(objs) > 1:
            raise ValueError(f"Multiple objects found for {self.iri} {predicate}")
        return objs[0]

    def ref_subjs(self, predicate: URIRef) -> Iterable[UriNode]:
        """
        Yields all URIs that can reach the current object using `predicate`, as `UriNode` instances.
        """
        for subj in self.graph.subjects(predicate=predicate, object=self.iri):
            if not isinstance(subj, URIRef):
                raise ValueError(f"Subject is not a URI for {subj} {predicate}")
            yield UriNode(self.graph, subj)
    
    def ref_subj(self, predicate: URIRef) -> UriNode:
        """
        Yields one `UriNode` that can reach the current object using `predicate`.
        Fails if there are no subjects or more than one subject.
        """
        subjs = list(self.ref_subjs(predicate))
        if len(subjs) == 0:
            raise ValueError(f"Subject not found for {self.iri} {predicate}")
        elif len(subjs) > 1:
            raise ValueError(f"Multiple subjects found for {self.iri} {predicate}")
        return subjs[0]

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
