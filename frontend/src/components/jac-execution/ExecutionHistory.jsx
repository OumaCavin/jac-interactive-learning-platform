import React, { useState, useEffect } from 'react';
import { 
  History, 
  Clock, 
  CheckCircle, 
  XCircle, 
  AlertTriangle, 
  Loader,
  Search,
  Filter,
  Trash2,
  Play,
  BarChart3,
  Calendar,
  ChevronLeft,
  ChevronRight,
  RefreshCw
} from 'lucide-react';

const ExecutionHistory = ({ onSelectExecution, onRefreshHistory }) => {
  const [executions, setExecutions] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(false);
  const [currentPage, setCurrentPage] = useState(1);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');
  const [languageFilter, setLanguageFilter] = useState('all');
  const [showStats, setShowStats] = useState(false);
  const itemsPerPage = 10;

  const API_BASE = '/api/jac-execution';

  useEffect(() => {
    loadHistory();
  }, [currentPage, searchTerm, statusFilter, languageFilter]);

  const loadHistory = async () => {
    setLoading(true);
    try {
      const token = localStorage.getItem('access_token');
      const params = new URLSearchParams({
        page: currentPage,
        per_page: itemsPerPage,
        ...(searchTerm && { search: searchTerm }),
        ...(statusFilter !== 'all' && { status: statusFilter }),
        ...(languageFilter !== 'all' && { language: languageFilter })
      });

      const [historyResponse, statsResponse] = await Promise.all([
        fetch(`${API_BASE}/executions/history/?${params}`, {
          headers: { 'Authorization': `Bearer ${token}` }
        }),
        fetch(`${API_BASE}/executions/statistics/`, {
          headers: { 'Authorization': `Bearer ${token}` }
        })
      ]);

      if (historyResponse.ok) {
        const historyData = await historyResponse.json();
        setExecutions(historyData.results || []);
      }

      if (statsResponse.ok) {
        const statsData = await statsResponse.json();
        setStats(statsData);
      }
    } catch (error) {
      console.error('Failed to load execution history:', error);
    } finally {
      setLoading(false);
    }
  };

  const clearHistory = async () => {
    if (!window.confirm('Are you sure you want to clear all execution history? This action cannot be undone.')) {
      return;
    }

    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch(`${API_BASE}/executions/clear_history/`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` }
      });

      if (response.ok) {
        setExecutions([]);
        setCurrentPage(1);
        loadHistory(); // Refresh to update stats
      }
    } catch (error) {
      console.error('Failed to clear history:', error);
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="w-4 h-4 text-green-500" />;
      case 'failed':
        return <XCircle className="w-4 h-4 text-red-500" />;
      case 'timeout':
        return <AlertTriangle className="w-4 h-4 text-orange-500" />;
      case 'running':
        return <Loader className="w-4 h-4 text-blue-500 animate-spin" />;
      default:
        return <Clock className="w-4 h-4 text-gray-500" />;
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'completed':
        return 'bg-green-100 text-green-800';
      case 'failed':
        return 'bg-red-100 text-red-800';
      case 'timeout':
        return 'bg-orange-100 text-orange-800';
      case 'running':
        return 'bg-blue-100 text-blue-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const handleSelectExecution = (execution) => {
    onSelectExecution(execution);
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleString();
  };

  const filteredExecutions = executions.filter(execution => {
    if (searchTerm) {
      const searchLower = searchTerm.toLowerCase();
      return execution.summary?.status?.toLowerCase().includes(searchLower) ||
             execution.language?.toLowerCase().includes(searchLower);
    }
    return true;
  });

  return (
    <div className="bg-white border-t border-gray-200">
      <div className="p-4">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-gray-900 flex items-center space-x-2">
            <History className="w-5 h-5" />
            <span>Execution History</span>
          </h3>
          
          <div className="flex items-center space-x-2">
            <button
              onClick={() => setShowStats(!showStats)}
              className="p-2 text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded-lg"
              title="Show Statistics"
            >
              <BarChart3 className="w-4 h-4" />
            </button>
            
            <button
              onClick={loadHistory}
              className="p-2 text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded-lg"
              title="Refresh"
              disabled={loading}
            >
              <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
            </button>
            
            <button
              onClick={clearHistory}
              className="p-2 text-red-600 hover:text-red-800 hover:bg-red-50 rounded-lg"
              title="Clear History"
            >
              <Trash2 className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Statistics Panel */}
        {showStats && stats && (
          <div className="mb-4 p-3 bg-blue-50 rounded-lg">
            <h4 className="font-medium text-blue-900 mb-2">Statistics</h4>
            <div className="grid grid-cols-2 gap-3 text-sm">
              <div>
                <span className="text-blue-700">Total Executions:</span>
                <span className="font-medium text-blue-900 ml-1">{stats.total_executions}</span>
              </div>
              <div>
                <span className="text-blue-700">Success Rate:</span>
                <span className="font-medium text-blue-900 ml-1">{stats.success_rate.toFixed(1)}%</span>
              </div>
              <div>
                <span className="text-blue-700">Python Executions:</span>
                <span className="font-medium text-blue-900 ml-1">{stats.language_distribution?.python || 0}</span>
              </div>
              <div>
                <span className="text-blue-700">JAC Executions:</span>
                <span className="font-medium text-blue-900 ml-1">{stats.language_distribution?.jac || 0}</span>
              </div>
            </div>
          </div>
        )}

        {/* Search and Filters */}
        <div className="space-y-3">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
            <input
              type="text"
              placeholder="Search executions..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-medium text-gray-700 mb-1">
                Status
              </label>
              <select
                value={statusFilter}
                onChange={(e) => setStatusFilter(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="all">All Statuses</option>
                <option value="completed">Completed</option>
                <option value="failed">Failed</option>
                <option value="timeout">Timeout</option>
                <option value="running">Running</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-medium text-gray-700 mb-1">
                Language
              </label>
              <select
                value={languageFilter}
                onChange={(e) => setLanguageFilter(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="all">All Languages</option>
                <option value="python">Python</option>
                <option value="jac">JAC</option>
              </select>
            </div>
          </div>
        </div>

        {/* Executions List */}
        <div className="mt-4 max-h-80 overflow-y-auto">
          {loading ? (
            <div className="flex items-center justify-center py-8">
              <Loader className="w-6 h-6 text-blue-500 animate-spin mr-2" />
              <span className="text-gray-600">Loading executions...</span>
            </div>
          ) : filteredExecutions.length === 0 ? (
            <div className="text-center py-8 text-gray-500">
              <History className="w-12 h-12 mx-auto mb-3 text-gray-300" />
              <p className="text-sm">
                {searchTerm || statusFilter !== 'all' || languageFilter !== 'all'
                  ? 'No executions found matching your criteria'
                  : 'No execution history available'}
              </p>
            </div>
          ) : (
            <div className="space-y-2">
              {filteredExecutions.map((execution) => (
                <div
                  key={execution.id}
                  className="border border-gray-200 rounded-lg p-3 hover:border-blue-300 transition-colors cursor-pointer"
                  onClick={() => handleSelectExecution(execution)}
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                      {getStatusIcon(execution.status)}
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center space-x-2 mb-1">
                          <span className={`px-2 py-1 text-xs rounded-full ${getStatusColor(execution.status)}`}>
                            {execution.status}
                          </span>
                          <span className={`px-2 py-1 text-xs rounded-full ${
                            execution.language === 'python' 
                              ? 'bg-green-100 text-green-800' 
                              : 'bg-blue-100 text-blue-800'
                          }`}>
                            {execution.language}
                          </span>
                        </div>
                        
                        <div className="text-sm text-gray-600">
                          {execution.execution_time && (
                            <span>{execution.execution_time.toFixed(3)}s</span>
                          )}
                        </div>
                      </div>
                    </div>
                    
                    <div className="text-right">
                      <div className="text-xs text-gray-500 mb-1">
                        {formatDate(execution.created_at)}
                      </div>
                      {execution.summary && (
                        <div className="text-xs text-gray-400">
                          {execution.summary.has_output && '📤 '}
                          {execution.summary.has_error && '⚠️ '}
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Pagination */}
        {filteredExecutions.length > 0 && (
          <div className="mt-4 flex items-center justify-between">
            <div className="text-sm text-gray-600">
              Page {currentPage}
            </div>
            
            <div className="flex items-center space-x-2">
              <button
                onClick={() => setCurrentPage(Math.max(1, currentPage - 1))}
                disabled={currentPage <= 1}
                className="p-2 text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <ChevronLeft className="w-4 h-4" />
              </button>
              
              <button
                onClick={() => setCurrentPage(currentPage + 1)}
                disabled={executions.length < itemsPerPage}
                className="p-2 text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <ChevronRight className="w-4 h-4" />
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ExecutionHistory;