/**
 * Authentication Hook
 *
 * Provides authentication context and methods throughout the app
 * Implements JWT token management as specified in PROJECT_BRIEF.md
 */

import { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { authService, User } from '../services/auth.service';
import { logger } from '../utils/logger';

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, name: string) => Promise<void>;
  logout: () => void;
  refreshUser: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

interface AuthProviderProps {
  children: ReactNode;
}

/**
 * Authentication Provider Component
 * Wraps the application to provide auth context
 */
export function AuthProvider({ children }: AuthProviderProps) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  // Check for existing session on mount
  useEffect(() => {
    checkExistingSession();
  }, []);

  /**
   * Check if user has valid token in localStorage
   */
  const checkExistingSession = async () => {
    try {
      const token = localStorage.getItem('auth_token');
      if (token) {
        const userData = await authService.verifyToken(token);
        setUser(userData);
        logger.info('Session restored from token');
      }
    } catch (error) {
      // Invalid token, clear it
      localStorage.removeItem('auth_token');
      logger.warn('Invalid stored token, cleared');
    } finally {
      setIsLoading(false);
    }
  };

  /**
   * Login user with email and password
   */
  const login = async (email: string, password: string) => {
    try {
      const { user: userData, token } = await authService.login(email, password);

      // Store token
      localStorage.setItem('auth_token', token);

      // Update state
      setUser(userData);

      logger.info(`User logged in: ${email}`);
    } catch (error) {
      logger.error('Login failed:', error);
      throw error;
    }
  };

  /**
   * Register new user
   */
  const register = async (email: string, password: string, name: string) => {
    try {
      const { user: userData, token } = await authService.register(email, password, name);

      // Store token
      localStorage.setItem('auth_token', token);

      // Update state
      setUser(userData);

      logger.info(`User registered: ${email}`);
    } catch (error) {
      logger.error('Registration failed:', error);
      throw error;
    }
  };

  /**
   * Logout user
   */
  const logout = () => {
    // Clear token
    localStorage.removeItem('auth_token');

    // Clear user state
    setUser(null);

    logger.info('User logged out');
  };

  /**
   * Refresh user data
   */
  const refreshUser = async () => {
    try {
      const token = localStorage.getItem('auth_token');
      if (token) {
        const userData = await authService.verifyToken(token);
        setUser(userData);
      }
    } catch (error) {
      logger.error('Failed to refresh user:', error);
      logout();
    }
  };

  const value: AuthContextType = {
    user,
    isAuthenticated: !!user,
    isLoading,
    login,
    register,
    logout,
    refreshUser
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

/**
 * Hook to access auth context
 * Must be used within AuthProvider
 */
export function useAuth(): AuthContextType {
  const context = useContext(AuthContext);

  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }

  return context;
}

/**
 * Hook to require authentication
 * Redirects to login if not authenticated
 */
export function useRequireAuth() {
  const { isAuthenticated, isLoading } = useAuth();

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      // Redirect to login
      window.location.href = '/login';
    }
  }, [isAuthenticated, isLoading]);

  return { isAuthenticated, isLoading };
}
