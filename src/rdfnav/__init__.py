from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Iterable, Self, cast
from rdflib import RDF, Graph, URIRef, Literal, IdentifiedNode
from rdflib.graph import _TripleType, _PredicateType, _ObjectType
from rdflib.query import ResultRow


@dataclass
class GraphNavigator:
    """
    Wraps an RDF graph and provides methods to navigate through it using URIs.
    """

    graph: Graph

    def __getitem__(self, uri: IdentifiedNode) -> UriNode:
        "Traverses to a given node"
        return UriNode(self, uri)

    def subjects(self, predicate: URIRef, object: URIRef) -> Iterable[UriNode]:
        """
        Yields navigator objects for all nodes that are subjects of the given predicate and object
        """
        for subj in self.graph.subjects(predicate, object):
            if isinstance(subj, IdentifiedNode):
                yield UriNode(self, subj)
            else:
                raise ValueError(
                    f"{subj} is being used as a subject, but isn't a URI or BNode, which doesn't follow the RDF spec."
                )

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

    def ask_query(self, query: str, **kwargs: Any) -> bool:
        """
        Executes a SPARQL ASK query on the graph.
        Returns True if the query returns any results, False otherwise.

        This is a type-safe version of the `query` method that expects an ASK query.
        """
        result = self.graph.query(query, **kwargs)
        if not result.type == "ASK":
            raise ValueError("query must be an ASK query")
        return bool(result)

    def describe_query(self, query: str, **kwargs: Any) -> Graph:
        """
        Executes a SPARQL DESCRIBE query on the graph.
        Returns a subgraph containing the results of the query.

        This is a type-safe version of the `query` method that expects a DESCRIBE query.
        """
        result = self.graph.query(query, **kwargs)
        if not result.type == "DESCRIBE":
            raise ValueError("query must be a DESCRIBE query")
        return cast(Graph, result.graph)

    def select_query(self, query: str, **kwargs: Any) -> Iterable[ResultRow]:
        """
        Executes a SPARQL SELECT query on the graph.
        Returns an iterable of tuples containing the results of the query.

        This is a type-safe version of the `query` method that expects a SELECT query.
        """
        result = self.graph.query(query, **kwargs)
        if not result.type == "SELECT":
            raise ValueError("query must be a SELECT query")
        for row in result:
            yield cast(ResultRow, row)

    def construct_query(self, query: str, **kwargs: Any) -> Graph:
        """
        Executes a SPARQL CONSTRUCT query on the graph.
        Returns a subgraph containing the results of the query.

        This is a type-safe version of the `query` method that expects a CONSTRUCT query.
        """
        result = self.graph.query(query, **kwargs)
        if not result.type == "CONSTRUCT":
            raise ValueError("query must be a CONSTRUCT query")
        return cast(Graph, result.graph)


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

    navigator: GraphNavigator
    iri: IdentifiedNode

    @property
    def graph(self) -> Graph:
        "Returns the graph that this node belongs to."
        return self.navigator.graph

    @property
    def suffix(self) -> str:
        "Returns the suffix of the URI, which is the last part after the last slash or hash."
        return self.graph.namespace_manager.compute_qname(str(self.iri))[2]

    def ref_objs_via(self, predicate: URIRef | None = None) -> Iterable[UriNode]:
        """
        Yields navigator objects for all nodes that can be reached from the current object using `predicate`.

        Params:
            predicate: Optionally, a specific predicate to follow to find subjects.
                If None, all objects that are URIs or BNodes that can be reached from the current object will be returned.
        """
        for obj in self.graph.objects(subject=self.iri, predicate=predicate):
            if isinstance(obj, IdentifiedNode):
                yield UriNode(self.navigator, obj)

    def ref_objs(self) -> Iterable[tuple[URIRef, UriNode]]:
        """
        Yields pairs of predicates and object nodes that can be reached from the current object.
        Only predicates that are URIs are included, literals are excluded.
        """
        for pred, obj in self.graph.predicate_objects(subject=self.iri):
            if isinstance(obj, IdentifiedNode) and isinstance(pred, URIRef):
                yield pred, UriNode(self.navigator, obj)

    def ref_objs_prefix(self, *prefixes: str) -> Iterable[tuple[URIRef, UriNode]]:
        """
        Yields tuples of (predicate, `UriNode`) for objects that can be reached from the current object using predicates that start with `prefix`.
        """
        for pred, obj in self.ref_objs():
            for prefix in prefixes:
                if str(pred).startswith(prefix):
                    yield pred, obj
                    break

    def ref_objs_sans_prefix(self, *prefixes: str) -> Iterable[tuple[str, UriNode]]:
        """
        Yields tuples of (predicate without prefix, `UriNode`) for all objects that can be reached from the current object,
        """
        for pred, obj in self.ref_objs():
            for prefix in prefixes:
                if str(pred).startswith(prefix):
                    yield pred.removeprefix(prefix), obj
                    break

    def ref_obj_via(self, predicate: URIRef) -> UriNode:
        """
        Yields one `UriNode` that can be reached from the current object using `predicate`.
        Fails if there are no objects or more than one object.
        """
        objs = self.ref_objs_via(predicate)
        return exactly_one(objs)

    def lit_objs_via(self, predicate: URIRef) -> Iterable[Any]:
        """
        Yields all literals that can be reached from the current object using `predicate`.
        """
        for obj in self.graph.objects(subject=self.iri, predicate=predicate):
            if isinstance(obj, Literal):
                yield obj.value

    def lit_objs(self) -> Iterable[tuple[URIRef, Any]]:
        """
        Yields pair of predicates and literal objects that can be reached from the current object.
        """
        for pred, obj in self.graph.predicate_objects(subject=self.iri):
            if isinstance(obj, Literal) and isinstance(pred, URIRef):
                yield pred, obj.value

    def lit_obj_via(self, predicate: URIRef) -> Any:
        """
        Returns one literal that can be reached from the current object using `predicate`.
        Fails if there are no objects or more than one object.
        """
        objs = self.lit_objs_via(predicate)
        return exactly_one(objs)

    def lit_objs_prefix(self, *prefixes: str) -> Iterable[tuple[URIRef, Any]]:
        """
        Yields tuples of (predicate, literal) for objects that can be reached from the current object using predicates that start with `prefix`.
        """
        for pred, obj in self.lit_objs():
            for prefix in prefixes:
                if str(pred).startswith(prefix):
                    yield pred, obj
                    break

    def lit_objs_sans_prefix(self, *prefixes: str) -> Iterable[tuple[str, Any]]:
        """
        Yields tuples of (predicate without prefix, literal) for all objects that can be reached from the current object.
        """
        for pred, obj in self.lit_objs():
            for prefix in prefixes:
                if str(pred).startswith(prefix):
                    yield pred.removeprefix(prefix), obj
                    break

    def ref_subjs_via(self, predicate: URIRef) -> Iterable[UriNode]:
        """
        Yields all URIs that can reach the current object using `predicate`, as `UriNode` instances.

        Params:
            predicate: Optionally, a specific predicate to follow to find subjects.
                If None, all subjects of the current object will be returned.
        """
        for subj in self.graph.subjects(predicate=predicate, object=self.iri):
            if isinstance(subj, IdentifiedNode):
                yield UriNode(self.navigator, subj)

    def ref_subjs(self) -> Iterable[UriNode]:
        """
        Yields all subjects that can reach the current object via one predicate, as `UriNode` instances.
        """
        for subj in self.graph.subjects(object=self.iri):
            if isinstance(subj, IdentifiedNode):
                yield UriNode(self.navigator, subj)

    def ref_subj_via(self, predicate: URIRef) -> UriNode:
        """
        Yields one `UriNode` that can reach the current object using `predicate`.
        Fails if there are no subjects or more than one subject.
        """
        subjs = self.ref_subjs_via(predicate)
        return exactly_one(subjs)

    def subgraph(self) -> Graph:
        """
        Returns a subgraph containing only the current node and anything traversable from it.
        """
        result = self.graph.query(
            """
            CONSTRUCT {
                ?s ?p ?o .
            }
            WHERE {
                # Find any subject that can be reached from the root node via any number of any predicate
                ?root !<>* ?s .
                # Then return all triples whose subject is that node
                ?s ?p ?o . 
            }
        """,
            initBindings={"root": self.iri},
        )
        if result.graph is None:
            raise ValueError("Subgraph query did not return a Graph")
        return result.graph

    def cbd(self) -> Graph:
        """
        Returns the Concise Bounded Description (CBD) of the current node
        """
        return self.graph.cbd(self.iri)

    def change_iri(self, new_iri: URIRef) -> Self:
        """
        Changes all instance of the current IRI to a new IRI.
        This mutates the graph.
        """
        for triple in self.graph:
            if self.iri in triple:
                # We want the minimal mutations to the graph, so rather than creating a new one we remove only the triple that contains the old IRI
                self.graph.remove(triple)
                # Type is fine, as we're guaranteed to only ever add UriRefs
                self.graph.add(
                    cast(
                        _TripleType,
                        tuple(new_iri if x == self.iri else x for x in triple),
                    )
                )

        return self

    def delete(self, pred: _PredicateType, obj: _ObjectType | None = None) -> Self:
        """
        Deletes all triples that have the current IRI as subject and the given predicate and optionally object.
        This mutates the graph.
        """
        for trip in self.graph.triples((self.iri, pred, obj)):
            self.graph.remove(trip)
        return self

    def add(self, predicate: _PredicateType, obj: _ObjectType) -> Self:
        """
        Adds a new triple with the current IRI as subject, the given predicate and object.
        This mutates the graph.
        """
        self.graph.add((self.iri, predicate, obj))
        return self

    def replace(self, predicate: _PredicateType, obj: _ObjectType) -> Self:
        """
        Replaces all triples with the current IRI as subject and the given predicate with a new object.
        This mutates the graph.
        """
        self.delete(predicate)
        self.add(predicate, obj)
        return self

    def select_query(
        self, query: str, binding: str = "node", **kwargs: Any
    ) -> Iterable[ResultRow]:
        """
        Executes a SPARQL SELECT query on the graph, with the current node pre-bound into the graph.

        Params:
            query: The SPARQL query to execute.
            binding: The variable name to bind the current node to in the query. Defaults to "node".
        """
        if "initBindings" in kwargs:
            kwargs["initBindings"][binding] = self.iri
        else:
            kwargs["initBindings"] = {binding: self.iri}

        return self.navigator.select_query(query, **kwargs)

    def describe_query(self, query: str, binding: str = "node", **kwargs: Any) -> Graph:
        """
        Executes a SPARQL DESCRIBE query on the graph, with the current node pre-bound into the graph.

        Params:
            query: The SPARQL query to execute.
            binding: The variable name to bind the current node to in the query. Defaults to "node".
        """
        if "initBindings" in kwargs:
            kwargs["initBindings"][binding] = self.iri
        else:
            kwargs["initBindings"] = {binding: self.iri}

        return self.navigator.describe_query(query, **kwargs)

    def construct_query(
        self, query: str, binding: str = "node", **kwargs: Any
    ) -> Graph:
        """
        Executes a SPARQL CONSTRUCT query on the graph, with the current node pre-bound into the graph.

        Params:
            query: The SPARQL query to execute.
            binding: The variable name to bind the current node to in the query. Defaults to "node".
        """
        if "initBindings" in kwargs:
            kwargs["initBindings"][binding] = self.iri
        else:
            kwargs["initBindings"] = {binding: self.iri}

        return self.navigator.construct_query(query, **kwargs)

    def ask_query(self, query: str, binding: str = "node", **kwargs: Any) -> bool:
        """
        Executes a SPARQL ASK query on the graph, with the current node pre-bound into the graph.

        Params:
            query: The SPARQL query to execute.
            binding: The variable name to bind the current node to in the query. Defaults to "node".
        """
        if "initBindings" in kwargs:
            kwargs["initBindings"][binding] = self.iri
        else:
            kwargs["initBindings"] = {binding: self.iri}

        return self.navigator.ask_query(query, **kwargs)

    def is_instance_of(self, type_uri: URIRef) -> bool:
        """
        Checks if the current node is a subclass of the given type URI.
        """
        return self.ask_query(
            # Find the type of `node` and then check if it is a subclass of `type_uri`
            """
            ASK WHERE {
                ?node a ?immediate_type .
                ?immediate_type rdfs:subClassOf* ?type .
            }
            """,
            initBindings={"type": type_uri},
        )

    def is_subclass_of(self, type_uri: URIRef) -> bool:
        """
        Checks if the current node is a subclass of the given type URI.
        """
        return self.ask_query(
            """
            ASK WHERE {
                ?node rdfs:subClassOf* ?type .
            }
            """,
            initBindings={"type": type_uri},
        )
