# RdfNav

Utilities for navigating an RDF graph in Python.

## Usage

In this example, we navigate the results graph [generated as a report](https://www.w3.org/TR/shacl/#validation-report) from SHACL validation.

```python
from rdflib import Graph, URIRef, IdentifiedNode, SH, RDF, RDFS
from rdfnav import GraphNavigator, UriNode

def raise_exceptions(results_graph: Graph):
    # Start navigating a graph
    nav = GraphNavigator(results_graph)

    # Find all objects of class sh:ValidationReport
    # by finding subjects that match (?, rdf:type, sh:ValidationReport) 
    validation_report = nav.subject(
        predicate=RDF.type,
        object=SH.ValidationReport,
    )
    # Follow all sh:result properties to find validation result nodes
    for result in validation_report.ref_objs(SH.result):
        # Follow one single sh:resultMessage property to find the string message for this result
        yield ValidationError(
            message=result.lit_obj(SH.resultMessage)
        )

```

[More detailed API docs can be found here](docs/api.md).
