"""
Knowledge Graph Population Service for JAC Learning Platform

Populates the knowledge graph with comprehensive JAC programming concepts
extracted from https://jac-lang.org/ and related resources.
"""

import uuid
import json
from typing import List, Dict, Any
from django.utils import timezone
from django.contrib.auth import get_user_model
from apps.knowledge_graph.models import (
    KnowledgeNode, KnowledgeEdge, LearningGraph, 
    UserKnowledgeState, LearningPath, ConceptRelation
)

User = get_user_model()


class JACKnowledgeGraphPopulator:
    """
    Service class to populate the knowledge graph with JAC programming content
    """
    
    def __init__(self):
        self.jac_concepts = self._get_jac_concepts()
        self.relationships = self._get_jac_relationships()
        self.learning_paths = self._get_jac_learning_paths()
        
    def populate_graph(self):
        """Main method to populate the entire knowledge graph"""
        print("Starting JAC Knowledge Graph Population...")
        
        # Create JAC-specific concepts
        concepts = self._create_concepts()
        print(f"Created {len(concepts)} JAC concepts")
        
        # Create relationships between concepts
        relations = self._create_relationships(concepts)
        print(f"Created {len(relations)} concept relationships")
        
        # Create learning graphs
        graphs = self._create_learning_graphs(concepts)
        print(f"Created {len(graphs)} learning graphs")
        
        # Create concept relations
        concept_relations = self._create_concept_relations()
        print(f"Created {len(concept_relations)} concept relations")
        
        print("JAC Knowledge Graph population completed!")
        return {
            'concepts': concepts,
            'relationships': relations,
            'graphs': graphs,
            'concept_relations': concept_relations
        }
    
    def _get_jac_concepts(self) -> List[Dict]:
        """Define comprehensive JAC programming concepts based on extracted content"""
        return [
            # Core JAC Concepts
            {
                'name': 'JAC Programming Language',
                'title': 'Introduction to JAC (Jaseci Architecture Code)',
                'description': 'JAC is an AI-first, Object-Spatial Programming language built on top of Python',
                'detailed_explanation': 'JAC (Jaseci Architecture Code) is a modern programming language designed for AI and machine learning applications. It provides native support for Object-Spatial Programming (OSP) concepts and integrates seamlessly with large language models.',
                'concept_type': 'core_concept',
                'difficulty_level': 'beginner',
                'category': 'programming_language',
                'tags': ['programming', 'AI', 'language', 'python'],
                'learning_objectives': [
                    'Understand what JAC programming is',
                    'Know the key features and benefits',
                    'Set up development environment'
                ],
                'code_examples': [
                    {
                        'title': 'Hello World in JAC',
                        'code': 'walker hello_world {\n    can print;\n    print("Hello from JAC!");\n}'
                    }
                ],
                'search_keywords': ['JAC', 'Jaseci', 'programming language', 'AI']
            },
            
            # Object-Spatial Programming (OSP)
            {
                'name': 'Object-Spatial Programming',
                'title': 'Object-Spatial Programming (OSP) Fundamentals',
                'description': 'OSP is a paradigm where objects and relationships are first-class citizens in the programming model',
                'detailed_explanation': 'Object-Spatial Programming treats objects, their relationships, and spatial connections as fundamental building blocks. Unlike traditional OOP, OSP emphasizes the spatial relationships between objects and how they interact in a graph-like structure.',
                'concept_type': 'paradigm',
                'difficulty_level': 'intermediate',
                'category': 'programming_paradigm',
                'tags': ['OSP', 'paradigm', 'objects', 'spatial'],
                'learning_objectives': [
                    'Understand OSP concepts',
                    'Compare OSP to traditional OOP',
                    'Apply spatial thinking to programming'
                ],
                'code_examples': [
                    {
                        'title': 'Simple OSP Example',
                        'code': 'node person {\n    has name, age;\n}\n\nwalker connect_people {\n    person1 = spawn node.person(name="Alice", age=25);\n    person2 = spawn node.person(name="Bob", age=30);\n    report {"person1": person1, "person2": person2};\n}'
                    }
                ],
                'search_keywords': ['OSP', 'object-spatial', 'paradigm', 'spatial programming']
            },
            
            # Nodes and Edges
            {
                'name': 'Nodes',
                'title': 'Nodes in Object-Spatial Programming',
                'description': 'Nodes represent data objects and are the fundamental building blocks in OSP',
                'detailed_explanation': 'Nodes are the core data structures in JAC\'s OSP paradigm. They represent entities in your program and can hold data, have abilities (methods), and can be connected to other nodes via edges.',
                'concept_type': 'jac_specific',
                'difficulty_level': 'intermediate',
                'category': 'data_structures',
                'tags': ['nodes', 'OSP', 'data', 'objects'],
                'learning_objectives': [
                    'Define nodes with attributes and abilities',
                    'Create and spawn nodes',
                    'Understand node properties and methods'
                ],
                'code_examples': [
                    {
                        'title': 'Basic Node Definition',
                        'code': 'node person {\n    has name, age;\n    can greet with person entry {\n        can print;\n        print(f"Hello, I am {here.name} and I am {here.age} years old");\n    }\n}\n\nwalker create_person {\n    person = spawn node.person(name="Alice", age=25);\n    report person;\n}'
                    }
                ],
                'search_keywords': ['nodes', 'node definition', 'data objects', 'attributes']
            },
            
            {
                'name': 'Edges',
                'title': 'Edges and Node Connections',
                'description': 'Edges create relationships and connections between nodes in the spatial graph',
                'detailed_explanation': 'Edges represent relationships between nodes and can be unidirectional or bidirectional. They enable nodes to reference and interact with other nodes in the system.',
                'concept_type': 'jac_specific',
                'difficulty_level': 'intermediate',
                'category': 'data_structures',
                'tags': ['edges', 'relationships', 'connections', 'links'],
                'learning_objectives': [
                    'Create edges between nodes',
                    'Understand edge properties and types',
                    'Traverse edges in graph operations'
                ],
                'code_examples': [
                    {
                        'title': 'Creating Edge Connections',
                        'code': 'node person {\n    has name, age;\n}\n\nedge friendship {\n    has strength;\n}\n\nwalker create_friendship {\n    person1 = spawn node.person(name="Alice", age=25);\n    person2 = spawn node.person(name="Bob", age=30);\n    \n    # Create friendship edge\n    spawn edge.friendship(person1, person2, strength=0.8);\n    report "Friendship created!";\n}'
                    }
                ],
                'search_keywords': ['edges', 'relationships', 'connections', 'graph']
            },
            
            # Walkers
            {
                'name': 'Walkers',
                'title': 'Walkers - Graph Traversal and Actions',
                'description': 'Walkers are entities that navigate through the node-edge graph and perform actions',
                'detailed_explanation': 'Walkers are special entities that can traverse the spatial graph, visit nodes, follow edges, and perform various operations. They are like agents that can move through the spatial structure.',
                'concept_type': 'jac_specific',
                'difficulty_level': 'advanced',
                'category': 'execution',
                'tags': ['walkers', 'traversal', 'navigation', 'agents'],
                'learning_objectives': [
                    'Create and define walkers',
                    'Use walkers to traverse graphs',
                    'Implement walker abilities and behaviors'
                ],
                'code_examples': [
                    {
                        'title': 'Basic Walker',
                        'code': 'walker visitor {\n    can print;\n    \n    with entry {\n        print("Starting walker execution...");\n    }\n    \n    with exit {\n        print("Walker execution completed!");\n    }\n    \n    can visit_nodes {\n        print("Visiting nodes in the graph");\n    }\n}\n\nwalker run_visitor {\n    visitor = spawn walker.visitor();\n    report {"walker_id": visitor};\n}'
                    }
                ],
                'search_keywords': ['walkers', 'traversal', 'navigation', 'graph walking']
            },
            
            # Abilities
            {
                'name': 'Abilities',
                'title': 'Node and Walker Abilities',
                'description': 'Abilities are methods that define the behavior and capabilities of nodes and walkers',
                'detailed_explanation': 'Abilities are the methods or functions that nodes and walkers can perform. They define the behavior of spatial entities and enable them to interact with their environment.',
                'concept_type': 'jac_specific',
                'difficulty_level': 'intermediate',
                'category': 'methods',
                'tags': ['abilities', 'methods', 'behaviors', 'functions'],
                'learning_objectives': [
                    'Define abilities for nodes and walkers',
                    'Understand entry and exit blocks',
                    'Implement custom behavior logic'
                ],
                'code_examples': [
                    {
                        'title': 'Node with Abilities',
                        'code': 'node calculator {\n    has current_value;\n    \n    can add with num_entry {\n        here.current_value += num.value;\n    }\n    \n    can multiply with num_entry {\n        here.current_value *= num.value;\n    }\n    \n    can get_result {\n        return here.current_value;\n    }\n}\n\nwalker calculator_demo {\n    calc = spawn node.calculator(current_value=0);\n    \n    spawn node.number(value=5) with calc.entry by add;\n    spawn node.number(value=3) with calc.entry by multiply;\n    \n    report {"result": calc.get_result};\n}'
                    }
                ],
                'search_keywords': ['abilities', 'methods', 'node methods', 'walker methods']
            },
            
            # JAC Book Chapters
            {
                'name': 'The Jac Book',
                'title': 'The Jac Book - Comprehensive Learning Guide',
                'description': 'A 20-chapter comprehensive guide covering all aspects of JAC programming',
                'detailed_explanation': 'The Jac Book is the definitive guide to JAC programming, covering everything from basic syntax to advanced AI operations and cloud deployment. It provides a structured learning path through 20 comprehensive chapters.',
                'concept_type': 'tool',
                'difficulty_level': 'beginner',
                'category': 'learning_resource',
                'tags': ['book', 'guide', 'tutorial', 'comprehensive'],
                'learning_objectives': [
                    'Access comprehensive JAC documentation',
                    'Follow structured learning path',
                    'Master all JAC concepts systematically'
                ],
                'code_examples': [],
                'search_keywords': ['jac book', 'documentation', 'guide', 'comprehensive']
            },
            
            # byLLM - AI Integration
            {
                'name': 'byLLM Integration',
                'title': 'Programming with Large Language Models',
                'description': 'Integrate LLMs directly into JAC code for AI-powered programming',
                'detailed_explanation': 'byLLM allows JAC programs to directly interact with large language models, enabling AI-powered code generation, natural language processing, and intelligent behavior.',
                'concept_type': 'jac_specific',
                'difficulty_level': 'advanced',
                'category': 'AI_integration',
                'tags': ['byLLM', 'AI', 'LLM', 'language models'],
                'learning_objectives': [
                    'Understand byLLM integration',
                    'Use LLMs in JAC programs',
                    'Implement AI-powered features'
                ],
                'code_examples': [
                    {
                        'title': 'Simple byLLM Usage',
                        'code': '# byllm example would go here\n# This requires LLM API integration'
                    }
                ],
                'search_keywords': ['byLLM', 'AI integration', 'language models', 'GPT']
            },
            
            # Jac Cloud
            {
                'name': 'Jac Cloud',
                'title': 'Cloud-Native JAC Applications',
                'description': 'Deploy and scale JAC applications in the cloud with Jac Cloud',
                'detailed_explanation': 'Jac Cloud provides cloud-native infrastructure for deploying and scaling JAC applications, including multi-user support, permissions, monitoring, and real-time features.',
                'concept_type': 'tool',
                'difficulty_level': 'advanced',
                'category': 'cloud',
                'tags': ['cloud', 'deployment', 'scaling', 'webhooks'],
                'learning_objectives': [
                    'Deploy applications to Jac Cloud',
                    'Configure multi-user access',
                    'Implement real-time features'
                ],
                'code_examples': [],
                'search_keywords': ['jac cloud', 'cloud deployment', 'scaling', 'multi-user']
            },
            
            # Jac Client
            {
                'name': 'Jac Client',
                'title': 'Frontend Development with Jac Client',
                'description': 'Build responsive web applications using Jac Client framework',
                'detailed_explanation': 'Jac Client is a modern frontend framework that allows building responsive web applications using familiar JavaScript patterns but with JAC integration.',
                'concept_type': 'tool',
                'difficulty_level': 'intermediate',
                'category': 'frontend',
                'tags': ['client', 'frontend', 'web', 'JavaScript'],
                'learning_objectives': [
                    'Set up Jac Client projects',
                    'Build reactive components',
                    'Integrate with JAC backends'
                ],
                'code_examples': [],
                'search_keywords': ['jac client', 'frontend', 'web development', 'components']
            }
        ]
    
    def _get_jac_relationships(self) -> List[Dict]:
        """Define relationships between JAC concepts"""
        return [
            # Prerequisite relationships
            {'from': 'JAC Programming Language', 'to': 'Object-Spatial Programming', 'type': 'prerequisite', 'strength': 'essential'},
            {'from': 'Object-Spatial Programming', 'to': 'Nodes', 'type': 'prerequisite', 'strength': 'essential'},
            {'from': 'Nodes', 'to': 'Edges', 'type': 'related', 'strength': 'strong'},
            {'from': 'Nodes', 'to': 'Walkers', 'type': 'related', 'strength': 'strong'},
            {'from': 'Walkers', 'to': 'Abilities', 'type': 'prerequisite', 'strength': 'essential'},
            
            # Learning path relationships
            {'from': 'The Jac Book', 'to': 'JAC Programming Language', 'type': 'part_of', 'strength': 'essential'},
            {'from': 'The Jac Book', 'to': 'Object-Spatial Programming', 'type': 'part_of', 'strength': 'essential'},
            {'from': 'The Jac Book', 'to': 'byLLM Integration', 'type': 'part_of', 'strength': 'moderate'},
            {'from': 'The Jac Book', 'to': 'Jac Cloud', 'type': 'part_of', 'strength': 'moderate'},
            
            # Implementation relationships
            {'from': 'byLLM Integration', 'to': 'JAC Programming Language', 'type': 'extends', 'strength': 'strong'},
            {'from': 'Jac Cloud', 'to': 'JAC Programming Language', 'type': 'extends', 'strength': 'strong'},
            {'from': 'Jac Client', 'to': 'JAC Programming Language', 'type': 'extends', 'strength': 'moderate'},
            
            # Concept relationships
            {'from': 'Nodes', 'to': 'Object-Spatial Programming', 'type': 'example_of', 'strength': 'essential'},
            {'from': 'Walkers', 'to': 'Object-Spatial Programming', 'type': 'example_of', 'strength': 'essential'},
            {'from': 'Abilities', 'to': 'Object-Spatial Programming', 'type': 'example_of', 'strength': 'essential'},
        ]
    
    def _get_jac_learning_paths(self) -> List[Dict]:
        """Define structured learning paths for JAC"""
        return [
            {
                'name': 'JAC Programming Fundamentals',
                'title': 'Complete JAC Programming Course',
                'description': 'Master JAC programming from basics to advanced concepts',
                'learning_outcomes': [
                    'Write basic JAC programs',
                    'Understand Object-Spatial Programming',
                    'Build spatial applications',
                    'Deploy to Jac Cloud'
                ],
                'difficulty_level': 'beginner',
                'estimated_duration': 120,  # 2 hours
                'category': 'programming',
                'concepts': [
                    'JAC Programming Language',
                    'Object-Spatial Programming',
                    'Nodes',
                    'Edges',
                    'Walkers',
                    'Abilities'
                ]
            },
            {
                'name': 'AI-Powered JAC Development',
                'title': 'JAC with AI Integration',
                'description': 'Learn to build AI-powered applications using byLLM and LLMs',
                'learning_outcomes': [
                    'Integrate LLMs in JAC programs',
                    'Build intelligent spatial applications',
                    'Implement natural language interfaces'
                ],
                'difficulty_level': 'advanced',
                'estimated_duration': 90,  # 1.5 hours
                'category': 'AI',
                'concepts': [
                    'JAC Programming Language',
                    'byLLM Integration',
                    'Abilities'
                ],
                'prerequisites': ['JAC Programming Fundamentals']
            },
            {
                'name': 'Full-Stack JAC Development',
                'title': 'Complete JAC Ecosystem',
                'description': 'Master the entire JAC ecosystem including frontend and cloud',
                'learning_outcomes': [
                    'Build complete JAC applications',
                    'Create responsive frontends with Jac Client',
                    'Deploy to Jac Cloud infrastructure'
                ],
                'difficulty_level': 'advanced',
                'estimated_duration': 180,  # 3 hours
                'category': 'fullstack',
                'concepts': [
                    'JAC Programming Language',
                    'Jac Cloud',
                    'Jac Client',
                    'byLLM Integration'
                ],
                'prerequisites': ['JAC Programming Fundamentals']
            }
        ]
    
    def _create_concepts(self) -> List[KnowledgeNode]:
        """Create knowledge nodes for JAC concepts"""
        created_nodes = []
        
        for concept_data in self.jac_concepts:
            # Check if concept already exists
            existing = KnowledgeNode.objects.filter(title=concept_data['title']).first()
            if existing:
                created_nodes.append(existing)
                continue
            
            # Create new knowledge node
            node = KnowledgeNode.objects.create(
                title=concept_data['title'],
                description=concept_data['description'],
                node_type='concept',
                difficulty_level=concept_data['difficulty_level'],
                content_uri=f"/learning/concepts/{concept_data['name'].lower().replace(' ', '-')}/",
                jac_code=self._extract_code_from_examples(concept_data.get('code_examples', [])),
                learning_objectives=concept_data.get('learning_objectives', []),
                prerequisites=concept_data.get('prerequisites', [])
            )
            created_nodes.append(node)
        
        return created_nodes
    
    def _create_relationships(self, concepts: List[KnowledgeNode]) -> List[KnowledgeEdge]:
        """Create relationships between concepts"""
        created_edges = []
        
        # Create a mapping from concept names to nodes
        concept_map = {node.title: node for node in concepts}
        
        for relation_data in self.relationships:
            source_node = concept_map.get(relation_data['from'])
            target_node = concept_map.get(relation_data['to'])
            
            if source_node and target_node:
                # Check if relationship already exists
                existing = KnowledgeEdge.objects.filter(
                    source_node=source_node,
                    target_node=target_node,
                    edge_type=relation_data['type']
                ).first()
                
                if existing:
                    created_edges.append(existing)
                    continue
                
                # Create new edge
                edge = KnowledgeEdge.objects.create(
                    source_node=source_node,
                    target_node=target_node,
                    edge_type=relation_data['type'],
                    strength=relation_data['strength'],
                    description=f"{relation_data['from']} {relation_data['type']} {relation_data['to']}"
                )
                created_edges.append(edge)
        
        return created_edges
    
    def _create_learning_graphs(self, concepts: List[KnowledgeNode]) -> List[LearningGraph]:
        """Create learning graphs for JAC"""
        created_graphs = []
        concept_map = {node.title: node for node in concepts}
        
        for path_data in self.learning_paths:
            # Check if learning graph already exists
            existing = LearningGraph.objects.filter(title=path_data['title']).first()
            if existing:
                created_graphs.append(existing)
                continue
            
            # Create new learning graph
            graph = LearningGraph.objects.create(
                title=path_data['title'],
                description=path_data['description'],
                graph_type='course',
                subject_area='JAC Programming',
                target_audience=path_data['difficulty_level'],
                estimated_duration=timezone.timedelta(minutes=path_data['estimated_duration'])
            )
            
            # Add concepts to the graph
            for concept_name in path_data['concepts']:
                concept_node = concept_map.get(concept_name)
                if concept_node:
                    from apps.knowledge_graph.models import LearningGraphNode
                    LearningGraphNode.objects.create(
                        learning_graph=graph,
                        knowledge_node=concept_node,
                        is_mandatory=True,
                        node_weight=1.0
                    )
            
            created_graphs.append(graph)
        
        return created_graphs
    
    def _create_concept_relations(self) -> List[ConceptRelation]:
        """Create high-level concept relations"""
        created_relations = []
        
        # Define semantic relationships
        semantic_relations = [
            {
                'concept_a': 'JAC Programming Language',
                'concept_b': 'Python',
                'relation_type': 'inherits',
                'domain': 'programming',
                'description': 'JAC extends and builds upon Python syntax and concepts'
            },
            {
                'concept_a': 'Object-Spatial Programming',
                'concept_b': 'Graph Theory',
                'relation_type': 'implements',
                'domain': 'programming_paradigm',
                'description': 'OSP implements spatial graph concepts for programming'
            },
            {
                'concept_a': 'byLLM Integration',
                'concept_b': 'Large Language Models',
                'relation_type': 'depends',
                'domain': 'AI',
                'description': 'byLLM depends on access to large language model APIs'
            }
        ]
        
        for rel_data in semantic_relations:
            # Check if relation already exists
            existing = ConceptRelation.objects.filter(
                concept_a=rel_data['concept_a'],
                concept_b=rel_data['concept_b'],
                relation_type=rel_data['relation_type']
            ).first()
            
            if existing:
                created_relations.append(existing)
                continue
            
            # Create new concept relation
            relation = ConceptRelation.objects.create(
                concept_a=rel_data['concept_a'],
                concept_b=rel_data['concept_b'],
                relation_type=rel_data['relation_type'],
                domain=rel_data['domain'],
                description=rel_data['description']
            )
            created_relations.append(relation)
        
        return created_relations
    
    def _extract_code_from_examples(self, code_examples: List[Dict]) -> str:
        """Extract code from examples for the knowledge node"""
        if not code_examples:
            return ""
        
        # Use the first example as the primary code
        if isinstance(code_examples[0], dict) and 'code' in code_examples[0]:
            return code_examples[0]['code']
        
        return str(code_examples[0])


def populate_jac_knowledge_graph():
    """Standalone function to populate the JAC knowledge graph"""
    populator = JACKnowledgeGraphPopulator()
    return populator.populate_graph()