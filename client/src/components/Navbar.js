import React from 'react';
import { useAuth } from '../contexts/AuthContext';

const Navbar = () => {
  const { user } = useAuth();

  return (
    <nav className="bg-white shadow-sm border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <div className="flex-shrink-0 flex items-center">
              <svg className="h-8 w-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
              <span className="ml-2 text-xl font-semibold text-gray-900">
                Google Login App
              </span>
            </div>
          </div>
          
          <div className="flex items-center">
            {user ? (
              <div className="flex items-center space-x-4">
                <div className="flex items-center space-x-2">
                  {user.picture && (
                    <img
                      src={user.picture}
                      alt="Profile"
                      className="h-8 w-8 rounded-full"
                    />
                  )}
                  <span className="text-sm font-medium text-gray-700">
                    {user.name}
                  </span>
                </div>
              </div>
            ) : (
              <div className="text-sm text-gray-500">
                Not signed in
              </div>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar; 