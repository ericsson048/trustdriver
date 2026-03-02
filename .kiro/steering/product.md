---
inclusion: always
---

# TrustDriver Product Overview

TrustDriver is a cloud file storage and sharing application similar to Google Drive or Dropbox. Users can:

- Register and authenticate with email verification
- Upload and organize files in folders
- Download files
- Share files via secure tokens
- Manage their personal drive space

The application consists of a React frontend and Django REST API backend, deployed separately (frontend on Vercel, backend on Render).

Key features:
- User authentication with session-based auth
- File/folder management with hierarchical structure
- Secure file sharing with token-based access
- Email verification for new accounts
- Support for multiple file types (documents, images, audio, etc.)
