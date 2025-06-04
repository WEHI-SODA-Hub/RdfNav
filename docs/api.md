## rdfnav

**Classes:**

- [**GraphNavigator**](#rdfnav.GraphNavigator) – Wraps an RDF graph and provides methods to navigate through it using URIs.
- [**UriNode**](#rdfnav.UriNode) – Navigation helper for a single node in the RDF graph, identified by a URI.

### rdfnav.GraphNavigator

```python
GraphNavigator(graph)
```

Wraps an RDF graph and provides methods to navigate through it using URIs.

**Functions:**

- [**subject**](#rdfnav.GraphNavigator.subject) – Yields a single navigator object for the subject of the given predicate and object.
- [**subjects**](#rdfnav.GraphNavigator.subjects) – Yields navigator objects for all nodes that are subjects of the given predicate and object

**Attributes:**

- [**graph**](#rdfnav.GraphNavigator.graph) (<code>[Graph](#rdflib.Graph)</code>) –

#### rdfnav.GraphNavigator.graph

```python
graph: Graph
```

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
UriNode(graph, iri)
```

Navigation helper for a single node in the RDF graph, identified by a URI.
Typically this is created by the `GraphNavigator` class.

**Functions:**

- [**lit_obj**](#rdfnav.UriNode.lit_obj) – Returns one literal that can be reached from the current object using `predicate`.
- [**lit_objs**](#rdfnav.UriNode.lit_objs) – Yields all literals that can be reached from the current object using `predicate`.
- [**ref_obj**](#rdfnav.UriNode.ref_obj) – Yields one `UriNode` that can be reached from the current object using `predicate`.
- [**ref_objs**](#rdfnav.UriNode.ref_objs) – Yields navigator objects for all nodes that can be reached from the current object using `predicate`.
- [**ref_subj**](#rdfnav.UriNode.ref_subj) – Yields one `UriNode` that can reach the current object using `predicate`.
- [**ref_subjs**](#rdfnav.UriNode.ref_subjs) – Yields all URIs that can reach the current object using `predicate`, as `UriNode` instances.

**Attributes:**

- [**graph**](#rdfnav.UriNode.graph) (<code>[Graph](#rdflib.Graph)</code>) –
- [**iri**](#rdfnav.UriNode.iri) (<code>[Node](#rdflib.Node)</code>) –
- [**suffix**](#rdfnav.UriNode.suffix) (<code>[str](#str)</code>) – Returns the suffix of the URI, which is the last part after the last slash or hash.

#### rdfnav.UriNode.graph

```python
graph: Graph
```

#### rdfnav.UriNode.iri

```python
iri: Node
```

#### rdfnav.UriNode.lit_obj

```python
lit_obj(predicate)
```

Returns one literal that can be reached from the current object using `predicate`.
Fails if there are no objects or more than one object.

#### rdfnav.UriNode.lit_objs

```python
lit_objs(predicate)
```

Yields all literals that can be reached from the current object using `predicate`.

#### rdfnav.UriNode.ref_obj

```python
ref_obj(predicate)
```

Yields one `UriNode` that can be reached from the current object using `predicate`.
Fails if there are no objects or more than one object.

#### rdfnav.UriNode.ref_objs

```python
ref_objs(predicate)
```

Yields navigator objects for all nodes that can be reached from the current object using `predicate`.

#### rdfnav.UriNode.ref_subj

```python
ref_subj(predicate)
```

Yields one `UriNode` that can reach the current object using `predicate`.
Fails if there are no subjects or more than one subject.

#### rdfnav.UriNode.ref_subjs

```python
ref_subjs(predicate)
```

Yields all URIs that can reach the current object using `predicate`, as `UriNode` instances.

#### rdfnav.UriNode.suffix

```python
suffix: str
```

Returns the suffix of the URI, which is the last part after the last slash or hash.
