from rdflib import Graph, URIRef, SDO
import pytest
from rdfnav import GraphNavigator

@pytest.fixture
def graph_nav() -> GraphNavigator:
    test_graph = Graph()
    test_graph.parse(data="""
    @prefix schema: <https://schema.org/> .
    @prefix ex: <http://example.org/> .
    
    ex:TechCompany a schema:Organization ;
        schema:location ex:HeadquartersLocation ;
        schema:department ex:RnDDepartment ;
        schema:makesOffer ex:ProductOffer1 ;
        schema:brand ex:CompanyBrand .
    
    ex:RnDDepartment a schema:Organization ;
        schema:parentOrganization ex:TechCompany ;
        schema:subOrganization ex:AITeam ;
        schema:employee ex:TeamLead .
    
    ex:ProductOffer1 a schema:Offer ;
        schema:itemOffered ex:AISoftware .
    
    ex:HeadquartersLocation a schema:Place ;
        schema:address ex:HeadquartersAddress ;
        schema:geo ex:GeoCoordinates ;
        schema:containedInPlace ex:TechPark .
    
    ex:CompanyBrand a schema:Brand ;
        schema:logo ex:CompanyLogo .
    
    ex:AITeam a schema:Organization ;
        schema:parentOrganization ex:RnDDepartment ;
        schema:project ex:AIProject .
    
    ex:AISoftware a schema:SoftwareApplication ;
        schema:softwareRequirements ex:SystemRequirements ;
        schema:review ex:ProductReview1 .
    
    ex:HeadquartersAddress a schema:PostalAddress .
    
    ex:GeoCoordinates a schema:GeoCoordinates .
    
    ex:TechPark a schema:Place ;
        schema:geo ex:TechParkGeoCoordinates .
    
    ex:AIProject a schema:CreativeWork ;
        schema:documentation ex:ProjectDocumentation .
    
    ex:SystemRequirements a schema:PropertyValue .
    
    ex:ProductReview1 a schema:Review ;
        schema:reviewRating ex:Rating ;
        schema:author ex:Reviewer .
    
    ex:TechParkGeoCoordinates a schema:GeoCoordinates .
    
    ex:ProjectDocumentation a schema:DigitalDocument .
    
    ex:Rating a schema:Rating .

    ex:Reviewer a schema:Person .
    
    ex:CompanyLogo a schema:ImageObject .
    
    ex:TeamLead a schema:OrganizationRole .
    """)
    return GraphNavigator(test_graph)

def test_subgraph(graph_nav: GraphNavigator):
    review = graph_nav.instance(SDO.Review)
    triples = list(review.subgraph())
    assert len(triples) == 5

    subjects = set(triple[0] for triple in triples)
    assert subjects == {
        URIRef("http://example.org/ProductReview1"),
        URIRef("http://example.org/Rating"),
        URIRef("http://example.org/Reviewer"),
    }

    objects = set(triple[2] for triple in triples)  
    assert objects == {
        URIRef("http://example.org/Rating"),
        URIRef("http://example.org/Reviewer"),
        SDO.Review,
        SDO.Rating,
        SDO.Person
    }

def test_graphnavigator_subjects(graph_nav: GraphNavigator):
    subjects = list(graph_nav.subjects(URIRef("https://schema.org/location"), URIRef("http://example.org/HeadquartersLocation")))
    assert any(node.iri == URIRef("http://example.org/TechCompany") for node in subjects)

def test_graphnavigator_subject(graph_nav: GraphNavigator):
    subject = graph_nav.subject(URIRef("https://schema.org/location"), URIRef("http://example.org/HeadquartersLocation"))
    assert subject.iri == URIRef("http://example.org/TechCompany")

def test_graphnavigator_instances(graph_nav: GraphNavigator):
    instances = list(graph_nav.instances(URIRef("https://schema.org/Organization")))
    assert URIRef("http://example.org/TechCompany") in [node.iri for node in instances]

def test_graphnavigator_instance(graph_nav: GraphNavigator):
    instance = graph_nav.instance(URIRef("https://schema.org/Offer"))
    assert instance.iri == URIRef("http://example.org/ProductOffer1")

def test_urinode_suffix(graph_nav: GraphNavigator):
    node = graph_nav[URIRef("http://example.org/TechCompany")]
    assert node.suffix == "TechCompany"

def test_urinode_ref_objs_via(graph_nav: GraphNavigator):
    node = graph_nav[URIRef("http://example.org/TechCompany")]
    objs = list(node.ref_objs_via(URIRef("https://schema.org/location")))
    assert any(obj.iri == URIRef("http://example.org/HeadquartersLocation") for obj in objs)

def test_urinode_ref_objs(graph_nav: GraphNavigator):
    node = graph_nav[URIRef("http://example.org/TechCompany")]
    pairs = list(node.ref_objs())
    assert any(obj.iri == URIRef("http://example.org/HeadquartersLocation") for _, obj in pairs)

def test_urinode_ref_objs_prefix(graph_nav: GraphNavigator):
    node = graph_nav[URIRef("http://example.org/TechCompany")]
    pairs = list(node.ref_objs_prefix("https://schema.org/"))
    assert any(obj.iri == URIRef("http://example.org/HeadquartersLocation") for _, obj in pairs)

def test_urinode_ref_objs_sans_prefix(graph_nav: GraphNavigator):
    node = graph_nav[URIRef("http://example.org/TechCompany")]
    pairs = list(node.ref_objs_sans_prefix("https://schema.org/"))
    assert any(obj.iri == URIRef("http://example.org/HeadquartersLocation") for _, obj in pairs)

def test_urinode_ref_obj_via(graph_nav: GraphNavigator):
    node = graph_nav[URIRef("http://example.org/TechCompany")]
    obj = node.ref_obj_via(URIRef("https://schema.org/location"))
    assert obj.iri == URIRef("http://example.org/HeadquartersLocation")

def test_urinode_lit_objs_via(graph_nav: GraphNavigator):
    node = graph_nav[URIRef("http://example.org/TechCompany")]
    # No literals in fixture, just check it runs
    assert list(node.lit_objs_via(URIRef("https://schema.org/location"))) == []

def test_urinode_lit_objs(graph_nav: GraphNavigator):
    node = graph_nav[URIRef("http://example.org/TechCompany")]
    assert list(node.lit_objs()) == []

def test_urinode_lit_obj_via(graph_nav: GraphNavigator):
    node = graph_nav[URIRef("http://example.org/TechCompany")]
    try:
        node.lit_obj_via(URIRef("https://schema.org/location"))
    except ValueError:
        pass
    else:
        assert False, "Should raise ValueError for no literal"

def test_urinode_lit_objs_prefix(graph_nav: GraphNavigator):
    node = graph_nav[URIRef("http://example.org/TechCompany")]
    assert list(node.lit_objs_prefix("https://schema.org/")) == []

def test_urinode_lit_objs_sans_prefix(graph_nav: GraphNavigator):
    node = graph_nav[URIRef("http://example.org/TechCompany")]
    assert list(node.lit_objs_sans_prefix("https://schema.org/")) == []

def test_urinode_ref_subjs_via(graph_nav: GraphNavigator):
    node = graph_nav[URIRef("http://example.org/HeadquartersLocation")]
    subjs = list(node.ref_subjs_via(URIRef("https://schema.org/location")))
    assert any(subj.iri == URIRef("http://example.org/TechCompany") for subj in subjs)

def test_urinode_ref_subjs(graph_nav: GraphNavigator):
    node = graph_nav[URIRef("http://example.org/HeadquartersLocation")]
    subjs = list(node.ref_subjs())
    assert any(subj.iri == URIRef("http://example.org/TechCompany") for subj in subjs)

def test_urinode_ref_subj_via(graph_nav: GraphNavigator):
    node = graph_nav[URIRef("http://example.org/HeadquartersLocation")]
    subj = node.ref_subj_via(URIRef("https://schema.org/location"))
    assert subj.iri == URIRef("http://example.org/TechCompany")

def test_urinode_cbd(graph_nav: GraphNavigator):
    node = graph_nav[URIRef("http://example.org/TechCompany")]
    cbd_graph = node.cbd()
    assert isinstance(cbd_graph, Graph)

def test_urinode_change_iri(graph_nav: GraphNavigator):
    node = graph_nav[URIRef("http://example.org/TechCompany")]
    new_iri = URIRef("http://example.org/NewTechCompany")
    node.change_iri(new_iri)
    assert (new_iri, URIRef("https://schema.org/location"), URIRef("http://example.org/HeadquartersLocation")) in graph_nav.graph
    assert (URIRef("http://example.org/TechCompany"), URIRef("https://schema.org/location"), URIRef("http://example.org/HeadquartersLocation")) not in graph_nav.graph

def test_urinode_delete(graph_nav: GraphNavigator):
    node = graph_nav[URIRef("http://example.org/TechCompany")]
    node.delete(URIRef("https://schema.org/location"), URIRef("http://example.org/HeadquartersLocation"))
    assert (URIRef("http://example.org/TechCompany"), URIRef("https://schema.org/location"), URIRef("http://example.org/HeadquartersLocation")) not in graph_nav.graph

def test_urinode_add(graph_nav: GraphNavigator):
    node = graph_nav[URIRef("http://example.org/TechCompany")]
    node.add(URIRef("https://schema.org/testPredicate"), URIRef("http://example.org/TestObject"))
    assert (URIRef("http://example.org/TechCompany"), URIRef("https://schema.org/testPredicate"), URIRef("http://example.org/TestObject")) in graph_nav.graph

def test_urinode_replace(graph_nav: GraphNavigator):
    node = graph_nav[URIRef("http://example.org/TechCompany")]
    node.replace(URIRef("https://schema.org/brand"), URIRef("http://example.org/NewBrand"))
    assert (URIRef("http://example.org/TechCompany"), URIRef("https://schema.org/brand"), URIRef("http://example.org/NewBrand")) in graph_nav.graph
    assert (URIRef("http://example.org/TechCompany"), URIRef("https://schema.org/brand"), URIRef("http://example.org/CompanyBrand")) not in graph_nav.graph
