/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useEffect, useState } from 'react';
import DriveInterface from './components/DriveInterface';
import SharedFileView from './components/SharedFileView';
import LandingPage from './components/LandingPage';
import Auth from './components/Auth';
import { apiUrl } from './lib/apiConfig';

export default function App() {
  const [path, setPath] = useState(window.location.pathname);
  const [user, setUser] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [authMode, setAuthMode] = useState<'login' | 'register'>('login');
  const [showAuth, setShowAuth] = useState(false);

  useEffect(() => {
    const checkAuth = async () => {
      try {
        const res = await fetch(apiUrl('/auth/me'));
        if (res.ok) {
          const data = await res.json();
          setUser(data.user);
        }
      } catch (error) {
        console.error('Auth check failed', error);
      } finally {
        setLoading(false);
      }
    };
    checkAuth();

    const handlePopState = () => setPath(window.location.pathname);
    window.addEventListener('popstate', handlePopState);
    return () => window.removeEventListener('popstate', handlePopState);
  }, []);

  // Simple router for shared links (public access)
  if (path.startsWith('/shared/')) {
    const token = path.split('/shared/')[1];
    if (token) {
      return <SharedFileView token={token} />;
    }
  }

  if (loading) {
    return <div className="min-h-screen flex items-center justify-center bg-white">
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
    </div>;
  }

  if (user) {
    return <DriveInterface onLogout={async () => {
      await fetch(apiUrl('/auth/logout'), { method: 'POST' });
      setUser(null);
    }} />;
  }

  if (showAuth) {
    return (
      <Auth 
        mode={authMode} 
        onSuccess={(user) => {
          setUser(user);
          setShowAuth(false);
        }}
        onSwitchMode={() => setAuthMode(authMode === 'login' ? 'register' : 'login')}
        onBack={() => setShowAuth(false)}
      />
    );
  }

  return (
    <LandingPage 
      onGetStarted={() => {
        setAuthMode('register');
        setShowAuth(true);
      }}
      onLogin={() => {
        setAuthMode('login');
        setShowAuth(true);
      }}
    />
  );
}

