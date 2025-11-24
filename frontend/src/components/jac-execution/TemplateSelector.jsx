import React, { useState } from 'react';
import { 
  Code, 
  Search, 
  Filter, 
  Star, 
  Play, 
  Download, 
  User,
  Clock,
  Tag,
  ChevronDown,
  ChevronUp,
  X
} from 'lucide-react';

const TemplateSelector = ({ 
  templates = [], 
  onSelectTemplate, 
  onRefreshTemplates 
}) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedLanguage, setSelectedLanguage] = useState('all');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [expandedTemplate, setExpandedTemplate] = useState(null);
  const [showFilters, setShowFilters] = useState(false);

  // Filter templates based on search and filters
  const filteredTemplates = templates.filter(template => {
    const matchesSearch = template.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         template.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         (template.tags && template.tags.some(tag => 
                           tag.toLowerCase().includes(searchTerm.toLowerCase())
                         ));
    
    const matchesLanguage = selectedLanguage === 'all' || template.language === selectedLanguage;
    const matchesCategory = selectedCategory === 'all' || template.category === selectedCategory;
    
    return matchesSearch && matchesLanguage && matchesCategory;
  });

  // Get unique languages and categories for filters
  const languages = [...new Set(templates.map(t => t.language))];
  const categories = [...new Set(templates.map(t => t.category).filter(Boolean))];

  const handleSelectTemplate = (template) => {
    onSelectTemplate(template.code, template.language, template.stdin);
    setExpandedTemplate(null);
  };

  const toggleExpanded = (templateId) => {
    setExpandedTemplate(expandedTemplate === templateId ? null : templateId);
  };

  const executeTemplate = (template, e) => {
    e.stopPropagation();
    onSelectTemplate(template.code, template.language, template.stdin);
    // Trigger execution logic could be added here
  };

  return (
    <div className="bg-white border-t border-gray-200">
      <div className="p-4">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-gray-900 flex items-center space-x-2">
            <Code className="w-5 h-5" />
            <span>Code Templates</span>
          </h3>
          
          <button
            onClick={() => setShowFilters(!showFilters)}
            className="p-2 text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded-lg"
            title="Show/Hide Filters"
          >
            <Filter className="w-4 h-4" />
          </button>
        </div>

        {/* Search and Filters */}
        <div className="space-y-3">
          {/* Search Bar */}
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
            <input
              type="text"
              placeholder="Search templates..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          {/* Filter Controls */}
          {showFilters && (
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-xs font-medium text-gray-700 mb-1">
                  Language
                </label>
                <select
                  value={selectedLanguage}
                  onChange={(e) => setSelectedLanguage(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="all">All Languages</option>
                  {languages.map(lang => (
                    <option key={lang} value={lang}>
                      {lang.toUpperCase()}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-xs font-medium text-gray-700 mb-1">
                  Category
                </label>
                <select
                  value={selectedCategory}
                  onChange={(e) => setSelectedCategory(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="all">All Categories</option>
                  {categories.map(cat => (
                    <option key={cat} value={cat}>
                      {cat}
                    </option>
                  ))}
                </select>
              </div>
            </div>
          )}
        </div>

        {/* Templates List */}
        <div className="mt-4 max-h-80 overflow-y-auto space-y-2">
          {filteredTemplates.length === 0 ? (
            <div className="text-center py-8 text-gray-500">
              <Code className="w-12 h-12 mx-auto mb-3 text-gray-300" />
              <p className="text-sm">
                {searchTerm || selectedLanguage !== 'all' || selectedCategory !== 'all'
                  ? 'No templates found matching your criteria'
                  : 'No templates available'}
              </p>
            </div>
          ) : (
            filteredTemplates.map((template) => (
              <div
                key={template.id}
                className="border border-gray-200 rounded-lg overflow-hidden hover:border-blue-300 transition-colors"
              >
                <div
                  className="p-3 cursor-pointer"
                  onClick={() => toggleExpanded(template.id)}
                >
                  <div className="flex items-start justify-between">
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center space-x-2 mb-1">
                        <h4 className="font-medium text-gray-900 truncate">
                          {template.name}
                        </h4>
                        <span className={`px-2 py-1 text-xs rounded-full ${
                          template.language === 'python' 
                            ? 'bg-green-100 text-green-800' 
                            : 'bg-blue-100 text-blue-800'
                        }`}>
                          {template.language}
                        </span>
                        {template.is_public && (
                          <Star className="w-3 h-3 text-yellow-500" />
                        )}
                      </div>
                      
                      <p className="text-sm text-gray-600 line-clamp-2 mb-2">
                        {template.description}
                      </p>
                      
                      <div className="flex items-center space-x-3 text-xs text-gray-500">
                        <div className="flex items-center space-x-1">
                          <User className="w-3 h-3" />
                          <span>{template.creator_name}</span>
                        </div>
                        
                        <div className="flex items-center space-x-1">
                          <Clock className="w-3 h-3" />
                          <span>{new Date(template.updated_at).toLocaleDateString()}</span>
                        </div>
                        
                        {template.category && (
                          <div className="flex items-center space-x-1">
                            <Tag className="w-3 h-3" />
                            <span>{template.category}</span>
                          </div>
                        )}
                      </div>
                      
                      {template.tags && template.tags.length > 0 && (
                        <div className="flex flex-wrap gap-1 mt-2">
                          {template.tags.slice(0, 3).map((tag, index) => (
                            <span
                              key={index}
                              className="px-2 py-1 text-xs bg-gray-100 text-gray-700 rounded"
                            >
                              {tag}
                            </span>
                          ))}
                          {template.tags.length > 3 && (
                            <span className="px-2 py-1 text-xs text-gray-500">
                              +{template.tags.length - 3} more
                            </span>
                          )}
                        </div>
                      )}
                    </div>
                    
                    <div className="flex items-center space-x-1 ml-2">
                      <button
                        onClick={(e) => executeTemplate(template, e)}
                        className="p-1 text-green-600 hover:text-green-800 hover:bg-green-50 rounded"
                        title="Load & Execute"
                      >
                        <Play className="w-4 h-4" />
                      </button>
                      
                      {expandedTemplate === template.id ? (
                        <ChevronUp className="w-4 h-4 text-gray-400" />
                      ) : (
                        <ChevronDown className="w-4 h-4 text-gray-400" />
                      )}
                    </div>
                  </div>
                </div>

                {/* Expanded Template Preview */}
                {expandedTemplate === template.id && (
                  <div className="border-t border-gray-200 bg-gray-50">
                    <div className="p-4">
                      <div className="mb-3">
                        <div className="flex items-center justify-between mb-2">
                          <span className="text-sm font-medium text-gray-700">Code Preview</span>
                          <button
                            onClick={() => handleSelectTemplate(template)}
                            className="px-3 py-1 bg-blue-600 text-white text-sm rounded hover:bg-blue-700 transition-colors"
                          >
                            Use This Template
                          </button>
                        </div>
                        
                        <div className="bg-gray-900 rounded-lg p-3 max-h-48 overflow-y-auto">
                          <pre className="text-green-400 text-xs font-mono">
                            <code>{template.code}</code>
                          </pre>
                        </div>
                      </div>
                      
                      {template.stdin && (
                        <div className="mb-3">
                          <span className="text-sm font-medium text-gray-700 block mb-1">
                            Standard Input
                          </span>
                          <div className="bg-gray-900 rounded-lg p-3">
                            <pre className="text-yellow-400 text-xs font-mono">
                              <code>{template.stdin}</code>
                            </pre>
                          </div>
                        </div>
                      )}
                      
                      <div className="flex items-center justify-between text-xs text-gray-500">
                        <span>
                          Created: {new Date(template.created_at).toLocaleDateString()}
                        </span>
                        <span>
                          Updated: {new Date(template.updated_at).toLocaleDateString()}
                        </span>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            ))
          )}
        </div>

        {/* Template Count */}
        {filteredTemplates.length > 0 && (
          <div className="mt-4 text-center text-sm text-gray-500">
            Showing {filteredTemplates.length} of {templates.length} templates
          </div>
        )}
      </div>
    </div>
  );
};

export default TemplateSelector;