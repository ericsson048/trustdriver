import React, { useEffect, useState } from 'react';
import { Download, File, AlertCircle } from 'lucide-react';
import { FileNode } from '../types';
import { format } from 'date-fns';

interface SharedFileViewProps {
  token: string;
}

export default function SharedFileView({ token }: SharedFileViewProps) {
  const [file, setFile] = useState<FileNode | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchSharedFile = async () => {
      try {
        const res = await fetch(`/api/shared/${token}`);
        if (!res.ok) {
          throw new Error('File not found or link expired');
        }
        const data = await res.json();
        setFile(data);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchSharedFile();
  }, [token]);

  const handleDownload = () => {
    window.location.href = `/api/shared/${token}/download`;
  };

  const formatSize = (bytes?: number) => {
    if (bytes === undefined) return '-';
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (error || !file) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
        <div className="bg-white rounded-2xl shadow-xl p-8 max-w-md w-full text-center">
          <div className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <AlertCircle className="w-8 h-8 text-red-600" />
          </div>
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Access Denied</h2>
          <p className="text-gray-600">{error || 'This link may be invalid or expired.'}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl shadow-xl max-w-lg w-full overflow-hidden">
        <div className="bg-blue-600 p-8 text-center">
          <div className="w-20 h-20 bg-white/20 rounded-2xl flex items-center justify-center mx-auto backdrop-blur-sm">
            <File className="w-10 h-10 text-white" />
          </div>
          <h1 className="text-white text-xl font-semibold mt-4 truncate px-4">
            {file.name}
          </h1>
          <p className="text-blue-100 mt-2 text-sm">Shared with you</p>
        </div>
        
        <div className="p-8">
          <div className="space-y-4 mb-8">
            <div className="flex justify-between py-3 border-b border-gray-100">
              <span className="text-gray-500">Type</span>
              <span className="font-medium text-gray-900 uppercase">{file.mime_type?.split('/')[1] || 'File'}</span>
            </div>
            <div className="flex justify-between py-3 border-b border-gray-100">
              <span className="text-gray-500">Size</span>
              <span className="font-medium text-gray-900">{formatSize(file.size)}</span>
            </div>
            <div className="flex justify-between py-3 border-b border-gray-100">
              <span className="text-gray-500">Created</span>
              <span className="font-medium text-gray-900">{format(new Date(file.created_at), 'PPP')}</span>
            </div>
          </div>

          <button
            onClick={handleDownload}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-4 px-6 rounded-xl flex items-center justify-center space-x-2 transition-colors shadow-lg shadow-blue-600/20"
          >
            <Download className="w-5 h-5" />
            <span>Download File</span>
          </button>
        </div>
      </div>
    </div>
  );
}
