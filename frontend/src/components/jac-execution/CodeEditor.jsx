import React, { useState, useRef, useEffect } from 'react';
import { Editor } from '@monaco-editor/react';

const CodeEditor = ({ value, onChange, language = 'python', readOnly = false }) => {
  const [fontSize, setFontSize] = useState(14);
  const [theme, setTheme] = useState('vs-dark');
  const [showSettings, setShowSettings] = useState(false);
  const editorRef = useRef(null);

  const languageOptions = {
    python: {
      language: 'python',
      extensions: ['.py']
    },
    jac: {
      language: 'javascript', // Using JavaScript as fallback for JAC
      extensions: ['.jac']
    }
  };

  const handleEditorDidMount = (editor, monaco) => {
    editorRef.current = editor;
    
    // Configure editor options
    editor.updateOptions({
      fontSize,
      minimap: { enabled: false },
      scrollBeyondLastLine: false,
      automaticLayout: true,
      tabSize: 4,
      insertSpaces: true,
      wordWrap: 'on',
      lineNumbers: 'on',
      folding: true,
      glyphMargin: false,
      lineDecorationsWidth: 0,
      lineNumbersMinChars: 3,
      renderLineHighlight: 'all',
      contextmenu: true,
      mouseWheelZoom: true,
      smoothScrolling: true,
      cursorBlinking: 'smooth',
      cursorSmoothCaretAnimation: 'on',
      foldingHighlight: true,
      foldingImportsByDefault: true,
      showFoldingControls: 'always',
      bracketPairColorization: { enabled: true },
      guides: {
        bracketPairs: true,
        indentation: true
      }
    });

    // Add custom keybindings
    editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.KeyS, () => {
      // Save functionality could be added here
      console.log('Save executed');
    });

    editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.KeyEnter, () => {
      // Execute code functionality could be added here
      console.log('Execute triggered');
    });
  };

  const handleEditorChange = (newValue) => {
    if (!readOnly) {
      onChange(newValue || '');
    }
  };

  const increaseFontSize = () => {
    const newSize = Math.min(fontSize + 2, 24);
    setFontSize(newSize);
    if (editorRef.current) {
      editorRef.current.updateOptions({ fontSize: newSize });
    }
  };

  const decreaseFontSize = () => {
    const newSize = Math.max(fontSize - 2, 8);
    setFontSize(newSize);
    if (editorRef.current) {
      editorRef.current.updateOptions({ fontSize: newSize });
    }
  };

  const toggleTheme = () => {
    const newTheme = theme === 'vs-dark' ? 'light' : 'vs-dark';
    setTheme(newTheme);
  };

  const resetEditor = () => {
    if (editorRef.current) {
      const model = editorRef.current.getModel();
      if (model) {
        model.setValue('');
      }
    }
    onChange('');
  };

  const formatCode = () => {
    if (editorRef.current) {
      editorRef.current.getAction('editor.action.formatDocument').run();
    }
  };

  const toggleWordWrap = () => {
    if (editorRef.current) {
      const current = editorRef.current.getOption(EditorOption.wordWrap);
      editorRef.current.updateOptions({
        wordWrap: current === 'on' ? 'off' : 'on'
      });
    }
  };

  return (
    <div className="h-full flex flex-col">
      {/* Editor Toolbar */}
      <div className="bg-gray-50 border-b border-gray-200 px-4 py-2 flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <span className="text-sm font-medium text-gray-700">
            {languageOptions[language]?.language?.toUpperCase() || language.toUpperCase()} Editor
          </span>
          
          <div className="flex items-center space-x-1">
            <button
              onClick={decreaseFontSize}
              className="p-1 text-gray-600 hover:text-gray-800 hover:bg-gray-200 rounded"
              title="Decrease Font Size"
            >
              A-
            </button>
            <span className="text-sm text-gray-600 px-1">{fontSize}px</span>
            <button
              onClick={increaseFontSize}
              className="p-1 text-gray-600 hover:text-gray-800 hover:bg-gray-200 rounded"
              title="Increase Font Size"
            >
              A+
            </button>
          </div>
        </div>

        <div className="flex items-center space-x-2">
          <button
            onClick={formatCode}
            disabled={readOnly}
            className="px-2 py-1 text-xs bg-blue-100 text-blue-700 rounded hover:bg-blue-200 disabled:opacity-50 disabled:cursor-not-allowed"
            title="Format Code"
          >
            Format
          </button>
          
          <button
            onClick={toggleWordWrap}
            disabled={readOnly}
            className="px-2 py-1 text-xs bg-gray-100 text-gray-700 rounded hover:bg-gray-200 disabled:opacity-50 disabled:cursor-not-allowed"
            title="Toggle Word Wrap"
          >
            Wrap
          </button>
          
          <button
            onClick={toggleTheme}
            className="px-2 py-1 text-xs bg-gray-100 text-gray-700 rounded hover:bg-gray-200"
            title="Toggle Theme"
          >
            {theme === 'vs-dark' ? 'Light' : 'Dark'}
          </button>
          
          <button
            onClick={() => setShowSettings(!showSettings)}
            className="p-1 text-gray-600 hover:text-gray-800 hover:bg-gray-200 rounded"
            title="Editor Settings"
          >
            ⚙
          </button>
        </div>
      </div>

      {/* Editor Settings Panel */}
      {showSettings && (
        <div className="bg-gray-100 border-b border-gray-200 px-4 py-2">
          <div className="flex items-center space-x-4 text-sm">
            <label className="flex items-center space-x-2">
              <span>Tab Size:</span>
              <select
                onChange={(e) => {
                  const size = parseInt(e.target.value);
                  if (editorRef.current) {
                    editorRef.current.updateOptions({ tabSize: size });
                  }
                }}
                className="px-2 py-1 border border-gray-300 rounded text-xs"
                defaultValue="4"
              >
                <option value="2">2</option>
                <option value="4">4</option>
                <option value="8">8</option>
              </select>
            </label>
            
            <label className="flex items-center space-x-2">
              <input
                type="checkbox"
                onChange={(e) => {
                  if (editorRef.current) {
                    editorRef.current.updateOptions({ 
                      minimap: { enabled: e.target.checked }
                    });
                  }
                }}
                className="rounded"
              />
              <span>Minimap</span>
            </label>
            
            <label className="flex items-center space-x-2">
              <input
                type="checkbox"
                defaultChecked
                onChange={(e) => {
                  if (editorRef.current) {
                    editorRef.current.updateOptions({ 
                      lineNumbers: e.target.checked ? 'on' : 'off'
                    });
                  }
                }}
                className="rounded"
              />
              <span>Line Numbers</span>
            </label>
          </div>
        </div>
      )}

      {/* Monaco Editor */}
      <div className="flex-1 min-h-0">
        <Editor
          height="100%"
          language={languageOptions[language]?.language || language}
          value={value}
          onChange={handleEditorChange}
          onMount={handleEditorDidMount}
          theme={theme}
          options={{
            readOnly,
            scrollBeyondLastLine: false,
            automaticLayout: true,
            minimap: { enabled: false },
            fontSize,
            tabSize: 4,
            insertSpaces: true,
            wordWrap: 'on',
            lineNumbers: 'on',
            folding: true,
            glyphMargin: false,
            lineDecorationsWidth: 0,
            lineNumbersMinChars: 3,
            renderLineHighlight: 'all',
            contextmenu: true,
            mouseWheelZoom: true,
            smoothScrolling: true,
            cursorBlinking: 'smooth',
            cursorSmoothCaretAnimation: 'on',
            foldingHighlight: true,
            foldingImportsByDefault: true,
            showFoldingControls: 'always',
            bracketPairColorization: { enabled: true },
            guides: {
              bracketPairs: true,
              indentation: true
            }
          }}
        />
      </div>

      {/* Status Bar */}
      <div className="bg-gray-100 border-t border-gray-200 px-4 py-1 text-xs text-gray-600 flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <span>Language: {language.toUpperCase()}</span>
          <span>Lines: {value.split('\n').length}</span>
          <span>Characters: {value.length}</span>
        </div>
        
        <div className="flex items-center space-x-2">
          {readOnly && (
            <span className="text-orange-600">Read Only</span>
          )}
          <span>UTF-8</span>
        </div>
      </div>
    </div>
  );
};

export default CodeEditor;