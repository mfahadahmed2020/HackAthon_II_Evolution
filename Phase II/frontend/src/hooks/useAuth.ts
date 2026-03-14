/**
 * useAuth hook
 * Provides authentication state and actions to components
 */

'use client';

import { useState, useEffect, useCallback } from 'react';
import { useRouter, usePathname } from 'next/navigation';
import { loginUser, registerUser, getCurrentUser, authClient } from './api';
import {
  storeSession,
  getToken,
  getUser,
  clearSession,
  isAuthenticated,
  handleTokenExpiration,
  SessionUser,
} from './auth';

/**
 * Authentication state
 */
interface AuthState {
  user: SessionUser | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  error: string | null;
}

/**
 * Authentication actions
 */
interface AuthActions {
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string) => Promise<void>;
  logout: () => void;
  clearError: () => void;
}

/**
 * useAuth hook return type
 */
interface UseAuthReturn extends AuthState, AuthActions {}

/**
 * useAuth hook
 * Provides authentication state and actions
 * 
 * @example
 * ```tsx
 * function MyComponent() {
 *   const { user, isLoading, login, logout } = useAuth();
 *   
 *   if (isLoading) return <div>Loading...</div>;
 *   if (!user) return <LoginForm />;
 *   
 *   return <div>Welcome {user.email} <button onClick={logout}>Logout</button></div>;
 * }
 * ```
 */
export function useAuth(): UseAuthReturn {
  const [user, setUser] = useState<SessionUser | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();
  const pathname = usePathname();

  // Initialize auth state on mount
  useEffect(() => {
    const initAuthState = () => {
      const token = getToken();
      const storedUser = getUser();
      
      if (token && storedUser) {
        setUser(storedUser);
        authClient.setToken(token);
      }
      
      setIsLoading(false);
    };
    
    initAuthState();
  }, []);

  // Login function
  const login = useCallback(async (email: string, password: string) => {
    setIsLoading(true);
    setError(null);
    
    try {
      const response = await loginUser({ email, password });
      
      // Store session
      storeSession(
        response.access_token,
        response.user,
        response.expires_in
      );
      
      // Update state
      setUser(response.user);
      
      // Redirect to dashboard
      router.push('/dashboard');
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Login failed';
      setError(errorMessage);
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, [router]);

  // Register function
  const register = useCallback(async (email: string, password: string) => {
    setIsLoading(true);
    setError(null);
    
    try {
      const user = await registerUser({ email, password });
      
      // Auto-login after registration
      await login(email, password);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Registration failed';
      setError(errorMessage);
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, [login]);

  // Logout function
  const logout = useCallback(() => {
    clearSession();
    setUser(null);
    router.push('/login?loggedout=true');
  }, [router]);

  // Clear error
  const clearError = useCallback(() => {
    setError(null);
  }, []);

  return {
    user,
    isLoading,
    isAuthenticated: !!user,
    error,
    login,
    register,
    logout,
    clearError,
  };
}

/**
 * AuthGuard component
 * Protects routes requiring authentication
 */
export interface AuthGuardProps {
  children: React.ReactNode;
  redirectTo?: string;
}

export function AuthGuard({ children, redirectTo = '/login' }: AuthGuardProps) {
  const { user, isLoading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isLoading && !user) {
      router.push(redirectTo);
    }
  }, [user, isLoading, router, redirectTo]);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-teal-500"></div>
      </div>
    );
  }

  if (!user) {
    return null;
  }

  return <>{children}</>;
}

export default useAuth;
