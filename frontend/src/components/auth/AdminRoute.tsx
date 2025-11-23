/**
 * AdminRoute Component
 * Protects admin-only routes by checking user privileges
 */

import React from 'react';
import { Navigate } from 'react-router-dom';
import { useSelector } from 'react-redux';
import { RootState } from '../../store/store';
import { XCircleIcon } from '@heroicons/react/24/outline';
import { useSelector as useReduxSelector } from 'react-redux';

interface AdminRouteProps {
  children: React.ReactNode;
}

const AdminRoute: React.FC<AdminRouteProps> = ({ children }) => {
  const { user, isAuthenticated } = useSelector((state: RootState) => state.auth);

  // Check if user is authenticated
  if (!isAuthenticated || !user) {
    return <Navigate to="/login" replace />;
  }

  // Check if user has admin privileges
  if (!user.is_staff) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-red-50 to-red-100 flex items-center justify-center">
        <div className="bg-white rounded-lg shadow-lg p-8 max-w-md text-center">
          <XCircleIcon className="h-16 w-16 text-red-500 mx-auto mb-4" />
          <h2 className="text-xl font-bold text-gray-900 mb-2">Access Denied</h2>
          <p className="text-gray-600 mb-4">
            You need administrator privileges to access this page.
          </p>
          <div className="bg-gray-50 rounded-md p-4 text-left">
            <h3 className="text-sm font-medium text-gray-900 mb-2">Admin Features Available:</h3>
            <ul className="text-sm text-gray-600 space-y-1">
              <li>• User management and analytics</li>
              <li>• Content creation and management</li>
              <li>• Learning path administration</li>
              <li>• System-wide statistics</li>
            </ul>
          </div>
          <button
            onClick={() => window.history.back()}
            className="mt-4 bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded-lg text-sm"
          >
            Go Back
          </button>
        </div>
      </div>
    );
  }

  return <>{children}</>;
};

export default AdminRoute;