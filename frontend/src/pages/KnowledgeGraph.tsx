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
  StarIcon,
  ExclamationTriangleIcon,
  ArrowDownTrayIcon
} from '@heroicons/react/24/outline';
import { useSelector } from 'react-redux';
import { selectLearning, selectUserLearningPaths, selectUserModuleProgress } from '../store/slices/learningSlice';
import { selectUser } from '../store/slices/authSlice';
import knowledgeGraphService, { 
  GraphData, 
  KnowledgeNode, 
  KnowledgeEdge, 
  GraphAnalytics,
  GraphSearchParams 
} from '../services/knowledgeGraphService';

// Types for knowledge graph visualization
interface GraphNode {
  id: string;
  type: KnowledgeNode['node_type'];
  label: string;
  x: number;
  y: number;
  vx?: number;
  vy?: number;
  size: number;
  color: string;
  data: KnowledgeNode;
  isCompleted?: boolean;
  progress?: number;
}

interface GraphEdge {
  source: string;
  target: string;
  type: KnowledgeEdge['edge_type'];
  strength: number;
  data: KnowledgeEdge;
}

interface LayoutType {
  name: string;
  value: 'force' | 'hierarchical' | 'circular' | 'grid';
}

// Graph loading and error states
interface LoadingState {
  graph: boolean;
  analytics: boolean;
  search: boolean;
}

interface ErrorState {
  graph: string | null;
  analytics: string | null;
  search: string | null;
}

const KnowledgeGraph: React.FC = () => {
  const svgRef = useRef<SVGSVGElement>(null);
  const [nodes, setNodes] = useState<GraphNode[]>([]);
  const [edges, setEdges] = useState<GraphEdge[]>([]);
  const [selectedNode, setSelectedNode] = useState<GraphNode | null>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [filters, setFilters] = useState({
    difficulty: [] as string[],
    concept: [] as string[],
    nodeTypes: [] as string[],
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
  const [analytics, setAnalytics] = useState<GraphAnalytics | null>(null);
  
  // Loading and error states
  const [loading, setLoading] = useState<LoadingState>({
    graph: true,
    analytics: false,
    search: false
  });
  
  const [errors, setErrors] = useState<ErrorState>({
    graph: null,
    analytics: null,
    search: null
  });
  
  const user = useSelector(selectUser);
  const learningPaths = useSelector(selectLearning).learning_paths;
  const userLearningPaths = useSelector(selectUserLearningPaths);
  const userModuleProgress = useSelector(selectUserModuleProgress);

  // Load knowledge graph data from API
  const loadGraphData = useCallback(async () => {
    setLoading(prev => ({ ...prev, graph: true }));
    setErrors(prev => ({ ...prev, graph: null }));
    
    try {
      const graphData: GraphData = await knowledgeGraphService.getCompleteGraph();
      
      // Convert backend nodes to visualization nodes
      const graphNodes: GraphNode[] = graphData.nodes.map((node, index) => {
        const userPathProgress = userLearningPaths.find(p => p.learning_path === node.id);
        const userModule = userModuleProgress.find(p => p.module === node.id);
        const isCompleted = userPathProgress?.status === 'completed' || userModule?.status === 'completed';
        const progress = userPathProgress?.progress_percentage || userModule?.progress_percentage || 0;
        
        // Calculate position based on node type and index
        let x = node.x_position || 400;
        let y = node.y_position || 300;
        let size = 20;
        
        switch (node.node_type) {
          case 'learning_path':
            size = 40;
            if (!node.x_position || !node.y_position) {
              x = Math.cos((index / graphData.nodes.filter(n => n.node_type === 'learning_path').length) * 2 * Math.PI) * 300 + 400;
              y = Math.sin((index / graphData.nodes.filter(n => n.node_type === 'learning_path').length) * 2 * Math.PI) * 200 + 300;
            }
            break;
          case 'module':
            size = 25;
            if (!node.x_position || !node.y_position) {
              x = 400 + (Math.random() - 0.5) * 100;
              y = 300 + (Math.random() - 0.5) * 100;
            }
            break;
          case 'concept':
            size = 15;
            if (!node.x_position || !node.y_position) {
              const conceptIndex = graphData.nodes.filter(n => n.node_type === 'concept').indexOf(node);
              x = Math.cos((conceptIndex / graphData.nodes.filter(n => n.node_type === 'concept').length) * 2 * Math.PI) * 400 + 400;
              y = Math.sin((conceptIndex / graphData.nodes.filter(n => n.node_type === 'concept').length) * 2 * Math.PI) * 300 + 300;
            }
            break;
          default:
            size = 20;
        }
        
        return {
          id: node.id,
          type: node.node_type,
          label: node.title,
          x,
          y,
          size,
          color: getDifficultyColor(node.difficulty_level),
          data: node,
          isCompleted,
          progress
        };
      });

      // Convert backend edges to visualization edges
      const graphEdges: GraphEdge[] = graphData.edges.map(edge => ({
        source: edge.source_node,
        target: edge.target_node,
        type: edge.edge_type,
        strength: edge.strength,
        data: edge
      }));

      setNodes(graphNodes);
      setEdges(graphEdges);
    } catch (error: any) {
      console.error('Error loading knowledge graph:', error);
      setErrors(prev => ({ 
        ...prev, 
        graph: error.message || 'Failed to load knowledge graph data' 
      }));
    } finally {
      setLoading(prev => ({ ...prev, graph: false }));
    }
  }, [userLearningPaths, userModuleProgress]);

  // Load analytics data
  const loadAnalytics = useCallback(async () => {
    setLoading(prev => ({ ...prev, analytics: true }));
    setErrors(prev => ({ ...prev, analytics: null }));
    
    try {
      const analyticsData = await knowledgeGraphService.getGraphAnalytics();
      setAnalytics(analyticsData);
    } catch (error: any) {
      console.error('Error loading analytics:', error);
      setErrors(prev => ({ 
        ...prev, 
        analytics: error.message || 'Failed to load graph analytics' 
      }));
    } finally {
      setLoading(prev => ({ ...prev, analytics: false }));
    }
  }, []);

  // Search graph
  const searchGraph = useCallback(async (query: string, searchFilters?: Partial<GraphSearchParams>) => {
    if (!query.trim()) {
      // If no query, reload the complete graph
      loadGraphData();
      return;
    }

    setLoading(prev => ({ ...prev, search: true }));
    setErrors(prev => ({ ...prev, search: null }));
    
    try {
      const searchParams: GraphSearchParams = {
        query: query.trim(),
        node_types: searchFilters?.nodeTypes,
        difficulty_levels: searchFilters?.difficulty_levels,
        limit: 100
      };
      
      const searchResults = await knowledgeGraphService.searchGraph(searchParams);
      
      // Convert search results to visualization format
      const graphNodes: GraphNode[] = searchResults.nodes.map(node => ({
        id: node.id,
        type: node.node_type,
        label: node.title,
        x: node.x_position || 400,
        y: node.y_position || 300,
        size: node.node_type === 'learning_path' ? 40 : node.node_type === 'module' ? 25 : 15,
        color: getDifficultyColor(node.difficulty_level),
        data: node
      }));

      const graphEdges: GraphEdge[] = searchResults.edges.map(edge => ({
        source: edge.source_node,
        target: edge.target_node,
        type: edge.edge_type,
        strength: edge.strength,
        data: edge
      }));

      setNodes(graphNodes);
      setEdges(graphEdges);
    } catch (error: any) {
      console.error('Error searching graph:', error);
      setErrors(prev => ({ 
        ...prev, 
        search: error.message || 'Failed to search knowledge graph' 
      }));
    } finally {
      setLoading(prev => ({ ...prev, search: false }));
    }
  }, [loadGraphData]);

  // Initialize graph data and analytics on component mount
  useEffect(() => {
    loadGraphData();
    loadAnalytics();
  }, [loadGraphData, loadAnalytics]);

  // Get color for difficulty level
  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'beginner': return '#10B981'; // green
      case 'intermediate': return '#F59E0B'; // amber
      case 'advanced': return '#EF4444'; // red
      default: return '#6B7280'; // gray
    }
  };

  // Get color for node type
  const getNodeTypeColor = (nodeType: string) => {
    const colors = {
      learning_path: '#3B82F6',
      module: '#10B981',
      concept: '#8B5CF6',
      lesson: '#F59E0B',
      assessment: '#EF4444'
    };
    return colors[nodeType as keyof typeof colors] || '#6B7280';
  };

  // Get node icon based on type
  const getNodeIcon = (type: string) => {
    switch (type) {
      case 'learning_path': return '📚';
      case 'module': return '📖';
      case 'concept': return '💡';
      case 'lesson': return '📝';
      case 'assessment': return '✅';
      default: return '●';
    }
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
    const matchesSearch = node.label.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         node.data.description?.toLowerCase().includes(searchQuery.toLowerCase());
    
    // Apply difficulty filter
    if (filters.difficulty.length > 0) {
      if (!filters.difficulty.includes(node.data.difficulty_level)) return false;
    }

    // Apply node type filter
    if (filters.nodeTypes.length > 0) {
      if (!filters.nodeTypes.includes(node.type)) return false;
    }

    // Apply status filter
    if (node.type === 'learning_path' || node.type === 'module') {
      if (node.isCompleted && !filters.showCompleted) return false;
      if (!node.isCompleted && node.progress && node.progress > 0 && !filters.showInProgress) return false;
      if (!node.isCompleted && (!node.progress || node.progress === 0) && !filters.showNotStarted) return false;
    }

    return matchesSearch;
  });

  // Handle search input change with debouncing
  const handleSearchChange = useCallback((query: string) => {
    setSearchQuery(query);
    // Debounce search to avoid too many API calls
    const timeoutId = setTimeout(() => {
      if (query.trim()) {
        searchGraph(query, {
          node_types: filters.nodeTypes.length > 0 ? filters.nodeTypes : undefined,
          difficulty_levels: filters.difficulty.length > 0 ? filters.difficulty : undefined
        });
      } else {
        loadGraphData();
      }
    }, 500);

    return () => clearTimeout(timeoutId);
  }, [filters.nodeTypes, filters.difficulty, searchGraph, loadGraphData]);

  // Handle filter changes
  const handleFilterChange = useCallback((filterType: string, value: any) => {
    setFilters(prev => ({
      ...prev,
      [filterType]: value
    }));
    
    // If we have an active search, re-search with new filters
    if (searchQuery.trim()) {
      searchGraph(searchQuery, {
        node_types: filterType === 'nodeTypes' ? value : filters.nodeTypes,
        difficulty_levels: filterType === 'difficulty' ? value : filters.difficulty
      });
    }
  }, [searchQuery, filters.nodeTypes, filters.difficulty, searchGraph]);

  // Calculate statistics from current graph data
  const stats = {
    totalPaths: nodes.filter(n => n.type === 'learning_path').length,
    totalModules: nodes.filter(n => n.type === 'module').length,
    totalConcepts: nodes.filter(n => n.type === 'concept').length,
    completedPaths: nodes.filter(n => n.type === 'learning_path' && n.isCompleted).length,
    completedModules: nodes.filter(n => n.type === 'module' && n.isCompleted).length,
    averageProgress: nodes.filter(n => n.type === 'learning_path' || n.type === 'module')
      .reduce((sum, node) => sum + (node.progress || 0), 0) / 
      Math.max(nodes.filter(n => n.type === 'learning_path' || n.type === 'module').length, 1),
    totalNodes: nodes.length,
    totalEdges: edges.length
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
              placeholder="Search concepts, modules, paths..."
              value={searchQuery}
              onChange={(e) => handleSearchChange(e.target.value)}
              disabled={loading.search}
              className="pl-10 pr-4 py-2 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 w-full sm:w-64 disabled:opacity-50"
            />
            {loading.search && (
              <div className="absolute right-3 top-1/2 transform -translate-y-1/2">
                <ArrowPathIcon className="w-4 h-4 text-gray-400 animate-spin" />
              </div>
            )}
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
            
            <button
              onClick={() => {
                loadGraphData();
                loadAnalytics();
              }}
              disabled={loading.graph || loading.analytics}
              className="px-4 py-2 bg-white/10 border border-white/20 rounded-lg text-white hover:bg-white/20 transition-colors flex items-center gap-2 disabled:opacity-50"
            >
              <ArrowPathIcon className={`w-4 h-4 ${loading.graph || loading.analytics ? 'animate-spin' : ''}`} />
              Refresh
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

      {/* Error States */}
      {(errors.graph || errors.search) && (
        <div className="mb-6 bg-red-500/10 border border-red-500/20 rounded-lg p-4">
          <div className="flex items-center gap-2 text-red-400">
            <ExclamationTriangleIcon className="w-5 h-5" />
            <span className="font-medium">Error Loading Data</span>
          </div>
          <p className="text-red-300 mt-2">
            {errors.graph || errors.search}
          </p>
          <button
            onClick={() => {
              setErrors({ graph: null, analytics: null, search: null });
              loadGraphData();
            }}
            className="mt-3 px-4 py-2 bg-red-500/20 hover:bg-red-500/30 rounded-lg text-red-300 transition-colors flex items-center gap-2"
          >
            <ArrowPathIcon className="w-4 h-4" />
            Retry
          </button>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
        {/* Main Graph Area */}
        <div className="lg:col-span-3">
          <div className="bg-white/10 backdrop-blur-lg rounded-lg p-6 h-[600px] relative overflow-hidden">
            {/* Loading Overlay */}
            {loading.graph && (
              <div className="absolute inset-0 bg-black/20 backdrop-blur-sm z-10 flex items-center justify-center">
                <div className="text-center">
                  <ArrowPathIcon className="w-8 h-8 text-white animate-spin mx-auto mb-2" />
                  <p className="text-white">Loading knowledge graph...</p>
                </div>
              </div>
            )}
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
              <div className="grid grid-cols-2 gap-2">
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
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 rounded-full bg-amber-500"></div>
                  <span>Lessons</span>
                </div>
              </div>
              
              {/* Edge Types Legend */}
              <div className="mt-3 pt-3 border-t border-white/20">
                <div className="text-xs text-gray-300 mb-1">Relationships:</div>
                <div className="grid grid-cols-1 gap-1 text-xs">
                  <div className="flex items-center gap-2">
                    <div className="w-3 h-0.5 bg-red-500"></div>
                    <span>Prerequisite</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <div className="w-3 h-0.5 bg-blue-500"></div>
                    <span>Contains</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <div className="w-3 h-0.5 bg-purple-500"></div>
                    <span>Related</span>
                  </div>
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
                {loading.analytics && <ArrowPathIcon className="w-4 h-4 animate-spin" />}
              </h3>
              <div className="space-y-3 text-sm">
                <div className="flex justify-between text-white">
                  <span>Total Nodes:</span>
                  <span className="font-semibold">{stats.totalNodes}</span>
                </div>
                <div className="flex justify-between text-white">
                  <span>Total Edges:</span>
                  <span className="font-semibold">{stats.totalEdges}</span>
                </div>
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
                
                {/* Analytics from backend if available */}
                {analytics && !loading.analytics && (
                  <>
                    <div className="border-t border-white/20 pt-3 mt-3">
                      <h4 className="text-sm font-medium text-gray-300 mb-2">Analytics</h4>
                      {analytics.completion_statistics && (
                        <div className="space-y-2">
                          <div className="flex justify-between text-white">
                            <span>Completed Paths:</span>
                            <span className="font-semibold">{analytics.completion_statistics.completed_paths}</span>
                          </div>
                          <div className="flex justify-between text-white">
                            <span>In Progress:</span>
                            <span className="font-semibold">{analytics.completion_statistics.in_progress_paths}</span>
                          </div>
                          <div className="flex justify-between text-white">
                            <span>Completion Rate:</span>
                            <span className="font-semibold">{analytics.completion_statistics.average_completion_rate.toFixed(1)}%</span>
                          </div>
                        </div>
                      )}
                    </div>
                  </>
                )}
                
                {errors.analytics && (
                  <div className="text-red-400 text-xs">
                    {errors.analytics}
                  </div>
                )}
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
                
                {/* Node Type Filter */}
                <div className="mb-4">
                  <label className="text-sm text-gray-300 mb-2 block">Node Types</label>
                  <div className="space-y-2">
                    {[
                      { value: 'learning_path', label: 'Learning Paths', icon: '📚' },
                      { value: 'module', label: 'Modules', icon: '📖' },
                      { value: 'concept', label: 'Concepts', icon: '💡' },
                      { value: 'lesson', label: 'Lessons', icon: '📝' },
                      { value: 'assessment', label: 'Assessments', icon: '✅' }
                    ].map((nodeType) => (
                      <label key={nodeType.value} className="flex items-center text-white text-sm">
                        <input
                          type="checkbox"
                          checked={filters.nodeTypes.includes(nodeType.value)}
                          onChange={(e) => {
                            const updatedTypes = e.target.checked
                              ? [...filters.nodeTypes, nodeType.value]
                              : filters.nodeTypes.filter(t => t !== nodeType.value);
                            handleFilterChange('nodeTypes', updatedTypes);
                          }}
                          className="mr-2 rounded"
                        />
                        <span className="mr-2">{nodeType.icon}</span>
                        <span className="capitalize">{nodeType.label}</span>
                      </label>
                    ))}
                  </div>
                </div>

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
                            const updatedDifficulty = e.target.checked
                              ? [...filters.difficulty, difficulty]
                              : filters.difficulty.filter(d => d !== difficulty);
                            handleFilterChange('difficulty', updatedDifficulty);
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
                  
                  {selectedNode.data?.difficulty_level && (
                    <div>
                      <span className="text-gray-300">Difficulty:</span>
                      <span className="ml-2 capitalize">{selectedNode.data.difficulty_level}</span>
                    </div>
                  )}
                  
                  {selectedNode.data?.description && (
                    <div>
                      <span className="text-gray-300">Description:</span>
                      <p className="mt-1 text-gray-100">{selectedNode.data.description}</p>
                    </div>
                  )}
                  
                  {selectedNode.data?.learning_objectives && selectedNode.data.learning_objectives.length > 0 && (
                    <div>
                      <span className="text-gray-300">Learning Objectives:</span>
                      <ul className="mt-1 list-disc list-inside text-gray-100">
                        {selectedNode.data.learning_objectives.map((objective: string, index: number) => (
                          <li key={index} className="text-xs">{objective}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                  
                  {selectedNode.data?.prerequisites && selectedNode.data.prerequisites.length > 0 && (
                    <div>
                      <span className="text-gray-300">Prerequisites:</span>
                      <div className="mt-1 flex flex-wrap gap-1">
                        {selectedNode.data.prerequisites.map((prereq: string) => (
                          <span
                            key={prereq}
                            className="px-2 py-1 bg-red-500/20 text-red-300 rounded text-xs"
                          >
                            {prereq}
                          </span>
                        ))}
                      </div>
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
                  
                  {selectedNode.data?.view_count !== undefined && (
                    <div>
                      <span className="text-gray-300">Views:</span>
                      <span className="ml-2">{selectedNode.data.view_count}</span>
                    </div>
                  )}
                  
                  <div className="pt-2 border-t border-white/20">
                    <button
                      onClick={() => selectedNode && knowledgeGraphService.incrementNodeView(selectedNode.id)}
                      className="text-blue-400 hover:text-blue-300 text-xs flex items-center gap-1"
                    >
                      <ArrowDownTrayIcon className="w-3 h-3" />
                      Mark as Viewed
                    </button>
                  </div>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>
    </div>
  );

  // Helper functions
  function getNodeTypeIcon(type: string) {
    switch (type) {
      case 'learning_path': return <BookOpenIcon className="w-5 h-5" />;
      case 'module': return <AcademicCapIcon className="w-5 h-5" />;
      case 'concept': return <CodeBracketIcon className="w-5 h-5" />;
      case 'lesson': return <StarIcon className="w-5 h-5" />;
      case 'assessment': return <StarIcon className="w-5 h-5" />;
      default: return <StarIcon className="w-5 h-5" />;
    }
  }

  function getEdgeColor(type: string) {
    switch (type) {
      case 'prerequisite': return '#EF4444';
      case 'prerequisite_of': return '#EF4444';
      case 'contains': return '#3B82F6';
      case 'related': return '#8B5CF6';
      case 'leads_to': return '#10B981';
      case 'mastery': return '#10B981';
      default: return '#6B7280';
    }
  }
};

export default KnowledgeGraph;