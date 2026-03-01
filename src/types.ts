export interface FileNode {
  id: string;
  parent_id: string | null;
  name: string;
  type: 'file' | 'folder';
  size?: number;
  mime_type?: string;
  created_at: number;
  updated_at: number;
  share_token?: string;
  is_shared?: number; // 0 or 1
}

export interface Breadcrumb {
  id: string;
  name: string;
  parent_id: string | null;
}

export interface FolderResponse {
  files: FileNode[];
  currentFolder: FileNode | null;
  breadcrumbs: Breadcrumb[];
}
