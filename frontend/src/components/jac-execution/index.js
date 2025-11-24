// Frontend Components Index
// JAC Code Execution Platform Components

export { default as CodeExecutionPanel } from './CodeExecutionPanel';
export { default as CodeEditor } from './CodeEditor';
export { default as OutputWindow } from './OutputWindow';
export { default as TemplateSelector } from './TemplateSelector';
export { default as ExecutionHistory } from './ExecutionHistory';
export { default as SecuritySettings } from './SecuritySettings';
export { default as CodeTranslationPanel } from './CodeTranslationPanel';

// Component metadata for easy importing
export const componentInfo = {
  'CodeExecutionPanel': {
    name: 'CodeExecutionPanel',
    description: 'Main code execution interface with editor, output, and controls',
    features: [
      'Code editing with syntax highlighting',
      'Real-time code execution',
      'Output and error display',
      'Template selection',
      'Execution history',
      'User statistics',
      'Security settings'
    ],
    dependencies: [
      'CodeEditor',
      'OutputWindow', 
      'TemplateSelector',
      'ExecutionHistory',
      'SecuritySettings',
      'CodeTranslationPanel'
    ]
  },
  'CodeEditor': {
    name: 'CodeEditor',
    description: 'Monaco-based code editor with syntax highlighting and settings',
    features: [
      'Syntax highlighting for Python and JAC',
      'Customizable font size and theme',
      'Code formatting',
      'Line numbers and minimap',
      'Keyboard shortcuts'
    ],
    dependencies: ['@monaco-editor/react']
  },
  'OutputWindow': {
    name: 'OutputWindow',
    description: 'Display execution results, errors, and performance metrics',
    features: [
      'Standard output display',
      'Error output display',
      'Copy and download functionality',
      'Execution status indicators',
      'Performance metrics'
    ],
    dependencies: []
  },
  'TemplateSelector': {
    name: 'TemplateSelector',
    description: 'Browse and select from pre-built code templates',
    features: [
      'Template filtering and search',
      'Code preview',
      'Category organization',
      'Quick template loading'
    ],
    dependencies: []
  },
  'ExecutionHistory': {
    name: 'ExecutionHistory',
    description: 'View and manage execution history with statistics',
    features: [
      'Execution history display',
      'Statistics and analytics',
      'Filtering and search',
      'History management'
    ],
    dependencies: []
  },
  'SecuritySettings': {
    name: 'SecuritySettings',
    description: 'Configure security and execution parameters',
    features: [
      'Language support configuration',
      'Resource limit settings',
      'Security controls',
      'Rate limiting configuration'
    ],
    dependencies: []
  },
  'CodeTranslationPanel': {
    name: 'CodeTranslationPanel',
    description: 'Bidirectional code translation between JAC and Python',
    features: [
      'JAC to Python conversion',
      'Python to JAC conversion',
      'Side-by-side code comparison',
      'Translation validation and error reporting',
      'Copy and download translated code',
      'Load translated code to editor'
    ],
    dependencies: ['CodeEditor']
  }
};

// Installation and setup instructions
export const setupInstructions = {
  backend: [
    'Ensure Django is installed and configured',
    'Install required dependencies: djangorestframework',
    'Run migrations: python manage.py migrate',
    'Configure CORS settings for frontend integration',
    'Set up authentication for API access'
  ],
  frontend: [
    'Install required packages: react, @monaco-editor/react, lucide-react',
    'Import components from this package',
    'Configure API endpoints in CodeExecutionPanel',
    'Set up authentication token storage',
    'Configure Monaco Editor language support'
  ],
  integration: [
    'Add jac_execution URLs to main Django URLs',
    'Configure JWT authentication',
    'Set up CORS headers for cross-origin requests',
    'Test API endpoints and frontend communication',
    'Configure environment variables for security settings'
  ]
};