/**
 * Signup page
 * User registration page with email and password form
 */

'use client';

import React from 'react';
import { useRouter } from 'next/navigation';
import { SignupForm } from '../../components/auth/signup-form';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';

export default function SignupPage() {
  const router = useRouter();

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800 px-4 py-12">
      <Card className="w-full max-w-md shadow-2xl">
        <CardHeader className="space-y-1">
          <CardTitle className="text-2xl font-bold text-center">Create an account</CardTitle>
          <CardDescription className="text-center">
            Enter your email and password to create an account
          </CardDescription>
        </CardHeader>
        <CardContent>
          <SignupForm 
            onLoginClick={() => router.push('/login')}
          />
        </CardContent>
      </Card>
    </div>
  );
}
