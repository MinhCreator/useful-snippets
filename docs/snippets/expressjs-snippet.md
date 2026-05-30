# Useful Node.js & Express.js Codeblock Patterns

> Practical, copy-paste-ready Express.js snippets for building production-ready REST APIs.

---

## 1. Basic Server Setup

### Minimal Express Server

```js
const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;

app.get('/', (req, res) => {
  res.json({ message: 'Server is running!' });
});

app.listen(PORT, () => {
  console.log(`Server listening on port ${PORT}`);
});
```

### Production-Ready Express App (app.js)

```js
const express = require('express');
const helmet = require('helmet');
const cors = require('cors');
const morgan = require('morgan');
const compression = require('compression');

const app = express();

// Security headers
app.use(helmet());

// CORS
app.use(cors({
  origin: process.env.ALLOWED_ORIGINS
    ? process.env.ALLOWED_ORIGINS.split(',')
    : ['http://localhost:3000'],
  methods: ['GET', 'POST', 'PUT', 'PATCH', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization'],
}));

// Compression
app.use(compression());

// Body parsing with size limits
app.use(express.json({ limit: '10kb' }));
app.use(express.urlencoded({ extended: true, limit: '10kb' }));

// Request logging
app.use(morgan(process.env.NODE_ENV === 'production' ? 'combined' : 'dev'));

// Static files
app.use(express.static('public'));

// Routes
app.use('/api/users', require('./routes/users'));
app.use('/api/auth', require('./routes/auth'));

// Health check
app.get('/health', (_req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// 404 handler
app.use((_req, res) => {
  res.status(404).json({ error: { code: 'NOT_FOUND', message: 'Endpoint not found' } });
});

// Global error handler (MUST be last)
app.use(require('./middleware/errorHandler'));

module.exports = app;
```

### Server Entry Point (server.js)

```js
const app = require('./app');
const { connectDB } = require('./config/database');

const PORT = process.env.PORT || 3000;

const start = async () => {
  try {
    await connectDB();
    app.listen(PORT, () => {
      console.log(`Server running on port ${PORT} in ${process.env.NODE_ENV} mode`);
    });
  } catch (err) {
    console.error('Failed to start server:', err);
    process.exit(1);
  }
};

start();
```

---

## 2. Project Structure

```
my-api/
  src/
    config/          # DB connection, env config
    controllers/     # Request/response handlers
    middleware/      # Auth, validation, error handling
    models/          # Database schemas (Mongoose, Sequelize, etc.)
    routes/          # Express routers
    services/        # Business logic
    utils/           # Helper functions, custom errors
    validators/      # Request validation schemas (Joi, Zod)
  tests/             # Test files
  app.js             # Express app (exported for testing)
  server.js          # Starts the server
  .env
```

---

## 3. Routing Patterns

### Router Setup

```js
const express = require('express');
const router = express.Router();
const controller = require('../controllers/userController');
const { authenticate } = require('../middleware/auth');
const { validate } = require('../middleware/validate');
const { createUserSchema, updateUserSchema } = require('../validators/userValidator');

router.get('/', authenticate, controller.getAll);
router.get('/:id', authenticate, controller.getById);
router.post('/', validate(createUserSchema), controller.create);
router.put('/:id', authenticate, validate(updateUserSchema), controller.update);
router.delete('/:id', authenticate, controller.remove);

module.exports = router;
```

### Route with URL Params

```js
// GET /api/users/123
router.get('/:id', async (req, res) => {
  const { id } = req.params;
  // ...
});

// GET /api/users/123/posts/456
router.get('/:userId/posts/:postId', async (req, res) => {
  const { userId, postId } = req.params;
  // ...
});
```

### Route with Query Params

```js
// GET /api/users?page=2&limit=20&sort=name
router.get('/', async (req, res) => {
  const { page = 1, limit = 10, sort = 'createdAt' } = req.query;
  const skip = (parseInt(page) - 1) * parseInt(limit);
  // ...
});
```

### Route with Multiple Middleware

```js
router.post(
  '/',
  authenticate,                    // Verify JWT
  authorize('admin'),              // Check role
  rateLimit({ windowMs: 15*60*1000, max: 10 }), // Rate limit
  validate(createUserSchema),      // Validate body
  controller.create                // Handle request
);
```

---

## 4. Controller Pattern

### Thin Controller (no business logic)

```js
// controllers/userController.js
const userService = require('../services/userService');

exports.getAll = async (req, res, next) => {
  try {
    const { page, limit, sort } = req.query;
    const result = await userService.findAll({ page, limit, sort });
    res.json({ success: true, data: result.data, meta: result.meta });
  } catch (err) {
    next(err);
  }
};

exports.getById = async (req, res, next) => {
  try {
    const user = await userService.findById(req.params.id);
    res.json({ success: true, data: user });
  } catch (err) {
    next(err);
  }
};

exports.create = async (req, res, next) => {
  try {
    const user = await userService.create(req.body);
    res.status(201).json({ success: true, data: user });
  } catch (err) {
    next(err);
  }
};

exports.update = async (req, res, next) => {
  try {
    const user = await userService.update(req.params.id, req.body);
    res.json({ success: true, data: user });
  } catch (err) {
    next(err);
  }
};

exports.remove = async (req, res, next) => {
  try {
    await userService.remove(req.params.id);
    res.status(204).end();
  } catch (err) {
    next(err);
  }
};
```

### Clean Controller with asyncHandler

```js
const asyncHandler = (fn) => (req, res, next) => {
  Promise.resolve(fn(req, res, next)).catch(next);
};

// No more try/catch needed
exports.getAll = asyncHandler(async (req, res) => {
  const users = await userService.findAll();
  res.json({ success: true, data: users });
});

exports.getById = asyncHandler(async (req, res) => {
  const user = await userService.findById(req.params.id);
  res.json({ success: true, data: user });
});
```

---

## 5. Service Layer (Business Logic)

```js
// services/userService.js
const User = require('../models/User');
const { AppError } = require('../middleware/errorHandler');

exports.findAll = async ({ page = 1, limit = 10, sort = 'createdAt' } = {}) => {
  const skip = (parseInt(page) - 1) * parseInt(limit);
  const [data, total] = await Promise.all([
    User.find().sort(sort).skip(skip).limit(parseInt(limit)),
    User.countDocuments(),
  ]);

  return {
    data,
    meta: {
      total,
      page: parseInt(page),
      limit: parseInt(limit),
      totalPages: Math.ceil(total / parseInt(limit)),
    },
  };
};

exports.findById = async (id) => {
  const user = await User.findById(id);
  if (!user) throw new AppError('User not found', 404);
  return user;
};

exports.create = async ({ email, password, name }) => {
  const existing = await User.findOne({ email });
  if (existing) throw new AppError('Email already registered', 409);

  const user = await User.create({ email, password, name });
  return { id: user.id, email: user.email, name: user.name };
};

exports.update = async (id, data) => {
  const user = await User.findByIdAndUpdate(id, data, { new: true, runValidators: true });
  if (!user) throw new AppError('User not found', 404);
  return user;
};

exports.remove = async (id) => {
  const user = await User.findByIdAndDelete(id);
  if (!user) throw new AppError('User not found', 404);
};
```

---

## 6. Middleware Patterns

### Authentication Middleware (JWT)

```js
// middleware/auth.js
const jwt = require('jsonwebtoken');
const { AppError } = require('./errorHandler');

const authenticate = (req, res, next) => {
  const authHeader = req.headers.authorization;

  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    throw new AppError('No token provided', 401);
  }

  const token = authHeader.split(' ')[1];

  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    req.user = { id: decoded.id, email: decoded.email, role: decoded.role };
    next();
  } catch (err) {
    if (err.name === 'TokenExpiredError') {
      throw new AppError('Token expired', 401);
    }
    throw new AppError('Invalid token', 401);
  }
};

module.exports = { authenticate };
```

### Role-Based Authorization

```js
// middleware/authorize.js
const { AppError } = require('./errorHandler');

const authorize = (...allowedRoles) => {
  return (req, res, next) => {
    if (!req.user) {
      throw new AppError('Not authenticated', 401);
    }
    if (!allowedRoles.includes(req.user.role)) {
      throw new AppError('Insufficient permissions', 403);
    }
    next();
  };
};

// Usage:
// router.delete('/:id', authenticate, authorize('admin', 'moderator'), controller.remove);
```

### Request Validation Middleware (Joi)

```js
// middleware/validate.js
const validate = (schema, property = 'body') => {
  return (req, res, next) => {
    const { error, value } = schema.validate(req[property], {
      abortEarly: false,
      stripUnknown: true,
    });

    if (error) {
      const messages = error.details.map((d) => d.message);
      return res.status(400).json({
        error: 'Validation failed',
        details: messages,
      });
    }

    req[property] = value; // use sanitized values
    next();
  };
};

module.exports = { validate };
```

### Request Validation Middleware (Zod)

```js
// middleware/validateZod.js
const validate = (schema, property = 'body') => {
  return (req, res, next) => {
    const result = schema.safeParse(req[property]);

    if (!result.success) {
      const messages = result.error.errors.map((e) => e.message);
      return res.status(400).json({
        error: 'Validation failed',
        details: messages,
      });
    }

    req[property] = result.data;
    next();
  };
};

module.exports = { validate };
```

### Rate Limiting

```js
// middleware/rateLimiter.js
const rateLimit = require('express-rate-limit');

const globalLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100,                  // limit each IP to 100 requests per window
  message: { error: 'Too many requests, please try again later' },
  standardHeaders: true,
  legacyHeaders: false,
});

const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 10,                   // stricter limit for auth endpoints
  message: { error: 'Too many login attempts, please try again later' },
});

module.exports = { globalLimiter教务, authLimiter };
```

### Request ID Tracing

```js
// middleware/requestId.js
const { v4: uuidv4 } = require('uuid');

const requestId = (req, res, next) => {
  req.id = req.headers['x-request-id'] || uuidv4();
  res.setHeader('x-request-id', req.id);
  next();
};

module.exports = { requestId };
```

---

## 7. Error Handling

### Custom Error Class

```js
// middleware/errorHandler.js
class AppError extends Error {
  constructor(message, statusCode, details = null) {
    super(message);
    this.statusCode = statusCode;
    this.details = details;
    this.isOperational = true;
    Error.captureStackTrace(this, this.constructor);
  }
}

// Factory methods
AppError.badRequest = (msg) => new AppError(msg, 400);
AppError.unauthorized = (msg) => new AppError(msg || 'Unauthorized', 401);
AppError.forbidden = (msg) => new AppError(msg || 'Forbidden', 403);
AppError.notFound = (msg) => new AppError(msg || 'Resource not found', 404);
AppError.conflict = (msg) => new AppError(msg, 409);
AppError.internal = (msg) => new AppError(msg || 'Internal server error', 500);
```

### Global Error Handler Middleware

```js
// middleware/errorHandler.js (continued)
const errorHandler = (err, req, res, _next) => {
  // Default to 500
  const statusCode = err.statusCode || 500;
  const message = err.isOperational ? err.message : 'Internal server error';

  // Log server errors
  if (statusCode >= 500) {
    console.error(`[${req.id}] ${err.stack || err.message}`);
  } else {
    console.warn(`[${req.id}] ${err.message}`);
  }

  res.status(statusCode).json({
    success: false,
    error: {
      code: statusCode,
      message,
      ...(err.details && { details: err.details }),
      ...(process.env.NODE_ENV === 'development' && { stack: err.stack }),
    },
    ...(req.id && { requestId: req.id }),
  });
};

module.exports = { AppError, errorHandler };
```

### Async Handler Wrapper

```js
// utils/asyncHandler.js
const asyncHandler = (fn) => (req, res, next) => {
  Promise.resolve(fn(req, res, next)).catch(next);
};

module.exports = asyncHandler;

// Usage:
// const asyncHandler = require('../utils/asyncHandler');
// router.get('/:id', asyncHandler(async (req, res) => { ... }));
```

---

## 8. Authentication — JWT with Access + Refresh Tokens

### JWT Helpers

```js
// utils/jwt.js
const jwt = require('jsonwebtoken');

const generateAccessToken = (payload) => {
  return jwt.sign(payload, process.env.JWT_SECRET, { expiresIn: '15m' });
};

const generateRefreshToken = (payload) => {
  return jwt.sign(payload, process.env.JWT_REFRESH_SECRET, { expiresIn: '7d' });
};

const verifyAccessToken = (token) => {
  return jwt.verify(token, process.env.JWT_SECRET);
};

const verifyRefreshToken = (token) => {
  return jwt.verify(token, process.env.JWT_REFRESH_SECRET);
};

module.exports = { generateAccessToken, generateRefreshToken, verifyAccessToken, verifyRefreshToken };
```

### Auth Controller

```js
// controllers/authController.js
const bcrypt = require('bcryptjs');
const jwtUtils = require('../utils/jwt');
const User = require('../models/User');
const { AppError } = require('../middleware/errorHandler');

exports.register = asyncHandler(async (req, res) => {
  const { email, password, name } = req.body;

  const existing = await User.findOne({ email });
  if (existing) throw AppError.conflict('Email already registered');

  const hashed = await bcrypt.hash(password, 12);
  const user = await User.create({ email, password: hashed, name });

  const accessToken = jwtUtils.generateAccessToken({ id: user.id, role: user.role });
  const refreshToken = jwtUtils.generateRefreshToken({ id: user.id });

  res.status(201).json({
    success: true,
    data: { user: { id: user.id, email: user.email, name: user.name }, accessToken, refreshToken },
  });
});

exports.login = asyncHandler(async (req, res) => {
  const { email, password } = req.body;

  const user = await User.findOne({ email }).select('+password');
  if (!user) throw AppError.unauthorized('Invalid email or password');

  const match = await bcrypt.compare(password, user.password);
  if (!match) throw AppError.unauthorized('Invalid email or password');

  const accessToken = jwtUtils.generateAccessToken({ id: user.id, role: user.role });
  const refreshToken = jwtUtils.generateRefreshToken({ id: user.id });

  res.json({
    success: true,
    data: {
      user: { id: user.id, email: user.email, name: user.name, role: user.role },
      accessToken,
      refreshToken,
    },
  });
});

exports.refresh = asyncHandler(async (req, res) => {
  const { refreshToken } = req.body;
  if (!refreshToken) throw AppError.badRequest('Refresh token required');

  const decoded = jwtUtils.verifyRefreshToken(refreshToken);
  const user = await User.findById(decoded.id);
  if (!user) throw AppError.unauthorized('User not found');

  const accessToken = jwtUtils.generateAccessToken({ id: user.id, role: user.role });
  res.json({ success: true, data: { accessToken } });
});

exports.logout = asyncHandler(async (req, res) => {
  // In stateless JWT, logout is handled client-side by discarding the token.
  // For blacklisting, add the token to a Redis blocklist here.
  res.json({ success: true, message: 'Logged out' });
});
```

---

## 9. Validation Schemas

### Joi Schemas

```js
// validators/userValidator.js
const Joi = require('joi');

const createUserSchema = Joi.object({
  email: Joi.string().email().required(),
  password: Joi.string().min(8).max(128).required(),
  name: Joi.string().trim().min(2).max(100).required(),
  role: Joi.string().valid('user', 'admin').default('user'),
});

const updateUserSchema = Joi.object({
  email: Joi.string().email(),
  name: Joi.string().trim().min(2).max(100),
  role: Joi.string().valid('user', 'admin'),
}).min(1); // at least one field

const loginSchema = Joi.object({
  email: Joi.string().email().required(),
  password: Joi.string().required(),
});

const paginationSchema = Joi.object({
  page: Joi.number().integer().min(1).default(1),
  limit: Joi.number().integer().min(1).max(100).default(10),
  sort: Joi.string().default('createdAt'),
});

module.exports = { createUserSchema, updateUserSchema, loginSchema, paginationSchema };
```

### Zod Schemas

```js
// validators/userValidatorZod.js
const { z } = require('zod');

const createUserSchema = z.object({
  email: z.string().email('Invalid email format'),
  password: z.string().min(8, 'Password must be at least 8 characters').max(128),
  name: z.string().trim().min(2).max(100),
  role: z.enum(['user', 'admin']).default('user'),
});

const updateUserSchema = z.object({
  email: z.string().email().optional(),
  name: z.string().trim().min(2).max(100).optional(),
  role: z.enum(['user', 'admin']).optional(),
});

const loginSchema = z.object({
  email: z.string().email(),
  password: z.string().min(1, 'Password is required'),
});

module.exports = { createUserSchema, updateUserSchema, loginSchema };
```

---

## 10. Database Integration

### MongoDB with Mongoose

```js
// config/database.js
const mongoose = require('mongoose');

const connectDB = async () => {
  const conn = await mongoose.connect(process.env.MONGODB_URI);
  console.log(`MongoDB connected: ${conn.connection.host}`);
};

module.exports = { connectDB };
```

### Mongoose Model

```js
// models/User.js
const mongoose = require('mongoose');

const userSchema = new mongoose.Schema(
  {
    email: { type: String, required: true, unique: true, lowercase: true, trim: true },
    password: { type: String, required: true, select: false },
    name: { type: String, required: true, trim: true },
    role: { type: String, enum: ['user', 'admin'], default: 'user' },
    isActive: { type: Boolean, default: true },
  },
  { timestamps: true }
);

userSchema.index({ email: 1 });
userSchema.index({ role: 1, createdAt: -1 });

module.exports = mongoose.model('User', userSchema);
```

### PostgreSQL with pg (raw)

```js
// config/database.js
const { Pool } = require('pg');

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  max: 20,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});

pool.on('error', (err) => {
  console.error('Unexpected database pool error:', err);
  process.exit(-1);
});

const query = (text, params) => pool.query(text, params);

module.exports = { pool, query };
```

### PostgreSQL Repository Pattern

```js
// repositories/userRepository.js
const { query } = require('../config/database');

exports.findAll = async ({ limit, offset, sort }) => {
  const sql = `SELECT id, email, name, role, created_at
               FROM users
               ORDER BY ${sort}
               LIMIT $1 OFFSET $2`;
  const { rows } = await query(sql, [limit, offset]);
  const { rowCount } = await query('SELECT COUNT(*) FROM users');
  return { data: rows, total: parseInt(rowCount) };
};

exports.findById = async (id) => {
  const { rows } = await query('SELECT * FROM users WHERE id = $1', [id]);
  return rows[0] || null;
};

exports.findByEmail = async (email) => {
  const { rows } = await query('SELECT * FROM users WHERE email = $1', [email]);
  return rows[0] || null;
};

exports.create = async ({ email, password, name, role }) => {
  const { rows } = await query(
    `INSERT INTO users (email, password, name, role)
     VALUES ($1, $2, $3, $4) RETURNING id, email, name, role, created_at`,
    [email, password, name, role || 'user']
  );
  return rows[0];
};

exports.update = async (id, fields) => {
  const setClauses = [];
  const values = [];
  let idx = 1;

  for (const [key, value] of Object.entries(fields)) {
    setClauses.push(`${key} = $${idx}`);
    values.push(value);
    idx++;
  }

  values.push(id);
  const sql = `UPDATE users SET ${setClauses.join(', ')} WHERE id = $${idx}
               RETURNING id, email, name, role, created_at`;
  const { rows } = await query(sql, values);
  return rows[0] || null;
};

exports.remove = async (id) => {
  const { rowCount } = await query('DELETE FROM users WHERE id = $1', [id]);
  return rowCount > 0;
};
```

---

## 11. File Upload with Multer

```js
const multer = require('multer');
const path = require('path');
const { v4: uuidv4 } = require('uuid');

// Disk storage
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, 'uploads/');
  },
  filename: (req, file, cb) => {
    const ext = path.extname(file.originalname);
    cb(null, `${uuidv4()}${ext}`);
  },
});

// File filter
const fileFilter = (req, file, cb) => {
  const allowed = ['.jpg', '.jpeg', '.png', '.gif', '.pdf'];
  const ext = path.extname(file.originalname).toLowerCase();

  if (allowed.includes(ext)) {
    cb(null, true);
  } else {
    cb(new Error(`File type ${ext} is not allowed`), false);
  }
};

const upload = multer({
  storage,
  fileFilter,
  limits: { fileSize: 5 * 1024 * 1024 }, // 5MB
});

// Usage in route:
// router.post('/upload', authenticate, upload.single('avatar'), controller.uploadAvatar);
// router.post('/uploads', authenticate, upload.array('files', 5), controller.uploadFiles);

// Route handler:
exports.uploadAvatar = asyncHandler(async (req, res) => {
  if (!req.file) throw AppError.badRequest('No file uploaded');

  res.json({
    success: true,
    data: {
      filename: req.file.filename,
      size: req.file.size,
      mimetype: req.file.mimetype,
      url: `/uploads/${req.file.filename}`,
    },
  });
});
```

---

## 12. Pagination Utility

```js
// utils/pagination.js
const paginate = (page = 1, limit = 10) => {
  const p = Math.max(1, parseInt(page));
  const l = Math.min(100, Math.max(1, parseInt(limit)));

  return {
    page: p,
    limit: l,
    skip: (p - 1) * l,
  };
};

const paginationMeta = (total, page, limit) => ({
  total,
  page,
  limit,
  totalPages: Math.ceil(total / limit),
  hasNext: page * limit < total,
  hasPrev: page > 1,
});

module.exports = { paginate, paginationMeta };

// Usage:
// const { page, limit, skip } = paginate(req.query.page, req.query.limit);
// const data = await Model.find().skip(skip).limit(limit);
// const total = await Model.countDocuments();
// res.json({ success: true, data, meta: paginationMeta(total, page, limit) });
```

---

## 13. API Response Helper

```js
// utils/response.js
class ApiResponse {
  static success(res, data, statusCode = 200, meta = null) {
    const response = { success: true, data };
    if (meta) response.meta = meta;
    return res.status(statusCode).json(response);
  }

  static created(res, data) {
    return this.success(res, data, 201);
  }

  static noContent(res) {
    return res.status(204).end();
  }

  static error(res, message, statusCode = 500, details = null) {
    const response = {
      success: false,
      error: { code: statusCode, message },
    };
    if (details) response.error.details = details;
    return res.status(statusCode).json(response);
  }

  static badRequest(res, message = 'Bad request') {
    return this.error(res, message, 400);
  }

  static notFound(res, message = 'Resource not found') {
    return this.error(res, message, 404);
  }

  static unauthorized(res, message = 'Unauthorized') {
    return this.error(res, message, 401);
  }

  static forbidden(res, message = 'Forbidden') {
    return this.error(res, message, 403);
  }
}

module.exports = ApiResponse;

// Usage:
// ApiResponse.success(res, user);
// ApiResponse.created(res, newUser);
// ApiResponse.notFound(res, 'User not found');
```

---

## 14. Graceful Shutdown

```js
// server.js
const app = require('./app');
const { connectDB, disconnectDB } = require('./config/database');

const server = app.listen(process.env.PORT || 3000, async () => {
  await connectDB();
  console.log(`Server running on port ${process.env.PORT || 3000}`);
});

const gracefulShutdown = async (signal) => {
  console.log(`\n${signal} received. Shutting down gracefully...`);

  server.close(async () => {
    await disconnectDB();
    console.log('Server closed');
    process.exit(0);
  });

  // Force shutdown after 30s
  setTimeout(() => {
    console.error('Forced shutdown after timeout');
    process.exit(1);
  }, 30000);
};

process.on('SIGTERM', () => gracefulShutdown('SIGTERM'));
process.on('SIGINT', () => gracefulShutdown('SIGINT'));
```

---

## 15. Environment Config

```js
// config/env.js
const path = require('path');
require('dotenv').config({ path: path.resolve(__dirname, '../.env') });

const config = Object.freeze({
  nodeEnv: process.env.NODE_ENV || 'development',
  port: parseInt(process.env.PORT, 10) || 3000,

  db: {
    uri: process.env.MONGODB_URI || process.env.DATABASE_URL,
  },

  jwt: {
    secret: process.env.JWT_SECRET,
    refreshSecret: process.env.JWT_REFRESH_SECRET,
    accessExpiresIn: process.env.JWT_ACCESS_EXPIRES || '15m',
    refreshExpiresIn: process.env.JWT_REFRESH_EXPIRES || '7d',
  },

  cors: {
    allowedOrigins: process.env.ALLOWED_ORIGINS
      ? process.env.ALLOWED_ORIGINS.split(',')
      : ['http://localhost:3000'],
  },

  rateLimit: {
    windowMs: 15 * 60 * 1000,
    max: parseInt(process.env.RATE_LIMIT_MAX, 10) || 100,
  },

  upload: {
    maxFileSize: 5 * 1024 * 1024, // 5MB
  },
});

module.exports = config;
```

---

## 16. Testing with Jest & Supertest

```js
// tests/users.test.js
const request = require('supertest');
const app = require('../app');
const mongoose = require('mongoose');

beforeAll(async () => {
  await mongoose.connect(process.env.MONGODB_URI_TEST);
});

afterAll(async () => {
  await mongoose.connection.dropDatabase();
  await mongoose.disconnect();
});

describe('POST /api/users', () => {
  it('should create a new user', async () => {
    const res = await request(app)
      .post('/api/users')
      .send({ email: 'test@test.com', password: 'password123', name: 'Test' })
      .expect(201);

    expect(res.body.success).toBe(true);
    expect(res.body.data.email).toBe('test@test.com');
  });

  it('should return 400 for invalid input', async () => {
    const res = await request(app)
      .post('/api/users')
      .send({ email: 'invalid' })
      .expect(400);

    expect(res.body.error).toBe('Validation failed');
  });
});

describe('GET /api/users', () => {
  it('should return paginated users', async () => {
    const res = await request(app)
      .get('/api/users?page=1&limit=10')
      .set('Authorization', `Bearer ${testToken}`)
      .expect(200);

    expect(res.body.success).toBe(true);
    expect(res.body.meta).toHaveProperty('totalPages');
  });

  it('should return 401 without auth token', async () => {
    await request(app).get('/api/users').expect(401);
  });
});
```

---

## 17. WebSocket with Socket.io

```js
// server.js
const http = require('http');
const { Server } = require('socket.io');
const app = require('./app');

const server = http.createServer(app);
const io = new Server(server, {
  cors: { origin: process.env.ALLOWED_ORIGINS?.split(',') },
});

io.use((socket, next) => {
  const token = socket.handshake.auth.token;
  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    socket.userId = decoded.id;
    next();
  } catch {
    next(new Error('Authentication failed'));
  }
});

io.on('connection', (socket) => {
  console.log(`User ${socket.userId} connected`);

  socket.join(`user:${socket.userId}`);

  socket.on('join:room', (roomId) => {
    socket.join(roomId);
  });

  socket.on('message:send', (data) => {
    io.to(data.roomId).emit('message:new', {
      userId: socket.userId,
      text: data.text,
      timestamp: new Date(),
    });
  });

  socket.on('disconnect', () => {
    console.log(`User ${socket.userId} disconnected`);
  });
});

server.listen(process.env.PORT || 3000);
```

---

## 18. Cron Jobs with node-cron

```js
// jobs/cleanup.js
const cron = require('node-cron');
const User = require('../models/User');

// Run every day at midnight
cron.schedule('0 0 * * *', async () => {
  try {
    const result = await User.deleteMany({
      isActive: false,
      updatedAt: { $lt: new Date(Date.now() - 90 * 24 * 60 * 60 * 1000) }, // 90 days
    });
    console.log(`Cleaned up ${result.deletedCount} inactive users`);
  } catch (err) {
    console.error('Cron job failed:', err);
  }
});
```

---

## 19. Logging with Winston

```js
// utils/logger.js
const winston = require('winston');
const path = require('path');

const logger = winston.createLogger({
  level: process.env.NODE_ENV === 'production' ? 'info' : 'debug',
  format: winston.format.combine(
    winston.format.timestamp({ format: 'YYYY-MM-DD HH:mm:ss' }),
    winston.format.errors({ stack: true }),
    winston.format.json()
  ),
  defaultMeta: { service: 'api' },
  transports: [
    new winston.transports.File({
      filename: path.join('logs', 'error.log'),
      level: 'error',
      maxsize: 5 * 1024 * 1024,
      maxFiles: 5,
    }),
    new winston.transports.File({
      filename: path.join('logs', 'combined.log'),
      maxsize: 5 * 1024 * 1024,
      maxFiles: 5,
    }),
  ],
});

if (process.env.NODE_ENV !== 'production') {
  logger.add(
    new winston.transports.Console({
      format: winston.format.combine(winston.format.colorize(), winston.format.simple()),
    })
  );
}

module.exports = logger;

// Usage:
// logger.info('Server started', { port: 3000 });
// logger.error('Database connection failed', { error: err.message });
```

---

## 20. Redis Caching Middleware

```js
// middleware/cache.js
const redis = require('redis');

const client = redis.createClient({ url: process.env.REDIS_URL });

client.on('error', (err) => console.error('Redis error:', err));

const cache = (duration = 60) => {
  return async (req, res, next) => {
    const key = `cache:${req.originalUrl || req.url}`;

    try {
      const cached = await client.get(key);
      if (cached) {
        return res.json(JSON.parse(cached));
      }

      // Override res.json to cache the response
      const originalJson = res.json.bind(res);
      res.json = (body) => {
        client.setEx(key, duration, JSON.stringify(body)).catch(() => {});
        return originalJson(body);
      };

      next();
    } catch {
      // Cache miss — proceed without caching
      next();
    }
  };
};

module.exports = { cache, client };

// Usage:
// router.get('/products', cache(300), controller.getAll);
```

---

*These patterns follow a layered architecture (Routes -> Controllers -> Services -> Models/Repositories) with centralized error handling, input validation, and security best practices. Adjust imports and database schemas to match your specific stack.*
