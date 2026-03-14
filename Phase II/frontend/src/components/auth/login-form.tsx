/**
 * Login form component
 * Allows users to authenticate with email and password
 */

'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { loginUser } from '../lib/api';
import { validateEmail } from '../lib/auth';

/**
 * Form state
 */
interface FormData {
  email: string;
  password: string;
}

/**
 * Validation errors
 */
interface FormErrors {
  email?: string;
  password?: string;
  general?: string;
}

/**
 * LoginForm props
 */
export interface LoginFormProps {
  onSuccess?: () => void;
  onSignupClick?: () => void;
}

/**
 * LoginForm component
 */
export function LoginForm({ onSuccess, onSignupClick }: LoginFormProps) {
  const router = useRouter();
  const [formData, setFormData] = useState<FormData>({
    email: '',
    password: '',
  });
  const [errors, setErrors] = useState<FormErrors>({});
  const [isLoading, setIsLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);

  // Validate email field
  const validateEmailField = (email: string): string | undefined => {
    const result = validateEmail(email);
    return result.valid ? undefined : result.error;
  };

  // Handle email change
  const handleEmailChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const email = e.target.value;
    setFormData(prev => ({ ...prev, email }));
    
    const error = validateEmailField(email);
    setErrors(prev => ({ ...prev, email: error }));
  };

  // Handle password change
  const handlePasswordChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const password = e.target.value;
    setFormData(prev => ({ ...prev, password }));
    
    // Clear password error on change
    setErrors(prev => ({ ...prev, password: undefined }));
  };

  // Handle form submission
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrors({});
    
    // Validate fields
    const emailError = validateEmailField(formData.email);
    
    if (emailError) {
      setErrors(prev => ({ ...prev, email: emailError }));
      return;
    }
    
    setIsLoading(true);
    
    try {
      // Login
      await loginUser({
        email: formData.email,
        password: formData.password,
      });
      
      // Success - redirect to dashboard or call onSuccess
      if (onSuccess) {
        onSuccess();
      } else {
        router.push('/dashboard');
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Login failed';
      setErrors(prev => ({ ...prev, general: errorMessage }));
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {/* General error */}
      {errors.general && (
        <div className="p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
          {errors.general}
        </div>
      )}

      {/* Email field */}
      <div>
        <label htmlFor="email" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Email address
        </label>
        <input
          id="email"
          type="email"
          value={formData.email}
          onChange={handleEmailChange}
          disabled={isLoading}
          placeholder="you@example.com"
          className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent dark:bg-gray-800 dark:text-white dark:border-gray-700 ${
            errors.email ? 'border-red-500' : 'border-gray-300'
          }`}
          aria-invalid={!!errors.email}
          aria-describedby={errors.email ? 'email-error' : undefined}
        />
        {errors.email && (
          <p id="email-error" className="mt-1 text-sm text-red-600">
            {errors.email}
          </p>
        )}
      </div>

      {/* Password field */}
      <div>
        <label htmlFor="password" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Password
        </label>
        <div className="relative">
          <input
            id="password"
            type={showPassword ? 'text' : 'password'}
            value={formData.password}
            onChange={handlePasswordChange}
            disabled={isLoading}
            placeholder="••••••••"
            className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent dark:bg-gray-800 dark:text-white dark:border-gray-700 ${
              errors.password ? 'border-red-500' : 'border-gray-300'
            }`}
            aria-invalid={!!errors.password}
            aria-describedby={errors.password ? 'password-error' : undefined}
          />
          <button
            type="button"
            onClick={() => setShowPassword(!showPassword)}
            className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-700 dark:text-gray-400"
            aria-label={showPassword ? 'Hide password' : 'Show password'}
          >
            {showPassword ? (
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
              </svg>
            ) : (
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
              </svg>
            )}
          </button>
        </div>
        {errors.password && (
          <p id="password-error" className="mt-1 text-sm text-red-600">
            {errors.password}
          </p>
        )}
        <p className="mt-2 text-xs text-gray-500 dark:text-gray-400">
          Enter your password to sign in
        </p>
      </div>

      {/* Submit button */}
      <button
        type="submit"
        disabled={isLoading}
        className="w-full py-2 px-4 bg-teal-600 hover:bg-teal-700 text-white font-medium rounded-lg transition-colors focus:outline-none focus:ring-2 focus:ring-teal-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {isLoading ? (
          <span className="flex items-center justify-center">
            <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
            </svg>
            Signing in...
          </span>
        ) : (
          'Sign in'
        )}
      </button>

      {/* Signup link */}
      <p className="text-center text-sm text-gray-600 dark:text-gray-400">
        Don&apos;t have an account?{' '}
        <button
          type="button"
          onClick={onSignupClick || (() => router.push('/signup'))}
          className="text-teal-600 hover:text-teal-700 font-medium"
        >
          Sign up
        </button>
      </p>
    </form>
  );
}

export default LoginForm;
