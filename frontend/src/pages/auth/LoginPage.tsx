import React, { useState, useEffect } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { motion } from 'framer-motion';
import { useForm } from 'react-hook-form';
import { EyeIcon, EyeSlashIcon } from '@heroicons/react/24/outline';
import { useDispatch, useSelector } from 'react-redux';
import { RootState } from '../../store/store';
import { loginUser } from '../../store/slices/authSlice';
import { toast } from 'react-hot-toast';

interface LoginFormData {
  email: string;
  password: string;
  rememberMe: boolean;
}

export const LoginPage: React.FC = () => {
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const location = useLocation();
  const { isAuthenticated } = useSelector((state: RootState) => state.auth);
  
  // Show message from registration redirect
  useEffect(() => {
    const message = location.state?.message;
    if (message) {
      toast.success(message);
      // Clear the message by updating the state
      window.history.replaceState({}, document.title, location.pathname);
    }
  }, [location]);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginFormData>();

  const onSubmit = async (data: LoginFormData) => {
    setIsLoading(true);

    try {
      // Mock authentication - in real app, this would call your auth service
      await new Promise(resolve => setTimeout(resolve, 1000));

      // Simulate successful login
      // TODO: Remove mock data when backend integration is ready
      // eslint-disable-next-line @typescript-eslint/no-unused-vars
      const mockUser = {
        id: 1,
        email: data.email,
        name: 'John Doe',
        avatar: null,
        role: 'student' as const,
        preferences: {
          theme: 'light',
          notifications: true,
          language: 'en',
        },
      };

      // Mock token
      const mockToken = 'mock-jwt-token-' + Date.now();

      // Store token in localStorage
      localStorage.setItem('token', mockToken);

      // Update Redux state
      (dispatch as any)(loginUser({ username: data.email, password: data.password }));

      toast.success('Welcome back! You have been logged in successfully.');
      
      // Redirect to dashboard after successful login
      navigate('/dashboard', { replace: true });

    } catch (error) {
      console.error('Login error:', error);
      toast.error('Invalid email or password. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  if (isAuthenticated) {
    return null; // Will be redirected by the route protection
  }

  return (
    <div className="w-full max-w-md">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        <div className="text-center mb-8">
          <h2 className="text-3xl font-bold text-gray-900">Welcome back</h2>
          <p className="text-gray-600 mt-2">
            Sign in to your JAC Learning Platform account
          </p>
        </div>

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
          {/* Email Field */}
          <div>
            <label htmlFor="email" className="block text-sm font-medium text-gray-800 mb-1">
              Email address
            </label>
            <input
              {...register('email', {
                required: 'Email is required',
                pattern: {
                  value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                  message: 'Invalid email address',
                },
              })}
              type="email"
              id="email"
              autoComplete="email"
              className={`w-full px-3 py-2 border rounded-md shadow-sm placeholder-gray-500 focus:outline-none focus:ring-primary-500 focus:border-primary-500 ${
                errors.email ? 'border-red-300' : 'border-gray-300'
              }`}
              placeholder="Enter your email"
            />
            {errors.email && (
              <p className="mt-1 text-sm text-red-600">{errors.email.message}</p>
            )}
          </div>

          {/* Password Field */}
          <div>
            <label htmlFor="password" className="block text-sm font-medium text-gray-800 mb-1">
              Password
            </label>
            <div className="relative">
              <input
                {...register('password', {
                  required: 'Password is required',
                  minLength: {
                    value: 6,
                    message: 'Password must be at least 6 characters',
                  },
                })}
                type={showPassword ? 'text' : 'password'}
                id="password"
                autoComplete="current-password"
                className={`w-full px-3 py-2 pr-10 border rounded-md shadow-sm placeholder-gray-500 focus:outline-none focus:ring-primary-500 focus:border-primary-500 ${
                  errors.password ? 'border-red-300' : 'border-gray-300'
                }`}
                placeholder="Enter your password"
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400 hover:text-gray-600"
              >
                {showPassword ? (
                  <EyeSlashIcon className="h-5 w-5" />
                ) : (
                  <EyeIcon className="h-5 w-5" />
                )}
              </button>
            </div>
            {errors.password && (
              <p className="mt-1 text-sm text-red-600">{errors.password.message}</p>
            )}
          </div>

          {/* Remember Me & Forgot Password */}
          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <input
                {...register('rememberMe')}
                id="rememberMe"
                type="checkbox"
                className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
              />
              <label htmlFor="rememberMe" className="ml-2 block text-sm text-gray-800 font-medium">
                Remember me
              </label>
            </div>
            <Link
              to="/forgot-password"
              className="text-sm text-primary-700 hover:text-primary-800 font-semibold"
            >
              Forgot password?
            </Link>
          </div>

          {/* Submit Button */}
          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            type="submit"
            disabled={isLoading}
            className={`w-full flex justify-center py-3 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white transition-colors ${
              isLoading
                ? 'bg-gray-400 cursor-not-allowed'
                : 'bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500'
            }`}
          >
            {isLoading ? (
              <div className="flex items-center">
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2" />
                Signing in...
              </div>
            ) : (
              'Sign in'
            )}
          </motion.button>

          {/* Demo Credentials */}
          <div className="bg-gray-100 border border-gray-400 rounded-lg p-4">
            <h4 className="text-sm font-medium text-gray-800 mb-2">Demo Credentials</h4>
            <p className="text-xs text-gray-700 mb-1">
              <strong>Email:</strong> demo@example.com
            </p>
            <p className="text-xs text-gray-700">
              <strong>Password:</strong> demo123
            </p>
          </div>

          {/* Sign Up Link */}
          <div className="text-center">
            <p className="text-sm text-gray-700">
              Don't have an account?{' '}
              <Link
                to="/register"
                className="text-primary-700 hover:text-primary-800 font-semibold"
              >
                Sign up for free
              </Link>
            </p>
          </div>
        </form>
      </motion.div>
    </div>
  );
};

export default LoginPage;