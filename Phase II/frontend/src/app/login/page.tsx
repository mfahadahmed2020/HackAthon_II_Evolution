/**
 * Login page
 * User authentication page with email and password form
 */

'use client';

import React from 'react';
import { useRouter } from 'next/navigation';
import { LoginForm } from '../../components/auth/login-form';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';

export default function LoginPage() {
  const router = useRouter();

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800 px-4 py-12">
      <Card className="w-full max-w-md shadow-2xl">
        <CardHeader className="space-y-1">
          <CardTitle className="text-2xl font-bold text-center">Welcome back</CardTitle>
          <CardDescription className="text-center">
            Sign in to your account to continue
          </CardDescription>
        </CardHeader>
        <CardContent>
          <LoginForm 
            onSignupClick={() => router.push('/signup')}
          />
        </CardContent>
      </Card>
    </div>
  );
}
