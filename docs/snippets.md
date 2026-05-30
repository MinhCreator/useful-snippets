---
title: "Code Snippets"
description: "A collection of reusable code snippets and patterns."
---

# Code Snippets 🚀

A curated collection of reusable code snippets and patterns for everyday development.

## Quick Start

Browse snippets by language or category using the sidebar.

## Features

### 1. Language Support

::: tabs
== tab "JavaScript"

```javascript
// Example snippet
function greet(name) {
  return `Hello, ${name}!`;
}
```

== tab "Python"

```python
# Example snippet
def greet(name):
    return f"Hello, {name}!"
```

== tab "TypeScript"

```TypeScript
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

== tab "Java"

```Java
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}

```

:::

### 2. Categories

- **Utilities** — Helper functions and common patterns
- **Algorithms** — Sorting, searching, and data structures
- **Config** — Framework and tool configurations
- **CLI** — Command-line one-liners and scripts

### 3. Snippet Format

::: callout tip "Pro Tip"
Each snippet includes a description, code block, and usage example.
:::

## Contributing

See the [contribution guidelines](https://docs.docmd.io) to add your own snippets.

Happy coding! 🎉
