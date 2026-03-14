'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { isAuthenticated } from '@/lib/api';

export default function HomePage() {
  const router = useRouter();

  useEffect(() => {
    // Redirect based on authentication status
    if (isAuthenticated()) {
      router.push('/dashboard');
    } else {
      router.push('/login');
    }
  }, [router]);

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <div className="text-center">
        <h1 className="text-4xl font-bold mb-4">Phase 2 Todo App</h1>
        <p className="text-lg text-gray-600">Redirecting...</p>
      </div>
    </main>
  );
}
