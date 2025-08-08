## rdfnav

**Classes:**

- [**GraphNavigator**](#rdfnav.GraphNavigator) – Wraps an RDF graph and provides methods to navigate through it using URIs.
- [**UriNode**](#rdfnav.UriNode) – Navigation helper for a single node in the RDF graph, identified by a URI.

**Functions:**

- [**exactly_one**](#rdfnav.exactly_one) – Helper function to ensure that exactly one item is returned from an iterable.

### rdfnav.GraphNavigator

```python
GraphNavigator(graph)
```

Wraps an RDF graph and provides methods to navigate through it using URIs.

**Functions:**

- [**ask_query**](#rdfnav.GraphNavigator.ask_query) – Executes a SPARQL ASK query on the graph.
- [**construct_query**](#rdfnav.GraphNavigator.construct_query) – Executes a SPARQL CONSTRUCT query on the graph.
- [**describe_query**](#rdfnav.GraphNavigator.describe_query) – Executes a SPARQL DESCRIBE query on the graph.
- [**instance**](#rdfnav.GraphNavigator.instance) – Returns a single navigator object for an instance of the given type URI.
- [**instances**](#rdfnav.GraphNavigator.instances) – Yields navigator objects for all instances of the given type URI.
- [**select_query**](#rdfnav.GraphNavigator.select_query) – Executes a SPARQL SELECT query on the graph.
- [**subject**](#rdfnav.GraphNavigator.subject) – Yields a single navigator object for the subject of the given predicate and object.
- [**subjects**](#rdfnav.GraphNavigator.subjects) – Yields navigator objects for all nodes that are subjects of the given predicate and object

**Attributes:**

- [**graph**](#rdfnav.GraphNavigator.graph) (<code>[Graph](#rdflib.Graph)</code>) –

#### rdfnav.GraphNavigator.ask_query

```python
ask_query(query, **kwargs)
```

Executes a SPARQL ASK query on the graph.
Returns True if the query returns any results, False otherwise.

This is a type-safe version of the `query` method that expects an ASK query.

#### rdfnav.GraphNavigator.construct_query

```python
construct_query(query, **kwargs)
```

Executes a SPARQL CONSTRUCT query on the graph.
Returns a subgraph containing the results of the query.

This is a type-safe version of the `query` method that expects a CONSTRUCT query.

#### rdfnav.GraphNavigator.describe_query

```python
describe_query(query, **kwargs)
```

Executes a SPARQL DESCRIBE query on the graph.
Returns a subgraph containing the results of the query.

This is a type-safe version of the `query` method that expects a DESCRIBE query.

#### rdfnav.GraphNavigator.graph

```python
graph: Graph
```

#### rdfnav.GraphNavigator.instance

```python
instance(type_uri)
```

Returns a single navigator object for an instance of the given type URI.

#### rdfnav.GraphNavigator.instances

```python
instances(type_uri)
```

Yields navigator objects for all instances of the given type URI.

#### rdfnav.GraphNavigator.select_query

```python
select_query(query, **kwargs)
```

Executes a SPARQL SELECT query on the graph.
Returns an iterable of tuples containing the results of the query.

This is a type-safe version of the `query` method that expects a SELECT query.

#### rdfnav.GraphNavigator.subject

```python
subject(predicate, object)
```

Yields a single navigator object for the subject of the given predicate and object.
Raises an error if there are is not exactly one such subject.

#### rdfnav.GraphNavigator.subjects

```python
subjects(predicate, object)
```

Yields navigator objects for all nodes that are subjects of the given predicate and object

### rdfnav.UriNode

```python
UriNode(navigator, iri)
```

Navigation helper for a single node in the RDF graph, identified by a URI.
Typically this is created by the `GraphNavigator` class.

**Functions:**

- [**add**](#rdfnav.UriNode.add) – Adds a new triple with the current IRI as subject, the given predicate and object.
- [**ask_query**](#rdfnav.UriNode.ask_query) – Executes a SPARQL ASK query on the graph, with the current node pre-bound into the graph.
- [**cbd**](#rdfnav.UriNode.cbd) – Returns the Concise Bounded Description (CBD) of the current node
- [**change_iri**](#rdfnav.UriNode.change_iri) – Changes all instance of the current IRI to a new IRI.
- [**construct_query**](#rdfnav.UriNode.construct_query) – Executes a SPARQL CONSTRUCT query on the graph, with the current node pre-bound into the graph.
- [**delete**](#rdfnav.UriNode.delete) – Deletes all triples that have the current IRI as subject and the given predicate and optionally object.
- [**describe_query**](#rdfnav.UriNode.describe_query) – Executes a SPARQL DESCRIBE query on the graph, with the current node pre-bound into the graph.
- [**is_instance_of**](#rdfnav.UriNode.is_instance_of) – Checks if the current node is a subclass of the given type URI.
- [**is_subclass_of**](#rdfnav.UriNode.is_subclass_of) – Checks if the current node is a subclass of the given type URI.
- [**lit_obj_via**](#rdfnav.UriNode.lit_obj_via) – Returns one literal that can be reached from the current object using `predicate`.
- [**lit_objs**](#rdfnav.UriNode.lit_objs) – Yields pair of predicates and literal objects that can be reached from the current object.
- [**lit_objs_prefix**](#rdfnav.UriNode.lit_objs_prefix) – Yields tuples of (predicate, literal) for objects that can be reached from the current object using predicates that start with `prefix`.
- [**lit_objs_sans_prefix**](#rdfnav.UriNode.lit_objs_sans_prefix) – Yields tuples of (predicate without prefix, literal) for all objects that can be reached from the current object.
- [**lit_objs_via**](#rdfnav.UriNode.lit_objs_via) – Yields all literals that can be reached from the current object using `predicate`.
- [**ref_obj_via**](#rdfnav.UriNode.ref_obj_via) – Yields one `UriNode` that can be reached from the current object using `predicate`.
- [**ref_objs**](#rdfnav.UriNode.ref_objs) – Yields pairs of predicates and object nodes that can be reached from the current object.
- [**ref_objs_prefix**](#rdfnav.UriNode.ref_objs_prefix) – Yields tuples of (predicate, `UriNode`) for objects that can be reached from the current object using predicates that start with `prefix`.
- [**ref_objs_sans_prefix**](#rdfnav.UriNode.ref_objs_sans_prefix) – Yields tuples of (predicate without prefix, `UriNode`) for all objects that can be reached from the current object,
- [**ref_objs_via**](#rdfnav.UriNode.ref_objs_via) – Yields navigator objects for all nodes that can be reached from the current object using `predicate`.
- [**ref_subj_via**](#rdfnav.UriNode.ref_subj_via) – Yields one `UriNode` that can reach the current object using `predicate`.
- [**ref_subjs**](#rdfnav.UriNode.ref_subjs) – Yields all subjects that can reach the current object via one predicate, as `UriNode` instances.
- [**ref_subjs_via**](#rdfnav.UriNode.ref_subjs_via) – Yields all URIs that can reach the current object using `predicate`, as `UriNode` instances.
- [**replace**](#rdfnav.UriNode.replace) – Replaces all triples with the current IRI as subject and the given predicate with a new object.
- [**select_query**](#rdfnav.UriNode.select_query) – Executes a SPARQL SELECT query on the graph, with the current node pre-bound into the graph.
- [**subgraph**](#rdfnav.UriNode.subgraph) – Returns a subgraph containing only the current node and anything traversable from it.

**Attributes:**

- [**graph**](#rdfnav.UriNode.graph) (<code>[Graph](#rdflib.Graph)</code>) – Returns the graph that this node belongs to.
- [**iri**](#rdfnav.UriNode.iri) (<code>[Node](#rdflib.Node)</code>) –
- [**navigator**](#rdfnav.UriNode.navigator) (<code>[GraphNavigator](#rdfnav.GraphNavigator)</code>) –
- [**suffix**](#rdfnav.UriNode.suffix) (<code>[str](#str)</code>) – Returns the suffix of the URI, which is the last part after the last slash or hash.

#### rdfnav.UriNode.add

```python
add(predicate, obj)
```

Adds a new triple with the current IRI as subject, the given predicate and object.
This mutates the graph.

#### rdfnav.UriNode.ask_query

```python
ask_query(query, binding='node', **kwargs)
```

Executes a SPARQL ASK query on the graph, with the current node pre-bound into the graph.

**Parameters:**

- **query** (<code>[str](#str)</code>) – The SPARQL query to execute.
- **binding** (<code>[str](#str)</code>) – The variable name to bind the current node to in the query. Defaults to "node".

#### rdfnav.UriNode.cbd

```python
cbd()
```

Returns the Concise Bounded Description (CBD) of the current node

#### rdfnav.UriNode.change_iri

```python
change_iri(new_iri)
```

Changes all instance of the current IRI to a new IRI.
This mutates the graph.

#### rdfnav.UriNode.construct_query

```python
construct_query(query, binding='node', **kwargs)
```

Executes a SPARQL CONSTRUCT query on the graph, with the current node pre-bound into the graph.

**Parameters:**

- **query** (<code>[str](#str)</code>) – The SPARQL query to execute.
- **binding** (<code>[str](#str)</code>) – The variable name to bind the current node to in the query. Defaults to "node".

#### rdfnav.UriNode.delete

```python
delete(pred, obj=None)
```

Deletes all triples that have the current IRI as subject and the given predicate and optionally object.
This mutates the graph.

#### rdfnav.UriNode.describe_query

```python
describe_query(query, binding='node', **kwargs)
```

Executes a SPARQL DESCRIBE query on the graph, with the current node pre-bound into the graph.

**Parameters:**

- **query** (<code>[str](#str)</code>) – The SPARQL query to execute.
- **binding** (<code>[str](#str)</code>) – The variable name to bind the current node to in the query. Defaults to "node".

#### rdfnav.UriNode.graph

```python
graph: Graph
```

Returns the graph that this node belongs to.

#### rdfnav.UriNode.iri

```python
iri: Node
```

#### rdfnav.UriNode.is_instance_of

```python
is_instance_of(type_uri)
```

Checks if the current node is a subclass of the given type URI.

#### rdfnav.UriNode.is_subclass_of

```python
is_subclass_of(type_uri)
```

Checks if the current node is a subclass of the given type URI.

#### rdfnav.UriNode.lit_obj_via

```python
lit_obj_via(predicate)
```

Returns one literal that can be reached from the current object using `predicate`.
Fails if there are no objects or more than one object.

#### rdfnav.UriNode.lit_objs

```python
lit_objs()
```

Yields pair of predicates and literal objects that can be reached from the current object.

#### rdfnav.UriNode.lit_objs_prefix

```python
lit_objs_prefix(*prefixes)
```

Yields tuples of (predicate, literal) for objects that can be reached from the current object using predicates that start with `prefix`.

#### rdfnav.UriNode.lit_objs_sans_prefix

```python
lit_objs_sans_prefix(*prefixes)
```

Yields tuples of (predicate without prefix, literal) for all objects that can be reached from the current object.

#### rdfnav.UriNode.lit_objs_via

```python
lit_objs_via(predicate)
```

Yields all literals that can be reached from the current object using `predicate`.

#### rdfnav.UriNode.navigator

```python
navigator: GraphNavigator
```

#### rdfnav.UriNode.ref_obj_via

```python
ref_obj_via(predicate)
```

Yields one `UriNode` that can be reached from the current object using `predicate`.
Fails if there are no objects or more than one object.

#### rdfnav.UriNode.ref_objs

```python
ref_objs()
```

Yields pairs of predicates and object nodes that can be reached from the current object.
Only predicates that are URIs are included, literals are excluded.

#### rdfnav.UriNode.ref_objs_prefix

```python
ref_objs_prefix(*prefixes)
```

Yields tuples of (predicate, `UriNode`) for objects that can be reached from the current object using predicates that start with `prefix`.

#### rdfnav.UriNode.ref_objs_sans_prefix

```python
ref_objs_sans_prefix(*prefixes)
```

Yields tuples of (predicate without prefix, `UriNode`) for all objects that can be reached from the current object,

#### rdfnav.UriNode.ref_objs_via

```python
ref_objs_via(predicate=None)
```

Yields navigator objects for all nodes that can be reached from the current object using `predicate`.

**Parameters:**

- **predicate** (<code>[URIRef](#rdflib.URIRef) | None</code>) – Optionally, a specific predicate to follow to find subjects.
  If None, all objects that are URIs or BNodes that can be reached from the current object will be returned.

#### rdfnav.UriNode.ref_subj_via

```python
ref_subj_via(predicate)
```

Yields one `UriNode` that can reach the current object using `predicate`.
Fails if there are no subjects or more than one subject.

#### rdfnav.UriNode.ref_subjs

```python
ref_subjs()
```

Yields all subjects that can reach the current object via one predicate, as `UriNode` instances.

#### rdfnav.UriNode.ref_subjs_via

```python
ref_subjs_via(predicate)
```

Yields all URIs that can reach the current object using `predicate`, as `UriNode` instances.

**Parameters:**

- **predicate** (<code>[URIRef](#rdflib.URIRef)</code>) – Optionally, a specific predicate to follow to find subjects.
  If None, all subjects of the current object will be returned.

#### rdfnav.UriNode.replace

```python
replace(predicate, obj)
```

Replaces all triples with the current IRI as subject and the given predicate with a new object.
This mutates the graph.

#### rdfnav.UriNode.select_query

```python
select_query(query, binding='node', **kwargs)
```

Executes a SPARQL SELECT query on the graph, with the current node pre-bound into the graph.

**Parameters:**

- **query** (<code>[str](#str)</code>) – The SPARQL query to execute.
- **binding** (<code>[str](#str)</code>) – The variable name to bind the current node to in the query. Defaults to "node".

#### rdfnav.UriNode.subgraph

```python
subgraph()
```

Returns a subgraph containing only the current node and anything traversable from it.

#### rdfnav.UriNode.suffix

```python
suffix: str
```

Returns the suffix of the URI, which is the last part after the last slash or hash.

### rdfnav.exactly_one

```python
exactly_one(items)
```

Helper function to ensure that exactly one item is returned from an iterable.
Raises ValueError if there are no items or more than one item.
