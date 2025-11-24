import React, { useState, useRef, useEffect } from 'react';
import { 
  Play, 
  Square, 
  Copy, 
  Download, 
  Upload, 
  FileText, 
  Code, 
  Terminal,
  Clock,
  CheckCircle,
  XCircle,
  AlertCircle,
  Loader,
  History,
  Settings,
  Save,
  Share,
  ArrowRightLeft,
  X
} from 'lucide-react';
import CodeEditor from './CodeEditor';
import OutputWindow from './OutputWindow';
import TemplateSelector from './TemplateSelector';
import ExecutionHistory from './ExecutionHistory';
import SecuritySettings from './SecuritySettings';
import CodeTranslationPanel from './CodeTranslationPanel';

const CodeExecutionPanel = () => {
  const [code, setCode] = useState('# Welcome to JAC Code Executor\nprint("Hello, JAC Learning Platform!")');
  const [language, setLanguage] = useState('python');
  const [stdin, setStdin] = useState('');
  const [output, setOutput] = useState('');
  const [stderr, setStderr] = useState('');
  const [isExecuting, setIsExecuting] = useState(false);
  const [executionStatus, setExecutionStatus] = useState('idle'); // idle, running, completed, error, timeout
  const [executionTime, setExecutionTime] = useState(null);
  const [returnCode, setReturnCode] = useState(null);
  const [executionId, setExecutionId] = useState(null);
  const [showHistory, setShowHistory] = useState(false);
  const [showSettings, setShowSettings] = useState(false);
  const [showTranslation, setShowTranslation] = useState(false);
  const [templates, setTemplates] = useState([]);
  const [userStats, setUserStats] = useState(null);
  const [supportedLanguages, setSupportedLanguages] = useState({});
  
  const executionTimeoutRef = useRef(null);

  // API endpoints
  const API_BASE = '/api/jac-execution';

  // Load supported languages on component mount
  useEffect(() => {
    loadSupportedLanguages();
    loadUserStats();
    loadTemplates();
  }, []);

  const loadSupportedLanguages = async () => {
    try {
      const response = await fetch(`${API_BASE}/languages/`);
      if (response.ok) {
        const data = await response.json();
        setSupportedLanguages(data.supported_languages);
      }
    } catch (error) {
      console.error('Failed to load supported languages:', error);
    }
  };

  const loadUserStats = async () => {
    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch(`${API_BASE}/executions/statistics/`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      if (response.ok) {
        const data = await response.json();
        setUserStats(data);
      }
    } catch (error) {
      console.error('Failed to load user stats:', error);
    }
  };

  const loadTemplates = async () => {
    try {
      const response = await fetch(`${API_BASE}/templates/popular/`);
      if (response.ok) {
        const data = await response.json();
        setTemplates(data);
      }
    } catch (error) {
      console.error('Failed to load templates:', error);
    }
  };

  const executeCode = async (saveToHistory = true) => {
    if (isExecuting) return;

    setIsExecuting(true);
    setExecutionStatus('running');
    setOutput('');
    setStderr('');
    setExecutionTime(null);
    setReturnCode(null);

    try {
      const token = localStorage.getItem('access_token');
      let endpoint, method;
      
      if (saveToHistory) {
        endpoint = 'api/executions/execute/';
        method = 'POST';
      } else {
        endpoint = 'api/executions/quick-execute/';
        method = 'POST';
      }
      
      const response = await fetch(`${API_BASE}/${endpoint}`, {
        method,
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          language,
          code,
          stdin
        })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Execution failed');
      }

      const result = await response.json();
      
      if (result.success) {
        if (saveToHistory && result.execution) {
          setExecutionId(result.execution.id);
        }
        
        const outputData = result.output || result;
        setOutput(outputData.stdout || '');
        setStderr(outputData.stderr || '');
        setExecutionTime(outputData.execution_time || 0);
        setReturnCode(outputData.return_code || 0);
        
        if (outputData.status === 'timeout') {
          setExecutionStatus('timeout');
        } else if (outputData.return_code === 0) {
          setExecutionStatus('completed');
        } else {
          setExecutionStatus('error');
        }

        // Refresh user stats if execution was saved
        if (saveToHistory) {
          loadUserStats();
        }
      } else {
        throw new Error(result.error || 'Execution failed');
      }
    } catch (error) {
      setExecutionStatus('error');
      setStderr(error.message);
      setReturnCode(1);
    } finally {
      setIsExecuting(false);
    }
  };

  const stopExecution = () => {
    setIsExecuting(false);
    setExecutionStatus('error');
    setStderr('Execution stopped by user');
    if (executionTimeoutRef.current) {
      clearTimeout(executionTimeoutRef.current);
    }
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text).then(() => {
      // Could add a toast notification here
    });
  };

  const downloadCode = () => {
    const filename = `code.${language === 'python' ? 'py' : 'jac'}`;
    const element = document.createElement('a');
    const file = new Blob([code], { type: 'text/plain' });
    element.href = URL.createObjectURL(file);
    element.download = filename;
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
  };

  const loadTemplate = (templateCode, templateLanguage, templateStdin) => {
    setCode(templateCode);
    setLanguage(templateLanguage);
    if (templateStdin) {
      setStdin(templateStdin);
    }
  };

  const loadFromHistory = (execution) => {
    setCode(execution.code);
    setLanguage(execution.language);
    setStdin(execution.stdin || '');
    setExecutionId(execution.id);
  };

  const getStatusIcon = () => {
    switch (executionStatus) {
      case 'running':
        return <Loader className="w-5 h-5 text-blue-500 animate-spin" />;
      case 'completed':
        return <CheckCircle className="w-5 h-5 text-green-500" />;
      case 'error':
        return <XCircle className="w-5 h-5 text-red-500" />;
      case 'timeout':
        return <AlertCircle className="w-5 h-5 text-orange-500" />;
      default:
        return <Terminal className="w-5 h-5 text-gray-500" />;
    }
  };

  const getStatusText = () => {
    switch (executionStatus) {
      case 'running':
        return 'Executing...';
      case 'completed':
        return 'Completed Successfully';
      case 'error':
        return 'Execution Failed';
      case 'timeout':
        return 'Execution Timeout';
      default:
        return 'Ready to Execute';
    }
  };

  return (
    <div className="flex flex-col h-full bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <h1 className="text-2xl font-bold text-gray-900">JAC Code Executor</h1>
            <div className="flex items-center space-x-2">
              {getStatusIcon()}
              <span className="text-sm font-medium text-gray-600">{getStatusText()}</span>
            </div>
          </div>
          
          <div className="flex items-center space-x-3">
            {userStats && (
              <div className="flex items-center space-x-4 text-sm text-gray-600">
                <span>{userStats.total_executions} executions</span>
                <span>{userStats.success_rate.toFixed(1)}% success rate</span>
              </div>
            )}
            
            <button
              onClick={() => setShowHistory(!showHistory)}
              className="p-2 text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded-lg"
              title="Execution History"
            >
              <History className="w-5 h-5" />
            </button>
            
            <button
              onClick={() => setShowTranslation(!showTranslation)}
              className="p-2 text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded-lg"
              title="Code Translation"
            >
              <ArrowRightLeft className="w-5 h-5" />
            </button>
            
            <button
              onClick={() => setShowSettings(!showSettings)}
              className="p-2 text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded-lg"
              title="Settings"
            >
              <Settings className="w-5 h-5" />
            </button>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex overflow-hidden">
        {/* Left Panel - Code Editor and Controls */}
        <div className="flex-1 flex flex-col">
          {/* Language Selection and Quick Actions */}
          <div className="bg-white border-b border-gray-200 px-6 py-3">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-4">
                <select
                  value={language}
                  onChange={(e) => setLanguage(e.target.value)}
                  className="px-3 py-2 border border-gray-300 rounded-md text-sm font-medium focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  {Object.entries(supportedLanguages).map(([key, info]) => (
                    <option key={key} value={key}>
                      {info.name}
                    </option>
                  ))}
                </select>
                
                {executionTime && (
                  <div className="flex items-center space-x-1 text-sm text-gray-600">
                    <Clock className="w-4 h-4" />
                    <span>{executionTime.toFixed(3)}s</span>
                  </div>
                )}
              </div>

              <div className="flex items-center space-x-2">
                <button
                  onClick={() => copyToClipboard(code)}
                  className="p-2 text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded-lg"
                  title="Copy Code"
                >
                  <Copy className="w-4 h-4" />
                </button>
                
                <button
                  onClick={downloadCode}
                  className="p-2 text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded-lg"
                  title="Download Code"
                >
                  <Download className="w-4 h-4" />
                </button>
                
                <button
                  onClick={() => setStdin('')}
                  className="px-3 py-2 text-sm text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded-lg"
                  title="Clear Input"
                >
                  Clear Input
                </button>
              </div>
            </div>
          </div>

          {/* Code Editor */}
          <div className="flex-1 bg-white">
            <CodeEditor
              value={code}
              onChange={setCode}
              language={language}
              readOnly={isExecuting}
            />
          </div>

          {/* Input Section */}
          <div className="bg-white border-t border-gray-200 p-4">
            <div className="mb-2">
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Standard Input (optional)
              </label>
            </div>
            <textarea
              value={stdin}
              onChange={(e) => setStdin(e.target.value)}
              placeholder="Enter input data for your program..."
              className="w-full h-24 px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
              disabled={isExecuting}
            />
          </div>

          {/* Execution Controls */}
          <div className="bg-white border-t border-gray-200 px-6 py-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                {!isExecuting ? (
                  <>
                    <button
                      onClick={() => executeCode(false)}
                      className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                    >
                      <Play className="w-4 h-4" />
                      <span>Quick Execute</span>
                    </button>
                    
                    <button
                      onClick={() => executeCode(true)}
                      className="flex items-center space-x-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
                    >
                      <Save className="w-4 h-4" />
                      <span>Execute & Save</span>
                    </button>
                  </>
                ) : (
                  <button
                    onClick={stopExecution}
                    className="flex items-center space-x-2 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
                  >
                    <Square className="w-4 h-4" />
                    <span>Stop</span>
                  </button>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Right Panel - Output and Sidebar */}
        <div className="w-96 flex flex-col border-l border-gray-200 bg-white">
          {/* Output Window */}
          <div className="flex-1">
            <OutputWindow
              output={output}
              stderr={stderr}
              returnCode={returnCode}
              isLoading={isExecuting}
            />
          </div>

          {/* Sidebar with Templates and History */}
          {(showHistory || templates.length > 0) && (
            <div className="border-t border-gray-200">
              <TemplateSelector
                templates={templates}
                onSelectTemplate={loadTemplate}
                onRefreshTemplates={loadTemplates}
              />
              
              {showHistory && (
                <ExecutionHistory
                  onSelectExecution={loadFromHistory}
                  onRefreshHistory={loadUserStats}
                />
              )}
            </div>
          )}
        </div>
      </div>

      {/* Translation Panel */}
      {showTranslation && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg shadow-xl max-w-6xl w-full mx-4 max-h-[90vh] overflow-hidden relative">
            <CodeTranslationPanel
              originalCode={code}
              onCodeChange={setCode}
              currentLanguage={language}
              onLanguageChange={setLanguage}
              className="border-0 rounded-lg"
            />
            <button
              onClick={() => setShowTranslation(false)}
              className="absolute top-4 right-4 p-2 text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded-lg z-10"
              title="Close Translation"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>
      )}

      {/* Settings Panel */}
      {showSettings && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full mx-4 max-h-[80vh] overflow-y-auto">
            <SecuritySettings
              onClose={() => setShowSettings(false)}
              supportedLanguages={supportedLanguages}
            />
          </div>
        </div>
      )}
    </div>
  );
};

export default CodeExecutionPanel;