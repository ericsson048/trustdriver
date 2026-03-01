import { Folder, File, MoreVertical, Download, Trash2, FolderPlus, FileUp, ChevronRight, Home, Share2, X, Copy, Check } from 'lucide-react';
import React, { useState, useEffect, useRef } from 'react';
import { FileNode, Breadcrumb } from '../types';
import { format } from 'date-fns';
import { apiFetch, apiUrl, sharedFileUrl } from '../lib/apiConfig';
import { cn } from '../lib/utils';

interface DriveInterfaceProps {
  onLogout: () => void;
  onSessionExpired: () => void;
}

export default function DriveInterface({ onLogout, onSessionExpired }: DriveInterfaceProps) {
  const [currentFolderId, setCurrentFolderId] = useState<string | null>(null);
  const [files, setFiles] = useState<FileNode[]>([]);
  const [breadcrumbs, setBreadcrumbs] = useState<Breadcrumb[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [showNewFolderDialog, setShowNewFolderDialog] = useState(false);
  const [newFolderName, setNewFolderName] = useState('');
  
  // Share Dialog State
  const [shareDialogFile, setShareDialogFile] = useState<FileNode | null>(null);
  const [shareLink, setShareLink] = useState<string | null>(null);
  const [isSharing, setIsSharing] = useState(false);
  const [copied, setCopied] = useState(false);

  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleUnauthorized = () => {
    setFiles([]);
    setBreadcrumbs([]);
    onSessionExpired();
  };

  const fetchFiles = async (folderId: string | null) => {
    setIsLoading(true);
    try {
      const url = folderId ? `${apiUrl('/files')}?parentId=${folderId}` : apiUrl('/files');
      const res = await apiFetch(url);
      if (res.status === 401) {
        handleUnauthorized();
        return;
      }

      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.error || 'Failed to fetch files');
      }

      setFiles(Array.isArray(data.files) ? data.files : []);
      setBreadcrumbs(Array.isArray(data.breadcrumbs) ? data.breadcrumbs : []);
    } catch (error) {
      console.error('Failed to fetch files', error);
      setFiles([]);
      setBreadcrumbs([]);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchFiles(currentFolderId);
  }, [currentFolderId]);

  const handleCreateFolder = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newFolderName.trim()) return;

    try {
      const res = await apiFetch(apiUrl('/folders'), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: newFolderName, parentId: currentFolderId }),
      });
      if (res.status === 401) {
        handleUnauthorized();
        return;
      }
      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.error || 'Failed to create folder');
      }
      setNewFolderName('');
      setShowNewFolderDialog(false);
      fetchFiles(currentFolderId);
    } catch (error) {
      console.error('Failed to create folder', error);
    }
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files || e.target.files.length === 0) return;
    
    const file = e.target.files[0];
    const formData = new FormData();
    formData.append('file', file);
    if (currentFolderId) {
      formData.append('parentId', currentFolderId);
    }

    setIsUploading(true);
    try {
      const res = await apiFetch(apiUrl('/upload'), {
        method: 'POST',
        body: formData,
      });
      if (res.status === 401) {
        handleUnauthorized();
        return;
      }
      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.error || 'Failed to upload file');
      }
      fetchFiles(currentFolderId);
    } catch (error) {
      console.error('Failed to upload file', error);
    } finally {
      setIsUploading(false);
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    }
  };

  const handleDelete = async (id: string, e: React.MouseEvent) => {
    e.stopPropagation();
    if (!confirm('Are you sure you want to delete this item?')) return;

    try {
      const res = await apiFetch(apiUrl(`/nodes/${id}`), { method: 'DELETE' });
      if (res.status === 401) {
        handleUnauthorized();
        return;
      }

      const data = await res.json();
      if (!res.ok) {
        alert(data.error || 'Failed to delete');
        return;
      }
      fetchFiles(currentFolderId);
    } catch (error) {
      console.error('Failed to delete', error);
    }
  };

  const handleDownload = (id: string, e: React.MouseEvent) => {
    e.stopPropagation();
    window.open(apiUrl(`/download/${id}`), '_blank');
  };

  const openShareDialog = async (file: FileNode, e: React.MouseEvent) => {
    e.stopPropagation();
    setShareDialogFile(file);
    setCopied(false);
    
    if (file.is_shared && file.share_token) {
      setShareLink(sharedFileUrl(file.share_token));
    } else {
      setShareLink(null);
    }
  };

  const toggleShare = async (enable: boolean) => {
    if (!shareDialogFile) return;
    setIsSharing(true);
    try {
      const res = await apiFetch(apiUrl(`/share/${shareDialogFile.id}`), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ enable }),
      });
      if (res.status === 401) {
        handleUnauthorized();
        return;
      }

      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.error || 'Failed to update sharing');
      }
      
      if (data.success) {
        if (data.shareToken) {
          setShareLink(sharedFileUrl(data.shareToken));
        } else {
          setShareLink(null);
        }
        // Update local state
        setFiles((currentFiles) =>
          currentFiles.map((file) =>
            file.id === shareDialogFile.id
              ? { ...file, is_shared: enable ? 1 : 0, share_token: data.shareToken }
              : file
          )
        );
        setShareDialogFile({ ...shareDialogFile, is_shared: enable ? 1 : 0, share_token: data.shareToken });
      }
    } catch (error) {
      console.error('Failed to toggle share', error);
    } finally {
      setIsSharing(false);
    }
  };

  const copyToClipboard = () => {
    if (shareLink) {
      navigator.clipboard.writeText(shareLink);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  const formatSize = (bytes?: number) => {
    if (bytes === undefined) return '-';
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  return (
    <div className="flex h-screen bg-gray-50 text-gray-900 font-sans">
      {/* Sidebar */}
      <aside className="w-64 bg-white border-r border-gray-200 flex-shrink-0 hidden md:flex flex-col">
        <div className="p-6 flex items-center space-x-2">
          <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
            <Folder className="text-white w-5 h-5" />
          </div>
          <span className="text-xl font-semibold text-gray-800">Trust Driver</span>
        </div>

        <div className="px-4 mb-6">
          <button 
            onClick={() => setShowNewFolderDialog(true)}
            className="w-full flex items-center justify-center space-x-2 bg-white border border-gray-300 shadow-sm hover:bg-gray-50 text-gray-700 py-3 px-4 rounded-full transition-colors"
          >
            <FolderPlus className="w-5 h-5" />
            <span className="font-medium">New Folder</span>
          </button>
          
          <div className="mt-3">
             <input 
              type="file" 
              ref={fileInputRef}
              onChange={handleFileUpload}
              className="hidden" 
              id="file-upload"
            />
            <label 
              htmlFor="file-upload"
              className={cn(
                "w-full flex items-center justify-center space-x-2 bg-blue-600 hover:bg-blue-700 text-white py-3 px-4 rounded-full cursor-pointer transition-colors shadow-md",
                isUploading && "opacity-70 cursor-not-allowed"
              )}
            >
              <FileUp className="w-5 h-5" />
              <span className="font-medium">{isUploading ? 'Uploading...' : 'File Upload'}</span>
            </label>
          </div>
        </div>

        <nav className="flex-1 px-2 space-y-1">
          <button 
            onClick={() => setCurrentFolderId(null)}
            className={cn(
              "w-full flex items-center space-x-3 px-4 py-2 rounded-r-full text-sm font-medium transition-colors",
              currentFolderId === null ? "bg-blue-50 text-blue-700" : "text-gray-700 hover:bg-gray-100"
            )}
          >
            <Home className="w-5 h-5" />
            <span>My Drive</span>
          </button>
          {/* Add more sidebar items here if needed */}
        </nav>

        <div className="p-4 border-t border-gray-200">
          <button 
            onClick={onLogout}
            className="w-full flex items-center space-x-3 px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-lg transition-colors text-sm font-medium"
          >
            <span className="text-red-600">Log Out</span>
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col overflow-hidden">
        {/* Header / Breadcrumbs */}
        <header className="h-16 bg-white border-b border-gray-200 flex items-center px-6 justify-between">
          <div className="flex items-center space-x-2 text-gray-600 overflow-x-auto">
            <button 
              onClick={() => setCurrentFolderId(null)}
              className="hover:bg-gray-100 p-1 rounded text-gray-500 hover:text-gray-900"
            >
              <Home className="w-5 h-5" />
            </button>
            
            {breadcrumbs.map((crumb) => (
              <div key={crumb.id} className="flex items-center space-x-2">
                <ChevronRight className="w-4 h-4 text-gray-400" />
                <button 
                  onClick={() => setCurrentFolderId(crumb.id)}
                  className="hover:bg-gray-100 px-2 py-1 rounded text-gray-700 font-medium hover:text-gray-900 whitespace-nowrap"
                >
                  {crumb.name}
                </button>
              </div>
            ))}
          </div>
          
          {/* Mobile Actions */}
          <div className="md:hidden flex space-x-2">
            <button onClick={() => setShowNewFolderDialog(true)} className="p-2 text-gray-600 hover:bg-gray-100 rounded-full">
              <FolderPlus className="w-6 h-6" />
            </button>
             <label htmlFor="file-upload" className="p-2 text-gray-600 hover:bg-gray-100 rounded-full cursor-pointer">
              <FileUp className="w-6 h-6" />
            </label>
          </div>
        </header>

        {/* File List */}
        <div className="flex-1 overflow-y-auto p-6">
          {isLoading ? (
            <div className="flex justify-center items-center h-full text-gray-400">Loading...</div>
          ) : files.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-full text-gray-400 space-y-4">
              <div className="w-32 h-32 bg-gray-100 rounded-full flex items-center justify-center">
                <Folder className="w-16 h-16 text-gray-300" />
              </div>
              <p className="text-lg">This folder is empty</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {files.map((file) => (
                <div 
                  key={file.id}
                  onClick={() => file.type === 'folder' && setCurrentFolderId(file.id)}
                  className={cn(
                    "group relative bg-white border border-gray-200 rounded-xl p-4 hover:shadow-md transition-all cursor-pointer flex flex-col justify-between h-40",
                    file.type === 'folder' ? "hover:border-blue-300 hover:bg-blue-50/30" : "hover:border-gray-300"
                  )}
                >
                  <div className="flex items-start justify-between">
                    <div className={cn(
                      "p-2 rounded-lg",
                      file.type === 'folder' ? "bg-blue-100 text-blue-600" : "bg-gray-100 text-gray-600"
                    )}>
                      {file.type === 'folder' ? <Folder className="w-6 h-6" /> : <File className="w-6 h-6" />}
                    </div>
                    
                    <div className="opacity-0 group-hover:opacity-100 transition-opacity flex space-x-1">
                      {file.type === 'file' && (
                        <>
                          <button 
                            onClick={(e) => openShareDialog(file, e)}
                            className={cn(
                              "p-1.5 hover:bg-gray-100 rounded-full",
                              file.is_shared ? "text-blue-500" : "text-gray-600"
                            )}
                            title="Share"
                          >
                            <Share2 className="w-4 h-4" />
                          </button>
                          <button 
                            onClick={(e) => handleDownload(file.id, e)}
                            className="p-1.5 hover:bg-gray-100 rounded-full text-gray-600"
                            title="Download"
                          >
                            <Download className="w-4 h-4" />
                          </button>
                        </>
                      )}
                      <button 
                        onClick={(e) => handleDelete(file.id, e)}
                        className="p-1.5 hover:bg-red-100 rounded-full text-red-500"
                        title="Delete"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                  </div>

                  <div className="mt-4">
                    <h3 className="font-medium text-gray-900 truncate" title={file.name}>
                      {file.name}
                    </h3>
                    <div className="flex items-center justify-between mt-1 text-xs text-gray-500">
                      <span>{format(new Date(file.created_at), 'MMM d, yyyy')}</span>
                      <span>{formatSize(file.size)}</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </main>

      {/* New Folder Dialog */}
      {showNewFolderDialog && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-2xl shadow-xl w-full max-w-md p-6">
            <h2 className="text-xl font-semibold mb-4">New Folder</h2>
            <form onSubmit={handleCreateFolder}>
              <input
                type="text"
                autoFocus
                placeholder="Folder name"
                value={newFolderName}
                onChange={(e) => setNewFolderName(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 mb-6"
              />
              <div className="flex justify-end space-x-3">
                <button
                  type="button"
                  onClick={() => setShowNewFolderDialog(false)}
                  className="px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-lg font-medium"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={!newFolderName.trim()}
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  Create
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Share Dialog */}
      {shareDialogFile && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-2xl shadow-xl w-full max-w-md p-6">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-xl font-semibold">Share "{shareDialogFile.name}"</h2>
              <button onClick={() => setShareDialogFile(null)} className="text-gray-400 hover:text-gray-600">
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="space-y-6">
              {!shareLink ? (
                <div className="text-center py-8">
                  <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <Share2 className="w-8 h-8 text-gray-400" />
                  </div>
                  <p className="text-gray-500 mb-6">This file is currently private.</p>
                  <button
                    onClick={() => toggleShare(true)}
                    disabled={isSharing}
                    className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-3 px-4 rounded-xl transition-colors disabled:opacity-70"
                  >
                    {isSharing ? 'Generating Link...' : 'Create Shareable Link'}
                  </button>
                </div>
              ) : (
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Shareable Link</label>
                    <div className="flex space-x-2">
                      <input
                        type="text"
                        readOnly
                        value={shareLink}
                        className="flex-1 px-4 py-2 border border-gray-300 rounded-lg bg-gray-50 text-gray-600 text-sm focus:outline-none"
                      />
                      <button
                        onClick={copyToClipboard}
                        className={cn(
                          "px-4 py-2 rounded-lg font-medium transition-colors flex items-center space-x-2",
                          copied ? "bg-green-100 text-green-700" : "bg-gray-100 text-gray-700 hover:bg-gray-200"
                        )}
                      >
                        {copied ? <Check className="w-4 h-4" /> : <Copy className="w-4 h-4" />}
                      </button>
                    </div>
                  </div>

                  <div className="pt-4 border-t border-gray-100">
                    <button
                      onClick={() => toggleShare(false)}
                      disabled={isSharing}
                      className="text-red-600 hover:text-red-700 text-sm font-medium flex items-center space-x-1"
                    >
                      <Trash2 className="w-4 h-4" />
                      <span>Stop Sharing</span>
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
