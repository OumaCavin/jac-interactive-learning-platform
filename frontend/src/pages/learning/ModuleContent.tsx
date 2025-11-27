// JAC Learning Platform - TypeScript utilities by Cavin Otieno

import React, { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import {
  ArrowLeftIcon,
  ArrowRightIcon,
  BookOpenIcon,
  CodeBracketIcon,
  AcademicCapIcon,
  CheckCircleIcon,
  ClockIcon,
  PlayIcon,
  PauseIcon,
  ForwardIcon,
  BackwardIcon,
  ShareIcon,
  BookmarkIcon,
  ChevronDownIcon,
  ChevronUpIcon,
} from '@heroicons/react/24/outline';

// Mock module content with rich learning material
const MOCK_MODULE_CONTENT = {
  id: 1,
  title: 'Introduction to Variables',
  type: 'lesson',
  content: {
    sections: [
      {
        id: 'introduction',
        title: 'What are Variables?',
        content: `
Variables are fundamental building blocks in programming. Think of them as labeled containers that store information you can use and change throughout your program.

In JAC, variables are like labeled boxes where you can put different types of information - numbers, text, true/false values, and more.

**Key Concepts:**
- Variables store data
- They have names (identifiers)
- They hold different types of values
- You can change their values

Let's start by learning how to create and use variables in JAC.
        `
      },
      {
        id: 'syntax',
        title: 'Variable Declaration Syntax',
        content: `
In JAC, you declare variables using the \`var\` keyword followed by the variable name:

\`\`\`jac
var myVariable;
\`\`\`

You can also declare and assign a value in one step:

\`\`\`jac
var greeting = "Hello, World!";
var count = 42;
var isActive = true;
\`\`\`

**Variable Naming Rules:**
- Must start with a letter or underscore
- Can contain letters, numbers, and underscores
- Case-sensitive (myVar and myvar are different)
- Cannot be JAC keywords
        `
      },
      {
        id: 'types',
        title: 'Basic Data Types',
        content: `
JAC supports several basic data types:

**Numbers:**
- Integers: \`var age = 25;\`
- Decimals: \`var price = 19.99;\`

**Text:**
- Strings: \`var name = "Alice";\`
- Characters: \`var grade = 'A';\`

**Boolean:**
- True/False: \`var isComplete = true;\`

**Examples:**
\`\`\`jac
var studentName = "John Doe";
var age = 20;
var gpa = 3.8;
var isEnrolled = true;
var courseCode = "CS101";
\`\`\`
        `
      },
      {
        id: 'practice',
        title: 'Practice Exercise',
        content: `
Now it's your turn! Create variables for a student profile:

1. Create a variable called \`studentName\` and assign your name as a string
2. Create a variable called \`studentAge\` and assign your age as a number
3. Create a variable called \`isGraduated\` and assign \`false\`
4. Create a variable called \`studentId\` and assign any number

Try writing this in the code editor below and see what happens!
        `,
        exercise: {
          type: 'code',
          instructions: [
            'Declare a variable called studentName and assign your name',
            'Declare a variable called studentAge and assign your age',
            'Declare a variable called isGraduated and assign false',
            'Declare a variable called studentId and assign any number'
          ],
          template: `// Create your student profile variables here
var studentName = ""; // Replace with your name
var studentAge = 0;   // Replace with your age  
var isGraduated = false;
var studentId = 0;    // Replace with any number`,
          expectedOutput: 'All variables should be declared and initialized with appropriate values.'
        }
      }
    ],
    summary: 'Variables are containers that store data. In JAC, you declare them using the \`var\` keyword and can assign different types of values including numbers, strings, and booleans.'
  }
};

const ModuleContent: React.FC = () => {
  const { pathId, moduleId } = useParams<{ pathId: string; moduleId: string }>();
  const navigate = useNavigate();
  
  const [moduleData, setModuleData] = useState(MOCK_MODULE_CONTENT);
  const [currentSection, setCurrentSection] = useState(0);
  const [isCompleted, setIsCompleted] = useState(false);
  const [timeSpent, setTimeSpent] = useState(0);
  const [startTime] = useState(Date.now());
  const [showCodeEditor, setShowCodeEditor] = useState(false);
  const [userCode, setUserCode] = useState('');
  const [isPlaying, setIsPlaying] = useState(false);
  const [showAllSections, setShowAllSections] = useState(false);

  // Simulate time tracking
  useEffect(() => {
    const interval = setInterval(() => {
      setTimeSpent(Math.floor((Date.now() - startTime) / 1000));
    }, 1000);

    return () => clearInterval(interval);
  }, [startTime]);

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const handleNext = () => {
    if (currentSection < moduleData.content.sections.length - 1) {
      setCurrentSection(currentSection + 1);
    }
  };

  const handlePrevious = () => {
    if (currentSection > 0) {
      setCurrentSection(currentSection - 1);
    }
  };

  const handleComplete = () => {
    setIsCompleted(true);
    // In a real app, you would update the user's progress
  };

  const handleShare = () => {
    if (navigator.share) {
      navigator.share({
        title: moduleData.title,
        text: `Learning about ${moduleData.title}`,
        url: window.location.href,
      });
    } else {
      navigator.clipboard.writeText(window.location.href);
      // You could show a toast notification here
    }
  };

  const handleBookmark = () => {
    // In a real app, you would save/bookmark this module
    // toast.success('Module bookmarked successfully');
  };

  const getModuleTypeIcon = (type: string) => {
    switch (type) {
      case 'lesson': return <BookOpenIcon className="w-5 h-5" />;
      case 'exercise': return <CodeBracketIcon className="w-5 h-5" />;
      case 'assessment': return <AcademicCapIcon className="w-5 h-5" />;
      default: return <BookOpenIcon className="w-5 h-5" />;
    }
  };

  const getModuleTypeColor = (type: string) => {
    switch (type) {
      case 'lesson': return 'bg-blue-100 text-blue-800';
      case 'exercise': return 'bg-green-100 text-green-800';
      case 'assessment': return 'bg-purple-100 text-purple-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const currentSectionData = moduleData.content.sections[currentSection];

  return (
    <div className="container mx-auto px-4 py-8 max-w-5xl">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center gap-4 mb-4">
          <Link 
            to={`/learning/${pathId}`}
            className="flex items-center gap-2 text-blue-600 hover:text-blue-800 transition-colors"
          >
            <ArrowLeftIcon className="w-4 h-4" />
            Back to Learning Path
          </Link>
          
          <span className="text-gray-400">|</span>
          
          <div className="flex items-center gap-2">
            <ClockIcon className="w-4 h-4 text-gray-500" />
            <span className="text-sm text-gray-600">{formatTime(timeSpent)}</span>
          </div>
        </div>

        <div className="flex flex-col lg:flex-row lg:items-start lg:justify-between gap-6">
          <div className="flex-1">
            <div className="flex items-center gap-3 mb-4">
              <span className={`inline-flex items-center gap-2 px-3 py-1 rounded-full text-sm font-medium ${getModuleTypeColor(moduleData.type)}`}>
                {getModuleTypeIcon(moduleData.type)}
                {moduleData.type.charAt(0).toUpperCase() + moduleData.type.slice(1)}
              </span>
              
              {isCompleted && (
                <span className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-sm font-medium bg-green-100 text-green-800">
                  <CheckCircleIcon className="w-4 h-4" />
                  Completed
                </span>
              )}
            </div>
            
            <h1 className="text-3xl font-bold text-gray-900 mb-2">{moduleData.title}</h1>
            <p className="text-gray-600">
              Module {moduleId} of Learning Path {pathId}
            </p>
          </div>

          <div className="flex items-center gap-3">
            <button
              onClick={handleShare}
              className="flex items-center gap-2 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
            >
              <ShareIcon className="w-4 h-4" />
              Share
            </button>
            
            <button
              onClick={handleBookmark}
              className="flex items-center gap-2 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
            >
              <BookmarkIcon className="w-4 h-4" />
              Bookmark
            </button>
            
            <button
              onClick={() => setShowCodeEditor(!showCodeEditor)}
              className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              <CodeBracketIcon className="w-4 h-4" />
              Code Editor
            </button>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
        {/* Main Content */}
        <div className="lg:col-span-3">
          {/* Progress Bar */}
          <div className="mb-8">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm text-gray-600">Progress</span>
              <span className="text-sm text-gray-600">
                {currentSection + 1} of {moduleData.content.sections.length}
              </span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div
                className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                style={{ width: `${((currentSection + 1) / moduleData.content.sections.length) * 100}%` }}
              />
            </div>
          </div>

          {/* Section Navigation */}
          <div className="bg-white rounded-lg border border-gray-200 p-4 mb-6">
            <button
              onClick={() => setShowAllSections(!showAllSections)}
              className="flex items-center justify-between w-full text-left"
            >
              <span className="font-medium text-gray-900">Table of Contents</span>
              {showAllSections ? (
                <ChevronUpIcon className="w-5 h-5 text-gray-500" />
              ) : (
                <ChevronDownIcon className="w-5 h-5 text-gray-500" />
              )}
            </button>
            
            {showAllSections && (
              <div className="mt-4 space-y-2">
                {moduleData.content.sections.map((section, index) => (
                  <button
                    key={section.id}
                    onClick={() => setCurrentSection(index)}
                    className={`w-full text-left p-2 rounded transition-colors ${
                      currentSection === index
                        ? 'bg-blue-50 text-blue-700'
                        : 'text-gray-600 hover:bg-gray-50'
                    }`}
                  >
                    <div className="flex items-center gap-3">
                      <div className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-medium ${
                        currentSection === index
                          ? 'bg-blue-600 text-white'
                          : 'bg-gray-200 text-gray-600'
                      }`}>
                        {index + 1}
                      </div>
                      <span className="text-sm">{section.title}</span>
                    </div>
                  </button>
                ))}
              </div>
            )}
          </div>

          {/* Section Content */}
          <motion.div
            key={currentSection}
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.3 }}
            className="bg-white rounded-lg border border-gray-200 p-8"
          >
            <h2 className="text-2xl font-bold text-gray-900 mb-6">
              {currentSectionData.title}
            </h2>
            
            <div className="prose prose-gray max-w-none mb-8">
              {currentSectionData.content.split('\n').map((paragraph, index) => {
                if (paragraph.trim() === '') return null;
                
                // Handle code blocks
                if (paragraph.startsWith('```')) {
                  const language = paragraph.substring(3);
                  const nextIndex = currentSectionData.content.indexOf('\n', currentSectionData.content.indexOf(paragraph)) + 1;
                  const endIndex = currentSectionData.content.indexOf('\n```', nextIndex);
                  const codeContent = currentSectionData.content.substring(nextIndex, endIndex);
                  
                  return (
                    <div key={index} className="my-6">
                      <pre className="bg-gray-900 text-gray-100 p-4 rounded-lg overflow-x-auto">
                        <code>{codeContent}</code>
                      </pre>
                    </div>
                  );
                }
                
                // Handle headers
                if (paragraph.startsWith('**') && paragraph.endsWith('**')) {
                  return (
                    <h3 key={index} className="text-lg font-semibold text-gray-900 mt-6 mb-3">
                      {paragraph.slice(2, -2)}
                    </h3>
                  );
                }
                
                // Handle bold text
                if (paragraph.includes('**')) {
                  const parts = paragraph.split('**');
                  return (
                    <p key={index} className="mb-4 text-gray-700 leading-relaxed">
                      {parts.map((part, partIndex) => 
                        partIndex % 2 === 1 ? (
                          <strong key={partIndex} className="font-semibold">{part}</strong>
                        ) : (
                          part
                        )
                      )}
                    </p>
                  );
                }
                
                // Regular paragraph
                return (
                  <p key={index} className="mb-4 text-gray-700 leading-relaxed">
                    {paragraph}
                  </p>
                );
              })}
            </div>

            {/* Exercise Section */}
            {currentSectionData.exercise && (
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-6 mt-8">
                <h3 className="text-lg font-semibold text-blue-900 mb-4">Practice Exercise</h3>
                <div className="space-y-4">
                  <div>
                    <h4 className="font-medium text-blue-800 mb-2">Instructions:</h4>
                    <ol className="list-decimal list-inside space-y-1 text-blue-700">
                      {currentSectionData.exercise.instructions.map((instruction, index) => (
                        <li key={index} className="text-sm">{instruction}</li>
                      ))}
                    </ol>
                  </div>
                  
                  {currentSectionData.exercise.template && (
                    <div>
                      <h4 className="font-medium text-blue-800 mb-2">Template:</h4>
                      <pre className="bg-blue-900 text-blue-100 p-3 rounded text-sm overflow-x-auto">
                        <code>{currentSectionData.exercise.template}</code>
                      </pre>
                    </div>
                  )}
                  
                  <div className="flex gap-3 mt-4">
                    <button className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors">
                      Run Code
                    </button>
                    <button className="px-4 py-2 border border-blue-600 text-blue-600 rounded hover:bg-blue-50 transition-colors">
                      Reset
                    </button>
                  </div>
                </div>
              </div>
            )}
          </motion.div>

          {/* Navigation */}
          <div className="flex items-center justify-between mt-8">
            <button
              onClick={handlePrevious}
              disabled={currentSection === 0}
              className="flex items-center gap-2 px-6 py-3 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <BackwardIcon className="w-4 h-4" />
              Previous
            </button>

            <div className="flex items-center gap-4">
              {/* Auto-play controls */}
              <button
                onClick={() => setIsPlaying(!isPlaying)}
                className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-colors ${
                  isPlaying 
                    ? 'bg-orange-600 text-white hover:bg-orange-700' 
                    : 'bg-blue-600 text-white hover:bg-blue-700'
                }`}
              >
                {isPlaying ? <PauseIcon className="w-4 h-4" /> : <PlayIcon className="w-4 h-4" />}
                {isPlaying ? 'Pause' : 'Auto-play'}
              </button>

              {currentSection === moduleData.content.sections.length - 1 && !isCompleted && (
                <button
                  onClick={handleComplete}
                  className="flex items-center gap-2 px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
                >
                  <CheckCircleIcon className="w-4 h-4" />
                  Mark Complete
                </button>
              )}
            </div>

            <button
              onClick={handleNext}
              disabled={currentSection === moduleData.content.sections.length - 1}
              className="flex items-center gap-2 px-6 py-3 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Next
              <ForwardIcon className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Module Summary */}
          <div className="bg-white rounded-lg border border-gray-200 p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Module Summary</h3>
            <p className="text-gray-600 text-sm leading-relaxed">
              {moduleData.content.summary}
            </p>
          </div>

          {/* Code Editor */}
          {showCodeEditor && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-white rounded-lg border border-gray-200 p-6"
            >
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Code Editor</h3>
              <textarea
                value={userCode}
                onChange={(e) => setUserCode(e.target.value)}
                placeholder="Write your JAC code here..."
                className="w-full h-40 p-3 border border-gray-300 rounded-lg font-mono text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
              <div className="flex gap-2 mt-4">
                <button className="flex-1 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors">
                  Run
                </button>
                <button
                  onClick={() => setUserCode('')}
                  className="px-4 py-2 border border-gray-300 rounded hover:bg-gray-50 transition-colors"
                >
                  Clear
                </button>
              </div>
            </motion.div>
          )}

          {/* Quick Actions */}
          <div className="bg-white rounded-lg border border-gray-200 p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
            <div className="space-y-3">
              <button
                onClick={() => setShowCodeEditor(!showCodeEditor)}
                className="w-full text-left px-3 py-2 text-sm text-gray-700 hover:bg-gray-50 rounded transition-colors"
              >
                {showCodeEditor ? 'Hide' : 'Show'} Code Editor
              </button>
              <button className="w-full text-left px-3 py-2 text-sm text-gray-700 hover:bg-gray-50 rounded transition-colors">
                Download Resources
              </button>
              <button className="w-full text-left px-3 py-2 text-sm text-gray-700 hover:bg-gray-50 rounded transition-colors">
                Report Issue
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ModuleContent;