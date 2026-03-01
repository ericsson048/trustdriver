import React, { useEffect, useState } from 'react';
import { HardDrive, Mail, Lock, Loader2, ArrowLeft } from 'lucide-react';
import { apiFetch, apiUrl } from '../lib/apiConfig';

interface AuthProps {
  mode: 'login' | 'register';
  onSuccess: (user: any) => void;
  onSwitchMode: () => void;
  onBack: () => void;
}

export default function Auth({ mode, onSuccess, onSwitchMode, onBack }: AuthProps) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [info, setInfo] = useState<string | null>(null);
  const [verificationEmail, setVerificationEmail] = useState<string | null>(null);
  const [resending, setResending] = useState(false);

  useEffect(() => {
    setError(null);
    setInfo(null);
    setVerificationEmail(null);
  }, [mode]);

  const resendVerification = async (targetEmail: string) => {
    setResending(true);
    setError(null);
    setInfo(null);

    try {
      const res = await apiFetch(apiUrl('/auth/resend-verification'), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: targetEmail }),
      });
      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.error || 'Unable to resend verification email');
      }

      setInfo(data.message || 'A new verification email has been sent.');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unable to resend verification email');
    } finally {
      setResending(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setInfo(null);
    setVerificationEmail(null);

    try {
      const endpoint = mode === 'login' ? apiUrl('/auth/login') : apiUrl('/auth/register');
      const res = await apiFetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });

      const data = await res.json();

      if (!res.ok) {
        if (data.requiresEmailVerification && data.email) {
          setVerificationEmail(data.email);
        }
        throw new Error(data.error || 'Authentication failed');
      }

      if (data.requiresEmailVerification) {
        setVerificationEmail(data.email || email);
        setInfo(data.message || 'Check your email to verify your account.');
        if (mode === 'register') {
          setPassword('');
        }
        return;
      }

      onSuccess(data.user);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Authentication failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <div className="flex justify-center mb-6">
          <div className="w-12 h-12 bg-blue-600 rounded-xl flex items-center justify-center">
            <HardDrive className="text-white w-7 h-7" />
          </div>
        </div>
        <h2 className="mt-2 text-center text-3xl font-bold tracking-tight text-gray-900">
          {mode === 'login' ? 'Sign in to your account' : 'Create your account'}
        </h2>
        <p className="mt-2 text-center text-sm text-gray-600">
          Or{' '}
          <button onClick={onSwitchMode} className="font-medium text-blue-600 hover:text-blue-500">
            {mode === 'login' ? 'create a new account' : 'sign in to existing account'}
          </button>
        </p>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <div className="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10 relative">
          <button 
            onClick={onBack}
            className="absolute top-4 left-4 text-gray-400 hover:text-gray-600"
          >
            <ArrowLeft className="w-5 h-5" />
          </button>

          <form className="space-y-6" onSubmit={handleSubmit}>
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700">
                Email address
              </label>
              <div className="mt-1 relative rounded-md shadow-sm">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Mail className="h-5 w-5 text-gray-400" />
                </div>
                <input
                  id="email"
                  name="email"
                  type="email"
                  autoComplete="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                  placeholder="you@example.com"
                />
              </div>
            </div>

            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-700">
                Password
              </label>
              <div className="mt-1 relative rounded-md shadow-sm">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Lock className="h-5 w-5 text-gray-400" />
                </div>
                <input
                  id="password"
                  name="password"
                  type="password"
                  autoComplete="current-password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                  placeholder="••••••••"
                />
              </div>
            </div>

            {error && (
              <div className="rounded-md bg-red-50 p-4">
                <div className="flex">
                  <div className="ml-3">
                    <h3 className="text-sm font-medium text-red-800">{error}</h3>
                  </div>
                </div>
              </div>
            )}

            {info && (
              <div className="rounded-md bg-green-50 p-4">
                <div className="flex">
                  <div className="ml-3">
                    <h3 className="text-sm font-medium text-green-800">{info}</h3>
                  </div>
                </div>
              </div>
            )}

            {verificationEmail && (
              <div className="rounded-md border border-blue-100 bg-blue-50 p-4 text-sm text-blue-900">
                <p className="font-medium">Verification pending for {verificationEmail}</p>
                <p className="mt-1">Open the email we sent you, then come back here to sign in.</p>
                <button
                  type="button"
                  onClick={() => resendVerification(verificationEmail)}
                  disabled={resending}
                  className="mt-3 text-sm font-semibold text-blue-700 hover:text-blue-800 disabled:opacity-50"
                >
                  {resending ? 'Sending...' : 'Resend verification email'}
                </button>
              </div>
            )}

            <div>
              <button
                type="submit"
                disabled={loading}
                className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? (
                  <Loader2 className="w-5 h-5 animate-spin" />
                ) : (
                  mode === 'login' ? 'Sign in' : 'Create account'
                )}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}
