/**
 * Jac-Client Frontend for Jeseci Learning Platform
 * React-style components for lessons, code editor, quizzes and progress dashboards
 * Uses Spawn() to call walkers directly from the UI
 */

// Main Jac-Client Interface
class JacClientApp {
    constructor() {
        this.user = null;
        this.currentSession = null;
        this.ospGraph = null;
        this.byllmAgents = null;
        
        // Initialize client
        this.initialize();
    }
    
    async initialize() {
        // Connect to Jac backend
        this.connection = await this.establishJacConnection();
        
        // Initialize OSP graph
        this.ospGraph = await this.spawn('initialize_osp_graph');
        
        // Initialize byLLM agents
        this.byllmAgents = await this.spawn('initialize_byllm_agents');
        
        this.setupEventListeners();
    }
    
    // Spawn() function to call walkers
    async spawn(walkerName, data = {}) {
        try {
            const response = await fetch('/jac-api/spawn', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    walker: walkerName,
                    data: data,
                    user_id: this.user?.id
                })
            });
            
            const result = await response.json();
            return result;
        } catch (error) {
            console.error('Spawn error:', error);
            throw error;
        }
    }
    
    setupEventListeners() {
        // Listen for Jac backend events
        document.addEventListener('jac-progress-update', this.handleProgressUpdate.bind(this));
        document.addEventListener('jac-lesson-complete', this.handleLessonComplete.bind(this));
        document.addEventListener('jac-quiz-completed', this.handleQuizCompleted.bind(this));
    }
}

// Learning Dashboard Component
class LearningDashboard extends React.Component {
    constructor(props) {
        super(props);
        this.jacClient = props.jacClient;
        this.state = {
            userProgress: null,
            skillMap: null,
            recommendations: [],
            currentPath: null
        };
    }
    
    async componentDidMount() {
        await this.loadDashboardData();
    }
    
    async loadDashboardData() {
        try {
            // Get user progress through Jac walker
            const progressData = await this.jacClient.spawn('get_user_progress', {
                user_id: this.jacClient.user.id
            });
            
            // Get skill map from OSP graph
            const skillMap = await this.jacClient.spawn('generate_skill_map', {
                user_id: this.jacClient.user.id
            });
            
            // Get learning recommendations from byLLM advisor
            const recommendations = await this.jacClient.spawn('provide_personalized_guidance', {
                user_id: this.jacClient.user.id,
                current_context: {
                    current_time: new Date().toISOString(),
                    recent_activities: progressData.recent_activities
                }
            });
            
            this.setState({
                userProgress: progressData,
                skillMap: skillMap,
                recommendations: recommendations.personalized_recommendations,
                currentPath: recommendations.optimal_next_steps
            });
            
        } catch (error) {
            console.error('Failed to load dashboard data:', error);
        }
    }
    
    render() {
        return React.createElement('div', { className: 'learning-dashboard' },
            React.createElement('div', { className: 'dashboard-header' },
                React.createElement('h1', null, 'Jeseci Learning Dashboard'),
                React.createElement('UserProgressSummary', { 
                    progress: this.state.userProgress 
                })
            ),
            React.createElement('div', { className: 'dashboard-content' },
                React.createElement('div', { className: 'skill-map-section' },
                    React.createElement('SkillMapVisualization', { 
                        skillMap: this.state.skillMap 
                    })
                ),
                React.createElement('div', { className: 'recommendations-section' },
                    React.createElement('PersonalizedRecommendations', { 
                        recommendations: this.state.recommendations 
                    })
                ),
                React.createElement('div', { className: 'current-path-section' },
                    React.createElement('LearningPathProgress', { 
                        currentPath: this.state.currentPath 
                    })
                )
            )
        );
    }
}

// Skill Map Visualization Component
class SkillMapVisualization extends React.Component {
    constructor(props) {
        super(props);
        this.canvasRef = React.createRef();
    }
    
    componentDidMount() {
        this.renderSkillMap();
    }
    
    componentDidUpdate() {
        this.renderSkillMap();
    }
    
    async renderSkillMap() {
        const canvas = this.canvasRef.current;
        if (!canvas || !this.props.skillMap) return;
        
        const ctx = canvas.getContext('2d');
        const concepts = this.props.skillMap.concepts;
        
        // Clear canvas
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        // Draw concept nodes
        for (const concept of concepts) {
            const x = concept.visual_position.x;
            const y = concept.visual_position.y;
            const mastery = concept.current_mastery || 0;
            
            // Node color based on mastery
            const color = this.getMasteryColor(mastery);
            
            // Draw node
            ctx.beginPath();
            ctx.arc(x, y, 20, 0, 2 * Math.PI);
            ctx.fillStyle = color;
            ctx.fill();
            ctx.strokeStyle = '#333';
            ctx.stroke();
            
            // Add label
            ctx.fillStyle = '#333';
            ctx.font = '12px Arial';
            ctx.textAlign = 'center';
            ctx.fillText(concept.concept_name, x, y + 35);
            
            // Add mastery percentage
            ctx.fillText(`${Math.round(mastery * 100)}%`, x, y + 50);
        }
        
        // Draw connections
        await this.drawConnections(ctx, concepts);
    }
    
    async drawConnections(ctx, concepts) {
        const connections = await this.jacClient.spawn('get_concept_connections', {
            concept_ids: concepts.map(c => c.concept_id)
        });
        
        for (const conn of connections) {
            const fromConcept = concepts.find(c => c.concept_id === conn.from);
            const toConcept = concepts.find(c => c.concept_id === conn.to);
            
            if (fromConcept && toConcept) {
                ctx.beginPath();
                ctx.moveTo(fromConcept.visual_position.x, fromConcept.visual_position.y);
                ctx.lineTo(toConcept.visual_position.x, toConcept.visual_position.y);
                
                // Connection style based on relationship type
                if (conn.relationship_type === 'prerequisite') {
                    ctx.strokeStyle = '#ff6b6b';
                    ctx.setLineDash([5, 5]);
                } else {
                    ctx.strokeStyle = '#4ecdc4';
                    ctx.setLineDash([]);
                }
                
                ctx.stroke();
                ctx.setLineDash([]); // Reset dash
            }
        }
    }
    
    getMasteryColor(mastery) {
        if (mastery >= 0.8) return '#4caf50'; // Green
        if (mastery >= 0.6) return '#ffeb3b'; // Yellow
        if (mastery >= 0.4) return '#ff9800'; // Orange
        if (mastery >= 0.2) return '#f44336'; // Red
        return '#9e9e9e'; // Gray
    }
    
    render() {
        return React.createElement('div', { className: 'skill-map-container' },
            React.createElement('h3', null, 'Skill Map'),
            React.createElement('canvas', {
                ref: this.canvasRef,
                width: 600,
                height: 400,
                className: 'skill-map-canvas'
            }),
            React.createElement('div', { className: 'skill-map-legend' },
                React.createElement('div', { className: 'legend-item' },
                    React.createElement('div', { className: 'legend-color', style: { backgroundColor: '#4caf50' } }),
                    React.createElement('span', null, 'Mastered (80%+)')
                ),
                React.createElement('div', { className: 'legend-item' },
                    React.createElement('div', { className: 'legend-color', style: { backgroundColor: '#ffeb3b' } }),
                    React.createElement('span', null, 'Learning (60-80%)')
                ),
                React.createElement('div', { className: 'legend-item' },
                    React.createElement('div', { className: 'legend-color', style: { backgroundColor: '#9e9e9e' } }),
                    React.createElement('span', null, 'Not Started')
                )
            )
        );
    }
}

// Interactive Code Editor Component (Monaco/CodeMirror integration)
class JacCodeEditor extends React.Component {
    constructor(props) {
        super(props);
        this.editorRef = React.createRef();
        this.state = {
            code: props.initialCode || '',
            concept: props.concept,
            exercise: props.exercise,
            validationResults: null,
            executionResults: null
        };
    }
    
    componentDidMount() {
        this.initializeEditor();
    }
    
    initializeEditor() {
        // Initialize Monaco Editor
        this.editor = monaco.editor.create(this.editorRef.current, {
            value: this.state.code,
            language: 'javascript', // Jac syntax highlighting
            theme: 'vs-dark',
            automaticLayout: true,
            minimap: { enabled: false },
            fontSize: 14,
            lineNumbers: 'on',
            scrollBeyondLastLine: false,
            wordWrap: 'on'
        });
        
        // Add Jac-specific syntax highlighting
        this.setupJacSyntaxHighlighting();
        
        // Set up event listeners
        this.editor.onDidChangeModelContent(() => {
            this.handleCodeChange();
        });
    }
    
    setupJacSyntaxHighlighting() {
        // Define Jac language tokens
        monaco.languages.setMonarchTokensProvider('jac', {
            tokenizer: {
                root: [
                    [/[a-zA-Z_][a-zA-Z0-9_]*/, { cases: { 
                        'walker|node|edge|can|has|spawn|report|with|from|import': 'keyword',
                        'true|false|null': 'literal',
                        'default': 'identifier'
                    }}],
                    [/".*?"/, 'string'],
                    [/\d+(\.\d+)?/, 'number'],
                    [/[{}()]/, '@brackets'],
                    [/;/, 'delimiter']
                ]
            }
        });
    }
    
    async handleCodeChange() {
        const newCode = this.editor.getValue();
        this.setState({ code: newCode });
        
        // Validate syntax using Jac walker
        await this.validateCode(newCode);
    }
    
    async validateCode(code) {
        try {
            const validationResult = await this.jacClient.spawn('validate_jac_syntax', {
                code: code,
                concept: this.state.concept
            });
            
            this.setState({ validationResults: validationResult });
            
            if (validationResult.isValid) {
                // Clear error markers
                this.editor.deltaDecorations([], []);
            } else {
                // Add error markers
                const errorMarkers = validationResult.errors.map(error => ({
                    startLineNumber: error.line,
                    startColumn: error.column,
                    endLineNumber: error.line,
                    endColumn: error.column + error.length,
                    message: error.message,
                    severity: monaco.MarkerSeverity.Error
                }));
                
                monaco.editor.setModelMarkers(this.editor.getModel(), 'jac', errorMarkers);
            }
        } catch (error) {
            console.error('Validation error:', error);
        }
    }
    
    async executeCode() {
        try {
            const executionResult = await this.jacClient.spawn('execute_jac_code', {
                code: this.state.code,
                concept: this.state.concept,
                user_id: this.jacClient.user.id,
                exercise_id: this.state.exercise?.id
            });
            
            this.setState({ executionResults: executionResult });
            
            // Dispatch event for parent components
            document.dispatchEvent(new CustomEvent('jac-code-executed', {
                detail: { result: executionResult, concept: this.state.concept }
            }));
            
        } catch (error) {
            console.error('Execution error:', error);
        }
    }
    
    render() {
        return React.createElement('div', { className: 'jac-code-editor' },
            React.createElement('div', { className: 'editor-header' },
                React.createElement('h3', null, `Jac Code Editor - ${this.state.concept}`),
                React.createElement('div', { className: 'editor-actions' },
                    React.createElement('button', {
                        onClick: () => this.validateCode(this.state.code),
                        className: 'validate-btn'
                    }, 'Validate'),
                    React.createElement('button', {
                        onClick: () => this.executeCode(),
                        className: 'execute-btn'
                    }, 'Run Code')
                )
            ),
            React.createElement('div', { ref: this.editorRef, className: 'editor-container' }),
            this.state.validationResults && React.createElement('ValidationPanel', {
                results: this.state.validationResults
            }),
            this.state.executionResults && React.createElement('ExecutionPanel', {
                results: this.state.executionResults
            })
        );
    }
}

// Interactive Lesson Component
class InteractiveLesson extends React.Component {
    constructor(props) {
        super(props);
        this.jacClient = props.jacClient;
        this.state = {
            lesson: null,
            currentBlock: 0,
            progress: 0,
            responses: [],
            isCompleted: false
        };
    }
    
    async componentDidMount() {
        await this.loadLesson();
    }
    
    async loadLesson() {
        try {
            const lessonData = await this.jacClient.spawn('deliver_lesson', {
                user_id: this.jacClient.user.id,
                lesson_id: this.props.lessonId
            });
            
            this.setState({ 
                lesson: lessonData,
                currentBlock: 0
            });
        } catch (error) {
            console.error('Failed to load lesson:', error);
        }
    }
    
    async handleBlockComplete(blockIndex, response) {
        // Track progress through Jac walker
        await this.jacClient.spawn('track_lesson_progress', {
            session_id: this.state.lesson.session_id,
            progress_data: {
                block_index: blockIndex,
                response: response,
                completed_successfully: response.success
            }
        });
        
        // Update local state
        const newResponses = [...this.state.responses];
        newResponses[blockIndex] = response;
        
        this.setState({
            responses: newResponses,
            progress: ((blockIndex + 1) / this.state.lesson.content_blocks.length) * 100
        });
        
        // Move to next block or complete lesson
        if (blockIndex + 1 < this.state.lesson.content_blocks.length) {
            this.setState({ currentBlock: blockIndex + 1 });
        } else {
            await this.completeLesson();
        }
    }
    
    async completeLesson() {
        try {
            const completionResult = await this.jacClient.spawn('complete_lesson', {
                session_id: this.state.lesson.session_id,
                user_id: this.jacClient.user.id,
                concept: this.state.lesson.concept_focus,
                responses: this.state.responses
            });
            
            this.setState({ isCompleted: true });
            
            // Dispatch completion event
            document.dispatchEvent(new CustomEvent('jac-lesson-complete', {
                detail: { 
                    lesson_id: this.props.lessonId,
                    concept: this.state.lesson.concept_focus,
                    mastery_improvement: completionResult.mastery_improvement
                }
            }));
            
        } catch (error) {
            console.error('Failed to complete lesson:', error);
        }
    }
    
    render() {
        if (!this.state.lesson) {
            return React.createElement('div', { className: 'lesson-loading' }, 'Loading lesson...');
        }
        
        const currentBlock = this.state.lesson.content_blocks[this.state.currentBlock];
        
        return React.createElement('div', { className: 'interactive-lesson' },
            React.createElement('div', { className: 'lesson-header' },
                React.createElement('h2', null, this.state.lesson.title),
                React.createElement('ProgressBar', { progress: this.state.progress }),
                React.createElement('div', { className: 'lesson-info' },
                    React.createElement('span', null, `Concept: ${this.state.lesson.concept_focus}`),
                    React.createElement('span', null, `Duration: ${this.state.lesson.estimated_duration} minutes`)
                )
            ),
            React.createElement('div', { className: 'lesson-content' },
                React.createElement(LessonBlock, {
                    block: currentBlock,
                    blockIndex: this.state.currentBlock,
                    onComplete: (response) => this.handleBlockComplete(this.state.currentBlock, response),
                    jacClient: this.jacClient
                })
            )
        );
    }
}

// Lesson Block Component
class LessonBlock extends React.Component {
    constructor(props) {
        super(props);
        this.jacClient = props.jacClient;
    }
    
    render() {
        const { block, blockIndex } = this.props;
        
        switch (block.type) {
            case 'text':
                return React.createElement(TextBlock, { block: block, blockIndex: blockIndex });
            
            case 'code_example':
                return React.createElement(CodeExampleBlock, { 
                    block: block, 
                    blockIndex: blockIndex,
                    jacClient: this.jacClient 
                });
            
            case 'interactive':
                return React.createElement(InteractiveBlock, { 
                    block: block, 
                    blockIndex: blockIndex,
                    jacClient: this.jacClient 
                });
            
            case 'quiz':
                return React.createElement(QuizBlock, { 
                    block: block, 
                    blockIndex: blockIndex,
                    jacClient: this.jacClient 
                });
            
            default:
                return React.createElement('div', null, 'Unknown block type');
        }
    }
}

// Export components for use in HTML
window.JacClientApp = JacClientApp;
window.LearningDashboard = LearningDashboard;
window.JacCodeEditor = JacCodeEditor;
window.InteractiveLesson = InteractiveLesson;