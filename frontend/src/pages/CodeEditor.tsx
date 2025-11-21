import React, { useState, useEffect, useRef } from 'react';
import { Editor } from '@monaco-editor/react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  PlayIcon,
  StopIcon,
  DocumentDuplicateIcon,
  CogIcon,
  CheckCircleIcon,
  ExclamationCircleIcon,
  ClockIcon,
} from '@heroicons/react/24/outline';
import { useSelector } from 'react-redux';
import { RootState } from '../store/store';
import { learningService, CodeExecutionRequest, CodeExecutionResponse } from '../services/learningService';
import { toast } from 'react-hot-toast';

interface ExecutionResult {
  success: boolean;
  output: string;
  error?: string;
  executionTime: number;
  memoryUsage: number;
}

const LANGUAGES = [
  { id: 'python', name: 'Python', ext: 'py' },
  { id: 'jac', name: 'JAC (Jaseci)', ext: 'jac' },
];

const TEMPLATES = {
  python: `# Python Template
# Welcome to JAC Learning Platform!

def fibonacci(n):
    """Calculate fibonacci number"""
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# Test the function
print("Fibonacci sequence:")
for i in range(10):
    print(f"fib({i}) = {fibonacci(i)}")
`,
  jac: `// JAC Template
// Welcome to JAC (Jaseci Architecture Code)!

walker hello_world {
    can print;
    print("Hello from JAC!");
    print("JAC is an AI-first programming language");
    
    // Define a simple node
    node person {
        has name, age;
        can greet with person entry {
            can print;
            print(f"Hello, I am {here.name} and I am {here.age} years old");
        }
    }
    
    // Create and interact with nodes
    person_1 = spawn node.person(name="Alice", age=25);
    person_2 = spawn node.person(name="Bob", age=30);
    
    report {"message": "JAC execution completed!", "result": "success"};
}`
};

const INITIAL_CODE = {
  python: TEMPLATES.python,
  jac: TEMPLATES.jac,
};

export const CodeEditor: React.FC = () => {
  const [selectedLanguage, setSelectedLanguage] = useState<'python' | 'jac'>('python');
  const [code, setCode] = useState(INITIAL_CODE.python);
  const [output, setOutput] = useState('');
  const [isExecuting, setIsExecuting] = useState(false);
  const [executionResult, setExecutionResult] = useState<ExecutionResult | null>(null);
  const [editorSettings, setEditorSettings] = useState({
    fontSize: 14,
    theme: 'vs-dark',
    minimap: true,
    wordWrap: 'on' as const,
  });
  
  // TODO: Use user data when implementing user-specific features
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const { user } = useSelector((state: RootState) => state.auth);
  const editorRef = useRef<any>(null);

  useEffect(() => {
    setCode(INITIAL_CODE[selectedLanguage]);
    setOutput('');
    setExecutionResult(null);
  }, [selectedLanguage]);

  const handleEditorDidMount = (editor: any, monaco: any) => {
    editorRef.current = editor;
    
    // Add custom themes for JAC
    monaco.editor.defineTheme('jac-dark', {
      base: 'vs-dark',
      inherit: true,
      rules: [
        { token: 'comment', foreground: '6A9955', fontStyle: 'italic' },
        { token: 'keyword', foreground: '569CD6' },
        { token: 'string', foreground: 'CE9178' },
        { token: 'number', foreground: 'B5CEA8' },
      ],
      colors: {
        'editor.background': '#1e1e1e',
        'editor.foreground': '#d4d4d4',
      }
    });
  };

  const executeCode = async () => {
    if (!code.trim()) {
      toast.error('Please enter some code to execute');
      return;
    }

    setIsExecuting(true);
    setOutput('');
    setExecutionResult(null);

    try {
      const request: CodeExecutionRequest = {
        code: code.trim(),
        language: selectedLanguage,
        timeout: 30,
        memory_limit: 512,
      };

      const startTime = Date.now();
      const response: CodeExecutionResponse = await learningService.executeCode(request);
      const endTime = Date.now();

      const result: ExecutionResult = {
        success: response.success,
        output: response.output,
        error: response.error,
        executionTime: response.execution_time || (endTime - startTime) / 1000,
        memoryUsage: response.memory_usage || 0,
      };

      setExecutionResult(result);
      setOutput(response.output || response.error || 'No output');

      if (response.success) {
        toast.success('Code executed successfully!');
      } else {
        toast.error('Code execution failed');
      }

    } catch (error: any) {
      console.error('Execution error:', error);
      const errorMessage = error.response?.data?.detail || error.message || 'Execution failed';
      setExecutionResult({
        success: false,
        output: '',
        error: errorMessage,
        executionTime: 0,
        memoryUsage: 0,
      });
      setOutput(`Error: ${errorMessage}`);
      toast.error('Code execution failed');
    } finally {
      setIsExecuting(false);
    }
  };

  const stopExecution = () => {
    setIsExecuting(false);
    toast.success('Execution stopped');
  };

  const duplicateCode = () => {
    navigator.clipboard.writeText(code);
    toast.success('Code copied to clipboard');
  };

  const resetCode = () => {
    setCode(INITIAL_CODE[selectedLanguage]);
    setOutput('');
    setExecutionResult(null);
    toast.success('Code reset to template');
  };

  const formatTime = (seconds: number) => {
    if (seconds < 1) {
      return `${(seconds * 1000).toFixed(0)}ms`;
    }
    return `${seconds.toFixed(2)}s`;
  };

  return (
    <div className="h-screen flex flex-col bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 px-6 py-4">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Code Editor</h1>
            <p className="text-gray-600 mt-1">
              Write and execute {selectedLanguage.toUpperCase()} code with real-time feedback
            </p>
          </div>
          
          <div className="flex items-center gap-4">
            {/* Language Selector */}
            <select
              value={selectedLanguage}
              onChange={(e) => setSelectedLanguage(e.target.value as 'python' | 'jac')}
              className="px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            >
              {LANGUAGES.map((lang) => (
                <option key={lang.id} value={lang.id}>
                  {lang.name}
                </option>
              ))}
            </select>
            
            {/* Editor Settings */}
            <button
              onClick={() => setEditorSettings(prev => ({ ...prev, theme: prev.theme === 'vs-dark' ? 'jac-dark' : 'vs-dark' }))}
              className="p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-md transition-colors"
              title="Toggle Theme"
            >
              <CogIcon className="h-5 w-5" />
            </button>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex overflow-hidden">
        {/* Code Editor */}
        <div className="flex-1 flex flex-col">
          <div className="flex-1 relative">
            <Editor
              height="100%"
              language={selectedLanguage === 'jac' ? 'javascript' : selectedLanguage}
              value={code}
              onChange={(value: string | undefined) => setCode(value || '')}
              theme={editorSettings.theme}
              options={{
                fontSize: editorSettings.fontSize,
                minimap: { enabled: editorSettings.minimap },
                wordWrap: editorSettings.wordWrap,
                scrollBeyondLastLine: false,
                automaticLayout: true,
                tabSize: 2,
                insertSpaces: true,
                folding: true,
                lineNumbers: 'on',
                roundedSelection: false,
                cursorStyle: 'line',
                cursorBlinking: 'blink',
                glyphMargin: true,
                guides: {
                  indentation: true,
                  bracketPairs: true,
                },
                suggestOnTriggerCharacters: true,
                quickSuggestions: true,
                parameterHints: {
                  enabled: true,
                },
              }}
              onMount={handleEditorDidMount}
            />
          </div>
          
          {/* Editor Controls */}
          <div className="bg-white border-t border-gray-200 px-6 py-3 flex items-center justify-between">
            <div className="flex items-center gap-3">
              {!isExecuting ? (
                <button
                  onClick={executeCode}
                  className="flex items-center gap-2 px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 transition-colors focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2"
                >
                  <PlayIcon className="h-4 w-4" />
                  Run Code
                </button>
              ) : (
                <button
                  onClick={stopExecution}
                  className="flex items-center gap-2 px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 transition-colors focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2"
                >
                  <StopIcon className="h-4 w-4" />
                  Stop
                </button>
              )}
              
              <button
                onClick={duplicateCode}
                className="flex items-center gap-2 px-3 py-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-md transition-colors"
              >
                <DocumentDuplicateIcon className="h-4 w-4" />
                Copy
              </button>
              
              <button
                onClick={resetCode}
                className="px-3 py-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-md transition-colors"
              >
                Reset
              </button>
            </div>
            
            <div className="text-sm text-gray-500">
              Lines: {code.split('\n').length} | Characters: {code.length}
            </div>
          </div>
        </div>

        {/* Output Panel */}
        <div className="w-1/2 bg-white border-l border-gray-200 flex flex-col">
          <div className="bg-gray-50 border-b border-gray-200 px-4 py-3">
            <h3 className="text-lg font-semibold text-gray-900 flex items-center gap-2">
              <span className="text-sm font-medium">Output</span>
              {isExecuting && (
                <motion.div
                  animate={{ rotate: 360 }}
                  transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
                  className="h-4 w-4 border-2 border-primary-600 border-t-transparent rounded-full"
                />
              )}
            </h3>
          </div>
          
          <div className="flex-1 p-4 font-mono text-sm overflow-auto bg-gray-900 text-green-400">
            <AnimatePresence mode="wait">
              {isExecuting ? (
                <motion.div
                  key="executing"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  className="flex items-center gap-2"
                >
                  <div className="flex space-x-1">
                    <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse" style={{ animationDelay: '0ms' }} />
                    <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse" style={{ animationDelay: '200ms' }} />
                    <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse" style={{ animationDelay: '400ms' }} />
                  </div>
                  <span>Executing {selectedLanguage} code...</span>
                </motion.div>
              ) : output ? (
                <motion.div
                  key="output"
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -10 }}
                  className="whitespace-pre-wrap"
                >
                  {output}
                </motion.div>
              ) : (
                <div className="text-gray-500 italic">
                  Execute your code to see the output here...
                </div>
              )}
            </AnimatePresence>
          </div>
          
          {/* Execution Metrics */}
          {executionResult && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="border-t border-gray-200 p-4 bg-gray-50"
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                  <div className="flex items-center gap-1">
                    {executionResult.success ? (
                      <CheckCircleIcon className="h-4 w-4 text-green-600" />
                    ) : (
                      <ExclamationCircleIcon className="h-4 w-4 text-red-600" />
                    )}
                    <span className={`text-sm font-medium ${
                      executionResult.success ? 'text-green-600' : 'text-red-600'
                    }`}>
                      {executionResult.success ? 'Success' : 'Failed'}
                    </span>
                  </div>
                  
                  <div className="flex items-center gap-1 text-gray-600">
                    <ClockIcon className="h-4 w-4" />
                    <span className="text-sm">{formatTime(executionResult.executionTime)}</span>
                  </div>
                  
                  <div className="text-sm text-gray-600">
                    Memory: {executionResult.memoryUsage}MB
                  </div>
                </div>
              </div>
            </motion.div>
          )}
        </div>
      </div>
    </div>
  );
};

export default CodeEditor;