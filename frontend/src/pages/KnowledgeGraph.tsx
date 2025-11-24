import React, { useState, useEffect, useRef, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  MagnifyingGlassIcon, 
  AdjustmentsHorizontalIcon,
  PlusIcon,
  MinusIcon,
  ArrowsPointingOutIcon,
  ArrowPathIcon,
  BookOpenIcon,
  AcademicCapIcon,
  CodeBracketIcon,
  StarIcon
} from '@heroicons/react/24/outline';
import { useSelector } from 'react-redux';
import { selectLearning, selectUserLearningPaths, selectUserModuleProgress } from '../store/slices/learningSlice';
import { selectUser } from '../store/slices/authSlice';

// Types for knowledge graph
interface GraphNode {
  id: string;
  type: 'learning_path' | 'module' | 'concept';
  label: string;
  x: number;
  y: number;
  vx?: number;
  vy?: number;
  size: number;
  color: string;
  data: any;
  isCompleted?: boolean;
  progress?: number;
}

interface GraphEdge {
  source: string;
  target: string;
  type: 'prerequisite' | 'contains' | 'related' | 'mastery';
  strength: number;
}

interface LayoutType {
  name: string;
  value: 'force' | 'hierarchical' | 'circular' | 'grid';
}

// Mock JAC Programming Concepts
const JAC_CONCEPTS = [
  { id: 'variables', name: 'Variables', category: 'fundamentals', difficulty: 'beginner' },
  { id: 'data_types', name: 'Data Types', category: 'fundamentals', difficulty: 'beginner' },
  { id: 'operators', name: 'Operators', category: 'fundamentals', difficulty: 'beginner' },
  { id: 'control_flow', name: 'Control Flow', category: 'logic', difficulty: 'beginner' },
  { id: 'loops', name: 'Loops', category: 'logic', difficulty: 'beginner' },
  { id: 'functions', name: 'Functions', category: 'structure', difficulty: 'intermediate' },
  { id: 'arrays', name: 'Arrays', category: 'data_structures', difficulty: 'intermediate' },
  { id: 'objects', name: 'Objects', category: 'data_structures', difficulty: 'intermediate' },
  { id: 'classes', name: 'Classes', category: 'oop', difficulty: 'intermediate' },
  { id: 'inheritance', name: 'Inheritance', category: 'oop', difficulty: 'advanced' },
  { id: 'polymorphism', name: 'Polymorphism', category: 'oop', difficulty: 'advanced' },
  { id: 'algorithms', name: 'Algorithms', category: 'advanced', difficulty: 'advanced' },
  { id: 'data_structures', name: 'Data Structures', category: 'advanced', difficulty: 'advanced' },
  { id: 'recursion', name: 'Recursion', category: 'advanced', difficulty: 'advanced' },
  { id: 'async_programming', name: 'Async Programming', category: 'advanced', difficulty: 'advanced' }
];

// Mock Learning Paths
const MOCK_LEARNING_PATHS = [
  {
    id: 'path-1',
    title: 'JAC Programming Fundamentals',
    description: 'Learn the basics of JAC programming language',
    difficulty: 'beginner' as const,
    moduleCount: 8,
    averageRating: 4.8,
    concepts: ['variables', 'data_types', 'operators', 'control_flow', 'loops']
  },
  {
    id: 'path-2', 
    title: 'Object-Oriented Programming',
    description: 'Master OOP concepts in JAC',
    difficulty: 'intermediate' as const,
    moduleCount: 6,
    averageRating: 4.6,
    concepts: ['functions', 'arrays', 'objects', 'classes']
  },
  {
    id: 'path-3',
    title: 'Advanced JAC Development',
    description: 'Advanced topics and algorithms',
    difficulty: 'advanced' as const,
    moduleCount: 10,
    averageRating: 4.9,
    concepts: ['inheritance', 'polymorphism', 'algorithms', 'data_structures', 'recursion', 'async_programming']
  }
];

// Mock Modules with concepts
const MOCK_MODULES = [
  { id: 'mod-1', title: 'Introduction to Variables', learningPath: 'path-1', concepts: ['variables'], difficulty: 'beginner', order: 1 },
  { id: 'mod-2', title: 'Data Types and Type Conversion', learningPath: 'path-1', concepts: ['data_types'], difficulty: 'beginner', order: 2 },
  { id: 'mod-3', title: 'Basic Operators', learningPath: 'path-1', concepts: ['operators'], difficulty: 'beginner', order: 3 },
  { id: 'mod-4', title: 'Control Structures', learningPath: 'path-1', concepts: ['control_flow'], difficulty: 'beginner', order: 4 },
  { id: 'mod-5', title: 'Loops and Iteration', learningPath: 'path-1', concepts: ['loops'], difficulty: 'beginner', order: 5 },
  { id: 'mod-6', title: 'Functions and Methods', learningPath: 'path-2', concepts: ['functions'], difficulty: 'intermediate', order: 1 },
  { id: 'mod-7', title: 'Working with Arrays', learningPath: 'path-2', concepts: ['arrays'], difficulty: 'intermediate', order: 2 },
  { id: 'mod-8', title: 'Objects and Properties', learningPath: 'path-2', concepts: ['objects'], difficulty: 'intermediate', order: 3 },
  { id: 'mod-9', title: 'Classes and Instances', learningPath: 'path-2', concepts: ['classes'], difficulty: 'intermediate', order: 4 },
  { id: 'mod-10', title: 'Inheritance Patterns', learningPath: 'path-3', concepts: ['inheritance'], difficulty: 'advanced', order: 1 },
  { id: 'mod-11', title: 'Algorithm Design', learningPath: 'path-3', concepts: ['algorithms'], difficulty: 'advanced', order: 2 },
  { id: 'mod-12', title: 'Recursion Techniques', learningPath: 'path-3', concepts: ['recursion'], difficulty: 'advanced', order: 3 }
];

const KnowledgeGraph: React.FC = () => {
  const svgRef = useRef<SVGSVGElement>(null);
  const [nodes, setNodes] = useState<GraphNode[]>([]);
  const [edges, setEdges] = useState<GraphEdge[]>([]);
  const [selectedNode, setSelectedNode] = useState<GraphNode | null>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [filters, setFilters] = useState({
    difficulty: [] as string[],
    concept: [] as string[],
    showCompleted: true,
    showInProgress: true,
    showNotStarted: true
  });
  const [layout, setLayout] = useState<LayoutType>({ name: 'Force Directed', value: 'force' });
  const [zoom, setZoom] = useState(1);
  const [pan, setPan] = useState({ x: 0, y: 0 });
  const [isDragging, setIsDragging] = useState(false);
  const [showFilters, setShowFilters] = useState(false);
  const [showStats, setShowStats] = useState(true);
  const [selectedConcept, setSelectedConcept] = useState<string | null>(null);
  
  const user = useSelector(selectUser);
  const learningPaths = useSelector(selectLearning).learning_paths;
  const userLearningPaths = useSelector(selectUserLearningPaths);
  const userModuleProgress = useSelector(selectUserModuleProgress);

  // Initialize graph data
  useEffect(() => {
    try {
      const graphNodes: GraphNode[] = [];
      const graphEdges: GraphEdge[] = [];

    // Add learning path nodes
    MOCK_LEARNING_PATHS.forEach((path, index) => {
      const userPathProgress = userLearningPaths.find(p => p.learning_path === path.id);
      const isCompleted = userPathProgress?.status === 'completed';
      
      graphNodes.push({
        id: path.id,
        type: 'learning_path',
        label: path.title,
        x: Math.cos((index / MOCK_LEARNING_PATHS.length) * 2 * Math.PI) * 300 + 400,
        y: Math.sin((index / MOCK_LEARNING_PATHS.length) * 2 * Math.PI) * 200 + 300,
        size: 40,
        color: getDifficultyColor(path.difficulty),
        data: path,
        isCompleted,
        progress: userPathProgress?.progress_percentage || 0
      });

      // Add edges from learning path to concepts
      path.concepts.forEach(conceptId => {
        const concept = JAC_CONCEPTS.find(c => c.id === conceptId);
        if (concept) {
          graphEdges.push({
            source: path.id,
            target: `concept-${conceptId}`,
            type: 'contains',
            strength: 1
          });
        }
      });
    });

    // Add module nodes
    MOCK_MODULES.forEach((module, index) => {
      const parentPath = graphNodes.find(n => n.id === module.learningPath);
      const userModule = userModuleProgress.find(p => p.module === module.id);
      const isCompleted = userModule?.status === 'completed';
      
      graphNodes.push({
        id: module.id,
        type: 'module',
        label: module.title,
        x: (parentPath?.x || 400) + (Math.random() - 0.5) * 100,
        y: (parentPath?.y || 300) + (Math.random() - 0.5) * 100,
        size: 25,
        color: getDifficultyColor(module.difficulty),
        data: module,
        isCompleted,
        progress: userModule?.progress_percentage || 0
      });

      // Add edges from module to concepts
      module.concepts.forEach(conceptId => {
        graphEdges.push({
          source: module.id,
          target: `concept-${conceptId}`,
          type: 'contains',
          strength: 1
        });
      });

      // Add prerequisite edges (simplified)
      if (module.order > 1) {
        const prevModule = MOCK_MODULES.find(m => m.learningPath === module.learningPath && m.order === module.order - 1);
        if (prevModule) {
          graphEdges.push({
            source: prevModule.id,
            target: module.id,
            type: 'prerequisite',
            strength: 0.8
          });
        }
      }
    });

    // Add concept nodes
    JAC_CONCEPTS.forEach((concept, index) => {
      const relatedModules = MOCK_MODULES.filter(m => m.concepts.includes(concept.id));
      const avgProgress = relatedModules.length > 0 
        ? relatedModules.reduce((sum, m) => {
            const userModule = userModuleProgress.find(p => p.module === m.id);
            return sum + (userModule?.progress_percentage || 0);
          }, 0) / relatedModules.length
        : 0;

      graphNodes.push({
        id: `concept-${concept.id}`,
        type: 'concept',
        label: concept.name,
        x: Math.cos((index / JAC_CONCEPTS.length) * 2 * Math.PI) * 400 + 400,
        y: Math.sin((index / JAC_CONCEPTS.length) * 2 * Math.PI) * 300 + 300,
        size: 15,
        color: getCategoryColor(concept.category),
        data: { ...concept, modules: relatedModules, progress: avgProgress }
      });

      // Add prerequisite relationships between concepts (simplified)
      if (concept.id === 'data_types' || concept.id === 'variables' || concept.id === 'operators') {
        graphEdges.push({
          source: 'concept-variables',
          target: `concept-${concept.id}`,
          type: 'prerequisite',
          strength: 0.6
        });
      }
    });

    setNodes(graphNodes);
    setEdges(graphEdges);
    } catch (error) {
      // Handle graph data initialization error gracefully
      console.warn('Error initializing knowledge graph data:', error);
    }
  }, [userLearningPaths, userModuleProgress]);

  // Get color for difficulty level
  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'beginner': return '#10B981'; // green
      case 'intermediate': return '#F59E0B'; // amber
      case 'advanced': return '#EF4444'; // red
      default: return '#6B7280'; // gray
    }
  };

  // Get color for concept category
  const getCategoryColor = (category: string) => {
    const colors = {
      fundamentals: '#3B82F6',
      logic: '#8B5CF6', 
      structure: '#10B981',
      data_structures: '#F59E0B',
      oop: '#EF4444',
      advanced: '#6366F1'
    };
    return colors[category as keyof typeof colors] || '#6B7280';
  };

  // Handle node click
  const handleNodeClick = useCallback((node: GraphNode) => {
    setSelectedNode(node);
  }, []);

  // Handle canvas click (deselect)
  const handleCanvasClick = useCallback((e: React.MouseEvent) => {
    if (e.target === svgRef.current) {
      setSelectedNode(null);
    }
  }, []);

  // Filter nodes based on search and filters
  const filteredNodes = nodes.filter(node => {
    const matchesSearch = node.label.toLowerCase().includes(searchQuery.toLowerCase());
    
    // Apply difficulty filter
    if (filters.difficulty.length > 0) {
      const nodeDifficulty = getNodeDifficulty(node);
      if (!filters.difficulty.includes(nodeDifficulty)) return false;
    }

    // Apply concept filter
    if (filters.concept.length > 0) {
      const nodeConcepts = getNodeConcepts(node);
      if (!nodeConcepts.some((concept: string) => filters.concept.includes(concept))) return false;
    }

    // Apply status filter
    if (node.type === 'learning_path' || node.type === 'module') {
      if (node.isCompleted && !filters.showCompleted) return false;
      if (!node.isCompleted && node.progress && node.progress > 0 && !filters.showInProgress) return false;
      if (!node.isCompleted && (!node.progress || node.progress === 0) && !filters.showNotStarted) return false;
    }

    return matchesSearch;
  });

  // Get node difficulty
  const getNodeDifficulty = (node: GraphNode) => {
    if (node.data?.difficulty) return node.data.difficulty;
    return 'beginner';
  };

  // Get node concepts
  const getNodeConcepts = (node: GraphNode) => {
    if (node.type === 'concept') {
      return [node.data.id];
    }
    if (node.data?.concepts) {
      return node.data.concepts;
    }
    return [];
  };

  // Calculate statistics
  const stats = {
    totalPaths: nodes.filter(n => n.type === 'learning_path').length,
    totalModules: nodes.filter(n => n.type === 'module').length,
    totalConcepts: nodes.filter(n => n.type === 'concept').length,
    completedPaths: nodes.filter(n => n.type === 'learning_path' && n.isCompleted).length,
    completedModules: nodes.filter(n => n.type === 'module' && n.isCompleted).length,
    averageProgress: nodes.filter(n => n.type === 'learning_path' || n.type === 'module')
      .reduce((sum, node) => sum + (node.progress || 0), 0) / 
      Math.max(nodes.filter(n => n.type === 'learning_path' || n.type === 'module').length, 1)
  };

  return (
    <div className="container mx-auto px-4 py-8 min-h-screen">
      {/* Header */}
      <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between mb-8">
        <h1 className="text-3xl font-bold text-white mb-4 lg:mb-0">Knowledge Graph</h1>
        
        {/* Search and Controls */}
        <div className="flex flex-col sm:flex-row gap-4">
          {/* Search */}
          <div className="relative">
            <MagnifyingGlassIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
            <input
              type="text"
              placeholder="Search nodes..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-10 pr-4 py-2 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 w-full sm:w-64"
            />
          </div>

          {/* Control Buttons */}
          <div className="flex gap-2">
            <button
              onClick={() => setShowFilters(!showFilters)}
              className="px-4 py-2 bg-white/10 border border-white/20 rounded-lg text-white hover:bg-white/20 transition-colors flex items-center gap-2"
            >
              <AdjustmentsHorizontalIcon className="w-4 h-4" />
              Filters
            </button>
            
            <select
              value={layout.value}
              onChange={(e) => setLayout({ name: e.target.value, value: e.target.value as any })}
              className="px-4 py-2 bg-white/10 border border-white/20 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="force">Force Directed</option>
              <option value="hierarchical">Hierarchical</option>
              <option value="circular">Circular</option>
              <option value="grid">Grid</option>
            </select>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
        {/* Main Graph Area */}
        <div className="lg:col-span-3">
          <div className="bg-white/10 backdrop-blur-lg rounded-lg p-6 h-[600px] relative overflow-hidden">
            {/* Graph Controls */}
            <div className="absolute top-4 right-4 z-10 flex gap-2">
              <button
                onClick={() => setZoom(Math.min(zoom * 1.2, 3))}
                className="p-2 bg-white/10 hover:bg-white/20 rounded-lg text-white transition-colors"
              >
                <PlusIcon className="w-4 h-4" />
              </button>
              <button
                onClick={() => setZoom(Math.max(zoom * 0.8, 0.3))}
                className="p-2 bg-white/10 hover:bg-white/20 rounded-lg text-white transition-colors"
              >
                <MinusIcon className="w-4 h-4" />
              </button>
              <button
                onClick={() => {
                  setZoom(1);
                  setPan({ x: 0, y: 0 });
                }}
                className="p-2 bg-white/10 hover:bg-white/20 rounded-lg text-white transition-colors"
              >
                <ArrowPathIcon className="w-4 h-4" />
              </button>
            </div>

            {/* SVG Graph */}
            <svg
              ref={svgRef}
              width="100%"
              height="100%"
              viewBox={`${-pan.x} ${-pan.y} ${800 / zoom} ${500 / zoom}`}
              onClick={handleCanvasClick}
              className="cursor-crosshair"
            >
              {/* Edges */}
              <g>
                {edges.map((edge, index) => {
                  const sourceNode = filteredNodes.find(n => n.id === edge.source);
                  const targetNode = filteredNodes.find(n => n.id === edge.target);
                  
                  if (!sourceNode || !targetNode) return null;
                  
                  return (
                    <motion.line
                      key={`${edge.source}-${edge.target}-${index}`}
                      x1={sourceNode.x}
                      y1={sourceNode.y}
                      x2={targetNode.x}
                      y2={targetNode.y}
                      stroke={getEdgeColor(edge.type)}
                      strokeWidth={edge.strength * 2}
                      strokeOpacity={0.6}
                      initial={{ pathLength: 0 }}
                      animate={{ pathLength: 1 }}
                      transition={{ duration: 0.5, delay: index * 0.01 }}
                    />
                  );
                })}
              </g>

              {/* Nodes */}
              <g>
                {filteredNodes.map((node) => (
                  <motion.g
                    key={node.id}
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    transition={{ duration: 0.3 }}
                    className="cursor-pointer"
                    onClick={() => handleNodeClick(node)}
                  >
                    {/* Node Circle */}
                    <motion.circle
                      cx={node.x}
                      cy={node.y}
                      r={node.size}
                      fill={node.color}
                      stroke="white"
                      strokeWidth={selectedNode?.id === node.id ? 4 : 2}
                      className="drop-shadow-lg"
                      whileHover={{ scale: 1.1 }}
                      whileTap={{ scale: 0.95 }}
                    />
                    
                    {/* Progress Ring for completed nodes */}
                    {node.progress !== undefined && node.progress > 0 && (
                      <motion.circle
                        cx={node.x}
                        cy={node.y}
                        r={node.size + 3}
                        fill="none"
                        stroke={node.isCompleted ? "#10B981" : "#3B82F6"}
                        strokeWidth={2}
                        strokeDasharray={`${2 * Math.PI * (node.size + 3)}`}
                        strokeDashoffset={`${2 * Math.PI * (node.size + 3) * (1 - node.progress / 100)}`}
                        className="drop-shadow-lg"
                        transform={`rotate(-90 ${node.x} ${node.y})`}
                      />
                    )}
                    
                    {/* Node Icon */}
                    <text
                      x={node.x}
                      y={node.y + (node.type === 'concept' ? 4 : 6)}
                      textAnchor="middle"
                      className="text-white pointer-events-none select-none"
                      style={{ fontSize: node.type === 'concept' ? '10px' : '12px' }}
                    >
                      {getNodeIcon(node.type)}
                    </text>
                    
                    {/* Node Label */}
                    {zoom > 0.7 && (
                      <text
                        x={node.x}
                        y={node.y + node.size + 15}
                        textAnchor="middle"
                        className="text-white text-sm pointer-events-none select-none fill-white"
                        style={{ textShadow: '1px 1px 2px rgba(0,0,0,0.8)' }}
                      >
                        {node.label.length > 15 ? node.label.substring(0, 15) + '...' : node.label}
                      </text>
                    )}
                  </motion.g>
                ))}
              </g>
            </svg>

            {/* Legend */}
            <div className="absolute bottom-4 left-4 bg-black/20 backdrop-blur-sm rounded-lg p-3 text-white text-sm">
              <div className="flex items-center gap-4">
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 rounded-full bg-blue-500"></div>
                  <span>Learning Paths</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 rounded-full bg-green-500"></div>
                  <span>Modules</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 rounded-full bg-purple-500"></div>
                  <span>Concepts</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Statistics */}
          {showStats && (
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              className="bg-white/10 backdrop-blur-lg rounded-lg p-6"
            >
              <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                <AcademicCapIcon className="w-5 h-5" />
                Statistics
              </h3>
              <div className="space-y-3 text-sm">
                <div className="flex justify-between text-white">
                  <span>Learning Paths:</span>
                  <span className="font-semibold">{stats.completedPaths}/{stats.totalPaths}</span>
                </div>
                <div className="flex justify-between text-white">
                  <span>Modules:</span>
                  <span className="font-semibold">{stats.completedModules}/{stats.totalModules}</span>
                </div>
                <div className="flex justify-between text-white">
                  <span>Concepts:</span>
                  <span className="font-semibold">{stats.totalConcepts}</span>
                </div>
                <div className="flex justify-between text-white">
                  <span>Avg. Progress:</span>
                  <span className="font-semibold">{stats.averageProgress.toFixed(1)}%</span>
                </div>
              </div>
            </motion.div>
          )}

          {/* Filters Panel */}
          <AnimatePresence>
            {showFilters && (
              <motion.div
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: 20 }}
                className="bg-white/10 backdrop-blur-lg rounded-lg p-6"
              >
                <h3 className="text-lg font-semibold text-white mb-4">Filters</h3>
                
                {/* Difficulty Filter */}
                <div className="mb-4">
                  <label className="text-sm text-gray-300 mb-2 block">Difficulty</label>
                  <div className="space-y-2">
                    {['beginner', 'intermediate', 'advanced'].map((difficulty) => (
                      <label key={difficulty} className="flex items-center text-white text-sm">
                        <input
                          type="checkbox"
                          checked={filters.difficulty.includes(difficulty)}
                          onChange={(e) => {
                            if (e.target.checked) {
                              setFilters(prev => ({
                                ...prev,
                                difficulty: [...prev.difficulty, difficulty]
                              }));
                            } else {
                              setFilters(prev => ({
                                ...prev,
                                difficulty: prev.difficulty.filter(d => d !== difficulty)
                              }));
                            }
                          }}
                          className="mr-2 rounded"
                        />
                        <span className="capitalize">{difficulty}</span>
                      </label>
                    ))}
                  </div>
                </div>

                {/* Status Filter */}
                <div className="mb-4">
                  <label className="text-sm text-gray-300 mb-2 block">Status</label>
                  <div className="space-y-2">
                    <label className="flex items-center text-white text-sm">
                      <input
                        type="checkbox"
                        checked={filters.showCompleted}
                        onChange={(e) => setFilters(prev => ({ ...prev, showCompleted: e.target.checked }))}
                        className="mr-2 rounded"
                      />
                      <span className="text-green-400">✓ Completed</span>
                    </label>
                    <label className="flex items-center text-white text-sm">
                      <input
                        type="checkbox"
                        checked={filters.showInProgress}
                        onChange={(e) => setFilters(prev => ({ ...prev, showInProgress: e.target.checked }))}
                        className="mr-2 rounded"
                      />
                      <span className="text-blue-400">▶ In Progress</span>
                    </label>
                    <label className="flex items-center text-white text-sm">
                      <input
                        type="checkbox"
                        checked={filters.showNotStarted}
                        onChange={(e) => setFilters(prev => ({ ...prev, showNotStarted: e.target.checked }))}
                        className="mr-2 rounded"
                      />
                      <span className="text-gray-400">○ Not Started</span>
                    </label>
                  </div>
                </div>
              </motion.div>
            )}
          </AnimatePresence>

          {/* Selected Node Details */}
          <AnimatePresence>
            {selectedNode && (
              <motion.div
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: 20 }}
                className="bg-white/10 backdrop-blur-lg rounded-lg p-6"
              >
                <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                  {getNodeTypeIcon(selectedNode.type)}
                  {selectedNode.label}
                </h3>
                
                <div className="space-y-3 text-sm text-white">
                  <div>
                    <span className="text-gray-300">Type:</span>
                    <span className="ml-2 capitalize">{selectedNode.type.replace('_', ' ')}</span>
                  </div>
                  
                  {selectedNode.data?.difficulty && (
                    <div>
                      <span className="text-gray-300">Difficulty:</span>
                      <span className="ml-2 capitalize">{selectedNode.data.difficulty}</span>
                    </div>
                  )}
                  
                  {selectedNode.data?.description && (
                    <div>
                      <span className="text-gray-300">Description:</span>
                      <p className="mt-1 text-gray-100">{selectedNode.data.description}</p>
                    </div>
                  )}
                  
                  {selectedNode.progress !== undefined && (
                    <div>
                      <span className="text-gray-300">Progress:</span>
                      <div className="mt-1">
                        <div className="w-full bg-gray-700 rounded-full h-2">
                          <div
                            className={`h-2 rounded-full ${
                              selectedNode.isCompleted ? 'bg-green-500' : 'bg-blue-500'
                            }`}
                            style={{ width: `${selectedNode.progress}%` }}
                          ></div>
                        </div>
                        <span className="text-xs text-gray-300 mt-1">
                          {selectedNode.progress.toFixed(1)}%
                        </span>
                      </div>
                    </div>
                  )}
                  
                  {selectedNode.data?.concepts && (
                    <div>
                      <span className="text-gray-300">Concepts:</span>
                      <div className="mt-1 flex flex-wrap gap-1">
                        {selectedNode.data.concepts.map((concept: string) => (
                          <span
                            key={concept}
                            className="px-2 py-1 bg-blue-500/20 text-blue-300 rounded text-xs"
                          >
                            {concept}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>
    </div>
  );

  // Helper functions
  function getNodeIcon(type: string) {
    switch (type) {
      case 'learning_path': return '📚';
      case 'module': return '📖';
      case 'concept': return '💡';
      default: return '●';
    }
  }

  function getNodeTypeIcon(type: string) {
    switch (type) {
      case 'learning_path': return <BookOpenIcon className="w-5 h-5" />;
      case 'module': return <AcademicCapIcon className="w-5 h-5" />;
      case 'concept': return <CodeBracketIcon className="w-5 h-5" />;
      default: return <StarIcon className="w-5 h-5" />;
    }
  }

  function getEdgeColor(type: string) {
    switch (type) {
      case 'prerequisite': return '#EF4444';
      case 'contains': return '#3B82F6';
      case 'related': return '#8B5CF6';
      case 'mastery': return '#10B981';
      default: return '#6B7280';
    }
  }
};

export default KnowledgeGraph;