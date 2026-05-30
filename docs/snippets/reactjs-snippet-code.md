# Useful ReactJS Codeblock Snippets

> Practical, copy-paste-ready React code examples for real projects.

---

## 1. Functional Components

### Basic Function Component

```jsx
export default function MyComponent() {
  return <div>MyComponent</div>;
}
```

### Function Component with Props

```jsx
export default function Greeting({ name }) {
  return <div>Hello, {name}!</div>;
}
```

### Arrow Function Component (exported)

```jsx
const MyComponent = () => {
  return <div>MyComponent</div>;
};

export default MyComponent;
```

### TypeScript Function Component with Props

```tsx
type Props = {
  title: string;
  count: number;
  children?: React.ReactNode;
};

export default function Card({ title, count, children }: Props) {
  return (
    <div>
      <h2>
        {title} ({count})
      </h2>
      {children}
    </div>
  );
}
```

### React.memo Component

```jsx
import { memo } from "react";

const ExpensiveList = memo(({ items }) => {
  return (
    <ul>
      {items.map((item) => (
        <li key={item.id}>{item.name}</li>
      ))}
    </ul>
  );
});

export default ExpensiveList;
```

### Component with Children (Slot Pattern)

```jsx
export default function Panel({ title, children }) {
  return (
    <div className="panel">
      <div className="panel-header">{title}</div>
      <div className="panel-body">{children}</div>
    </div>
  );
}

// Usage:
// <Panel title="Settings">
//   <p>Some content here</p>
// </Panel>
```

---

## 2. useState Patterns

### Basic Counter

```jsx
import { useState } from "react";

export default function Counter() {
  const [count, setCount] = useState(0);

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount((c) => c + 1)}>+1</button>
      <button onClick={() => setCount(0)}>Reset</button>
    </div>
  );
}
```

### Toggle (boolean state)

```jsx
import { useState } from "react";

export default function Toggle() {
  const [isOn, setIsOn] = useState(false);

  return (
    <button onClick={() => setIsOn((prev) => !prev)}>
      {isOn ? "ON" : "OFF"}
    </button>
  );
}
```

### Controlled Input

```jsx
import { useState } from "react";

export default function Form() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log({ name, email });
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        value={name}
        onChange={(e) => setName(e.target.value)}
        placeholder="Name"
      />
      <input
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Email"
      />
      <button type="submit">Submit</button>
    </form>
  );
}
```

### Derived State (no useEffect needed)

```jsx
import { useState, useMemo } from "react";

export default function ProductList({ products }) {
  const [filter, setFilter] = useState("");

  // Derived state — no useEffect needed
  const filtered = useMemo(() => {
    return products.filter((p) =>
      p.name.toLowerCase().includes(filter.toLowerCase()),
    );
  }, [products, filter]);

  return (
    <div>
      <input
        value={filter}
        onChange={(e) => setFilter(e.target.value)}
        placeholder="Search..."
      />
      <ul>
        {filtered.map((p) => (
          <li key={p.id}>{p.name}</li>
        ))}
      </ul>
    </div>
  );
}
```

---

## 3. useEffect Patterns

### Basic useEffect (data fetching)

```jsx
import { useState, useEffect } from "react";

export default function UserProfile({ userId }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let ignore = false;

    setLoading(true);
    fetch(`/api/users/${userId}`)
      .then((res) => {
        if (!res.ok) throw new Error("Failed to fetch");
        return res.json();
      })
      .then((data) => {
        if (!ignore) {
          setUser(data);
          setLoading(false);
        }
      })
      .catch((err) => {
        if (!ignore) {
          setError(err.message);
          setLoading(false);
        }
      });

    return () => {
      ignore = true;
    };
  }, [userId]);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;
  return <div>{user?.name}</div>;
}
```

### useEffect with Cleanup (event listeners)

```jsx
import { useState, useEffect } from "react";

export default function WindowTracker() {
  const [width, setWidth] = useState(window.innerWidth);

  useEffect(() => {
    const handleResize = () => setWidth(window.innerWidth);

    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  return <div>Window width: {width}px</div>;
}
```

### useEffect with Timer (setInterval)

```jsx
import { useState, useEffect } from "react";

export default function Timer() {
  const [seconds, setSeconds] = useState(0);

  useEffect(() => {
    const id = setInterval(() => {
      setSeconds((s) => s + 1);
    }, 1000);

    return () => clearInterval(id);
  }, []);

  return <div>Elapsed: {seconds}s</div>;
}
```

### Debounced Search Effect

```jsx
import { useState, useEffect } from "react";

export default function SearchResults() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);

  useEffect(() => {
    if (!query.trim()) {
      setResults([]);
      return;
    }

    const timer = setTimeout(async () => {
      const res = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
      const data = await res.json();
      setResults(data);
    }, 300);

    return () => clearTimeout(timer);
  }, [query]);

  return (
    <div>
      <input
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Search..."
      />
      <ul>
        {results.map((r) => (
          <li key={r.id}>{r.name}</li>
        ))}
      </ul>
    </div>
  );
}
```

### AbortController for Fetch Cleanup

```jsx
import { useState, useEffect } from "react";

export default function Search({ query }) {
  const [results, setResults] = useState([]);

  useEffect(() => {
    const controller = new AbortController();

    fetch(`/api/search?q=${query}`, { signal: controller.signal })
      .then((res) => res.json())
      .then(setResults)
      .catch((err) => {
        if (err.name !== "AbortError") console.error(err);
      });

    return () => controller.abort();
  }, [query]);

  return (
    <ul>
      {results.map((r) => (
        <li key={r.id}>{r.name}</li>
      ))}
    </ul>
  );
}
```

---

## 4. useRef Patterns

### Focus Input

```jsx
import { useRef } from "react";

export default function Form() {
  const inputRef = useRef(null);

  const focusInput = () => {
    inputRef.current?.focus();
  };

  return (
    <div>
      <input ref={inputRef} type="text" placeholder="Focus me" />
      <button onClick={focusInput}>Focus Input</button>
    </div>
  );
}
```

### Track Previous Value

```jsx
import { useState, useRef, useEffect } from "react";

export default function Counter() {
  const [count, setCount] = useState(0);
  const prevCountRef = useRef();

  useEffect(() => {
    prevCountRef.current = count;
  });

  const prevCount = prevCountRef.current;

  return (
    <div>
      <p>
        Now: {count}, before: {prevCount}
      </p>
      <button onClick={() => setCount((c) => c + 1)}>Increment</button>
    </div>
  );
}
```

### Stopwatch (interval ID in ref)

```jsx
import { useState, useRef } from "react";

export default function Stopwatch() {
  const [startTime, setStartTime] = useState(null);
  const [now, setNow] = useState(null);
  const intervalRef = useRef(null);

  const handleStart = () => {
    setStartTime(Date.now());
    setNow(Date.now());
    clearInterval(intervalRef.current);
    intervalRef.current = setInterval(() => {
      setNow(Date.now());
    }, 10);
  };

  const handleStop = () => {
    clearInterval(intervalRef.current);
  };

  const secondsPassed = startTime && now ? (now - startTime) / 1000 : 0;

  return (
    <div>
      <h1>Time: {secondsPassed.toFixed(3)}s</h1>
      <button onClick={handleStart}>Start</button>
      <button onClick={handleStop}>Stop</button>
    </div>
  );
}
```

### Reading Latest State in Async Code

```jsx
import { useState, useRef } from "react";

export default function Chat() {
  const [text, setText] = useState("");
  const textRef = useRef(text);

  const handleChange = (e) => {
    setText(e.target.value);
    textRef.current = e.target.value;
  };

  const handleSend = () => {
    setTimeout(() => {
      alert("Sending: " + textRef.current);
    }, 3000);
  };

  return (
    <div>
      <input value={text} onChange={handleChange} />
      <button onClick={handleSend}>Send</button>
    </div>
  );
}
```

---

## 5. useMemo & useCallback

### Expensive Computation with useMemo

```jsx
import { useMemo } from "react";

export default function Report({ transactions }) {
  const totals = useMemo(() => {
    return transactions.reduce(
      (acc, t) => {
        acc.total += t.amount;
        acc.count += 1;
        return acc;
      },
      { total: 0, count: 0 },
    );
  }, [transactions]);

  return (
    <div>
      <p>Total: ${totals.total}</p>
      <p>Count: {totals.count}</p>
    </div>
  );
}
```

### Stable Callback with useCallback

```jsx
import { useState, useCallback } from "react";
import { memo } from "react";

const ExpensiveChild = memo(({ onClick }) => {
  return <button onClick={onClick}>Click me</button>;
});

export default function Parent() {
  const [count, setCount] = useState(0);

  const handleClick = useCallback(() => {
    setCount((c) => c + 1);
  }, []);

  return (
    <div>
      <p>Count: {count}</p>
      <ExpensiveChild onClick={handleClick} />
    </div>
  );
}
```

---

## 6. useReducer

### Basic useReducer

```jsx
import { useReducer } from "react";

const reducer = (state, action) => {
  switch (action.type) {
    case "increment":
      return { count: state.count + 1 };
    case "decrement":
      return { count: state.count - 1 };
    case "reset":
      return { count: 0 };
    default:
      return state;
  }
};

export default function Counter() {
  const [state, dispatch] = useReducer(reducer, { count: 0 });

  return (
    <div>
      <p>Count: {state.count}</p>
      <button onClick={() => dispatch({ type: "increment" })}>+</button>
      <button onClick={() => dispatch({ type: "decrement" })}>-</button>
      <button onClick={() => dispatch({ type: "reset" })}>Reset</button>
    </div>
  );
}
```

### Async State Reducer

```jsx
import { useReducer } from "react";

const initialState = {
  data: null,
  loading: false,
  error: null,
};

const reducer = (state, action) => {
  switch (action.type) {
    case "fetch":
      return { ...state, loading: true, error: null };
    case "success":
      return { loading: false, data: action.payload, error: null };
    case "error":
      return { loading: false, data: null, error: action.payload };
    default:
      return state;
  }
};

export default function UserProfile({ userId }) {
  const [state, dispatch] = useReducer(reducer, initialState);

  const loadUser = async () => {
    dispatch({ type: "fetch" });
    try {
      const res = await fetch(`/api/users/${userId}`);
      if (!res.ok) throw new Error("Not found");
      const data = await res.json();
      dispatch({ type: "success", payload: data });
    } catch (err) {
      dispatch({ type: "error", payload: err.message });
    }
  };

  // ...
}
```

---

## 7. useContext + useReducer (State Management)

### Context Provider with Reducer

```jsx
import { createContext, useContext, useReducer } from "react";

const AuthContext = createContext(null);
const AuthDispatchContext = createContext(null);

const authReducer = (state, action) => {
  switch (action.type) {
    case "login":
      return { ...state, user: action.payload };
    case "logout":
      return { ...state, user: null };
    default:
      return state;
  }
};

export function AuthProvider({ children }) {
  const [state, dispatch] = useReducer(authReducer, { user: null });

  return (
    <AuthContext.Provider value={state}>
      <AuthDispatchContext.Provider value={dispatch}>
        {children}
      </AuthDispatchContext.Provider>
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}

export function useAuthDispatch() {
  return useContext(AuthDispatchContext);
}
```

### Using the Context

```jsx
import { useAuth, useAuthDispatch } from "./AuthProvider";

export default function LoginButton() {
  const { user } = useAuth();
  const dispatch = useAuthDispatch();

  if (user) {
    return (
      <div>
        Welcome, {user.name}
        <button onClick={() => dispatch({ type: "logout" })}>Logout</button>
      </div>
    );
  }

  const login = () => {
    dispatch({ type: "login", payload: { name: "Alice" } });
  };

  return <button onClick={login}>Login</button>;
}
```

---

## 8. Custom Hooks

### useFetch

```jsx
import { useState, useEffect } from "react";

export function useFetch(url) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!url) return;

    let ignore = false;
    const controller = new AbortController();

    setLoading(true);
    fetch(url, { signal: controller.signal })
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
      })
      .then((json) => {
        if (!ignore) {
          setData(json);
          setLoading(false);
        }
      })
      .catch((err) => {
        if (!ignore && err.name !== "AbortError") {
          setError(err.message);
          setLoading(false);
        }
      });

    return () => {
      ignore = true;
      controller.abort();
    };
  }, [url]);

  return { data, loading, error };
}

// Usage:
// const { data, loading, error } = useFetch('/api/users');
```

### useDebounce

```jsx
import { useState, useEffect } from "react";

export function useDebounce(value, delay = 300) {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const timer = setTimeout(() => setDebouncedValue(value), delay);
    return () => clearTimeout(timer);
  }, [value, delay]);

  return debouncedValue;
}

// Usage:
// const debouncedQuery = useDebounce(query, 500);
```

### useLocalStorage

```jsx
import { useState } from "react";

export function useLocalStorage(key, initialValue) {
  const [value, setValue] = useState(() => {
    try {
      const stored = localStorage.getItem(key);
      return stored ? JSON.parse(stored) : initialValue;
    } catch {
      return initialValue;
    }
  });

  const setStoredValue = (newValue) => {
    setValue(newValue);
    localStorage.setItem(key, JSON.stringify(newValue));
  };

  return [value, setStoredValue];
}

// Usage:
// const [name, setName] = useLocalStorage('name', '');
```

### useOnlineStatus

```jsx
import { useState, useEffect } from "react";

export function useOnlineStatus() {
  const [isOnline, setIsOnline] = useState(navigator.onLine);

  useEffect(() => {
    const goOnline = () => setIsOnline(true);
    const goOffline = () => setIsOnline(false);

    window.addEventListener("online", goOnline);
    window.addEventListener("offline", goOffline);
    return () => {
      window.removeEventListener("online", goOnline);
      window.removeEventListener("offline", goOffline);
    };
  }, []);

  return isOnline;
}

// Usage:
// const isOnline = useOnlineStatus();
```

### useWindowSize

```jsx
import { useState, useEffect } from "react";

export function useWindowSize() {
  const [size, setSize] = useState({
    width: window.innerWidth,
    height: window.innerHeight,
  });

  useEffect(() => {
    const handleResize = () => {
      setSize({ width: window.innerWidth, height: window.innerHeight });
    };

    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  return size;
}

// Usage:
// const { width, height } = useWindowSize();
```

### useCounter

```jsx
import { useState } from "react";

export function useCounter(initialValue = 0) {
  const [count, setCount] = useState(initialValue);

  const increment = () => setCount((prev) => prev + 1);
  const decrement = () => setCount((prev) => prev - 1);
  const reset = () => setCount(initialValue);
  const set = (n) => setCount(n);

  return { count, increment, decrement, reset, set };
}

// Usage:
// const { count, increment, decrement, reset } = useCounter(10);
```

### useIntersectionObserver (infinite scroll)

```jsx
import { useEffect, useRef, useState } from "react";

export function useIntersectionObserver(options = {}) {
  const ref = useRef(null);
  const [isIntersecting, setIsIntersecting] = useState(false);

  useEffect(() => {
    const element = ref.current;
    if (!element) return;

    const observer = new IntersectionObserver(
      ([entry]) => {
        setIsIntersecting(entry.isIntersecting);
      },
      { threshold: 0.1, ...options },
    );

    observer.observe(element);
    return () => observer.disconnect();
  }, [ref.current, options.threshold, options.rootMargin]);

  return [ref, isIntersecting];
}

// Usage:
// const [sentinelRef, isVisible] = useIntersectionObserver();
// useEffect(() => { if (isVisible) loadMore(); }, [isVisible]);
```

### usePrevious

```jsx
import { useRef, useEffect } from "react";

export function usePrevious(value) {
  const ref = useRef();

  useEffect(() => {
    ref.current = value;
  });

  return ref.current;
}

// Usage:
// const prevCount = usePrevious(count);
```

---

## 9. Event Handlers

### Form Submit

```jsx
import { useState } from "react";

export default function LoginForm() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    const res = await fetch("/api/login", {
      method: "POST",
      body: JSON.stringify({ email, password }),
      headers: { "Content-Type": "application/json" },
    });
    if (res.ok) {
      // redirect or update state
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <button type="submit">Login</button>
    </form>
  );
}
```

### Inline Change Handler (dynamic fields)

```jsx
import { useState } from "react";

export default function DynamicForm() {
  const [fields, setFields] = useState({ name: "", email: "", role: "" });

  const handleChange = (e) => {
    setFields((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  };

  return (
    <form>
      <input name="name" value={fields.name} onChange={handleChange} />
      <input name="email" value={fields.email} onChange={handleChange} />
      <input name="role" value={fields.role} onChange={handleChange} />
    </form>
  );
}
```

---

## 10. List Rendering

### Basic List with Map

```jsx
export default function UserList({ users }) {
  return (
    <ul>
      {users.map((user) => (
        <li key={user.id}>
          {user.name} - {user.email}
        </li>
      ))}
    </ul>
  );
}
```

### Filterable List

```jsx
import { useState, useMemo } from "react";

export default function FilterableList({ items }) {
  const [query, setQuery] = useState("");

  const filtered = useMemo(() => {
    return items.filter((item) =>
      item.name.toLowerCase().includes(query.toLowerCase()),
    );
  }, [items, query]);

  return (
    <div>
      <input
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Filter..."
      />
      <ul>
        {filtered.map((item) => (
          <li key={item.id}>{item.name}</li>
        ))}
      </ul>
    </div>
  );
}
```

### List with useDeferredValue (performance)

```jsx
import { useState, useDeferredValue, useMemo } from "react";

export default function LargeList({ items }) {
  const [query, setQuery] = useState("");
  const deferredQuery = useDeferredValue(query);

  const filtered = useMemo(() => {
    return items.filter((item) =>
      item.name.toLowerCase().includes(deferredQuery.toLowerCase()),
    );
  }, [items, deferredQuery]);

  return (
    <div>
      <input
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Search..."
      />
      <ul style={{ opacity: query !== deferredQuery ? 0.5 : 1 }}>
        {filtered.map((item) => (
          <li key={item.id}>{item.name}</li>
        ))}
      </ul>
    </div>
  );
}
```

### Empty State for Lists

```jsx
export default function UserList({ users }) {
  if (!users || users.length === 0) {
    return <div className="empty-state">No users found.</div>;
  }

  return (
    <ul>
      {users.map((user) => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  );
}
```

---

## 11. Modal Component

```jsx
import { useEffect, useRef } from "react";

export default function Modal({ isOpen, onClose, title, children }) {
  const overlayRef = useRef(null);

  useEffect(() => {
    const handleEscape = (e) => {
      if (e.key === "Escape") onClose();
    };

    if (isOpen) {
      document.addEventListener("keydown", handleEscape);
      document.body.style.overflow = "hidden";
    }

    return () => {
      document.removeEventListener("keydown", handleEscape);
      document.body.style.overflow = "";
    };
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <div
      ref={overlayRef}
      style={{
        position: "fixed",
        inset: 0,
        background: "rgba(0,0,0,0.5)",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        zIndex: 1000,
      }}
      onClick={(e) => {
        if (e.target === overlayRef.current) onClose();
      }}
    >
      <div
        style={{
          background: "#fff",
          padding: 24,
          borderRadius: 8,
          minWidth: 400,
        }}
      >
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            marginBottom: 16,
          }}
        >
          <h2>{title}</h2>
          <button onClick={onClose}>&times;</button>
        </div>
        {children}
      </div>
    </div>
  );
}

// Usage:
// <Modal isOpen={isOpen} onClose={() => setIsOpen(false)} title="Confirm">
//   <p>Are you sure?</p>
//   <button onClick={handleConfirm}>Yes</button>
// </Modal>
```

---

## 12. Tabs Component

```jsx
import { useState } from "react";

const tabs = [
  { id: "profile", label: "Profile" },
  { id: "settings", label: "Settings" },
  { id: "notifications", label: "Notifications" },
];

export default function Tabs() {
  const [activeTab, setActiveTab] = useState("profile");

  return (
    <div>
      <div style={{ display: "flex", gap: 8, borderBottom: "2px solid #ddd" }}>
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            style={{
              padding: "8px 16px",
              border: "none",
              borderBottom:
                activeTab === tab.id
                  ? "2px solid blue"
                  : "2px solid transparent",
              background: "transparent",
              cursor: "pointer",
              fontWeight: activeTab === tab.id ? "bold" : "normal",
            }}
          >
            {tab.label}
          </button>
        ))}
      </div>
      <div style={{ padding: 16 }}>
        {activeTab === "profile" && <div>Profile content</div>}
        {activeTab === "settings" && <div>Settings content</div>}
        {activeTab === "notifications" && <div>Notifications content</div>}
      </div>
    </div>
  );
}
```

---

## 13. Error Boundary

```jsx
import { Component } from "react";

export default class ErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, info) {
    console.error("ErrorBoundary caught:", error, info);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div style={{ padding: 24, textAlign: "center" }}>
          <h2>Something went wrong</h2>
          <p>{this.state.error?.message}</p>
          <button
            onClick={() => this.setState({ hasError: false, error: null })}
          >
            Try again
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}

// Usage:
// <ErrorBoundary>
//   <MyComponent />
// </ErrorBoundary>
```

---

## 14. React Portal

```jsx
import { createPortal } from "react-dom";

export default function Portal({ children }) {
  return createPortal(children, document.body);
}

// Usage:
// <Portal>
//   <div className="toast">Notification!</div>
// </Portal>
```

---

## 15. React Router Setup

```jsx
import {
  BrowserRouter,
  Routes,
  Route,
  Link,
  useParams,
  useNavigate,
} from "react-router-dom";

function Home() {
  return <h1>Home</h1>;
}

function User() {
  const { id } = useParams();
  const navigate = useNavigate();

  return (
    <div>
      <h1>User: {id}</h1>
      <button onClick={() => navigate("/")}>Back</button>
    </div>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <nav>
        <Link to="/">Home</Link>
        <Link to="/users/1">User 1</Link>
      </nav>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/users/:id" element={<User />} />
      </Routes>
    </BrowserRouter>
  );
}
```

---

## 16. React.lazy + Suspense

```jsx
import { lazy, Suspense } from "react";

const Dashboard = lazy(() => import("./Dashboard"));
const Settings = lazy(() => import("./Settings"));

export default function App() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <Dashboard />
      <Settings />
    </Suspense>
  );
}
```

---

## 17. forwardRef (ref forwarding)

```jsx
import { forwardRef } from "react";

const FancyInput = forwardRef((props, ref) => {
  return <input ref={ref} style={{ border: "2px solid blue" }} {...props} />;
});

export default FancyInput;

// Usage:
// const ref = useRef(null);
// <FancyInput ref={ref} />
// ref.current?.focus();
```

---

## 18. useImperativeHandle

```jsx
import { forwardRef, useImperativeHandle, useRef } from "react";

const CustomInput = forwardRef((props, ref) => {
  const inputRef = useRef(null);

  useImperativeHandle(ref, () => ({
    focus: () => inputRef.current?.focus(),
    clear: () => {
      inputRef.current.value = "";
    },
    getValue: () => inputRef.current?.value,
  }));

  return <input ref={inputRef} {...props} />;
});

export default CustomInput;

// Usage:
// const inputRef = useRef();
// <CustomInput ref={inputRef} />
// inputRef.current?.focus();
// inputRef.current?.clear();
```

---

## 19. Loading Spinner

```jsx
export default function Spinner({ size = 40, color = "#007bff" }) {
  return (
    <div
      style={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        padding: 24,
      }}
    >
      <div
        style={{
          width: size,
          height: size,
          border: `4px solid #e0e0e0`,
          borderTop: `4px solid ${color}`,
          borderRadius: "50%",
          animation: "spin 0.8s linear infinite",
        }}
      />
      <style>{`@keyframes spin { to { transform: rotate(360deg); } }`}</style>
    </div>
  );
}

// Usage:
// if (loading) return <Spinner />;
```

---

## 20. Debounced Search (full example)

```jsx
import { useState, useEffect } from "react";
import { useDebounce } from "./useDebounce";

export default function SearchPage() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const debouncedQuery = useDebounce(query, 300);

  useEffect(() => {
    if (!debouncedQuery.trim()) {
      setResults([]);
      return;
    }

    let cancelled = false;
    setLoading(true);

    fetch(`/api/search?q=${encodeURIComponent(debouncedQuery)}`)
      .then((res) => res.json())
      .then((data) => {
        if (!cancelled) {
          setResults(data);
          setLoading(false);
        }
      })
      .catch(() => {
        if (!cancelled) setLoading(false);
      });

    return () => {
      cancelled = true;
    };
  }, [debouncedQuery]);

  return (
    <div>
      <input
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Search..."
      />
      {loading && <div>Searching...</div>}
      <ul>
        {results.map((item) => (
          <li key={item.id}>{item.name}</li>
        ))}
      </ul>
    </div>
  );
}
```

---

## 21. Compound Components (Advanced Pattern)

```jsx
import { createContext, useContext, useState } from "react";

const AccordionContext = createContext(null);

function Accordion({ children, defaultOpen = null }) {
  const [openIndex, setOpenIndex] = useState(defaultOpen);
  return (
    <AccordionContext.Provider value={{ openIndex, setOpenIndex }}>
      {children}
    </AccordionContext.Provider>
  );
}

function Item({ index, title, children }) {
  const { openIndex, setOpenIndex } = useContext(AccordionContext);
  const isOpen = openIndex === index;

  return (
    <div>
      <button
        onClick={() => setOpenIndex(isOpen ? null : index)}
        style={{
          width: "100%",
          textAlign: "left",
          padding: 12,
          fontWeight: "bold",
        }}
      >
        {title}
      </button>
      {isOpen && <div style={{ padding: 12 }}>{children}</div>}
    </div>
  );
}

Accordion.Item = Item;
export default Accordion;

// Usage:
// <Accordion defaultOpen={0}>
//   <Accordion.Item index={0} title="Section 1">Content 1</Accordion.Item>
//   <Accordion.Item index={1} title="Section 2">Content 2</Accordion.Item>
// </Accordion>
```

---

## 22. useActionState (React 19)

```jsx
import { useActionState } from "react";

async function submitForm(prevState, formData) {
  const name = formData.get("name");
  const res = await fetch("/api/users", {
    method: "POST",
    body: JSON.stringify({ name }),
    headers: { "Content-Type": "application/json" },
  });

  if (!res.ok) {
    return { error: "Failed to create user" };
  }
  return { success: true, name };
}

export default function AddUserForm() {
  const [state, formAction, pending] = useActionState(submitForm, {
    error: null,
  });

  return (
    <form action={formAction}>
      <input name="name" type="text" required />
      <button type="submit" disabled={pending}>
        {pending ? "Creating..." : "Add User"}
      </button>
      {state?.error && <p style={{ color: "red" }}>{state.error}</p>}
      {state?.success && (
        <p style={{ color: "green" }}>User {state.name} created!</p>
      )}
    </form>
  );
}
```

---

## 23. useOptimistic (React 19)

```jsx
import { useState, useOptimistic, useRef } from "react";

async function sendMessage(prevMessages, formData) {
  const message = formData.get("message");
  return message;
}

export default function MessageList() {
  const [messages, setMessages] = useState([]);
  const [optimisticMessages, addOptimistic] = useOptimistic(
    messages,
    (state, newMessage) => [...state, { text: newMessage, sending: true }],
  );

  const formRef = useRef(null);

  const formAction = async (formData) => {
    const message = formData.get("message");
    addOptimistic(message);
    formRef.current?.reset();

    // Simulate API call
    await new Promise((resolve) => setTimeout(resolve, 1000));
    setMessages((prev) => [...prev, { text: message, sending: false }]);
  };

  return (
    <form action={formAction} ref={formRef}>
      <ul>
        {optimisticMessages.map((msg, i) => (
          <li key={i} style={{ opacity: msg.sending ? 0.5 : 1 }}>
            {msg.text} {msg.sending && "(sending...)"}
          </li>
        ))}
      </ul>
      <input name="message" type="text" required />
      <button type="submit">Send</button>
    </form>
  );
}
```

---

## 24. useTransition

```jsx
import { useState, useTransition } from "react";

export default function SearchPage() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [isPending, startTransition] = useTransition();

  const handleChange = (e) => {
    const value = e.target.value;
    setQuery(value); // urgent — update input immediately

    startTransition(() => {
      // non-urgent — can be interrupted
      const filtered = mockSearch(value);
      setResults(filtered);
    });
  };

  return (
    <div>
      <input value={query} onChange={handleChange} placeholder="Search..." />
      {isPending && <div>Updating results...</div>}
      <ul>
        {results.map((r) => (
          <li key={r.id}>{r.name}</li>
        ))}
      </ul>
    </div>
  );
}
```

---

## 25. Testing (React Testing Library)

```jsx
import { render, screen, fireEvent } from "@testing-library/react";
import Counter from "./Counter";

test("increments count when button is clicked", () => {
  render(<Counter />);
  const button = screen.getByText("+1");
  fireEvent.click(button);
  expect(screen.getByText(/count: 1/i)).toBeInTheDocument();
});
```

---

_These snippets target modern React (18/19) with functional components and hooks. Adjust import paths and API endpoints to match your project setup._
