import express from 'express';
import { createServer as createViteServer } from 'vite';
import multer from 'multer';
import Database from 'better-sqlite3';
import { v4 as uuidv4 } from 'uuid';
import path from 'path';
import fs from 'fs';
import { fileURLToPath } from 'url';
import bcrypt from 'bcryptjs';
import jwt from 'jsonwebtoken';
import cookieParser from 'cookie-parser';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const JWT_SECRET = process.env.JWT_SECRET || 'super-secret-key-change-this';

// Ensure uploads directory exists
const UPLOADS_DIR = path.join(__dirname, 'uploads');
if (!fs.existsSync(UPLOADS_DIR)) {
  fs.mkdirSync(UPLOADS_DIR);
}

// Database Setup
const db = new Database('drive.db');

// Users Table
db.exec(`
  CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    created_at INTEGER NOT NULL
  );
`);

// Nodes Table (Updated with user_id)
db.exec(`
  CREATE TABLE IF NOT EXISTS nodes (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    parent_id TEXT,
    name TEXT NOT NULL,
    type TEXT CHECK(type IN ('file', 'folder')) NOT NULL,
    size INTEGER,
    mime_type TEXT,
    path TEXT,
    created_at INTEGER NOT NULL,
    updated_at INTEGER NOT NULL,
    share_token TEXT,
    is_shared INTEGER DEFAULT 0,
    FOREIGN KEY(user_id) REFERENCES users(id)
  );
`);

// Migrations
try {
  db.exec("ALTER TABLE nodes ADD COLUMN user_id TEXT");
  // For existing nodes, we might need to assign them to a default user or delete them.
  // For this demo, let's just leave them or assign to the first user created.
} catch (e) {
  // Column likely exists
}

try {
  db.exec("ALTER TABLE nodes ADD COLUMN share_token TEXT");
} catch (e) {
  // Column likely exists
}
try {
  db.exec("ALTER TABLE nodes ADD COLUMN is_shared INTEGER DEFAULT 0");
} catch (e) {
  // Column likely exists
}

const upload = multer({ dest: UPLOADS_DIR });
const app = express();
const PORT = 3000;

app.use(express.json());
app.use(cookieParser());

// Middleware to check auth
const authenticateToken = (req: any, res: any, next: any) => {
  const token = req.cookies.token;

  if (!token) return res.sendStatus(401);

  jwt.verify(token, JWT_SECRET, (err: any, user: any) => {
    if (err) return res.sendStatus(403);
    req.user = user;
    next();
  });
};

// --- Auth Routes ---

app.post('/api/auth/register', async (req, res) => {
  const { email, password } = req.body;
  
  if (!email || !password) {
    return res.status(400).json({ error: 'Email and password are required' });
  }

  try {
    const existingUser = db.prepare('SELECT * FROM users WHERE email = ?').get(email);
    if (existingUser) {
      return res.status(400).json({ error: 'User already exists' });
    }

    const hashedPassword = await bcrypt.hash(password, 10);
    const id = uuidv4();
    const now = Date.now();

    db.prepare('INSERT INTO users (id, email, password, created_at) VALUES (?, ?, ?, ?)').run(id, email, hashedPassword, now);

    const token = jwt.sign({ id, email }, JWT_SECRET, { expiresIn: '24h' });
    res.cookie('token', token, { httpOnly: true, secure: process.env.NODE_ENV === 'production' });
    res.json({ success: true, user: { id, email } });
  } catch (error) {
    console.error('Registration error:', error);
    res.status(500).json({ error: 'Registration failed' });
  }
});

app.post('/api/auth/login', async (req, res) => {
  const { email, password } = req.body;

  try {
    const user = db.prepare('SELECT * FROM users WHERE email = ?').get(email) as any;
    if (!user) {
      return res.status(400).json({ error: 'Invalid credentials' });
    }

    const validPassword = await bcrypt.compare(password, user.password);
    if (!validPassword) {
      return res.status(400).json({ error: 'Invalid credentials' });
    }

    const token = jwt.sign({ id: user.id, email: user.email }, JWT_SECRET, { expiresIn: '24h' });
    res.cookie('token', token, { httpOnly: true, secure: process.env.NODE_ENV === 'production' });
    res.json({ success: true, user: { id: user.id, email: user.email } });
  } catch (error) {
    console.error('Login error:', error);
    res.status(500).json({ error: 'Login failed' });
  }
});

app.post('/api/auth/logout', (req, res) => {
  res.clearCookie('token');
  res.json({ success: true });
});

app.get('/api/auth/me', authenticateToken, (req: any, res) => {
  res.json({ user: req.user });
});

// --- Drive Routes (Protected) ---

// Share a file (Protected - only owner can share)
app.post('/api/share/:id', authenticateToken, (req: any, res) => {
  const { id } = req.params;
  const { enable } = req.body;
  const userId = req.user.id;

  try {
    const node = db.prepare('SELECT * FROM nodes WHERE id = ? AND user_id = ?').get(id, userId) as any;
    if (!node) {
      return res.status(404).json({ error: 'Node not found' });
    }

    if (enable) {
      const token = node.share_token || uuidv4();
      db.prepare('UPDATE nodes SET is_shared = 1, share_token = ? WHERE id = ?').run(token, id);
      res.json({ success: true, shareToken: token });
    } else {
      db.prepare('UPDATE nodes SET is_shared = 0 WHERE id = ?').run(id);
      res.json({ success: true, shareToken: null });
    }
  } catch (error) {
    console.error('Error sharing node:', error);
    res.status(500).json({ error: 'Failed to update share status' });
  }
});

// Get shared file info (Public)
app.get('/api/shared/:token', (req, res) => {
  const { token } = req.params;
  
  try {
    const node = db.prepare('SELECT * FROM nodes WHERE share_token = ? AND is_shared = 1').get(token) as any;
    
    if (!node) {
      return res.status(404).json({ error: 'Shared link not found or expired' });
    }

    // Return only safe info
    res.json({
      id: node.id,
      name: node.name,
      size: node.size,
      mime_type: node.mime_type,
      created_at: node.created_at,
      type: node.type
    });
  } catch (error) {
    console.error('Error fetching shared node:', error);
    res.status(500).json({ error: 'Failed to fetch shared info' });
  }
});

// Download shared file (Public)
app.get('/api/shared/:token/download', (req, res) => {
  const { token } = req.params;
  
  try {
    const node = db.prepare('SELECT * FROM nodes WHERE share_token = ? AND is_shared = 1').get(token) as any;
    
    if (!node || node.type !== 'file') {
      return res.status(404).json({ error: 'Shared file not found' });
    }

    const filePath = path.join(UPLOADS_DIR, node.path);
    if (!fs.existsSync(filePath)) {
      return res.status(404).json({ error: 'File on disk not found' });
    }

    res.download(filePath, node.name);
  } catch (error) {
    console.error('Error downloading shared file:', error);
    res.status(500).json({ error: 'Failed to download shared file' });
  }
});

// Get contents of a folder (Protected)
app.get('/api/files', authenticateToken, (req: any, res) => {
  const parentId = req.query.parentId as string || null;
  const userId = req.user.id;
  
  try {
    let query = 'SELECT * FROM nodes WHERE user_id = ? AND parent_id IS ? ORDER BY type DESC, name ASC';
    const rows = db.prepare(query).all(userId, parentId);
    
    // Also get the current folder details if we are not at root
    let currentFolder = null;
    if (parentId) {
      currentFolder = db.prepare('SELECT * FROM nodes WHERE id = ? AND user_id = ?').get(parentId, userId);
    }

    // Get breadcrumbs
    const breadcrumbs = [];
    let tempId = parentId;
    while (tempId) {
      const folder = db.prepare('SELECT id, name, parent_id FROM nodes WHERE id = ? AND user_id = ?').get(tempId, userId) as any;
      if (folder) {
        breadcrumbs.unshift(folder);
        tempId = folder.parent_id;
      } else {
        break;
      }
    }

    res.json({ files: rows, currentFolder, breadcrumbs });
  } catch (error) {
    console.error('Error fetching files:', error);
    res.status(500).json({ error: 'Failed to fetch files' });
  }
});

// Create a new folder (Protected)
app.post('/api/folders', authenticateToken, (req: any, res) => {
  const { name, parentId } = req.body;
  const userId = req.user.id;
  const id = uuidv4();
  const now = Date.now();

  try {
    const stmt = db.prepare(`
      INSERT INTO nodes (id, user_id, parent_id, name, type, created_at, updated_at)
      VALUES (?, ?, ?, ?, 'folder', ?, ?)
    `);
    stmt.run(id, userId, parentId || null, name, now, now);
    res.json({ id, name, parentId });
  } catch (error) {
    console.error('Error creating folder:', error);
    res.status(500).json({ error: 'Failed to create folder' });
  }
});

// Upload a file (Protected)
app.post('/api/upload', authenticateToken, upload.single('file'), (req: any, res) => {
  const { parentId } = req.body;
  const userId = req.user.id;
  const file = req.file;

  if (!file) {
    return res.status(400).json({ error: 'No file uploaded' });
  }

  const id = uuidv4();
  const now = Date.now();

  try {
    const stmt = db.prepare(`
      INSERT INTO nodes (id, user_id, parent_id, name, type, size, mime_type, path, created_at, updated_at)
      VALUES (?, ?, ?, ?, 'file', ?, ?, ?, ?, ?)
    `);
    
    stmt.run(id, userId, parentId || null, file.originalname, file.size, file.mimetype, file.filename, now, now);
    
    res.json({ success: true });
  } catch (error) {
    console.error('Error uploading file:', error);
    fs.unlinkSync(file.path);
    res.status(500).json({ error: 'Failed to upload file' });
  }
});

// Download a file (Protected - owner only)
app.get('/api/download/:id', authenticateToken, (req: any, res) => {
  const { id } = req.params;
  const userId = req.user.id;
  
  try {
    const fileNode = db.prepare('SELECT * FROM nodes WHERE id = ? AND user_id = ? AND type = "file"').get(id, userId) as any;
    
    if (!fileNode) {
      return res.status(404).json({ error: 'File not found' });
    }

    const filePath = path.join(UPLOADS_DIR, fileNode.path);
    
    if (!fs.existsSync(filePath)) {
      return res.status(404).json({ error: 'File on disk not found' });
    }

    res.download(filePath, fileNode.name);
  } catch (error) {
    console.error('Error downloading file:', error);
    res.status(500).json({ error: 'Failed to download file' });
  }
});

// Delete a file or folder (Protected)
app.delete('/api/nodes/:id', authenticateToken, (req: any, res) => {
  const { id } = req.params;
  const userId = req.user.id;

  try {
    const node = db.prepare('SELECT * FROM nodes WHERE id = ? AND user_id = ?').get(id, userId) as any;
    
    if (!node) {
      return res.status(404).json({ error: 'Node not found' });
    }

    if (node.type === 'file') {
      const filePath = path.join(UPLOADS_DIR, node.path);
      if (fs.existsSync(filePath)) {
        fs.unlinkSync(filePath);
      }
      db.prepare('DELETE FROM nodes WHERE id = ?').run(id);
    } else {
      const children = db.prepare('SELECT count(*) as count FROM nodes WHERE parent_id = ?').get(id) as any;
      if (children.count > 0) {
        return res.status(400).json({ error: 'Folder is not empty' });
      }
      db.prepare('DELETE FROM nodes WHERE id = ?').run(id);
    }

    res.json({ success: true });
  } catch (error) {
    console.error('Error deleting node:', error);
    res.status(500).json({ error: 'Failed to delete node' });
  }
});

async function startServer() {
  if (process.env.NODE_ENV !== 'production') {
    const vite = await createViteServer({
      server: { middlewareMode: true },
      appType: 'spa',
    });
    app.use(vite.middlewares);
  } else {
    app.use(express.static(path.join(__dirname, 'dist')));
  }

  app.listen(PORT, '0.0.0.0', () => {
    console.log(`Server running on http://localhost:${PORT}`);
  });
}

startServer();
