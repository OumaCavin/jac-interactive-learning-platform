import React, { useEffect, useRef } from 'react';
import { 
  CheckCircle, 
  XCircle, 
  AlertTriangle, 
  Clock,
  Copy,
  Download,
  Trash2,
  Eye,
  EyeOff,
  Terminal,
  ExternalLink
} from 'lucide-react';

const OutputWindow = ({ 
  output = '', 
  stderr = '', 
  returnCode = null, 
  isLoading = false,
  executionTime = null
}) => {
  const outputRef = useRef(null);
  const stderrRef = useRef(null);
  const [showOutput, setShowOutput] = React.useState(true);
  const [showStderr, setShowStderr] = React.useState(true);
  const [copiedOutput, setCopiedOutput] = React.useState(false);
  const [copiedStderr, setCopiedStderr] = React.useState(false);

  // Auto-scroll to bottom when new output arrives
  useEffect(() => {
    if (outputRef.current) {
      outputRef.current.scrollTop = outputRef.current.scrollHeight;
    }
  }, [output]);

  useEffect(() => {
    if (stderrRef.current) {
      stderrRef.current.scrollTop = stderrRef.current.scrollHeight;
    }
  }, [stderr]);

  const copyToClipboard = async (text, type) => {
    try {
      await navigator.clipboard.writeText(text);
      if (type === 'output') {
        setCopiedOutput(true);
        setTimeout(() => setCopiedOutput(false), 2000);
      } else {
        setCopiedStderr(true);
        setTimeout(() => setCopiedStderr(false), 2000);
      }
    } catch (err) {
      console.error('Failed to copy text: ', err);
    }
  };

  const downloadOutput = (text, filename) => {
    const element = document.createElement('a');
    const file = new Blob([text], { type: 'text/plain' });
    element.href = URL.createObjectURL(file);
    element.download = filename;
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
  };

  const clearOutput = () => {
    // This would typically call a parent function to clear the output
    // For now, we'll just clear the local state
    output = '';
    stderr = '';
  };

  const getStatusInfo = () => {
    if (isLoading) {
      return {
        icon: <Clock className="w-5 h-5 text-blue-500 animate-spin" />,
        text: 'Executing...',
        color: 'text-blue-600'
      };
    }

    if (returnCode === null) {
      return {
        icon: <Terminal className="w-5 h-5 text-gray-500" />,
        text: 'Ready to execute',
        color: 'text-gray-600'
      };
    }

    if (returnCode === 0) {
      return {
        icon: <CheckCircle className="w-5 h-5 text-green-500" />,
        text: 'Completed successfully',
        color: 'text-green-600'
      };
    } else if (returnCode === 124) {
      return {
        icon: <AlertTriangle className="w-5 h-5 text-orange-500" />,
        text: 'Execution timeout',
        color: 'text-orange-600'
      };
    } else {
      return {
        icon: <XCircle className="w-5 h-5 text-red-500" />,
        text: 'Execution failed',
        color: 'text-red-600'
      };
    }
  };

  const statusInfo = getStatusInfo();

  const renderOutputSection = (title, content, type, icon, showState, toggleShow) => {
    const hasContent = content && content.trim().length > 0;
    const isError = type === 'stderr';
    
    return (
      <div className="border-b border-gray-200 last:border-b-0">
        <div className="bg-gray-50 px-4 py-2 flex items-center justify-between">
          <div className="flex items-center space-x-2">
            {icon}
            <span className={`font-medium ${isError ? 'text-red-700' : 'text-gray-700'}`}>
              {title}
            </span>
            {hasContent && (
              <span className="text-xs text-gray-500 bg-gray-200 px-2 py-1 rounded">
                {content.split('\n').length} lines, {content.length} chars
              </span>
            )}
          </div>
          
          <div className="flex items-center space-x-2">
            {hasContent && (
              <>
                <button
                  onClick={() => copyToClipboard(content, type)}
                  className="p-1 text-gray-600 hover:text-gray-800 hover:bg-gray-200 rounded"
                  title="Copy to clipboard"
                >
                  <Copy className="w-4 h-4" />
                  {(type === 'output' && copiedOutput) || (type === 'stderr' && copiedStderr) ? (
                    <span className="text-xs text-green-600 ml-1">Copied!</span>
                  ) : null}
                </button>
                
                <button
                  onClick={() => downloadOutput(content, `${type}_${Date.now()}.txt`)}
                  className="p-1 text-gray-600 hover:text-gray-800 hover:bg-gray-200 rounded"
                  title="Download as file"
                >
                  <Download className="w-4 h-4" />
                </button>
              </>
            )}
            
            <button
              onClick={toggleShow}
              className="p-1 text-gray-600 hover:text-gray-800 hover:bg-gray-200 rounded"
              title={showState ? 'Hide' : 'Show'}
            >
              {showState ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
            </button>
          </div>
        </div>
        
        {showState && (
          <div className="relative">
            <div
              ref={type === 'output' ? outputRef : stderrRef}
              className={`h-48 overflow-y-auto p-4 font-mono text-sm ${
                isError 
                  ? 'bg-red-50 text-red-800' 
                  : 'bg-gray-900 text-green-400'
              }`}
            >
              {hasContent ? (
                <pre className="whitespace-pre-wrap break-words">
                  {content}
                </pre>
              ) : (
                <div className="text-gray-500 italic">
                  {isLoading ? 'Waiting for output...' : 'No output'}
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="h-full flex flex-col bg-white">
      {/* Header */}
      <div className="bg-gray-800 text-white px-4 py-3 flex items-center justify-between">
        <div className="flex items-center space-x-3">
          {statusInfo.icon}
          <span className={`font-medium ${statusInfo.color.replace('text-', 'text-white')}`}>
            {statusInfo.text}
          </span>
          {executionTime && (
            <span className="text-sm text-gray-300">
              ({executionTime.toFixed(3)}s)
            </span>
          )}
        </div>
        
        <div className="flex items-center space-x-2">
          <button
            onClick={clearOutput}
            className="p-1 text-gray-300 hover:text-white hover:bg-gray-700 rounded"
            title="Clear output"
          >
            <Trash2 className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Output Sections */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Standard Output */}
        {renderOutputSection(
          'Standard Output',
          output,
          'output',
          <Terminal className="w-4 h-4 text-green-500" />,
          showOutput,
          () => setShowOutput(!showOutput)
        )}
        
        {/* Standard Error */}
        {renderOutputSection(
          'Standard Error',
          stderr,
          'stderr',
          <XCircle className="w-4 h-4 text-red-500" />,
          showStderr,
          () => setShowStderr(!showStderr)
        )}
      </div>

      {/* Loading Indicator */}
      {isLoading && (
        <div className="absolute inset-0 bg-gray-900 bg-opacity-50 flex items-center justify-center z-10">
          <div className="bg-white rounded-lg p-6 flex items-center space-x-3">
            <Clock className="w-6 h-6 text-blue-500 animate-spin" />
            <span className="text-gray-700 font-medium">Executing code...</span>
          </div>
        </div>
      )}

      {/* Footer */}
      <div className="bg-gray-100 border-t border-gray-200 px-4 py-2 text-xs text-gray-600 flex items-center justify-between">
        <div className="flex items-center space-x-4">
          {returnCode !== null && (
            <span>
              Exit Code: <span className={returnCode === 0 ? 'text-green-600' : 'text-red-600'}>
                {returnCode}
              </span>
            </span>
          )}
          
          {executionTime && (
            <span>
              Execution Time: <span className="font-mono">{executionTime.toFixed(3)}s</span>
            </span>
          )}
        </div>
        
        <div className="flex items-center space-x-2">
          <span>Output Window</span>
          <ExternalLink className="w-3 h-3" />
        </div>
      </div>
    </div>
  );
};

export default OutputWindow;