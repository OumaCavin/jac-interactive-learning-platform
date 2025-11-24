import React, { useState, useEffect } from 'react';
import { 
  Settings, 
  Shield, 
  Clock, 
  HardDrive, 
  Zap,
  AlertTriangle,
  Save,
  X,
  Info,
  Lock,
  Unlock,
  Code,
  Network
} from 'lucide-react';

const SecuritySettings = ({ onClose, supportedLanguages = {} }) => {
  const [settings, setSettings] = useState({
    max_execution_time: 5.0,
    max_memory: 64,
    max_output_size: 10240,
    max_code_size: 102400,
    allowed_languages: ['python', 'jac'],
    enable_sandboxing: true,
    enable_network_access: false,
    max_executions_per_minute: 60,
    max_executions_per_hour: 1000,
    blocked_imports: ['os', 'sys', 'subprocess', 'importlib'],
    blocked_functions: ['eval', 'exec', 'open', '__import__']
  });

  const [loading, setLoading] = useState(false);
  const [hasChanges, setHasChanges] = useState(false);
  const [showAdvanced, setShowAdvanced] = useState(false);

  const API_BASE = '/api/jac-execution';

  useEffect(() => {
    loadSettings();
  }, []);

  const loadSettings = async () => {
    try {
      const response = await fetch(`${API_BASE}/security/`);
      if (response.ok) {
        const data = await response.json();
        setSettings(data);
      }
    } catch (error) {
      console.error('Failed to load security settings:', error);
    }
  };

  const updateSetting = (key, value) => {
    setSettings(prev => ({
      ...prev,
      [key]: value
    }));
    setHasChanges(true);
  };

  const updateArraySetting = (key, index, value) => {
    const newArray = [...settings[key]];
    newArray[index] = value;
    updateSetting(key, newArray);
  };

  const addToArray = (key, defaultValue = '') => {
    const newArray = [...settings[key], defaultValue];
    updateSetting(key, newArray);
  };

  const removeFromArray = (key, index) => {
    const newArray = settings[key].filter((_, i) => i !== index);
    updateSetting(key, newArray);
  };

  const saveSettings = async () => {
    setLoading(true);
    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch(`${API_BASE}/security/update_settings/`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(settings)
      });

      if (response.ok) {
        setHasChanges(false);
        // Could add success notification here
      } else {
        throw new Error('Failed to save settings');
      }
    } catch (error) {
      console.error('Failed to save settings:', error);
      // Could add error notification here
    } finally {
      setLoading(false);
    }
  };

  const resetToDefaults = () => {
    if (window.confirm('Reset all settings to default values?')) {
      setSettings({
        max_execution_time: 5.0,
        max_memory: 64,
        max_output_size: 10240,
        max_code_size: 102400,
        allowed_languages: ['python', 'jac'],
        enable_sandboxing: true,
        enable_network_access: false,
        max_executions_per_minute: 60,
        max_executions_per_hour: 1000,
        blocked_imports: ['os', 'sys', 'subprocess', 'importlib'],
        blocked_functions: ['eval', 'exec', 'open', '__import__']
      });
      setHasChanges(true);
    }
  };

  const toggleLanguage = (language) => {
    const newLanguages = settings.allowed_languages.includes(language)
      ? settings.allowed_languages.filter(l => l !== language)
      : [...settings.allowed_languages, language];
    updateSetting('allowed_languages', newLanguages);
  };

  const formatBytes = (bytes) => {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  };

  return (
    <div className="bg-white rounded-lg shadow-xl max-w-4xl w-full mx-4 max-h-[90vh] overflow-hidden">
      {/* Header */}
      <div className="bg-gray-50 border-b border-gray-200 px-6 py-4 flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <Settings className="w-6 h-6 text-gray-700" />
          <h2 className="text-xl font-semibold text-gray-900">Security Settings</h2>
          {hasChanges && (
            <span className="px-2 py-1 text-xs bg-orange-100 text-orange-800 rounded-full">
              Unsaved Changes
            </span>
          )}
        </div>
        
        <button
          onClick={onClose}
          className="p-2 text-gray-600 hover:text-gray-800 hover:bg-gray-200 rounded-lg"
        >
          <X className="w-5 h-5" />
        </button>
      </div>

      {/* Content */}
      <div className="p-6 overflow-y-auto max-h-[calc(90vh-140px)]">
        <div className="space-y-6">
          {/* Language Support */}
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <h3 className="flex items-center space-x-2 text-lg font-medium text-blue-900 mb-3">
              <Code className="w-5 h-5" />
              <span>Supported Languages</span>
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {Object.entries(supportedLanguages).map(([key, info]) => (
                <div
                  key={key}
                  className={`p-3 border rounded-lg cursor-pointer transition-colors ${
                    settings.allowed_languages.includes(key)
                      ? 'border-blue-500 bg-blue-100'
                      : 'border-gray-200 bg-white hover:bg-gray-50'
                  }`}
                  onClick={() => toggleLanguage(key)}
                >
                  <div className="flex items-center justify-between">
                    <div>
                      <h4 className="font-medium text-gray-900">{info.name}</h4>
                      <p className="text-sm text-gray-600">{info.description}</p>
                      <div className="mt-1">
                        {info.features?.slice(0, 3).map((feature, idx) => (
                          <span key={idx} className="inline-block px-2 py-1 text-xs bg-gray-100 text-gray-700 rounded mr-1">
                            {feature}
                          </span>
                        ))}
                      </div>
                    </div>
                    <div className={`w-5 h-5 rounded border-2 ${
                      settings.allowed_languages.includes(key)
                        ? 'bg-blue-500 border-blue-500'
                        : 'border-gray-300'
                    }`}>
                      {settings.allowed_languages.includes(key) && (
                        <div className="w-full h-full bg-white transform scale-50 rounded-full"></div>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Resource Limits */}
          <div className="bg-green-50 border border-green-200 rounded-lg p-4">
            <h3 className="flex items-center space-x-2 text-lg font-medium text-green-900 mb-3">
              <HardDrive className="w-5 h-5" />
              <span>Resource Limits</span>
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-green-900 mb-2">
                  <Clock className="w-4 h-4 inline mr-1" />
                  Max Execution Time (seconds)
                </label>
                <input
                  type="number"
                  min="1"
                  max="30"
                  step="0.1"
                  value={settings.max_execution_time}
                  onChange={(e) => updateSetting('max_execution_time', parseFloat(e.target.value))}
                  className="w-full px-3 py-2 border border-green-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                />
                <p className="text-xs text-green-700 mt-1">Maximum time a program can run</p>
              </div>

              <div>
                <label className="block text-sm font-medium text-green-900 mb-2">
                  <HardDrive className="w-4 h-4 inline mr-1" />
                  Max Memory Usage (MB)
                </label>
                <input
                  type="number"
                  min="16"
                  max="1024"
                  value={settings.max_memory}
                  onChange={(e) => updateSetting('max_memory', parseInt(e.target.value))}
                  className="w-full px-3 py-2 border border-green-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                />
                <p className="text-xs text-green-700 mt-1">Maximum memory a program can use</p>
              </div>

              <div>
                <label className="block text-sm font-medium text-green-900 mb-2">
                  <Zap className="w-4 h-4 inline mr-1" />
                  Max Output Size (bytes)
                </label>
                <input
                  type="number"
                  min="1024"
                  max="1048576"
                  step="1024"
                  value={settings.max_output_size}
                  onChange={(e) => updateSetting('max_output_size', parseInt(e.target.value))}
                  className="w-full px-3 py-2 border border-green-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                />
                <p className="text-xs text-green-700 mt-1">Maximum size of output ({formatBytes(settings.max_output_size)})</p>
              </div>

              <div>
                <label className="block text-sm font-medium text-green-900 mb-2">
                  <Code className="w-4 h-4 inline mr-1" />
                  Max Code Size (bytes)
                </label>
                <input
                  type="number"
                  min="1024"
                  max="1048576"
                  step="1024"
                  value={settings.max_code_size}
                  onChange={(e) => updateSetting('max_code_size', parseInt(e.target.value))}
                  className="w-full px-3 py-2 border border-green-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                />
                <p className="text-xs text-green-700 mt-1">Maximum size of submitted code ({formatBytes(settings.max_code_size)})</p>
              </div>
            </div>
          </div>

          {/* Security Controls */}
          <div className="bg-red-50 border border-red-200 rounded-lg p-4">
            <h3 className="flex items-center space-x-2 text-lg font-medium text-red-900 mb-3">
              <Shield className="w-5 h-5" />
              <span>Security Controls</span>
            </h3>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <h4 className="font-medium text-red-900">Enable Sandboxing</h4>
                  <p className="text-sm text-red-700">Run code in isolated environment</p>
                </div>
                <button
                  onClick={() => updateSetting('enable_sandboxing', !settings.enable_sandboxing)}
                  className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                    settings.enable_sandboxing ? 'bg-red-600' : 'bg-gray-200'
                  }`}
                >
                  <span
                    className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                      settings.enable_sandboxing ? 'translate-x-6' : 'translate-x-1'
                    }`}
                  />
                </button>
              </div>

              <div className="flex items-center justify-between">
                <div>
                  <h4 className="font-medium text-red-900">Enable Network Access</h4>
                  <p className="text-sm text-red-700">Allow programs to make network requests</p>
                </div>
                <button
                  onClick={() => updateSetting('enable_network_access', !settings.enable_network_access)}
                  className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                    settings.enable_network_access ? 'bg-red-600' : 'bg-gray-200'
                  }`}
                >
                  <span
                    className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                      settings.enable_network_access ? 'translate-x-6' : 'translate-x-1'
                    }`}
                  />
                </button>
              </div>
            </div>
          </div>

          {/* Rate Limiting */}
          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
            <h3 className="flex items-center space-x-2 text-lg font-medium text-yellow-900 mb-3">
              <Network className="w-5 h-5" />
              <span>Rate Limiting</span>
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-yellow-900 mb-2">
                  Max Executions per Minute
                </label>
                <input
                  type="number"
                  min="1"
                  max="300"
                  value={settings.max_executions_per_minute}
                  onChange={(e) => updateSetting('max_executions_per_minute', parseInt(e.target.value))}
                  className="w-full px-3 py-2 border border-yellow-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-yellow-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-yellow-900 mb-2">
                  Max Executions per Hour
                </label>
                <input
                  type="number"
                  min="1"
                  max="10000"
                  value={settings.max_executions_per_hour}
                  onChange={(e) => updateSetting('max_executions_per_hour', parseInt(e.target.value))}
                  className="w-full px-3 py-2 border border-yellow-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-yellow-500"
                />
              </div>
            </div>
          </div>

          {/* Advanced Settings */}
          <div className="border border-gray-200 rounded-lg">
            <button
              onClick={() => setShowAdvanced(!showAdvanced)}
              className="w-full px-4 py-3 flex items-center justify-between text-left hover:bg-gray-50"
            >
              <span className="font-medium text-gray-900">Advanced Security Settings</span>
              {showAdvanced ? <Unlock className="w-4 h-4" /> : <Lock className="w-4 h-4" />}
            </button>
            
            {showAdvanced && (
              <div className="border-t border-gray-200 p-4 space-y-4">
                {/* Blocked Imports */}
                <div>
                  <label className="block text-sm font-medium text-gray-900 mb-2">
                    Blocked Python Imports
                  </label>
                  <div className="space-y-2">
                    {settings.blocked_imports.map((importName, index) => (
                      <div key={index} className="flex items-center space-x-2">
                        <input
                          type="text"
                          value={importName}
                          onChange={(e) => updateArraySetting('blocked_imports', index, e.target.value)}
                          className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                        />
                        <button
                          onClick={() => removeFromArray('blocked_imports', index)}
                          className="px-2 py-2 text-red-600 hover:text-red-800 hover:bg-red-50 rounded-lg"
                        >
                          <X className="w-4 h-4" />
                        </button>
                      </div>
                    ))}
                    <button
                      onClick={() => addToArray('blocked_imports', '')}
                      className="px-3 py-2 text-sm text-blue-600 hover:text-blue-800 hover:bg-blue-50 rounded-lg border border-blue-300"
                    >
                      + Add Import
                    </button>
                  </div>
                </div>

                {/* Blocked Functions */}
                <div>
                  <label className="block text-sm font-medium text-gray-900 mb-2">
                    Blocked Python Functions
                  </label>
                  <div className="space-y-2">
                    {settings.blocked_functions.map((funcName, index) => (
                      <div key={index} className="flex items-center space-x-2">
                        <input
                          type="text"
                          value={funcName}
                          onChange={(e) => updateArraySetting('blocked_functions', index, e.target.value)}
                          className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                        />
                        <button
                          onClick={() => removeFromArray('blocked_functions', index)}
                          className="px-2 py-2 text-red-600 hover:text-red-800 hover:bg-red-50 rounded-lg"
                        >
                          <X className="w-4 h-4" />
                        </button>
                      </div>
                    ))}
                    <button
                      onClick={() => addToArray('blocked_functions', '')}
                      className="px-3 py-2 text-sm text-blue-600 hover:text-blue-800 hover:bg-blue-50 rounded-lg border border-blue-300"
                    >
                      + Add Function
                    </button>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Information Box */}
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <div className="flex items-start space-x-3">
              <Info className="w-5 h-5 text-blue-600 mt-0.5" />
              <div>
                <h4 className="font-medium text-blue-900 mb-1">Security Notice</h4>
                <p className="text-sm text-blue-800">
                  These settings control the security and performance of the code execution environment. 
                  Changes will affect all users. Be careful when modifying security restrictions.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Footer */}
      <div className="bg-gray-50 border-t border-gray-200 px-6 py-4 flex items-center justify-between">
        <button
          onClick={resetToDefaults}
          className="px-4 py-2 text-sm text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded-lg"
        >
          Reset to Defaults
        </button>
        
        <div className="flex items-center space-x-3">
          <button
            onClick={onClose}
            className="px-4 py-2 text-sm text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded-lg"
          >
            Cancel
          </button>
          
          <button
            onClick={saveSettings}
            disabled={!hasChanges || loading}
            className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white text-sm rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? (
              <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
            ) : (
              <Save className="w-4 h-4" />
            )}
            <span>{loading ? 'Saving...' : 'Save Settings'}</span>
          </button>
        </div>
      </div>
    </div>
  );
};

export default SecuritySettings;