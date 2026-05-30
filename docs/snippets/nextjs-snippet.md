# Useful Next.js Codeblock Patterns

> Practical, copy-paste-ready Next.js App Router patterns for building production applications (Next.js 15+).

---

## 1. App Router File Conventions

| File | Purpose | Component Type |
|------|---------|---------------|
| `page.tsx` | Route UI | Server by default |
| `layout.tsx` | Shared UI (persists across navigation) | Server by default |
| `template.tsx` | Shared UI (re-mounts on navigation) | Server by default |
| `loading.tsx` | Loading/Skeleton UI (Suspense boundary) | Server by default |
| `error.tsx` | Error boundary | **Must be Client** |
| `not-found.tsx` | 404 page | Server by default |
| `route.ts` | API endpoint (Route Handler) | Server |
| `global-error.tsx` | Root error boundary | **Must be Client** |
| `middleware.ts` | Request interception (project root) | Server (Edge/Node) |

---

## 2. Server Components (Default)

### Basic Server Component with Data Fetching

```tsx
// app/products/page.tsx — Server Component by default (no 'use client')
export default async function ProductsPage() {
  const products = await fetch('https://api.example.com/products', {
    next: { revalidate: 3600 }, // ISR: revalidate every hour
  }).then((res) => res.json());

  return (
    <ul>
      {products.map((p) => (
        <li key={p.id}>{p.name}</li>
      ))}
    </ul>
  );
}
```

### Server Component with Direct Database Access

```tsx
// app/dashboard/page.tsx
import { db } from '@/lib/db';

export default async function DashboardPage() {
  const userCount = await db.user.count();
  const recentOrders = await db.order.findMany({
    take: 5,
    orderBy: { createdAt: 'desc' },
  });

  return (
    <div>
      <h1>Dashboard</h1>
      <p>Users: {userCount}</p>
      <ul>
        {recentOrders.map((order) => (
          <li key={order.id}>{order.total}</li>
        ))}
      </ul>
    </div>
  );
}
```

### Server Component with Parallel Data Fetching

```tsx
// app/dashboard/page.tsx
export default async function DashboardPage() {
  // Fire all requests in parallel (no waterfall)
  const [user, posts, analytics] = await Promise.all([
    fetch('/api/user').then((r) => r.json()),
    fetch('/api/posts').then((r) => r.json()),
    fetch('/api/analytics').then((r) => r.json()),
  ]);

  return (
    <div>
      <h1>Welcome {user.name}</h1>
      <PostList posts={posts} />
      <AnalyticsChart data={analytics} />
    </div>
  );
}
```

---

## 3. Client Components

### Basic Client Component

```tsx
'use client';

import { useState } from 'react';

export default function Counter() {
  const [count, setCount] = useState(0);

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount((c) => c + 1)}>+1</button>
    </div>
  );
}
```

### Client Component with Browser API

```tsx
'use client';

import { useState, useEffect } from 'react';

export default function WindowSize() {
  const [width, setWidth] = useState(window.innerWidth);

  useEffect(() => {
    const handle = () => setWidth(window.innerWidth);
    window.addEventListener('resize', handle);
    return () => window.removeEventListener('resize', handle);
  }, []);

  return <div>Window width: {width}px</div>;
}
```

### Client Component with Event Handler

```tsx
'use client';

export default function SearchInput({ onSearch }) {
  const handleSubmit = (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    onSearch(formData.get('query'));
  };

  return (
    <form onSubmit={handleSubmit}>
      <input name="query" placeholder="Search..." />
      <button type="submit">Search</button>
    </form>
  );
}
```

---

## 4. Server + Client Composition Pattern

### Passing Server Data to Client Component (via props)

```tsx
// app/products/page.tsx — Server Component
import ProductCard from './ProductCard'; // Client Component

export default async function ProductsPage() {
  const products = await fetch('https://api.example.com/products').then((r) => r.json());

  return (
    <div>
      {products.map((product) => (
        <ProductCard key={product.id} product={product} />
      ))}
    </div>
  );
}
```

```tsx
// app/products/ProductCard.tsx — Client Component
'use client';

import { useState } from 'react';

export default function ProductCard({ product }) {
  const [liked, setLiked] = useState(false);

  return (
    <div>
      <h3>{product.name}</h3>
      <p>{product.price}</p>
      <button onClick={() => setLiked(!liked)}>
        {liked ? 'Unlike' : 'Like'}
      </button>
    </div>
  );
}
```

### Server Component as Children to Client Component

```tsx
// app/layout.tsx — Server Component
import Sidebar from './Sidebar'; // Client Component
import NavLinks from './NavLinks'; // Server Component

export default function Layout({ children }) {
  return (
    <Sidebar>
      {/* NavLinks is a Server Component — it's rendered on the server
          and passed as children to the Client Component */}
      <NavLinks />
      {children}
    </Sidebar>
  );
}
```

```tsx
// Sidebar.tsx — Client Component
'use client';

export default function Sidebar({ children }) {
  const [collapsed, setCollapsed] = useState(false);

  return (
    <aside style={{ width: collapsed ? 60 : 240 }}>
      <button onClick={() => setCollapsed(!collapsed)}>Toggle</button>
      {children}
    </aside>
  );
}
```

### Server Component with context provider

```tsx
// app/providers.tsx — Client Component
'use client';

import { createContext, useContext } from 'react';

const ThemeContext = createContext('light');

export function ThemeProvider({ children }) {
  return (
    <ThemeContext.Provider value="dark">
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  return useContext(ThemeContext);
}
```

```tsx
// app/layout.tsx — Server Component
import { ThemeProvider } from './providers';

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        <ThemeProvider>{children}</ThemeProvider>
      </body>
    </html>
  );
}
```

---

## 5. Layouts

### Root Layout

```tsx
// app/layout.tsx
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'My App',
  description: 'My Next.js application',
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <header>Site Header</header>
        <main>{children}</main>
        <footer>Site Footer</footer>
      </body>
    </html>
  );
}
```

### Nested Layout (Dashboard)

```tsx
// app/dashboard/layout.tsx
export default function DashboardLayout({ children }) {
  return (
    <div style={{ display: 'flex' }}>
      <nav style={{ width: 240 }}>
        <h2>Dashboard</h2>
        <a href="/dashboard">Overview</a>
        <a href="/dashboard/settings">Settings</a>
      </nav>
      <section style={{ flex: 1 }}>{children}</section>
    </div>
  );
}
```

### Route Group Layout

```tsx
// app/(marketing)/layout.tsx — isolated layout for marketing pages
export default function MarketingLayout({ children }) {
  return (
    <div>
      <nav>Marketing Nav</nav>
      {children}
      <footer>Marketing Footer</footer>
    </div>
  );
}

// app/(dashboard)/layout.tsx — isolated layout for dashboard pages
export default function DashboardLayout({ children }) {
  return (
    <div style={{ display: 'flex' }}>
      <DashboardSidebar />
      <main>{children}</main>
    </div>
  );
}
```

---

## 6. Dynamic Routes

### Basic Dynamic Route

```tsx
// app/products/[slug]/page.tsx
export default async function ProductPage({ params }) {
  const { slug } = await params; // params is a Promise in Next.js 15

  const product = await fetch(`https://api.example.com/products/${slug}`).then((r) => r.json());

  return (
    <div>
      <h1>{product.name}</h1>
      <p>{product.description}</p>
    </div>
  );
}
```

### generateStaticParams (SSG)

```tsx
// app/products/[slug]/page.tsx
export async function generateStaticParams() {
  const products = await fetch('https://api.example.com/products').then((r) => r.json());

  return products.map((product) => ({
    slug: product.slug,
  }));
}
```

### Catch-All Route

```tsx
// app/docs/[...slug]/page.tsx
export default async function DocPage({ params }) {
  const { slug } = await params;
  // slug is an array like ['getting-started', 'installation']

  return <div>Docs: {slug.join(' / ')}</div>;
}
```

### Optional Catch-All

```tsx
// app/blog/[[...slug]]/page.tsx — matches /blog, /blog/a, /blog/a/b
export default async function BlogPage({ params }) {
  const { slug } = await params;
  const segments = slug || [];

  return <div>Blog: {segments.join(' / ') || 'Home'}</div>;
}
```

---

## 7. Dynamic Metadata

```tsx
// app/products/[slug]/page.tsx
import type { Metadata } from 'next';

export async function generateMetadata({ params }): Promise<Metadata> {
  const { slug } = await params;
  const product = await fetch(`https://api.example.com/products/${slug}`).then((r) => r.json());

  return {
    title: product.name,
    description: product.description,
    openGraph: {
      images: [{ url: product.image }],
    },
  };
}

export default async function ProductPage({ params }) {
  // ...
}
```

---

## 8. Loading & Error UI

### Loading UI (Skeleton)

```tsx
// app/products/loading.tsx
export default function Loading() {
  return (
    <div style={{ display: 'grid', gap: 16 }}>
      {[1, 2, 3, 4].map((i) => (
        <div key={i} style={{ height: 100, background: '#e0e0e0', borderRadius: 8 }}>
          <div style={{ padding: 16, opacity: 0.5 }}>
            <div style={{ height: 20, width: '60%', background: '#ccc', marginBottom: 8 }} />
            <div style={{ height: 16, width: '40%', background: '#ddd' }} />
          </div>
        </div>
      ))}
    </div>
  );
}
```

### Error UI (must be Client Component)

```tsx
// app/products/error.tsx
'use client';

export default function Error({ error, reset }) {
  return (
    <div style={{ textAlign: 'center', padding: 48 }}>
      <h2>Something went wrong!</h2>
      <p style={{ color: '#666' }}>{error.message}</p>
      <button onClick={reset}>Try again</button>
    </div>
  );
}
```

### Granular Suspense Boundary (instead of loading.tsx)

```tsx
// app/dashboard/page.tsx
import { Suspense } from 'react';

export default function DashboardPage() {
  return (
    <div>
      <h1>Dashboard</h1>

      {/* This section streams in independently */}
      <Suspense fallback={<div>Loading posts...</div>}>
        <Posts />
      </Suspense>

      <Suspense fallback={<div>Loading analytics...</div>}>
        <Analytics />
      </Suspense>
    </div>
  );
}

async function Posts() {
  const posts = await fetch('/api/posts').then((r) => r.json());
  return <ul>{posts.map((p) => <li key={p.id}>{p.title}</li>)}</ul>;
}

async function Analytics() {
  const data = await fetch('/api/analytics').then((r) => r.json());
  return <div>Views: {data.views}</div>;
}
```

### Not Found Page

```tsx
// app/not-found.tsx
export default function NotFound() {
  return (
    <div style={{ textAlign: 'center', padding: 64 }}>
      <h1>404 — Page Not Found</h1>
      <p>The page you're looking for doesn't exist.</p>
      <a href="/">Go home</a>
    </div>
  );
}
```

---

## 9. Route Handlers (API Routes in App Router)

### Basic GET Handler

```tsx
// app/api/users/route.ts
import { NextResponse } from 'next/server';

export async function GET() {
  const users = await db.user.findMany();
  return NextResponse.json({ success: true, data: users });
}
```

### POST Handler

```tsx
// app/api/users/route.ts
import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  const body = await request.json();

  // Validate
  if (!body.email || !body.name) {
    return NextResponse.json(
      { error: 'Email and name are required' },
      { status: 400 }
    );
  }

  const user = await db.user.create({ data: body });
  return NextResponse.json({ success: true, data: user }, { status: 201 });
}
```

### Dynamic Route Handler

```tsx
// app/api/users/[id]/route.ts
import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest, { params }) {
  const { id } = await params;

  const user = await db.user.findUnique({ where: { id } });
  if (!user) {
    return NextResponse.json({ error: 'User not found' }, { status: 404 });
  }

  return NextResponse.json({ success: true, data: user });
}

export async function PATCH(request: NextRequest, { params }) {
  const { id } = await params;
  const body = await request.json();

  const user = await db.user.update({ where: { id }, data: body });
  return NextResponse.json({ success: true, data: user });
}

export async function DELETE(request: NextRequest, { params }) {
  const { id } = await params;

  await db.user.delete({ where: { id } });
  return NextResponse.json({ success: true }, { status: 200 });
}
```

### Route Handler with Auth

```tsx
// app/api/posts/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { getServerSession } from 'next-auth';
import { authOptions } from '@/lib/auth';

export async function POST(request: NextRequest) {
  const session = await getServerSession(authOptions);

  if (!session) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  const body = await request.json();
  const post = await db.post.create({
    data: { ...body, authorId: session.user.id },
  });

  return NextResponse.json({ success: true, data: post }, { status: 201 });
}
```

### Search Params in Route Handler

```tsx
// app/api/products/route.ts
import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const page = parseInt(searchParams.get('page') || '1');
  const limit = parseInt(searchParams.get('limit') || '10');
  const category = searchParams.get('category');

  const where = category ? { category } : {};
  const [data, total] = await Promise.all([
    db.product.findMany({
      where,
      skip: (page - 1) * limit,
      take: limit,
    }),
    db.product.count({ where }),
  ]);

  return NextResponse.json({
    success: true,
    data,
    meta: { page, limit, total, totalPages: Math.ceil(total / limit) },
  });
}
```

---

## 10. Server Actions

### Basic Server Action with Form

```tsx
// app/actions.ts
'use server';

import { revalidatePath } from 'next/cache';
import { redirect } from 'next/navigation';
import { db } from '@/lib/db';

export async function createPost(formData: FormData) {
  const title = formData.get('title');
  const content = formData.get('content');

  await db.post.create({
    data: { title, content },
  });

  revalidatePath('/blog');
  redirect('/blog');
}
```

```tsx
// app/blog/new/page.tsx
import { createPost } from '@/app/actions';

export default function NewPostPage() {
  return (
    <form action={createPost}>
      <input name="title" placeholder="Title" required />
      <textarea name="content" placeholder="Content" required />
      <button type="submit">Create Post</button>
    </form>
  );
}
```

### Server Action with Validation (Zod)

```tsx
// app/actions.ts
'use server';

import { z } from 'zod';
import { revalidatePath } from 'next/cache';
import { redirect } from 'next/navigation';
import { db } from '@/lib/db';

const PostSchema = z.object({
  title: z.string().min(3).max(100),
  content: z.string().min(10).max(5000),
});

export async function createPost(formData: FormData) {
  const parsed = PostSchema.safeParse({
    title: formData.get('title'),
    content: formData.get('content'),
  });

  if (!parsed.success) {
    return { error: parsed.error.flatten().fieldErrors };
  }

  await db.post.create({ data: parsed.data });

  revalidatePath('/blog');
  redirect('/blog');
}
```

### Server Action with useActionState (Loading + Errors)

```tsx
// app/actions.ts
'use server';

import { revalidatePath } from 'next/cache';
import { db } from '@/lib/db';

export async function createPost(prevState, formData) {
  const title = formData.get('title');
  const content = formData.get('content');

  if (!title || title.length < 3) {
    return { error: 'Title must be at least 3 characters' };
  }

  await db.post.create({ data: { title, content } });

  revalidatePath('/blog');
  return { success: true };
}
```

```tsx
// app/blog/new/page.tsx
'use client';

import { useActionState } from 'react';
import { createPost } from '@/app/actions';

export default function NewPostForm() {
  const [state, formAction, pending] = useActionState(createPost, null);

  return (
    <form action={formAction}>
      <input name="title" placeholder="Title" required />
      <textarea name="content" placeholder="Content" required />
      <button type="submit" disabled={pending}>
        {pending ? 'Creating...' : 'Create Post'}
      </button>
      {state?.error && <p style={{ color: 'red' }}>{state.error}</p>}
      {state?.success && <p style={{ color: 'green' }}>Post created!</p>}
    </form>
  );
}
```

### Server Action Called from Client Event Handler

```tsx
// app/actions.ts
'use server';

import { revalidatePath } from 'next/cache';

export async function toggleLike(postId, userId) {
  const existing = await db.like.findUnique({
    where: { postId_userId: { postId, userId } },
  });

  if (existing) {
    await db.like.delete({ where: { id: existing.id } });
  } else {
    await db.like.create({ data: { postId, userId } });
  }

  revalidatePath(`/posts/${postId}`);
}
```

```tsx
// app/components/LikeButton.tsx
'use client';

import { toggleLike } from '@/app/actions';

export default function LikeButton({ postId, userId, initialLiked }) {
  const [liked, setLiked] = useState(initialLiked);

  const handleClick = async () => {
    setLiked(!liked); // optimistic update
    await toggleLike(postId, userId);
  };

  return (
    <button onClick={handleClick}>
      {liked ? 'Unlike' : 'Like'}
    </button>
  );
}
```

### Server Action with useOptimistic

```tsx
// app/components/MessageList.tsx
'use client';

import { useOptimistic, useRef } from 'react';
import { sendMessage } from '@/app/actions';

export default function MessageList({ messages }) {
  const [optimisticMessages, addOptimistic] = useOptimistic(
    messages,
    (state, newMessage) => [...state, { text: newMessage, sending: true }]
  );

  const formRef = useRef(null);

  const formAction = async (formData) => {
    const message = formData.get('message');
    addOptimistic(message);
    formRef.current?.reset();
    await sendMessage(formData);
  };

  return (
    <form action={formAction} ref={formRef}>
      <ul>
        {optimisticMessages.map((msg, i) => (
          <li key={i} style={{ opacity: msg.sending ? 0.5 : 1 }}>
            {msg.text} {msg.sending && '(sending...)'}
          </li>
        ))}
      </ul>
      <input name="message" required />
      <button type="submit">Send</button>
    </form>
  );
}
```

### Server Action with Auth Check

```tsx
// app/actions.ts
'use server';

import { getServerSession } from 'next-auth';
import { authOptions } from '@/lib/auth';
import { revalidatePath } from 'next/cache';

export async function deletePost(postId) {
  const session = await getServerSession(authOptions);
  if (!session) throw new Error('Unauthenticated');

  const post = await db.post.findUnique({ where: { id: postId } });
  if (!post) throw new Error('Post not found');
  if (post.authorId !== session.user.id) throw new Error('Forbidden');

  await db.post.delete({ where: { id: postId } });
  revalidatePath('/dashboard');
}
```

---

## 11. Middleware

### Basic Auth Middleware

```tsx
// middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request) {
  const { pathname } = request.nextUrl;
  const token = request.cookies.get('session')?.value;

  // Public paths — no auth needed
  const publicPaths = ['/login', '/signup', '/', '/api/auth'];
  if (publicPaths.some((p) => pathname.startsWith(p))) {
    return NextResponse.next();
  }

  // Redirect to login if not authenticated
  if (!token) {
    const loginUrl = new URL('/login', request.url);
    loginUrl.searchParams.set('callbackUrl', pathname);
    return NextResponse.redirect(loginUrl);
  }

  return NextResponse.next();
}

export const config = {
  matcher: ['/((?!_next/static|_next/image|favicon.ico).*)'],
};
```

### Middleware with Role-Based Access

```tsx
// middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';
import { jwtVerify } from 'jose';

export async function middleware(request) {
  const { pathname } = request.nextUrl;
  const token = request.cookies.get('session')?.value;

  const publicPaths = ['/login', '/signup', '/'];
  if (publicPaths.some((p) => pathname.startsWith(p))) {
    return NextResponse.next();
  }

  if (!token) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  try {
    const { payload } = await jwtVerify(
      token,
      new TextEncoder().encode(process.env.JWT_SECRET)
    );
    const role = payload.role;

    // Role-based redirects
    if (pathname.startsWith('/admin') && role !== 'admin') {
      return NextResponse.redirect(new URL('/unauthorized', request.url));
    }

    // Pass role to Server Components via header
    const headers = new Headers(request.headers);
    headers.set('x-user-role', role);

    return NextResponse.next({ request: { headers } });
  } catch {
    return NextResponse.redirect(new URL('/login', request.url));
  }
}

export const config = {
  matcher: ['/((?!api|_next/static|_next/image|favicon.ico).*)'],
};
```

### Middleware with Redirects and Headers

```tsx
// middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request) {
  const { pathname, searchParams } = request.nextUrl;

  // Redirect old URLs
  if (pathname.startsWith('/old-blog')) {
    return NextResponse.redirect(new URL('/blog', request.url));
  }

  // Set security headers
  const response = NextResponse.next();
  response.headers.set('X-Frame-Options', 'DENY');
  response.headers.set('X-Content-Type-Options', 'nosniff');
  response.headers.set('Referrer-Policy', 'strict-origin-when-cross-origin');

  return response;
}
```

---

## 12. Data Fetching Patterns

### Fetch with Caching Options

```tsx
// Next.js 15: fetch is NOT cached by default — opt in explicitly

// Static data (cached until redeploy)
const data = await fetch('https://api.example.com/data', {
  cache: 'force-cache',
});

// Revalidate every 60 seconds (ISR)
const data = await fetch('https://api.example.com/data', {
  next: { revalidate: 60 },
});

// Dynamic data (no cache)
const data = await fetch('https://api.example.com/data', {
  cache: 'no-store',
});

// On-demand revalidation with tags
const data = await fetch('https://api.example.com/data', {
  next: { tags: ['products'] },
});
// Later: revalidateTag('products') in a Server Action
```

### Data Fetching with Error Handling

```tsx
// app/products/page.tsx
export default async function ProductsPage() {
  let products;

  try {
    const res = await fetch('https://api.example.com/products', {
      next: { revalidate: 3600 },
    });
    if (!res.ok) throw new Error('Failed to fetch');
    products = await res.json();
  } catch (error) {
    // Will be caught by the nearest error.tsx boundary
    throw new Error('Failed to load products. Please try again.');
  }

  return (
    <ul>
      {products.map((p) => (
        <li key={p.id}>{p.name}</li>
      ))}
    </ul>
  );
}
```

### Revalidate on Demand (after mutation)

```tsx
'use server';

import { revalidatePath, revalidateTag } from 'next/cache';

export async function updateProduct(formData) {
  // ... update DB

  // Revalidate a specific path
  revalidatePath('/products');

  // Or revalidate by tag (for fetch with next: { tags: ['products'] })
  revalidateTag('products');
}
```

### Infinite Scroll with Client Fetching

```tsx
// app/posts/page.tsx — Server Component (initial data)
export default async function PostsPage() {
  const initialPosts = await fetch('/api/posts?page=1').then((r) => r.json());

  return <PostListWithLoadMore initialPosts={initialPosts} />;
}
```

```tsx
// app/posts/PostListWithLoadMore.tsx — Client Component
'use client';

import { useState } from 'react';

export default function PostListWithLoadMore({ initialPosts }) {
  const [posts, setPosts] = useState(initialPosts.data);
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(false);
  const [hasMore, setHasMore] = useState(initialPosts.meta.hasNext);

  const loadMore = async () => {
    setLoading(true);
    const nextPage = page + 1;
    const res = await fetch(`/api/posts?page=${nextPage}`).then((r) => r.json());
    setPosts((prev) => [...prev, ...res.data]);
    setPage(nextPage);
    setHasMore(res.meta.hasNext);
    setLoading(false);
  };

  return (
    <div>
      {posts.map((post) => <div key={post.id}>{post.title}</div>)}
      {hasMore && (
        <button onClick={loadMore} disabled={loading}>
          {loading ? 'Loading...' : 'Load more'}
        </button>
      )}
    </div>
  );
}
```

---

## 13. Authentication (NextAuth.js v5)

### Route Protection in Server Component

```tsx
// app/dashboard/page.tsx
import { getServerSession } from 'next-auth';
import { authOptions } from '@/lib/auth';
import { redirect } from 'next/navigation';

export default async function DashboardPage() {
  const session = await getServerSession(authOptions);

  if (!session) {
    redirect('/login');
  }

  return (
    <div>
      <h1>Welcome, {session.user.name}</h1>
    </div>
  );
}
```

### Auth in Server Action

```tsx
'use server';

import { getServerSession } from 'next-auth';
import { authOptions } from '@/lib/auth';
import { revalidatePath } from 'next/cache';

export async function updateProfile(formData) {
  const session = await getServerSession(authOptions);
  if (!session) throw new Error('Unauthorized');

  await db.user.update({
    where: { email: session.user.email },
    data: { name: formData.get('name') },
  });

  revalidatePath('/dashboard');
}
```

### Auth in Route Handler

```tsx
// app/api/profile/route.ts
import { NextResponse } from 'next/server';
import { getServerSession } from 'next-auth';
import { authOptions } from '@/lib/auth';

export async function GET() {
  const session = await getServerSession(authOptions);

  if (!session) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  const user = await db.user.findUnique({
    where: { email: session.user.email },
    select: { id: true, name: true, email: true },
  });

  return NextResponse.json({ success: true, data: user });
}
```

---

## 14. Dynamic Imports / Code Splitting

```tsx
// Lazy-load a heavy client component
import dynamic from 'next/dynamic';

const HeavyChart = dynamic(() => import('@/components/HeavyChart'), {
  loading: () => <div style={{ height: 400, background: '#f0f0f0' }}>Loading chart...</div>,
  ssr: false, // Skip SSR if it uses browser APIs
});

export default function Dashboard() {
  return (
    <div>
      <h1>Dashboard</h1>
      <HeavyChart />
    </div>
  );
}
```

### Dynamic Import with Named Export

```tsx
const MarkdownEditor = dynamic(
  () => import('@/components/Editor').then((mod) => mod.MarkdownEditor),
  { loading: () => <div>Loading editor...</div> }
);
```

---

## 15. Search Params (URL State)

```tsx
// app/products/page.tsx — read search params
export default async function ProductsPage({ searchParams }) {
  const { q, page, sort } = await searchParams;
  const currentPage = parseInt(page || '1');
  const currentSort = sort || 'name';

  const products = await db.product.findMany({
    where: q ? { name: { contains: q } } : {},
    orderBy: { [currentSort]: 'asc' },
    skip: (currentPage - 1) * 20,
    take: 20,
  });

  return <ProductList products={products} />;
}
```

### Client-Side Search Params (useSearchParams)

```tsx
'use client';

import { useSearchParams, useRouter, usePathname } from 'next/navigation';

export default function SearchBar() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const pathname = usePathname();

  const handleSearch = (term) => {
    const params = new URLSearchParams(searchParams);
    if (term) {
      params.set('q', term);
    } else {
      params.delete('q');
    }
    params.set('page', '1');
    router.replace(`${pathname}?${params.toString()}`);
  };

  return (
    <input
      defaultValue={searchParams.get('q') || ''}
      onChange={(e) => handleSearch(e.target.value)}
      placeholder="Search..."
    />
  );
}
```

---

## 16. Parallel Routes

```tsx
// app/dashboard/layout.tsx
export default function DashboardLayout({ children, analytics, notifications }) {
  return (
    <div style={{ display: 'grid', gridTemplateColumns: '1fr 300px', gap: 24 }}>
      <main>{children}</main>
      <aside style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
        {analytics}
        {notifications}
      </aside>
    </div>
  );
}
```

```tsx
// app/dashboard/@analytics/page.tsx
export default async function Analytics() {
  const data = await fetch('/api/analytics').then((r) => r.json());
  return <div>Views: {data.views}</div>;
}
```

```tsx
// app/dashboard/@notifications/page.tsx
export default async function Notifications() {
  const notifs = await fetch('/api/notifications').then((r) => r.json());
  return (
    <ul>
      {notifs.map((n) => <li key={n.id}>{n.text}</li>)}
    </ul>
  );
}
```

```tsx
// app/dashboard/@notifications/default.tsx — required for parallel routes
export default function Default() {
  return <div>No notifications</div>;
}
```

---

## 17. Intercepting Routes (Modal Pattern)

```
app/
  @modal/
    (.)photo/[id]/page.tsx    # Intercept photo route within same level
  photo/
    [id]/page.tsx              # Full photo page on direct access
  layout.tsx                   # Root layout with modal slot
```

```tsx
// app/layout.tsx
export default function RootLayout({ children, modal }) {
  return (
    <html>
      <body>
        {children}
        {modal}
      </body>
    </html>
  );
}
```

```tsx
// app/@modal/(.)photo/[id]/page.tsx — intercepts /photo/123 for modal
'use client';

import { useRouter } from 'next/navigation';

export default function PhotoModal({ params }) {
  const router = useRouter();

  return (
    <div
      style={{ position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.5)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 1000 }}
      onClick={() => router.back()}
    >
      <div style={{ background: '#fff', padding: 24, borderRadius: 8 }} onClick={(e) => e.stopPropagation()}>
        <h2>Photo {params.id}</h2>
        <img src={`/photos/${params.id}`} alt="" />
      </div>
    </div>
  );
}
```

---

## 18. ISR (Incremental Static Regeneration)

```tsx
// app/products/[slug]/page.tsx
export default async function ProductPage({ params }) {
  const { slug } = await params;

  const product = await fetch(`https://api.example.com/products/${slug}`, {
    next: { revalidate: 60 }, // Revalidate every 60 seconds
  }).then((r) => r.json());

  return (
    <div>
      <h1>{product.name}</h1>
      <p>{product.price}</p>
    </div>
  );
}

// Pre-render the most popular products at build time
export async function generateStaticParams() {
  const products = await fetch('https://api.example.com/products?limit=10').then((r) => r.json());
  return products.map((p) => ({ slug: p.slug }));
}
```

---

## 19. Environment Variables

```tsx
// ✅ Public (exposed to client): prefix with NEXT_PUBLIC_
// NEXT_PUBLIC_API_URL=https://api.example.com
const apiUrl = process.env.NEXT_PUBLIC_API_URL;

// ✅ Private (server-only, never exposed to client)
// DATABASE_URL=postgresql://...
// Only accessible in Server Components, Route Handlers, Server Actions
import { db } from '@/lib/db';

// ✅ Protect secrets with 'server-only' package
// lib/secrets.ts
import 'server-only';

export const apiKey = process.env.INTERNAL_API_KEY;
// If imported in a Client Component, this will fail at build time
```

---

## 20. Server-Sent Events (SSE) Route Handler

```tsx
// app/api/events/route.ts
import { NextRequest } from 'next/server';

export async function GET(request) {
  const stream = new ReadableStream({
    start(controller) {
      // Send initial data
      controller.enqueue(`data: ${JSON.stringify({ connected: true })}\n\n`);

      const interval = setInterval(() => {
        controller.enqueue(`data: ${JSON.stringify({ time: Date.now() })}\n\n`);
      }, 1000);

      request.signal.addEventListener('abort', () => {
        clearInterval(interval);
        controller.close();
      });
    },
  });

  return new Response(stream, {
    headers: {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      Connection: 'keep-alive',
    },
  });
}
```

---

## 21. Testing

```tsx
// __tests__/page.test.tsx
import { render, screen } from '@testing-library/react';
import Page from '@/app/page';

// Mock fetch globally
global.fetch = jest.fn(() =>
  Promise.resolve({
    ok: true,
    json: () => Promise.resolve([{ id: 1, name: 'Test Product' }]),
  })
);

describe('Products Page', () => {
  it('renders products', async () => {
    const PageComponent = await Page();
    render(PageComponent);

    expect(screen.getByText('Test Product')).toBeInTheDocument();
  });
});
```

```tsx
// __tests__/api.test.ts
import { GET } from '@/app/api/users/route';
import { NextRequest } from 'next/server';

describe('GET /api/users', () => {
  it('returns users list', async () => {
    const request = new NextRequest(new URL('http://localhost/api/users'));
    const response = await GET();
    const body = await response.json();

    expect(response.status).toBe(200);
    expect(body.success).toBe(true);
  });
});
```

---

## 22. Image Optimization

```tsx
import Image from 'next/image';

export default function ProductImage({ src, alt, priority = false }) {
  return (
    <Image
      src={src}
      alt={alt}
      width={800}
      height={600}
      priority={priority} // Use for above-the-fold images
      placeholder="blur"   // Requires blurDataURL
      sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
    />
  );
}
```

---

## 23. Redirects

### In Server Components

```tsx
import { redirect } from 'next/navigation';

export default async function OldPage() {
  redirect('/new-page');
}
```

### In Server Actions

```tsx
'use server';
import { redirect } from 'next/navigation';

export async function submitForm(formData) {
  // ... save to DB
  redirect('/success');
}
```

### In middleware

```tsx
// middleware.ts
export function middleware(request) {
  if (request.nextUrl.pathname === '/old-page') {
    return NextResponse.redirect(new URL('/new-page', request.url));
  }
}
```

---

*These patterns target Next.js 15+ with the App Router. The key mental model: **Server Components** for data & layout, **Client Components** for interactivity, **Server Actions** for mutations, **Route Handlers** for external HTTP endpoints. Start on the server — add `'use client'` only where needed.*
