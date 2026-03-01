import React, { useEffect, useState } from 'react';
import { CheckCircle2, Loader2, MailWarning } from 'lucide-react';
import { apiFetch, apiUrl } from '../lib/apiConfig';

interface EmailVerificationProps {
  token: string;
  onContinue: () => void;
}

export default function EmailVerification({ token, onContinue }: EmailVerificationProps) {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [message, setMessage] = useState('');

  useEffect(() => {
    const verifyEmail = async () => {
      try {
        const res = await apiFetch(apiUrl(`/auth/verify/${token}`));
        const data = await res.json();

        if (!res.ok) {
          throw new Error(data.error || 'Unable to verify email.');
        }

        setMessage(data.message || 'Your email has been verified. You can now sign in.');
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unable to verify email.');
      } finally {
        setLoading(false);
      }
    };

    verifyEmail();
  }, [token]);

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center px-4">
      <div className="w-full max-w-md rounded-2xl bg-white p-8 shadow-xl">
        <div className="mb-6 flex justify-center">
          <div className={`flex h-14 w-14 items-center justify-center rounded-full ${error ? 'bg-red-100' : 'bg-green-100'}`}>
            {loading ? (
              <Loader2 className="h-7 w-7 animate-spin text-blue-600" />
            ) : error ? (
              <MailWarning className="h-7 w-7 text-red-600" />
            ) : (
              <CheckCircle2 className="h-7 w-7 text-green-600" />
            )}
          </div>
        </div>
        <h1 className="text-center text-2xl font-bold text-gray-900">
          {loading ? 'Verifying email' : error ? 'Verification failed' : 'Email verified'}
        </h1>
        <p className="mt-4 text-center text-sm text-gray-600">
          {loading ? 'Please wait while we verify your email address.' : error || message}
        </p>
        {!loading && (
          <button
            onClick={onContinue}
            className="mt-8 w-full rounded-xl bg-blue-600 px-4 py-3 text-sm font-semibold text-white transition-colors hover:bg-blue-700"
          >
            Go to sign in
          </button>
        )}
      </div>
    </div>
  );
}
