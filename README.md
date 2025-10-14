# RdfNav

`rdfnav` makes it easier to query `rdflib` graphs

## Motivation

- **Less boilerplate**: shortcut common queries like finding all instances of a class using [`.instances()`](https://wehi-soda-hub.github.io/RdfNav/#rdfnav.GraphNavigator.instances)
- **Type safety**: Some `rdflib` methods return type unions of multiple types, like `Literal` or `URIRef`, whereas `rdfnav` uses different methods like [`.lit_objs()`](https://wehi-soda-hub.github.io/RdfNav/#rdfnav.UriNode.lit_objs) vs [`.ref_objs()`](https://wehi-soda-hub.github.io/RdfNav/#rdfnav.UriNode.ref_objs) 
- **Stateful navigation**: `rdfnav` lets you "move" around the graph by jumping from one node to another, keeping the current node ID as a position, for example [`.ref_obj_via()`](https://wehi-soda-hub.github.io/RdfNav/#rdfnav.UriNode.ref_obj_via)
- **Singular methods**: If you expect a single result for your pattern, you can use the singular version of each method, like [`.ref_subj_via()`](https://wehi-soda-hub.github.io/RdfNav/#rdfnav.UriNode.ref_subj_via) instead of the plural [`.ref_subjs_via()`](https://wehi-soda-hub.github.io/RdfNav/#rdfnav.UriNode.ref_subjs_via)


## Usage

In this example, we navigate the results graph [generated as a report](https://www.w3.org/TR/shacl/#validation-report) from SHACL validation.

```python
from rdflib import Graph, URIRef, IdentifiedNode, SH, RDF, RDFS
from rdfnav import GraphNavigator, UriNode

def raise_exceptions(results_graph: Graph):
    "Raises an exception for each validation failure in the SHACL validation report"
    # Start navigating a graph
    nav = GraphNavigator(results_graph)

    # Find all objects of class sh:ValidationReport
    validation_report = nav.instance(SH.ValidationReport)
    # Follow all sh:result properties to find validation result nodes
    for result in validation_report.ref_objs_via(SH.result):
        # Follow one single sh:resultMessage property to find the string message for this result
        raise Exception(result.lit_obj(SH.resultMessage))

```
