---
title: "Home"
description: "Code Snippets — Your personal collection of reusable code snippets."
---

# Code Snippets 📁

A personal, organized collection of reusable code snippets covering multiple languages and use cases.

## Getting Started

Browse snippets by category on the left, or use the search bar to find exactly what you need.


## Browse by Category

| Category       | Description                                |
|----------------|--------------------------------------------|
| **Utilities**  | Helper functions, debounce, throttle, etc. |
| **Algorithms** | Sorting, searching, tree traversal         |
| **Config**     | dotfiles, ESLint, Prettier, tsconfig       |
| **CLI**        | Git commands, PowerShell one-liners        |
| **React**      | Hooks, patterns, component templates       |
| **Python**     | Decorators, context managers, recipes      |

## Featured Sample Snippet

::: tabs
== tab "JavaScript"
```javascript
const memoize = (fn) => {
  const cache = new Map();
  return (...args) => {
    const key = JSON.stringify(args);
    if (cache.has(key)) return cache.get(key);
    const result = fn(...args);
    cache.set(key, result);
    return result;
  };
};
```

== tab "Python"
```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```
:::

## Quick Links

- **[Browse Snippets](/snippets)** — View the full collection
- **[GitHub Repository](https://github.com/your-username/code-snippets)** — Source code & contributions

Happy coding! 🎉
