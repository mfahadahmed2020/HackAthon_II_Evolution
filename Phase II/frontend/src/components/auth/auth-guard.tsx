/**
 * Auth Guard component
 * Protects routes requiring authentication
 * Redirects unauthenticated users to login page
 */

'use client';

import React, { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { getToken, getUser } from '../../lib/auth';

/**
 * AuthGuard props
 */
export interface AuthGuardProps {
  children: React.ReactNode;
  redirectTo?: string;
  loadingComponent?: React.ReactNode;
}

/**
 * AuthGuard component
 * 
 * Usage:
 * ```tsx
 * // In a page component
 * export default function DashboardPage() {
 *   return (
 *     <AuthGuard>
 *       <DashboardContent />
 *     </AuthGuard>
 *   );
 * }
 * ```
 */
export function AuthGuard({
  children,
  redirectTo = '/login',
  loadingComponent,
}: AuthGuardProps) {
  const router = useRouter();
  const [isChecking, setIsChecking] = React.useState(true);
  const [isAuthenticated, setIsAuthenticated] = React.useState(false);

  useEffect(() => {
    // Check authentication status
    const checkAuth = () => {
      const token = getToken();
      const user = getUser();
      
      if (!token || !user) {
        // Not authenticated - redirect to login
        router.push(`${redirectTo}?from=${encodeURIComponent(window.location.pathname)}`);
        setIsAuthenticated(false);
      } else {
        // Authenticated
        setIsAuthenticated(true);
      }
      
      setIsChecking(false);
    };

    checkAuth();
  }, [router, redirectTo]);

  // Show loading state while checking
  if (isChecking) {
    if (loadingComponent) {
      return <>{loadingComponent}</>;
    }
    
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-teal-500 mx-auto mb-4"></div>
          <p className="text-gray-600 dark:text-gray-400">Checking authentication...</p>
        </div>
      </div>
    );
  }

  // Not authenticated - don't render children (redirect is happening)
  if (!isAuthenticated) {
    return null;
  }

  // Authenticated - render children
  return <>{children}</>;
}

/**
 * Higher-order component for protecting pages
 * 
 * Usage:
 * ```tsx
 * const ProtectedDashboard = withAuthGuard(DashboardPage);
 * export default ProtectedDashboard;
 * ```
 */
export function withAuthGuard<P extends object>(
  WrappedComponent: React.ComponentType<P>,
  redirectTo?: string
) {
  return function AuthGuardedComponent(props: P) {
    return (
      <AuthGuard redirectTo={redirectTo}>
        <WrappedComponent {...props} />
      </AuthGuard>
    );
  };
}

export default AuthGuard;
