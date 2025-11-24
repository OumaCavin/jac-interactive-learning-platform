import React from 'react';
import { motion } from 'framer-motion';

interface AuthLayoutProps {
  children: React.ReactNode;
}

const AuthLayout: React.FC<AuthLayoutProps> = ({ children }) => {
  return (
    <div className="min-h-screen flex">
      {/* Left side - Branding and background */}
      <div className="hidden lg:flex lg:flex-1 lg:flex-col lg:justify-center lg:px-12 bg-gradient-to-br from-primary-600 via-primary-700 to-secondary-600 relative overflow-hidden">
        {/* Background pattern */}
        <div className="absolute inset-0 bg-[url(&apos;data:image/svg+xml,%3Csvg width=&quot;60&quot; height=&quot;60&quot; viewBox=&quot;0 0 60 60&quot; xmlns=&quot;http://www.w3.org/2000/svg&quot;%3E%3Cg fill=&quot;none&quot; fill-rule=&quot;evenodd&quot;%3E%3Cg fill=&quot;%23ffffff&quot; fill-opacity=&quot;0.1&quot;%3E%3Ccircle cx=&quot;30&quot; cy=&quot;30&quot; r=&quot;2&quot;/%3E%3C/g%3E%3C/g%3E%3C/svg%3E&apos;)] opacity-20"></div>
        
        {/* Content */}
        <div className="relative z-10 text-white">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="max-w-md"
          >
            <h1 className="text-4xl font-bold mb-4">
              JAC Learning Platform
            </h1>
            <p className="text-xl text-primary-100 mb-8">
              Master AI-first programming with JAC (Jaseci Architecture Code)
            </p>
            
            <div className="space-y-4">
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 bg-white/20 rounded-lg flex items-center justify-center">
                  <span className="text-sm font-semibold">1</span>
                </div>
                <span className="text-primary-100">Interactive learning paths</span>
              </div>
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 bg-white/20 rounded-lg flex items-center justify-center">
                  <span className="text-sm font-semibold">2</span>
                </div>
                <span className="text-primary-100">Real-time code execution</span>
              </div>
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 bg-white/20 rounded-lg flex items-center justify-center">
                  <span className="text-sm font-semibold">3</span>
                </div>
                <span className="text-primary-100">AI-powered assessments</span>
              </div>
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 bg-white/20 rounded-lg flex items-center justify-center">
                  <span className="text-sm font-semibold">4</span>
                </div>
                <span className="text-primary-100">Multi-agent collaboration</span>
              </div>
            </div>
          </motion.div>
        </div>

        {/* Floating code elements */}
        <div className="absolute top-1/4 right-1/4 w-32 h-32 bg-white/10 rounded-full blur-xl"></div>
        <div className="absolute bottom-1/4 left-1/4 w-48 h-48 bg-secondary-500/20 rounded-full blur-xl"></div>
      </div>

      {/* Right side - Auth form */}
      <div className="flex flex-1 flex-col justify-center px-6 py-12 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="w-full max-w-md mx-auto"
        >
          {/* Logo for mobile */}
          <div className="lg:hidden mb-8">
            <h1 className="text-2xl font-bold text-center text-gray-900">
              JAC Learning Platform
            </h1>
            <p className="text-center text-gray-600 mt-2">
              Master AI-first programming
            </p>
          </div>

          {/* Auth form container */}
          <div className="bg-white rounded-2xl shadow-lg p-8 border border-gray-100">
            {children}
          </div>

          {/* Footer */}
          <div className="mt-8 text-center">
            <p className="text-sm text-gray-500">
              Powered by{' '}
              <span className="font-semibold text-primary-600">Jaseci</span>
              {' '}and{' '}
              <span className="font-semibold text-secondary-600">AI Agents</span>
            </p>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default AuthLayout;