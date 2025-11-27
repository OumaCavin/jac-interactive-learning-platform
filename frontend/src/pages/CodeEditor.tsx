// JAC Learning Platform - TypeScript utilities by Cavin Otieno

import React, { useState, useEffect, useRef } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { motion, AnimatePresence } from 'framer-motion';
import { Card, Button, Badge } from '../components/ui';
import { selectAuth } from '../store/slices/authSlice';
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
  { id: 'python', name: 'Python', ext: 'py', icon: '🐍' },
  { id: 'jac', name: 'JAC (Jaseci)', ext: 'jac', icon: '⚡' },
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

# Try your own code below:
# print("Hello, World!")`,
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
    
    // Try your own code below:
    // print("Your JAC code here!");
}`
};

const INITIAL_CODE = {
  python: TEMPLATES.python,
  jac: TEMPLATES.jac,
};

const CodeEditor: React.FC = () => {
  const dispatch = useDispatch();
  const { user } = useSelector(selectAuth);
  
  const [selectedLanguage, setSelectedLanguage] = useState<'python' | 'jac'>('python');
  const [code, setCode] = useState(INITIAL_CODE.python);
  const [output, setOutput] = useState('');
  const [isExecuting, setIsExecuting] = useState(false);
  const [executionResult, setExecutionResult] = useState<ExecutionResult | null>(null);
  const [showSettings, setShowSettings] = useState(false);
  
  const editorRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    setCode(INITIAL_CODE[selectedLanguage]);
    setOutput('');
    setExecutionResult(null);
  }, [selectedLanguage]);

  const executeCode = async () => {
    if (!code.trim()) {
      toast.error('Please enter some code to execute');
      return;
    }

    setIsExecuting(true);
    setOutput('🚀 Executing code...\n\n');
    setExecutionResult(null);

    try {
      const request: CodeExecutionRequest = {
        code: code.trim(),
        language: selectedLanguage,
        timeout: 30,
        memory_limit: 512,
      };

      const startTime = Date.now();
      const endTime = Date.now(); // Declare endTime early to avoid scope issues
      let response: CodeExecutionResponse;
      
      // Use JAC-specific execution for better functionality
      if (selectedLanguage === 'jac') {
        const jacResult = await learningService.executeJacCode(
          code.trim(), 
          selectedLanguage, 
          undefined // test cases can be added later
        );
        response = {
          success: jacResult.success,
          output: typeof jacResult.output === 'string' ? jacResult.output : JSON.stringify(jacResult.output),
          error: jacResult.error,
          execution_time: jacResult.execution_details?.execution_time || (endTime - startTime) / 1000,
          memory_usage: 0 // Not available in current response
        };
      } else {
        // Use generic execution for other languages
        response = await learningService.quickExecuteCode(code.trim(), selectedLanguage);
      }
      
      const result: ExecutionResult = {
        success: response.success,
        output: response.output,
        error: response.error,
        executionTime: response.execution_time || (endTime - startTime) / 1000,
        memoryUsage: response.memory_usage || 0,
      };

      setExecutionResult(result);
      
      if (response.success) {
        setOutput(`✅ Code executed successfully!\n\n${response.output || 'No output produced'}`);
        toast.success('Code executed successfully!');
      } else {
        setOutput(`❌ Execution failed\n\n${response.error || 'Unknown error occurred'}`);
        toast.error('Code execution failed');
      }

    } catch (error: any) {
      // Handle code execution error gracefully
      const errorMessage = error.response?.data?.detail || error.message || 'Execution failed';
      
      setExecutionResult({
        success: false,
        output: '',
        error: errorMessage,
        executionTime: 0,
        memoryUsage: 0,
      });
      
      setOutput(`💥 Execution Error\n\n${errorMessage}\n\nTip: Check your syntax and try again.`);
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

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
      e.preventDefault();
      executeCode();
    }
  };

  const insertAtCursor = (text: string) => {
    if (editorRef.current) {
      const textarea = editorRef.current;
      const start = textarea.selectionStart;
      const end = textarea.selectionEnd;
      const newCode = code.substring(0, start) + text + code.substring(end);
      setCode(newCode);
      
      // Restore cursor position
      setTimeout(() => {
        textarea.selectionStart = textarea.selectionEnd = start + text.length;
        textarea.focus();
      }, 0);
    }
  };

  const quickInsertButtons = [
    { label: 'Print', text: '\nprint("Hello, World!")', lang: ['python'] },
    { label: 'For Loop', text: '\nfor i in range(10):\n    print(i)', lang: ['python'] },
    { label: 'If/Else', text: '\nif condition:\n    print("True")\nelse:\n    print("False")', lang: ['python'] },
    { label: 'Walker', text: '\nwalker my_walker {\n    can print;\n    print("Hello from JAC!");\n}', lang: ['jac'] },
    { label: 'Node', text: '\nnode my_node {\n    has name, value;\n}', lang: ['jac'] },
    { label: 'Report', text: '\nreport {"status": "completed", "result": "success"};', lang: ['jac'] },
  ];

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold text-white flex items-center space-x-3">
            <span>💻</span>
            <span>Code Editor</span>
          </h1>
          <p className="text-white/90 mt-2">
            Write and execute {selectedLanguage.toUpperCase()} code with real-time feedback
          </p>
        </div>
        
        <div className="flex items-center space-x-4">
          {/* Language Selector */}
          <select
            value={selectedLanguage}
            onChange={(e) => setSelectedLanguage(e.target.value as 'python' | 'jac')}
            className="glass rounded-xl px-4 py-2 text-white focus:outline-none focus:ring-2 focus:ring-white/30"
          >
            {LANGUAGES.map((lang) => (
              <option key={lang.id} value={lang.id} className="bg-gray-800">
                {lang.icon} {lang.name}
              </option>
            ))}
          </select>
          
          <Button
            variant="ghost"
            size="sm"
            onClick={() => setShowSettings(!showSettings)}
          >
            ⚙️ Settings
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 h-[calc(100vh-200px)]">
        {/* Code Editor Panel */}
        <Card variant="glass" padding="none" className="flex flex-col h-full">
          <div className="p-4 border-b border-white/20">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <span className="text-2xl">{LANGUAGES.find(l => l.id === selectedLanguage)?.icon}</span>
                <h3 className="text-lg font-semibold text-white">
                  {LANGUAGES.find(l => l.id === selectedLanguage)?.name} Editor
                </h3>
              </div>
              
              <div className="flex items-center space-x-2">
                <Badge variant="info" glass={false} size="sm">
                  {code.split('\n').length} lines
                </Badge>
              </div>
            </div>
          </div>
          
          {/* Editor Controls */}
          <div className="p-4 border-b border-white/20">
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center space-x-2">
                {!isExecuting ? (
                  <Button
                    onClick={executeCode}
                    variant="success"
                    size="sm"
                  >
                    🚀 Run Code
                  </Button>
                ) : (
                  <Button
                    onClick={stopExecution}
                    variant="error"
                    size="sm"
                  >
                    ⏹️ Stop
                  </Button>
                )}
                
                <Button
                  onClick={duplicateCode}
                  variant="ghost"
                  size="sm"
                >
                  📋 Copy
                </Button>
                
                <Button
                  onClick={resetCode}
                  variant="ghost"
                  size="sm"
                >
                  🔄 Reset
                </Button>
              </div>
              
              <div className="text-xs text-white/85">
                Press Ctrl+Enter to run
              </div>
            </div>
            
            {/* Quick Insert Buttons */}
            <div className="flex flex-wrap gap-2">
              {quickInsertButtons
                .filter(btn => btn.lang.includes(selectedLanguage))
                .map((btn) => (
                  <button
                    key={btn.label}
                    onClick={() => insertAtCursor(btn.text)}
                    className="text-xs px-3 py-1 bg-white/10 hover:bg-white/20 text-white/80 hover:text-white rounded-full transition-colors"
                  >
                    + {btn.label}
                  </button>
                ))}
            </div>
          </div>
          
          {/* Code Input */}
          <div className="flex-1 p-4">
            <textarea
              ref={editorRef}
              value={code}
              onChange={(e) => setCode(e.target.value)}
              onKeyDown={handleKeyPress}
              placeholder={`Write your ${selectedLanguage} code here...`}
              className="w-full h-full resize-none glass rounded-xl p-4 text-white font-mono text-sm placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-white/30 focus:border-transparent"
              style={{
                background: 'rgba(255, 255, 255, 0.05)',
                backdropFilter: 'blur(10px)',
              }}
            />
          </div>
        </Card>

        {/* Output Panel */}
        <Card variant="glass" padding="none" className="flex flex-col h-full">
          <div className="p-4 border-b border-white/20">
            <h3 className="text-lg font-semibold text-white flex items-center space-x-2">
              <span>📺</span>
              <span>Output</span>
              {isExecuting && (
                <motion.div
                  animate={{ rotate: 360 }}
                  transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
                  className="h-4 w-4 border-2 border-primary-400 border-t-transparent rounded-full"
                />
              )}
            </h3>
          </div>
          
          <div className="flex-1 p-4 overflow-auto">
            <AnimatePresence mode="wait">
              {isExecuting ? (
                <motion.div
                  key="executing"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  className="flex items-center gap-2 text-white"
                >
                  <div className="flex space-x-1">
                    <div className="w-2 h-2 bg-primary-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                    <div className="w-2 h-2 bg-primary-400 rounded-full animate-bounce" style={{ animationDelay: '200ms' }} />
                    <div className="w-2 h-2 bg-primary-400 rounded-full animate-bounce" style={{ animationDelay: '400ms' }} />
                  </div>
                  <span>Executing {selectedLanguage} code...</span>
                </motion.div>
              ) : output ? (
                <motion.div
                  key="output"
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -10 }}
                  className="font-mono text-sm whitespace-pre-wrap text-white/90"
                >
                  {output}
                </motion.div>
              ) : (
                <div className="text-white/50 italic text-center py-8">
                  <div className="text-4xl mb-4">🚀</div>
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
              className="border-t border-white/20 p-4"
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-4">
                  <div className="flex items-center space-x-2">
                    {executionResult.success ? (
                      <>
                        <span className="text-success-400">✅</span>
                        <span className="text-sm font-medium text-success-400">Success</span>
                      </>
                    ) : (
                      <>
                        <span className="text-error-400">❌</span>
                        <span className="text-sm font-medium text-error-400">Failed</span>
                      </>
                    )}
                  </div>
                  
                  <div className="flex items-center space-x-1 text-white/90">
                    <span className="text-sm">⏱️ {formatTime(executionResult.executionTime)}</span>
                  </div>
                  
                  <div className="text-sm text-white/90">
                    💾 {executionResult.memoryUsage}MB
                  </div>
                </div>
                
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => setExecutionResult(null)}
                >
                  Clear Results
                </Button>
              </div>
            </motion.div>
          )}
        </Card>
      </div>

      {/* Settings Panel */}
      <AnimatePresence>
        {showSettings && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 20 }}
            className="mt-6"
          >
            <Card variant="glass" padding="md">
              <h3 className="text-lg font-semibold text-white mb-4 flex items-center space-x-2">
                <span>⚙️</span>
                <span>Editor Settings</span>
              </h3>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <label className="block text-sm font-medium text-white mb-2">
                    Execution Timeout (seconds)
                  </label>
                  <input
                    type="number"
                    min="5"
                    max="120"
                    defaultValue="30"
                    className="glass rounded-xl px-3 py-2 text-white text-sm focus:outline-none focus:ring-2 focus:ring-white/30"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-white mb-2">
                    Memory Limit (MB)
                  </label>
                  <input
                    type="number"
                    min="64"
                    max="1024"
                    step="64"
                    defaultValue="512"
                    className="glass rounded-xl px-3 py-2 text-white text-sm focus:outline-none focus:ring-2 focus:ring-white/30"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-white mb-2">
                    Auto Save
                  </label>
                  <div className="flex items-center space-x-2">
                    <input
                      type="checkbox"
                      defaultChecked
                      className="rounded border-white/20 bg-white/10 text-primary-500 focus:ring-white/30"
                    />
                    <span className="text-sm text-white/80">Enable auto-save</span>
                  </div>
                </div>
              </div>
            </Card>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default CodeEditor;