from rdflib import Graph, URIRef, SDO
import pytest
from rdfnav import GraphNavigator

@pytest.fixture
def graph_fixture() -> Graph:
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
    
    return test_graph

def test_subgraph(graph_fixture: Graph):
    nav = GraphNavigator(graph_fixture)
    review = nav.instance(SDO.Review)
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
