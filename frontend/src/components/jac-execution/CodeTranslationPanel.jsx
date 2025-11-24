import React, { useState } from 'react';
import {
  ArrowRightLeft,
  Copy,
  Download,
  Check,
  AlertCircle,
  Info,
  RefreshCw,
  Code,
  Zap,
  Settings,
  Eye,
  EyeOff
} from 'lucide-react';

const CodeTranslationPanel = ({ 
  originalCode, 
  onCodeChange, 
  currentLanguage, 
  onLanguageChange,
  className = '' 
}) => {
  const [translatedCode, setTranslatedCode] = useState('');
  const [translationStatus, setTranslationStatus] = useState('idle'); // idle, translating, success, error
  const [translationDirection, setTranslationDirection] = useState('auto'); // auto, jac_to_python, python_to_jac
  const [showOriginal, setShowOriginal] = useState(true);
  const [copiedTranslated, setCopiedTranslated] = useState(false);
  const [errors, setErrors] = useState([]);
  const [warnings, setWarnings] = useState([]);
  const [translationMetadata, setTranslationMetadata] = useState({});

  const API_BASE = '/api/jac-execution';

  const determineTranslationDirection = (sourceLang, targetLang) => {
    if (sourceLang === 'jac' && targetLang === 'python') return 'jac_to_python';
    if (sourceLang === 'python' && targetLang === 'jac') return 'python_to_jac';
    return 'auto';
  };

  const translateCode = async (direction = null) => {
    if (!originalCode.trim()) {
      setTranslationStatus('error');
      setErrors(['No code to translate']);
      return;
    }

    setTranslationStatus('translating');
    setErrors([]);
    setWarnings([]);
    setTranslatedCode('');

    try {
      const token = localStorage.getItem('access_token');
      let finalDirection = direction;

      // Auto-detect direction if not specified
      if (!finalDirection || finalDirection === 'auto') {
        const targetLang = currentLanguage === 'jac' ? 'python' : 'jac';
        finalDirection = determineTranslationDirection(currentLanguage, targetLang);
      }

      const requestBody = {
        code: originalCode,
        direction: finalDirection
      };

      const response = await fetch(`${API_BASE}/api/translation/quick_translate/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(requestBody)
      });

      const result = await response.json();

      if (result.success) {
        setTranslatedCode(result.translated_code);
        setTranslationStatus('success');
        setErrors(result.errors || []);
        setWarnings(result.warnings || []);
        setTranslationMetadata(result.metadata || {});

        // Update target language based on translation
        const targetLanguage = currentLanguage === 'jac' ? 'python' : 'jac';
        onLanguageChange(targetLanguage);
      } else {
        setTranslationStatus('error');
        setErrors(result.errors || [result.error || 'Translation failed']);
      }

    } catch (error) {
      setTranslationStatus('error');
      setErrors([`Translation request failed: ${error.message}`]);
    }
  };

  const copyTranslatedCode = async () => {
    try {
      await navigator.clipboard.writeText(translatedCode);
      setCopiedTranslated(true);
      setTimeout(() => setCopiedTranslated(false), 2000);
    } catch (error) {
      console.error('Failed to copy translated code:', error);
    }
  };

  const downloadTranslatedCode = () => {
    if (!translatedCode) return;

    const fileExtension = currentLanguage === 'python' ? 'py' : 'jac';
    const filename = `translated_code.${fileExtension}`;
    
    const element = document.createElement('a');
    const file = new Blob([translatedCode], { type: 'text/plain' });
    element.href = URL.createObjectURL(file);
    element.download = filename;
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
  };

  const loadTranslatedToEditor = () => {
    if (translatedCode) {
      onCodeChange(translatedCode);
    }
  };

  const clearTranslation = () => {
    setTranslatedCode('');
    setTranslationStatus('idle');
    setErrors([]);
    setWarnings([]);
    setTranslationMetadata({});
  };

  const toggleView = () => {
    setShowOriginal(!showOriginal);
  };

  return (
    <div className={`bg-white rounded-lg shadow-lg border border-gray-200 ${className}`}>
      {/* Header */}
      <div className="border-b border-gray-200 px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <ArrowRightLeft className="w-5 h-5 text-blue-600" />
            <h3 className="text-lg font-semibold text-gray-900">Code Translation</h3>
            <span className="text-sm text-gray-500">
              {currentLanguage.toUpperCase()} ↔ {currentLanguage === 'jac' ? 'PYTHON' : 'JAC'}
            </span>
          </div>
          
          <div className="flex items-center space-x-2">
            {/* Translation Direction Controls */}
            <select
              value={translationDirection}
              onChange={(e) => setTranslationDirection(e.target.value)}
              className="px-3 py-1 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="auto">Auto Detect</option>
              <option value="jac_to_python">JAC → Python</option>
              <option value="python_to_jac">Python → JAC</option>
            </select>

            {/* Translate Button */}
            <button
              onClick={() => translateCode(translationDirection)}
              disabled={translationStatus === 'translating' || !originalCode.trim()}
              className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-colors ${
                translationStatus === 'translating'
                  ? 'bg-gray-400 text-white cursor-not-allowed'
                  : 'bg-blue-600 text-white hover:bg-blue-700'
              }`}
            >
              {translationStatus === 'translating' ? (
                <RefreshCw className="w-4 h-4 animate-spin" />
              ) : (
                <Zap className="w-4 h-4" />
              )}
              <span>
                {translationStatus === 'translating' ? 'Translating...' : 'Translate'}
              </span>
            </button>

            {/* View Toggle */}
            <button
              onClick={toggleView}
              className="p-2 text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded-lg"
              title="Toggle View"
            >
              {showOriginal ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
            </button>
          </div>
        </div>
      </div>

      {/* Translation Status */}
      {(translationStatus === 'success' || translationStatus === 'error') && (
        <div className={`px-6 py-3 border-b border-gray-200 ${
          translationStatus === 'success' ? 'bg-green-50' : 'bg-red-50'
        }`}>
          <div className="flex items-center space-x-2">
            {translationStatus === 'success' ? (
              <Check className="w-4 h-4 text-green-600" />
            ) : (
              <AlertCircle className="w-4 h-4 text-red-600" />
            )}
            <span className={`text-sm font-medium ${
              translationStatus === 'success' ? 'text-green-800' : 'text-red-800'
            }`}>
              Translation {translationStatus === 'success' ? 'completed' : 'failed'}
            </span>
            
            {errors.length > 0 && (
              <span className="text-xs text-red-600">
                ({errors.length} error{errors.length > 1 ? 's' : ''})
              </span>
            )}
            
            {warnings.length > 0 && (
              <span className="text-xs text-yellow-600">
                ({warnings.length} warning{warnings.length > 1 ? 's' : ''})
              </span>
            )}
          </div>
        </div>
      )}

      {/* Main Content */}
      <div className="flex">
        {/* Original Code Panel */}
        {showOriginal && (
          <div className="flex-1 border-r border-gray-200">
            <div className="bg-gray-50 px-4 py-2 border-b border-gray-200">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium text-gray-700">
                  Original Code ({currentLanguage.toUpperCase()})
                </span>
                <span className="text-xs text-gray-500">
                  {originalCode.split('\n').length} lines
                </span>
              </div>
            </div>
            <div className="p-4">
              <textarea
                value={originalCode}
                onChange={(e) => onCodeChange(e.target.value)}
                placeholder="Enter your code here..."
                className="w-full h-40 p-3 border border-gray-300 rounded-md resize-none text-sm font-mono focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>
        )}

        {/* Translated Code Panel */}
        <div className="flex-1">
          <div className="bg-gray-50 px-4 py-2 border-b border-gray-200">
            <div className="flex items-center justify-between">
              <span className="text-sm font-medium text-gray-700">
                {translationStatus === 'idle' ? 'Translated Code' : 
                 translationStatus === 'translating' ? 'Translating...' :
                 'Translated Code'} ({currentLanguage === 'jac' ? 'PYTHON' : 'JAC'})
              </span>
              
              {translatedCode && (
                <div className="flex items-center space-x-2">
                  <button
                    onClick={copyTranslatedCode}
                    className="p-1 text-gray-600 hover:text-gray-800"
                    title="Copy Translated Code"
                  >
                    {copiedTranslated ? <Check className="w-4 h-4 text-green-600" /> : <Copy className="w-4 h-4" />}
                  </button>
                  
                  <button
                    onClick={downloadTranslatedCode}
                    className="p-1 text-gray-600 hover:text-gray-800"
                    title="Download Translated Code"
                  >
                    <Download className="w-4 h-4" />
                  </button>
                  
                  <button
                    onClick={loadTranslatedToEditor}
                    className="flex items-center space-x-1 px-2 py-1 text-xs bg-blue-100 text-blue-700 rounded hover:bg-blue-200"
                  >
                    <Code className="w-3 h-3" />
                    <span>Load to Editor</span>
                  </button>
                  
                  <button
                    onClick={clearTranslation}
                    className="p-1 text-gray-600 hover:text-gray-800"
                    title="Clear Translation"
                  >
                    <RefreshCw className="w-4 h-4" />
                  </button>
                </div>
              )}
            </div>
          </div>
          
          <div className="p-4">
            {translationStatus === 'idle' ? (
              <div className="h-40 flex items-center justify-center text-gray-500">
                <div className="text-center">
                  <ArrowRightLeft className="w-12 h-12 mx-auto mb-2 text-gray-300" />
                  <p>Click "Translate" to convert your code</p>
                  <p className="text-sm">Support for JAC ↔ Python translation</p>
                </div>
              </div>
            ) : translationStatus === 'translating' ? (
              <div className="h-40 flex items-center justify-center">
                <div className="text-center">
                  <RefreshCw className="w-8 h-8 animate-spin mx-auto mb-2 text-blue-600" />
                  <p>Translating your code...</p>
                </div>
              </div>
            ) : (
              <textarea
                value={translatedCode}
                readOnly
                placeholder="Translated code will appear here..."
                className="w-full h-40 p-3 border border-gray-300 rounded-md resize-none text-sm font-mono bg-gray-50"
              />
            )}
          </div>
        </div>
      </div>

      {/* Translation Issues */}
      {(errors.length > 0 || warnings.length > 0) && (
        <div className="border-t border-gray-200">
          {errors.length > 0 && (
            <div className="bg-red-50 px-4 py-3">
              <div className="flex items-start space-x-2">
                <AlertCircle className="w-4 h-4 text-red-600 mt-0.5" />
                <div>
                  <h4 className="text-sm font-medium text-red-800">Translation Errors</h4>
                  <ul className="mt-1 text-sm text-red-700 space-y-1">
                    {errors.map((error, index) => (
                      <li key={index} className="flex items-start space-x-1">
                        <span className="w-1 h-1 bg-red-600 rounded-full mt-2 flex-shrink-0"></span>
                        <span>{error}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          )}
          
          {warnings.length > 0 && (
            <div className="bg-yellow-50 px-4 py-3">
              <div className="flex items-start space-x-2">
                <Info className="w-4 h-4 text-yellow-600 mt-0.5" />
                <div>
                  <h4 className="text-sm font-medium text-yellow-800">Translation Warnings</h4>
                  <ul className="mt-1 text-sm text-yellow-700 space-y-1">
                    {warnings.map((warning, index) => (
                      <li key={index} className="flex items-start space-x-1">
                        <span className="w-1 h-1 bg-yellow-600 rounded-full mt-2 flex-shrink-0"></span>
                        <span>{warning}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Translation Metadata */}
      {translationMetadata && Object.keys(translationMetadata).length > 0 && (
        <div className="bg-blue-50 px-4 py-3 border-t border-gray-200">
          <div className="flex items-center space-x-2">
            <Info className="w-4 h-4 text-blue-600" />
            <span className="text-sm font-medium text-blue-800">Translation Info</span>
          </div>
          <div className="mt-1 text-sm text-blue-700">
            {translationMetadata.original_length && translationMetadata.translated_length && (
              <span>
                {translationMetadata.direction} • 
                Original: {translationMetadata.original_length} chars → 
                Translated: {translationMetadata.translated_length} chars
              </span>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default CodeTranslationPanel;