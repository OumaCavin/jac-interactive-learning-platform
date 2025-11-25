"""
Management Command to populate knowledge graph with JAC programming content

Usage:
    python manage.py populate_knowledge_graph
    python manage.py populate_knowledge_graph --force
"""

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from apps.knowledge_graph.services.jac_populator import JACKnowledgeGraphPopulator

User = get_user_model()


class Command(BaseCommand):
    help = 'Populate the knowledge graph with comprehensive JAC programming content'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force repopulation even if content exists',
        )
        parser.add_argument(
            '--check-only',
            action='store_true',
            help='Only check what would be populated without actually creating',
        )
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Enable verbose output',
        )

    def handle(self, *args, **options):
        force = options['force']
        check_only = options['check_only']
        verbose = options['verbose']

        self.stdout.write(
            self.style.SUCCESS('🚀 Starting JAC Knowledge Graph Population...')
        )

        try:
            # Initialize the populator
            populator = JACKnowledgeGraphPopulator()
            
            # Check existing content
            from apps.knowledge_graph.models import KnowledgeNode, KnowledgeEdge, LearningGraph
            existing_concepts = KnowledgeNode.objects.filter(node_type='concept').count()
            existing_relations = KnowledgeEdge.objects.count()
            existing_graphs = LearningGraph.objects.count()

            self.stdout.write(
                f"📊 Current Knowledge Graph Status:\n"
                f"   - Concepts: {existing_concepts}\n"
                f"   - Relations: {existing_relations}\n"
                f"   - Learning Graphs: {existing_graphs}\n"
            )

            if existing_concepts > 0 and not force and not check_only:
                self.stdout.write(
                    self.style.WARNING(
                        f'⚠️  Knowledge graph already contains {existing_concepts} concepts.\n'
                        f'   Use --force to repopulate or --check-only to see what would be created.'
                    )
                )
                return

            if check_only:
                self.stdout.write(
                    self.style.SUCCESS('🔍 Check Mode - Showing what would be populated:')
                )
                self._show_population_preview(populator)
                return

            # Perform population
            if verbose:
                self.stdout.write('📝 Creating JAC concepts...')
            
            result = populator.populate_graph()

            # Display results
            self.stdout.write(
                self.style.SUCCESS('✅ JAC Knowledge Graph Population Complete!')
            )
            self.stdout.write(
                f'📈 Population Results:\n'
                f'   - Concepts Created: {len(result["concepts"])}\n'
                f'   - Relationships Created: {len(result["relationships"])}\n'
                f'   - Learning Graphs Created: {len(result["graphs"])}\n'
                f'   - Concept Relations Created: {len(result["concept_relations"])}\n'
            )

            # Show some example concepts
            if verbose and result["concepts"]:
                self.stdout.write(
                    self.style.SUCCESS('\n🎯 Example Concepts Created:')
                )
                for i, concept in enumerate(result["concepts"][:5], 1):
                    self.stdout.write(
                        f'   {i}. {concept.title} (Difficulty: {concept.difficulty_level})'
                    )
                if len(result["concepts"]) > 5:
                    self.stdout.write(f'   ... and {len(result["concepts"]) - 5} more concepts')

            # Show learning paths
            if verbose and result["graphs"]:
                self.stdout.write(
                    self.style.SUCCESS('\n🛤️  Learning Paths Created:')
                )
                for graph in result["graphs"]:
                    self.stdout.write(
                        f'   - {graph.title}: {graph.description[:100]}...'
                    )

            # Verify population
            new_concepts = KnowledgeNode.objects.filter(node_type='concept').count()
            new_relations = KnowledgeEdge.objects.count()
            new_graphs = LearningGraph.objects.count()

            self.stdout.write(
                self.style.SUCCESS('\n📊 Final Knowledge Graph Status:')
            )
            self.stdout.write(f'   - Total Concepts: {new_concepts}')
            self.stdout.write(f'   - Total Relations: {new_relations}')
            self.stdout.write(f'   - Total Learning Graphs: {new_graphs}')

            if new_concepts > 0:
                self.stdout.write(
                    self.style.SUCCESS('🎉 Knowledge graph is ready for use!')
                )
                self.stdout.write(
                    '\n💡 Next Steps:\n'
                    '   1. Visit /api/knowledge-graph/api-extended/concepts/ to browse concepts\n'
                    '   2. Check /api/knowledge-graph/api-extended/learning_paths/ for learning paths\n'
                    '   3. Use AI agents at /api/ai-agents/available_agents/ to get started'
                )
            else:
                self.stdout.write(
                    self.style.ERROR('❌ No concepts were created. Please check the logs.')
                )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error during population: {str(e)}')
            )
            raise CommandError(f'Knowledge graph population failed: {str(e)}')

    def _show_population_preview(self, populator):
        """Show what would be populated without actually creating"""
        
        # Show concepts
        self.stdout.write(
            self.style.SUCCESS('\n📚 JAC Concepts that would be created:')
        )
        for i, concept_data in enumerate(populator.jac_concepts[:10], 1):
            self.stdout.write(
                f'   {i}. {concept_data["title"]}\n'
                f'      - Type: {concept_data["concept_type"]}\n'
                f'      - Difficulty: {concept_data["difficulty_level"]}\n'
                f'      - Category: {concept_data["category"]}\n'
            )
        if len(populator.jac_concepts) > 10:
            self.stdout.write(f'   ... and {len(populator.jac_concepts) - 10} more concepts')

        # Show relationships
        self.stdout.write(
            self.style.SUCCESS('\n🔗 Relationships that would be created:')
        )
        for i, rel in enumerate(populator.relationships[:5], 1):
            self.stdout.write(
                f'   {i}. {rel["from"]} --{rel["type"]}--> {rel["to"]} (strength: {rel["strength"]})'
            )
        if len(populator.relationships) > 5:
            self.stdout.write(f'   ... and {len(populator.relationships) - 5} more relationships')

        # Show learning paths
        self.stdout.write(
            self.style.SUCCESS('\n🛤️  Learning Paths that would be created:')
        )
        for i, path_data in enumerate(populator.learning_paths, 1):
            self.stdout.write(
                f'   {i}. {path_data["title"]}\n'
                f'      - Description: {path_data["description"]}\n'
                f'      - Difficulty: {path_data["difficulty_level"]}\n'
                f'      - Duration: {path_data["estimated_duration"]} minutes\n'
                f'      - Concepts: {len(path_data["concepts"])}\n'
            )

        self.stdout.write(
            self.style.SUCCESS(
                f'\n📊 Summary:\n'
                f'   - Concepts: {len(populator.jac_concepts)}\n'
                f'   - Relationships: {len(populator.relationships)}\n'
                f'   - Learning Paths: {len(populator.learning_paths)}'
            )
        )