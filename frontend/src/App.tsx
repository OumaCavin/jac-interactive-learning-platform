import React, { Suspense } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Provider } from 'react-redux';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { motion, AnimatePresence } from 'framer-motion';

// Store and Services
import { store } from './store/store';
import { authService } from './services/authService';

// Components
import { LoadingSpinner } from './components/ui/LoadingSpinner';
import { ErrorBoundary } from './components/ui/ErrorBoundary';
import { NotificationProvider } from './components/ui/NotificationProvider';

// Layout Components
import { MainLayout } from './components/layout/MainLayout';
import { AuthLayout } from './components/layout/AuthLayout';
import AdminRoute from './components/auth/AdminRoute';

// Pages (using React.lazy for code splitting)
const Dashboard = React.lazy(() => import('./pages/Dashboard'));
const LoginPage = React.lazy(() => import('./pages/auth/LoginPage'));
const RegisterPage = React.lazy(() => import('./pages/auth/RegisterPage'));
const LearningPaths = React.lazy(() => import('./pages/learning/LearningPaths'));
const LearningPathDetail = React.lazy(() => import('./pages/learning/LearningPathDetail'));
const ModuleContent = React.lazy(() => import('./pages/learning/ModuleContent'));
const CodeEditor = React.lazy(() => import('./pages/CodeEditor'));
const KnowledgeGraph = React.lazy(() => import('./pages/KnowledgeGraph'));
const Assessments = React.lazy(() => import('./pages/assessments/Assessments'));
const AssessmentDetail = React.lazy(() => import('./pages/assessments/AssessmentDetail'));
const AdminDashboard = React.lazy(() => import('./pages/AdminDashboard'));
const Progress = React.lazy(() => import('./pages/Progress'));
const Profile = React.lazy(() => import('./pages/Profile'));
const Settings = React.lazy(() => import('./pages/Settings'));
const Achievements = React.lazy(() => import('./pages/Achievements'));
const Chat = React.lazy(() => import('./pages/Chat'));
const SearchResultsPage = React.lazy(() => import('./pages/search/SearchResultsPage'));

// Create Query Client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 3,
      retryDelay: 1000,
      refetchOnWindowFocus: false,
      staleTime: 5 * 60 * 1000, // 5 minutes
    },
    mutations: {
      retry: 1,
    },
  },
});

// Protected Route Component
interface ProtectedRouteProps {
  children: React.ReactNode;
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children }) => {
  const isAuthenticated = authService.isAuthenticated();
  
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }
  
  return <>{children}</>;
};

// Public Route Component (redirect to dashboard if authenticated)
interface PublicRouteProps {
  children: React.ReactNode;
}

const PublicRoute: React.FC<PublicRouteProps> = ({ children }) => {
  const isAuthenticated = authService.isAuthenticated();
  
  if (isAuthenticated) {
    return <Navigate to="/dashboard" replace />;
  }
  
  return <>{children}</>;
};

// Page Transition Component
interface PageTransitionProps {
  children: React.ReactNode;
  pageKey: string;
}

const PageTransition: React.FC<PageTransitionProps> = ({ children, pageKey }) => {
  return (
    <AnimatePresence mode="wait">
      <motion.div
        key={pageKey}
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: -20 }}
        transition={{ duration: 0.3, ease: 'easeInOut' }}
        className="min-h-screen"
      >
        {children}
      </motion.div>
    </AnimatePresence>
  );
};

// Loading Fallback
const PageLoadingFallback: React.FC = () => (
  <div className="flex items-center justify-center min-h-screen">
    <LoadingSpinner size="lg" />
  </div>
);

const App: React.FC = () => {
  return (
    <ErrorBoundary>
      <Provider store={store}>
        <QueryClientProvider client={queryClient}>
          <NotificationProvider>
            <Router>
              <div className="min-h-screen bg-gradient-to-br from-primary-500 via-secondary-500 to-primary-700">
                <Suspense fallback={<PageLoadingFallback />}>
                  <Routes>
                    {/* Auth Routes */}
                    <Route 
                      path="/login" 
                      element={
                        <PublicRoute>
                          <AuthLayout>
                            <PageTransition pageKey="login">
                              <LoginPage />
                            </PageTransition>
                          </AuthLayout>
                        </PublicRoute>
                      } 
                    />
                    <Route 
                      path="/register" 
                      element={
                        <PublicRoute>
                          <AuthLayout>
                            <PageTransition pageKey="register">
                              <RegisterPage />
                            </PageTransition>
                          </AuthLayout>
                        </PublicRoute>
                      } 
                    />

                    {/* Protected Routes */}
                    <Route 
                      path="/" 
                      element={
                        <ProtectedRoute>
                          <MainLayout>
                            <PageTransition pageKey="dashboard">
                              <Dashboard />
                            </PageTransition>
                          </MainLayout>
                        </ProtectedRoute>
                      } 
                    />
                    
                    <Route 
                      path="/dashboard" 
                      element={
                        <ProtectedRoute>
                          <MainLayout>
                            <PageTransition pageKey="dashboard">
                              <Dashboard />
                            </PageTransition>
                          </MainLayout>
                        </ProtectedRoute>
                      } 
                    />

                    {/* Learning Routes */}
                    <Route 
                      path="/learning" 
                      element={
                        <ProtectedRoute>
                          <MainLayout>
                            <PageTransition pageKey="learning-paths">
                              <LearningPaths />
                            </PageTransition>
                          </MainLayout>
                        </ProtectedRoute>
                      } 
                    />
                    
                    <Route 
                      path="/learning/:pathId" 
                      element={
                        <ProtectedRoute>
                          <MainLayout>
                            <PageTransition pageKey="learning-path-detail">
                              <LearningPathDetail />
                            </PageTransition>
                          </MainLayout>
                        </ProtectedRoute>
                      } 
                    />
                    
                    <Route 
                      path="/learning/:pathId/module/:moduleId" 
                      element={
                        <ProtectedRoute>
                          <MainLayout>
                            <PageTransition pageKey="module-content">
                              <ModuleContent />
                            </PageTransition>
                          </MainLayout>
                        </ProtectedRoute>
                      } 
                    />

                    {/* Code Editor */}
                    <Route 
                      path="/code-editor" 
                      element={
                        <ProtectedRoute>
                          <MainLayout>
                            <PageTransition pageKey="code-editor">
                              <CodeEditor />
                            </PageTransition>
                          </MainLayout>
                        </ProtectedRoute>
                      } 
                    />

                    {/* Knowledge Graph */}
                    <Route 
                      path="/knowledge-graph" 
                      element={
                        <ProtectedRoute>
                          <MainLayout>
                            <PageTransition pageKey="knowledge-graph">
                              <KnowledgeGraph />
                            </PageTransition>
                          </MainLayout>
                        </ProtectedRoute>
                      } 
                    />
                    
                    {/* Admin Routes */}
                    <Route 
                      path="/admin" 
                      element={
                        <AdminRoute>
                          <MainLayout>
                            <PageTransition pageKey="admin">
                              <AdminDashboard />
                            </PageTransition>
                          </MainLayout>
                        </AdminRoute>
                      } 
                    />

                    {/* Assessment Routes */}
                    <Route 
                      path="/assessments" 
                      element={
                        <ProtectedRoute>
                          <MainLayout>
                            <PageTransition pageKey="assessments">
                              <Assessments />
                            </PageTransition>
                          </MainLayout>
                        </ProtectedRoute>
                      } 
                    />
                    
                    <Route 
                      path="/assessments/:assessmentId" 
                      element={
                        <ProtectedRoute>
                          <MainLayout>
                            <PageTransition pageKey="assessment-detail">
                              <AssessmentDetail />
                            </PageTransition>
                          </MainLayout>
                        </ProtectedRoute>
                      } 
                    />

                    {/* Progress and Analytics */}
                    <Route 
                      path="/progress" 
                      element={
                        <ProtectedRoute>
                          <MainLayout>
                            <PageTransition pageKey="progress">
                              <Progress />
                            </PageTransition>
                          </MainLayout>
                        </ProtectedRoute>
                      } 
                    />

                    {/* User Profile and Settings */}
                    <Route 
                      path="/profile" 
                      element={
                        <ProtectedRoute>
                          <MainLayout>
                            <PageTransition pageKey="profile">
                              <Profile />
                            </PageTransition>
                          </MainLayout>
                        </ProtectedRoute>
                      } 
                    />

                    <Route 
                      path="/settings" 
                      element={
                        <ProtectedRoute>
                          <MainLayout>
                            <PageTransition pageKey="settings">
                              <Settings />
                            </PageTransition>
                          </MainLayout>
                        </ProtectedRoute>
                      } 
                    />

                    {/* Achievements */}
                    <Route 
                      path="/achievements" 
                      element={
                        <ProtectedRoute>
                          <MainLayout>
                            <PageTransition pageKey="achievements">
                              <Achievements />
                            </PageTransition>
                          </MainLayout>
                        </ProtectedRoute>
                      } 
                    />

                    {/* AI Chat */}
                    <Route 
                      path="/chat" 
                      element={
                        <ProtectedRoute>
                          <MainLayout>
                            <PageTransition pageKey="chat">
                              <Chat />
                            </PageTransition>
                          </MainLayout>
                        </ProtectedRoute>
                      } 
                    />

                    {/* Search Results */}
                    <Route 
                      path="/search" 
                      element={
                        <ProtectedRoute>
                          <MainLayout>
                            <PageTransition pageKey="search-results">
                              <SearchResultsPage />
                            </PageTransition>
                          </MainLayout>
                        </ProtectedRoute>
                      } 
                    />

                    {/* Catch all route - redirect to dashboard */}
                    <Route path="*" element={<Navigate to="/dashboard" replace />} />
                  </Routes>
                </Suspense>
              </div>
            </Router>
          </NotificationProvider>
        </QueryClientProvider>
      </Provider>
    </ErrorBoundary>
  );
};

export default App;