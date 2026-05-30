# JavaScript Snippets

## Table of Contents

1. [Array Utilities](#1-array-utilities)
2. [Object Utilities](#2-object-utilities)
3. [String Utilities](#3-string-utilities)
4. [Number Utilities](#4-number-utilities)
5. [Function Utilities](#5-function-utilities)
6. [Async / Promise Patterns](#6-async--promise-patterns)
7. [Fetch API & HTTP](#7-fetch-api--http)
8. [Event Handling (DOM)](#8-event-handling-dom)
9. [Timers & Intervals](#9-timers--intervals)
10. [Classes & Prototypes](#10-classes--prototypes)
11. [Maps, Sets & Weak Collections](#11-maps-sets--weak-collections)
12. [Generators & Iterators](#12-generators--iterators)
13. [Proxy & Reflect](#13-proxy--reflect)
14. [Date & Time](#14-date--time)
15. [Storage (localStorage / sessionStorage)](#15-storage-localstorage--sessionstorage)
16. [Cookies](#16-cookies)
17. [Regular Expressions](#17-regular-expressions)
18. [Validation Utilities](#18-validation-utilities)
19. [DOM Manipulation](#19-dom-manipulation)
20. [URL & Query String](#20-url--query-string)
21. [Design Patterns](#21-design-patterns)
22. [Data Structures](#22-data-structures)
23. [Error Handling](#23-error-handling)
24. [Logging & Debugging](#24-logging--debugging)
25. [Polyfills & Compatibility](#25-polyfills--compatibility)

---

## 1. Array Utilities

### Unique values

```js
const unique = (arr) => [...new Set(arr)];

unique([1, 2, 2, 3]); // [1, 2, 3]
```

### Unique objects by key

```js
const uniqueBy = (arr, key) => [
  ...new Map(arr.map((item) => [item[key], item])).values(),
];

uniqueBy([{ id: 1 }, { id: 1 }, { id: 2 }], "id");
// [{ id: 1 }, { id: 2 }]
```

### Chunk array into groups

```js
const chunk = (arr, size) =>
  Array.from({ length: Math.ceil(arr.length / size) }, (_, i) =>
    arr.slice(i * size, i * size + size),
  );

chunk([1, 2, 3, 4, 5], 2); // [[1, 2], [3, 4], [5]]
```

### Shuffle array

```js
const shuffle = (arr) => {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
};

shuffle([1, 2, 3, 4, 5]); // [3, 1, 5, 2, 4]
```

### Group by key

```js
const groupBy = (arr, fn) =>
  arr.reduce((acc, item) => {
    const key = typeof fn === "function" ? fn(item) : item[fn];
    (acc[key] ||= []).push(item);
    return acc;
  }, {});

groupBy([{ type: "a" }, { type: "b" }, { type: "a" }], "type");
// { a: [{ type: 'a' }, { type: 'a' }], b: [{ type: 'b' }] }
```

### Partition array by predicate

```js
const partition = (arr, fn) =>
  arr.reduce(
    (acc, item) => {
      acc[fn(item) ? 0 : 1].push(item);
      return acc;
    },
    [[], []],
  );

partition([1, 2, 3, 4, 5], (n) => n % 2 === 0);
// [[2, 4], [1, 3, 5]]
```

### Intersection

```js
const intersection = (a, b) => a.filter((x) => b.includes(x));

intersection([1, 2, 3], [2, 3, 4]); // [2, 3]
```

### Difference

```js
const difference = (a, b) => a.filter((x) => !b.includes(x));

difference([1, 2, 3], [2, 3, 4]); // [1]
```

### Union

```js
const union = (a, b) => [...new Set([...a, ...b])];

union([1, 2, 3], [2, 3, 4]); // [1, 2, 3, 4]
```

### Flatten nested array

```js
const flatten = (arr, depth = Infinity) =>
  Array.isArray(arr)
    ? depth > 0
      ? arr.reduce((acc, item) => acc.concat(flatten(item, depth - 1)), [])
      : arr
    : [arr];

flatten([1, [2, [3, [4]]]], 2); // [1, 2, 3, [4]]
flatten([1, [2, [3, [4]]]]); // [1, 2, 3, 4]
```

### Sort by key

```js
const sortBy = (arr, key, order = "asc") =>
  [...arr].sort((a, b) =>
    order === "asc" ? (a[key] > b[key] ? 1 : -1) : b[key] > a[key] ? 1 : -1,
  );

sortBy([{ name: "Bob" }, { name: "Alice" }], "name");
// [{ name: 'Alice' }, { name: 'Bob' }]
```

### Range

```js
const range = (start, end, step = 1) =>
  Array.from(
    { length: Math.ceil((end - start) / step) },
    (_, i) => start + i * step,
  );

range(1, 5); // [1, 2, 3, 4]
range(0, 10, 2); // [0, 2, 4, 6, 8]
```

### Toggle element in array

```js
const toggle = (arr, item) =>
  arr.includes(item) ? arr.filter((x) => x !== item) : [...arr, item];

toggle([1, 2, 3], 2); // [1, 3]
toggle([1, 3], 2); // [1, 3, 2]
```

### Move element

```js
const move = (arr, from, to) => {
  const a = [...arr];
  const [item] = a.splice(from, 1);
  a.splice(to, 0, item);
  return a;
};

move([1, 2, 3, 4], 0, 2); // [2, 3, 1, 4]
```

### Array of consecutive numbers

```js
const times = (n) => Array.from({ length: n }, (_, i) => i);

times(5); // [0, 1, 2, 3, 4]
```

---

## 2. Object Utilities

### Pick keys

```js
const pick = (obj, keys) =>
  keys.reduce((acc, key) => {
    if (key in obj) acc[key] = obj[key];
    return acc;
  }, {});

pick({ a: 1, b: 2, c: 3 }, ["a", "c"]); // { a: 1, c: 3 }
```

### Omit keys

```js
const omit = (obj, keys) =>
  Object.fromEntries(
    Object.entries(obj).filter(([key]) => !keys.includes(key)),
  );

omit({ a: 1, b: 2, c: 3 }, ["a", "c"]); // { b: 2 }
```

### Deep clone

```js
const deepClone = (obj) => structuredClone(obj);

// Fallback for older environments
const deepCloneFallback = (obj) => JSON.parse(JSON.stringify(obj));
```

### Deep merge

```js
const deepMerge = (target, source) => {
  const output = { ...target };
  for (const key of Object.keys(source)) {
    if (isPlainObject(source[key]) && isPlainObject(target[key])) {
      output[key] = deepMerge(target[key], source[key]);
    } else {
      output[key] = source[key];
    }
  }
  return output;
};

const isPlainObject = (val) =>
  val !== null && typeof val === "object" && !Array.isArray(val);

deepMerge({ a: 1, b: { c: 2 } }, { b: { d: 3 }, e: 4 });
// { a: 1, b: { c: 2, d: 3 }, e: 4 }
```

### Rename keys

```js
const renameKeys = (obj, keyMap) =>
  Object.fromEntries(
    Object.entries(obj).map(([key, value]) => [keyMap[key] || key, value]),
  );

renameKeys({ firstName: "Alice" }, { firstName: "name" });
// { name: 'Alice' }
```

### Invert object (swap keys/values)

```js
const invert = (obj) =>
  Object.fromEntries(Object.entries(obj).map(([k, v]) => [v, k]));

invert({ a: 1, b: 2 }); // { 1: 'a', 2: 'b' }
```

### Get nested value safely

```js
const get = (obj, path, defaultValue) => {
  const keys = Array.isArray(path) ? path : path.split(".");
  let result = obj;
  for (const key of keys) {
    if (result == null || typeof result !== "object") return defaultValue;
    result = result[key];
  }
  return result ?? defaultValue;
};

get({ a: { b: { c: 42 } } }, "a.b.c"); // 42
get({ a: 1 }, "x.y.z", "default"); // 'default'
```

### Set nested value

```js
const set = (obj, path, value) => {
  const keys = Array.isArray(path) ? path : path.split(".");
  let current = obj;
  for (let i = 0; i < keys.length - 1; i++) {
    if (!(keys[i] in current) || typeof current[keys[i]] !== "object") {
      current[keys[i]] = {};
    }
    current = current[keys[i]];
  }
  current[keys[keys.length - 1]] = value;
  return obj;
};

const o = {};
set(o, "a.b.c", 42); // { a: { b: { c: 42 } } }
```

### Object is empty

```js
const isEmpty = (obj) =>
  obj && typeof obj === "object" && !Array.isArray(obj)
    ? Object.keys(obj).length === 0
    : !obj;

isEmpty({}); // true
isEmpty({ a: 1 }); // false
```

### Map object to array

```js
const mapObject = (obj, fn) =>
  Object.fromEntries(
    Object.entries(obj).map(([key, value], index) => [
      key,
      fn(value, key, index),
    ]),
  );

mapObject({ a: 1, b: 2 }, (v) => v * 2);
// { a: 2, b: 4 }
```

### Filter object

```js
const filterObject = (obj, fn) =>
  Object.fromEntries(
    Object.entries(obj).filter(([key, value]) => fn(value, key)),
  );

filterObject({ a: 1, b: 2, c: 3 }, (v) => v > 1);
// { b: 2, c: 3 }
```

### Object to query string

```js
const toQueryString = (params) => new URLSearchParams(params).toString();

toQueryString({ search: "test", page: 1 });
// 'search=test&page=1'
```

---

## 3. String Utilities

### Capitalize

```js
const capitalize = (str) =>
  str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();

capitalize("hello"); // 'Hello'
```

### Capitalize words

```js
const capitalizeWords = (str) => str.replace(/\b\w/g, (c) => c.toUpperCase());

capitalizeWords("hello world"); // 'Hello World'
```

### Truncate

```js
const truncate = (str, maxLen, suffix = "...") =>
  str.length > maxLen ? str.slice(0, maxLen - suffix.length) + suffix : str;

truncate("Hello world", 8); // 'Hello...'
```

### Slugify

```js
const slugify = (str) =>
  str
    .toLowerCase()
    .trim()
    .replace(/[\s_]+/g, "-")
    .replace(/[^\w-]/g, "")
    .replace(/--+/g, "-")
    .replace(/^-+|-+$/g, "");

slugify("Hello World!"); // 'hello-world'
```

### Camel case

```js
const camelCase = (str) =>
  str
    .replace(/[-_\s]+(.)?/g, (_, c) => (c ? c.toUpperCase() : ""))
    .replace(/^[A-Z]/, (c) => c.toLowerCase());

camelCase("hello-world"); // 'helloWorld'
camelCase("Hello World"); // 'helloWorld'
```

### Snake case

```js
const snakeCase = (str) =>
  str
    .replace(/([A-Z])/g, "_$1")
    .toLowerCase()
    .replace(/[-_\s]+/g, "_")
    .replace(/^_|_$/g, "");

snakeCase("helloWorld"); // 'hello_world'
```

### Kebab case

```js
const kebabCase = (str) =>
  str
    .replace(/([A-Z])/g, "-$1")
    .toLowerCase()
    .replace(/[\s_]+/g, "-")
    .replace(/^-+|-+$/g, "");

kebabCase("helloWorld"); // 'hello-world'
```

### Mask string

```js
const mask = (str, visible = 4, maskChar = "*") =>
  str.slice(0, visible).padEnd(str.length, maskChar);

mask("1234567890"); // '1234******'
mask("credit-card", 6, "#"); // 'credit######'
```

### Reverse string

```js
const reverse = (str) => [...str].reverse().join("");

reverse("hello"); // 'olleh'
```

### Count occurrences

```js
const countOccurrences = (str, substr) =>
  (str.match(new RegExp(substr, "g")) || []).length;

countOccurrences("hello world hello", "hello"); // 2
```

### Strip HTML tags

```js
const stripHtml = (str) => str.replace(/<[^>]*>/g, "");

stripHtml("<p>Hello <b>world</b></p>"); // 'Hello world'
```

### Escape HTML

```js
const escapeHtml = (str) =>
  str.replace(
    /[&<>"']/g,
    (ch) =>
      ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[
        ch
      ],
  );

escapeHtml('<script>alert("xss")</script>');
// '&lt;script&gt;alert(&quot;xss&quot;)&lt;/script&gt;'
```

### Unescape HTML

```js
const unescapeHtml = (str) =>
  str.replace(
    /&amp;|&lt;|&gt;|&quot;|&#39;/g,
    (ch) =>
      ({ "&amp;": "&", "&lt;": "<", "&gt;": ">", "&quot;": '"', "&#39;": "'" })[
        ch
      ],
  );
```

### Pad to length

```js
const pad = (str, len, char = " ") =>
  str
    .padStart(Math.floor((len - str.length) / 2) + str.length, char)
    .padEnd(len, char);

pad("hello", 11); // '   hello   '
pad("hi", 7, "-"); // '---hi--'
```

### Template string replacements

```js
const template = (str, data) =>
  str.replace(/\{\{(\w+)\}\}/g, (_, key) => data[key] ?? "");

template("Hello {{name}}!", { name: "World" }); // 'Hello World!'
```

---

## 4. Number Utilities

### Clamp

```js
const clamp = (num, min, max) => Math.min(Math.max(num, min), max);

clamp(5, 0, 10); // 5
clamp(-5, 0, 10); // 0
clamp(15, 0, 10); // 10
```

### Random integer (inclusive)

```js
const randomInt = (min, max) =>
  Math.floor(Math.random() * (max - min + 1)) + min;

randomInt(1, 10); // 1..10
```

### Random float

```js
const randomFloat = (min, max, decimals = 2) =>
  parseFloat((Math.random() * (max - min) + min).toFixed(decimals));

randomFloat(0, 1); // 0.73
```

### Round to decimals

```js
const round = (num, decimals = 0) =>
  Number(`${Math.round(Number(`${num}e${decimals}`))}e-${decimals}`);

round(1.2345, 2); // 1.23
```

### Is integer

```js
const isInt = (num) => Number.isInteger(num);

isInt(42); // true
isInt(4.2); // false
```

### Is even / odd

```js
const isEven = (num) => num % 2 === 0;
const isOdd = (num) => num % 2 !== 0;

isEven(2); // true
isOdd(3); // true
```

### Format with commas

```js
const formatNumber = (num) => num.toLocaleString("en-US");

formatNumber(1234567); // '1,234,567'
```

### Truncate decimal

```js
const truncateDecimal = (num, decimals) =>
  Math.trunc(num * 10 ** decimals) / 10 ** decimals;

truncateDecimal(1.2345, 2); // 1.23
```

### In range

```js
const inRange = (num, min, max) => num >= min && num <= max;

inRange(5, 0, 10); // true
inRange(15, 0, 10); // false
```

### Average

```js
const average = (...nums) => nums.reduce((a, b) => a + b, 0) / nums.length;

average(1, 2, 3); // 2
```

### Sum

```js
const sum = (...nums) => nums.reduce((a, b) => a + b, 0);

sum(1, 2, 3); // 6
```

### Convert bytes

```js
const formatBytes = (bytes, decimals = 2) => {
  if (bytes === 0) return "0 B";
  const k = 1024;
  const sizes = ["B", "KB", "MB", "GB", "TB"];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return `${parseFloat((bytes / Math.pow(k, i)).toFixed(decimals))} ${sizes[i]}`;
};

formatBytes(1234567); // '1.18 MB'
```

---

## 5. Function Utilities

### Debounce

```js
const debounce = (fn, delay) => {
  let timer;
  return (...args) => {
    clearTimeout(timer);
    timer = setTimeout(() => fn(...args), delay);
  };
};

// Usage
const handleSearch = debounce((query) => {
  console.log("Searching:", query);
}, 300);
```

### Throttle

```js
const throttle = (fn, interval) => {
  let lastCall = 0;
  return (...args) => {
    const now = Date.now();
    if (now - lastCall >= interval) {
      lastCall = now;
      fn(...args);
    }
  };
};

// Usage
const handleScroll = throttle(() => {
  console.log("Scrolled");
}, 200);
```

### Memoize

```js
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

const fib = memoize((n) => (n <= 1 ? n : fib(n - 1) + fib(n - 2)));
```

### Once (call only once)

```js
const once = (fn) => {
  let called = false;
  let result;
  return (...args) => {
    if (!called) {
      called = true;
      result = fn(...args);
    }
    return result;
  };
};

const initialize = once(() => console.log("Initialized"));
initialize(); // 'Initialized'
initialize(); // (nothing)
```

### Pipe (left-to-right composition)

```js
const pipe =
  (...fns) =>
  (value) =>
    fns.reduce((acc, fn) => fn(acc), value);

const add1 = (x) => x + 1;
const double = (x) => x * 2;
const add1ThenDouble = pipe(add1, double);
add1ThenDouble(3); // 8
```

### Compose (right-to-left)

```js
const compose =
  (...fns) =>
  (value) =>
    fns.reduceRight((acc, fn) => fn(acc), value);

const doubleThenAdd1 = compose(add1, double);
doubleThenAdd1(3); // 7
```

### Curry

```js
const curry = (fn, arity = fn.length, ...args) =>
  args.length >= arity
    ? fn(...args)
    : (...more) => curry(fn, arity, ...args, ...more);

const add = curry((a, b, c) => a + b + c);
add(1)(2)(3); // 6
add(1, 2)(3); // 6
```

### Partial application

```js
const partial =
  (fn, ...presetArgs) =>
  (...laterArgs) =>
    fn(...presetArgs, ...laterArgs);

const power = (base, exp) => base ** exp;
const square = partial(power, 2);
square(3); // 8 (2^3)
```

### Negate predicate

```js
const negate =
  (fn) =>
  (...args) =>
    !fn(...args);

const isEven = (n) => n % 2 === 0;
[1, 2, 3, 4].filter(negate(isEven)); // [1, 3]
```

### Retry

```js
const retry = async (fn, maxAttempts, delay = 0) => {
  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    try {
      return await fn();
    } catch (error) {
      if (attempt === maxAttempts) throw error;
      if (delay) await new Promise((r) => setTimeout(r, delay));
    }
  }
};

// Usage
const data = await retry(() => fetch("/api/data"), 3, 1000);
```

### Time function execution

```js
const time = async (fn) => {
  const start = performance.now();
  const result = await fn();
  const duration = performance.now() - start;
  return { result, duration };
};

const { result, duration } = await time(() => someExpensiveOp());
console.log(`Took ${duration}ms`);
```

---

## 6. Async / Promise Patterns

### Sleep / delay

```js
const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

await sleep(1000);
```

### Timeout a promise

```js
const timeout = (promise, ms) =>
  Promise.race([
    promise,
    new Promise((_, reject) =>
      setTimeout(() => reject(new Error("Timed out")), ms),
    ),
  ]);

const result = await timeout(fetch("/api/data"), 5000);
```

### Retry with backoff

```js
const retryWithBackoff = async (fn, maxRetries = 3, baseDelay = 500) => {
  for (let i = 0; i <= maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      if (i === maxRetries) throw error;
      const delay = baseDelay * 2 ** i;
      await new Promise((r) => setTimeout(r, delay));
    }
  }
};
```

### Promise queue (sequential)

```js
const promiseQueue = async (items, fn) => {
  const results = [];
  for (const item of items) {
    results.push(await fn(item));
  }
  return results;
};

await promiseQueue([1, 2, 3], async (n) => n * 2);
```

### Concurrent with limit

```js
const mapConcurrent = async (items, fn, concurrency = 3) => {
  const results = [];
  const executing = new Set();

  for (const [index, item] of items.entries()) {
    const p = Promise.resolve().then(() => fn(item, index));
    results.push(p);
    executing.add(p);

    const clean = () => executing.delete(p);
    p.then(clean, clean);

    if (executing.size >= concurrency) {
      await Promise.race(executing);
    }
  }

  return Promise.all(results);
};

const urls = ["/api/a", "/api/b", "/api/c", "/api/d"];
const data = await mapConcurrent(urls, fetch, 2);
```

### Deferred promise

```js
const deferred = () => {
  let resolve, reject;
  const promise = new Promise((res, rej) => {
    resolve = res;
    reject = rej;
  });
  return { promise, resolve, reject };
};

const d = deferred();
setTimeout(() => d.resolve("done"), 1000);
await d.promise; // 'done'
```

### Async pool (task queue)

```js
class AsyncPool {
  constructor(concurrency) {
    this.concurrency = concurrency;
    this.queue = [];
    this.active = 0;
  }

  async run(fn) {
    this.queue.push(fn);
    return this._next();
  }

  async _next() {
    if (this.active >= this.concurrency || this.queue.length === 0) return;
    const fn = this.queue.shift();
    this.active++;
    try {
      return await fn();
    } finally {
      this.active--;
      this._next();
    }
  }
}

const pool = new AsyncPool(2);
pool.run(() => fetch("/api/a"));
pool.run(() => fetch("/api/b"));
pool.run(() => fetch("/api/c"));
```

### Poll until condition

```js
const poll = async (fn, condition, interval = 1000, timeout = 30000) => {
  const start = Date.now();
  while (true) {
    const result = await fn();
    if (condition(result)) return result;
    if (Date.now() - start > timeout) throw new Error("Poll timed out");
    await sleep(interval);
  }
};

const jobStatus = await poll(
  () => fetch(`/api/jobs/${id}`).then((r) => r.json()),
  (data) => data.status === "completed",
  2000,
  60000,
);
```

---

## 7. Fetch API & HTTP

### GET with query params

```js
const get = async (url, params = {}, options = {}) => {
  const query = new URLSearchParams(params).toString();
  const fullUrl = query ? `${url}?${query}` : url;
  const response = await fetch(fullUrl, {
    method: "GET",
    headers: { Accept: "application/json", ...options.headers },
    ...options,
  });
  if (!response.ok) throw new Error(`GET ${url} failed: ${response.status}`);
  return response.json();
};
```

### POST with JSON body

```js
const post = async (url, data, options = {}) => {
  const response = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...options.headers },
    body: JSON.stringify(data),
    ...options,
  });
  if (!response.ok) throw new Error(`POST ${url} failed: ${response.status}`);
  return response.json();
};
```

### PUT / PATCH / DELETE

```js
const put = async (url, data) =>
  fetch(url, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  }).then((r) => r.json());

const patch = async (url, data) =>
  fetch(url, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  }).then((r) => r.json());

const del = async (url) =>
  fetch(url, { method: "DELETE" }).then((r) => r.json());
```

### Upload file

```js
const uploadFile = async (url, file, fieldName = "file", extraFields = {}) => {
  const formData = new FormData();
  formData.append(fieldName, file);
  Object.entries(extraFields).forEach(([key, value]) =>
    formData.append(key, value),
  );

  const response = await fetch(url, {
    method: "POST",
    body: formData,
  });
  if (!response.ok) throw new Error("Upload failed");
  return response.json();
};
```

### Download file as blob

```js
const downloadBlob = async (url, filename) => {
  const response = await fetch(url);
  const blob = await response.blob();
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = filename;
  link.click();
  URL.revokeObjectURL(link.href);
};

await downloadBlob("/api/report.pdf", "report.pdf");
```

### Fetch with progress (XMLHttpRequest)

```js
const fetchWithProgress = (url, onProgress) =>
  new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest();
    xhr.open("GET", url);
    xhr.responseType = "blob";

    xhr.addEventListener("progress", (event) => {
      if (event.lengthComputable) {
        onProgress(event.loaded / event.total);
      }
    });

    xhr.addEventListener("load", () => resolve(xhr.response));
    xhr.addEventListener("error", () => reject(new Error("Request failed")));
    xhr.send();
  });

await fetchWithProgress("/api/large-file", (pct) =>
  console.log(`${Math.round(pct * 100)}%`),
);
```

### AbortController wrapper

```js
const fetchWithAbort = (url, options = {}) => {
  const controller = new AbortController();
  const signal = controller.signal;

  const promise = fetch(url, { ...options, signal }).then((r) => r.json());

  return { promise, abort: () => controller.abort() };
};

const { promise, abort } = fetchWithAbort("/api/slow");
setTimeout(() => abort(), 2000);
await promise.catch((err) => console.log(err.name)); // 'AbortError'
```

---

## 8. Event Handling (DOM)

### On ready (DOMContentLoaded)

```js
const onReady = (fn) => {
  if (document.readyState !== "loading") {
    fn();
  } else {
    document.addEventListener("DOMContentLoaded", fn);
  }
};

onReady(() => console.log("DOM ready"));
```

### Delegate event

```js
const delegate = (parent, selector, eventType, handler) => {
  parent.addEventListener(eventType, (e) => {
    const target = e.target.closest(selector);
    if (target && parent.contains(target)) {
      handler(e, target);
    }
  });
};

delegate(document.getElementById("list"), "li.item", "click", (e, el) => {
  console.log("Clicked:", el.textContent);
});
```

### Trigger custom event

```js
const triggerEvent = (el, name, detail = {}) => {
  const event = new CustomEvent(name, {
    detail,
    bubbles: true,
    cancelable: true,
  });
  el.dispatchEvent(event);
};

triggerEvent(document, "user:login", { userId: 42 });
document.addEventListener("user:login", (e) => console.log(e.detail));
```

### Debounced resize handler

```js
const onResize = (fn, delay = 200) => {
  const handler = debounce(fn, delay);
  window.addEventListener("resize", handler);
  return () => window.removeEventListener("resize", handler);
};

const cleanup = onResize(() => console.log(window.innerWidth));
```

### Detect click outside element

```js
const onClickOutside = (el, handler) => {
  const listener = (e) => {
    if (!el.contains(e.target)) handler(e);
  };
  document.addEventListener("click", listener);
  return () => document.removeEventListener("click", listener);
};

const cleanup = onClickOutside(document.getElementById("modal"), () =>
  console.log("Clicked outside"),
);
```

---

## 9. Timers & Intervals

### Safe setInterval (no overlap)

```js
const safeInterval = (fn, delay) => {
  let timer;
  const run = async () => {
    await fn();
    timer = setTimeout(run, delay);
  };
  timer = setTimeout(run, delay);
  return () => clearTimeout(timer);
};

const stop = safeInterval(async () => {
  await fetch("/api/ping");
}, 5000);
```

### Countdown timer

```js
const countdown = (seconds, onTick, onComplete) => {
  const interval = setInterval(() => {
    seconds--;
    onTick(seconds);
    if (seconds <= 0) {
      clearInterval(interval);
      onComplete();
    }
  }, 1000);
  return () => clearInterval(interval);
};

const stop = countdown(
  10,
  (s) => console.log(`${s}s remaining`),
  () => console.log("Done!"),
);
```

### Run with delay then interval

```js
const delayThenInterval = (fn, delay, interval) => {
  setTimeout(() => {
    fn();
    setInterval(fn, interval);
  }, delay);
};

delayThenInterval(() => console.log("tick"), 2000, 1000);
```

---

## 10. Classes & Prototypes

### Basic class

```js
class Animal {
  constructor(name) {
    this.name = name;
  }

  speak() {
    return `${this.name} makes a noise.`;
  }
}

class Dog extends Animal {
  constructor(name, breed) {
    super(name);
    this.breed = breed;
  }

  speak() {
    return `${this.name} barks.`;
  }
}

const d = new Dog("Rex", "Lab");
d.speak(); // 'Rex barks.'
```

### Singleton class

```js
class Singleton {
  static #instance;

  constructor() {
    if (Singleton.#instance) return Singleton.#instance;
    Singleton.#instance = this;
  }

  static getInstance() {
    if (!Singleton.#instance) new Singleton();
    return Singleton.#instance;
  }
}

const a = new Singleton();
const b = new Singleton();
a === b; // true
```

### Mixin pattern

```js
const TimestampMixin = (Base) =>
  class extends Base {
    createdAt = new Date();
    updatedAt = new Date();

    touch() {
      this.updatedAt = new Date();
    }
  };

class User extends TimestampMixin(class {}) {
  constructor(name) {
    super();
    this.name = name;
  }
}

const user = new User("Alice");
console.log(user.createdAt);
```

### Private fields

```js
class Counter {
  #count = 0;

  increment() {
    this.#count++;
  }

  get value() {
    return this.#count;
  }
}

const c = new Counter();
c.increment();
console.log(c.value); // 1
// c.#count // SyntaxError
```

---

## 11. Maps, Sets & Weak Collections

### Map with default factory

```js
class DefaultMap extends Map {
  constructor(createDefault, entries) {
    super(entries);
    this.createDefault = createDefault;
  }

  get(key) {
    if (!this.has(key)) {
      this.set(key, this.createDefault(key));
    }
    return super.get(key);
  }
}

const counts = new DefaultMap(() => 0);
counts.get("a"); // 0
counts.set("a", 5);
counts.get("a"); // 5
```

### LRU Cache using Map

```js
class LRUCache {
  constructor(capacity) {
    this.capacity = capacity;
    this.cache = new Map();
  }

  get(key) {
    if (!this.cache.has(key)) return undefined;
    const value = this.cache.get(key);
    this.cache.delete(key);
    this.cache.set(key, value);
    return value;
  }

  set(key, value) {
    if (this.cache.has(key)) this.cache.delete(key);
    else if (this.cache.size >= this.capacity) {
      this.cache.delete(this.cache.keys().next().value);
    }
    this.cache.set(key, value);
  }
}

const lru = new LRUCache(2);
lru.set("a", 1);
lru.set("b", 2);
lru.get("a"); // 1
lru.set("c", 3); // evicts 'b'
lru.get("b"); // undefined
```

### Set operations

```js
const setUnion = (a, b) => new Set([...a, ...b]);
const setIntersection = (a, b) => new Set([...a].filter((x) => b.has(x)));
const setDifference = (a, b) => new Set([...a].filter((x) => !b.has(x)));
const setSymmetricDiff = (a, b) =>
  new Set([...a, ...b].filter((x) => !(a.has(x) && b.has(x))));
```

### WeakMap for private data

```js
const privates = new WeakMap();

class Person {
  constructor(name) {
    privates.set(this, { name });
  }

  getName() {
    return privates.get(this).name;
  }
}
```

---

## 12. Generators & Iterators

### Range generator

```js
function* rangeGen(start, end, step = 1) {
  for (let i = start; i < end; i += step) {
    yield i;
  }
}

for (const n of rangeGen(0, 5)) {
  console.log(n); // 0, 1, 2, 3, 4
}
```

### Fibonacci generator

```js
function* fibonacci() {
  let a = 0,
    b = 1;
  while (true) {
    yield a;
    [a, b] = [b, a + b];
  }
}

const fib = fibonacci();
fib.next().value; // 0
fib.next().value; // 1
fib.next().value; // 1
fib.next().value; // 2
```

### Paginated API generator

```js
async function* paginate(url, pageSize = 100) {
  let page = 1;
  let hasMore = true;

  while (hasMore) {
    const response = await fetch(`${url}?page=${page}&limit=${pageSize}`);
    const data = await response.json();
    yield data.items;
    hasMore = data.nextPage !== null;
    page++;
  }
}

for await (const batch of paginate("/api/items")) {
  console.log(batch);
}
```

### Generator with async iteration

```js
async function* asyncGenerator() {
  let i = 0;
  while (i < 5) {
    await sleep(500);
    yield i++;
  }
}

for await (const val of asyncGenerator()) {
  console.log(val);
}
```

---

## 13. Proxy & Reflect

### Validation proxy

```js
const validate = (target, schema) =>
  new Proxy(target, {
    set(obj, prop, value) {
      const validator = schema[prop];
      if (validator && !validator(value)) {
        throw new TypeError(`Invalid value for ${prop}: ${value}`);
      }
      obj[prop] = value;
      return true;
    },
  });

const user = validate(
  {},
  {
    age: (v) => typeof v === "number" && v >= 0,
    email: (v) => typeof v === "string" && v.includes("@"),
  },
);

user.age = 25; // OK
user.age = -1; // TypeError
```

### Logging proxy

```js
const logged = (target) =>
  new Proxy(target, {
    get(obj, prop) {
      console.log(`GET ${String(prop)}`);
      return Reflect.get(obj, prop);
    },
    set(obj, prop, value) {
      console.log(`SET ${String(prop)} = ${value}`);
      return Reflect.set(obj, prop, value);
    },
  });

const p = logged({ a: 1 });
p.a; // 'GET a'
p.b = 2; // 'SET b = 2'
```

### Readonly proxy

```js
const readonly = (target) =>
  new Proxy(target, {
    set() {
      throw new Error("Object is readonly");
    },
    deleteProperty() {
      throw new Error("Object is readonly");
    },
    defineProperty() {
      throw new Error("Object is readonly");
    },
  });

const config = readonly({ apiKey: "secret" });
config.apiKey = "new"; // Error
```

---

## 14. Date & Time

### Format date

```js
const formatDate = (date, locale = "en-US", options = {}) => {
  const defaults = {
    year: "numeric",
    month: "short",
    day: "numeric",
  };
  return new Intl.DateTimeFormat(locale, { ...defaults, ...options }).format(
    date,
  );
};

formatDate(new Date()); // 'May 25, 2026'
```

### Relative time

```js
const relativeTime = (date, locale = "en-US") => {
  const rtf = new Intl.RelativeTimeFormat(locale, { numeric: "auto" });
  const diff = date - new Date();
  const seconds = Math.round(diff / 1000);
  const minutes = Math.round(seconds / 60);
  const hours = Math.round(minutes / 60);
  const days = Math.round(hours / 24);
  const months = Math.round(days / 30);
  const years = Math.round(months / 12);

  if (Math.abs(seconds) < 60) return rtf.format(seconds, "second");
  if (Math.abs(minutes) < 60) return rtf.format(minutes, "minute");
  if (Math.abs(hours) < 24) return rtf.format(hours, "hour");
  if (Math.abs(days) < 30) return rtf.format(days, "day");
  if (Math.abs(months) < 12) return rtf.format(months, "month");
  return rtf.format(years, "year");
};

relativeTime(new Date(Date.now() - 7200000)); // '2 hours ago'
```

### Days between dates

```js
const daysBetween = (d1, d2) =>
  Math.round(Math.abs((d2 - d1) / (1000 * 60 * 60 * 24)));

daysBetween(new Date("2026-01-01"), new Date("2026-12-31")); // 364
```

### Is valid date

```js
const isValidDate = (date) => date instanceof Date && !isNaN(date.getTime());

isValidDate(new Date("invalid")); // false
```

### Start / end of day

```js
const startOfDay = (date) =>
  new Date(date.getFullYear(), date.getMonth(), date.getDate());
const endOfDay = (date) =>
  new Date(
    date.getFullYear(),
    date.getMonth(),
    date.getDate(),
    23,
    59,
    59,
    999,
  );

startOfDay(new Date()); // 00:00:00 today
endOfDay(new Date()); // 23:59:59 today
```

### Format ISO-like string without timezone

```js
const toISOLocal = (date) => {
  const offset = date.getTimezoneOffset();
  const local = new Date(date.getTime() - offset * 60000);
  return local.toISOString().slice(0, 16);
};

toISOLocal(new Date()); // '2026-05-25T14:30'
```

### Add days / months / years

```js
const addDays = (date, days) => {
  const result = new Date(date);
  result.setDate(result.getDate() + days);
  return result;
};

const addMonths = (date, months) => {
  const result = new Date(date);
  result.setMonth(result.getMonth() + months);
  return result;
};

addDays(new Date(), 7);
addMonths(new Date(), 1);
```

---

## 15. Storage (localStorage / sessionStorage)

### Safe storage wrapper

```js
const storage = {
  get(key, defaultValue = null) {
    try {
      const item = localStorage.getItem(key);
      return item ? JSON.parse(item) : defaultValue;
    } catch {
      return defaultValue;
    }
  },

  set(key, value) {
    try {
      localStorage.setItem(key, JSON.stringify(value));
      return true;
    } catch {
      return false;
    }
  },

  remove(key) {
    localStorage.removeItem(key);
  },

  clear() {
    localStorage.clear();
  },

  key(index) {
    return localStorage.key(index);
  },

  get length() {
    return localStorage.length;
  },
};

storage.set("user", { id: 1, name: "Alice" });
const user = storage.get("user");
```

### Session-only storage

```js
const session = {
  get(key, defaultValue = null) {
    try {
      const item = sessionStorage.getItem(key);
      return item ? JSON.parse(item) : defaultValue;
    } catch {
      return defaultValue;
    }
  },
  set(key, value) {
    sessionStorage.setItem(key, JSON.stringify(value));
  },
  remove(key) {
    sessionStorage.removeItem(key);
  },
  clear() {
    sessionStorage.clear();
  },
};
```

### Storage with expiry

```js
const storageWithExpiry = {
  set(key, value, ttlMs) {
    const item = {
      value,
      expiresAt: Date.now() + ttlMs,
    };
    localStorage.setItem(key, JSON.stringify(item));
  },

  get(key, defaultValue = null) {
    const raw = localStorage.getItem(key);
    if (!raw) return defaultValue;
    try {
      const item = JSON.parse(raw);
      if (Date.now() > item.expiresAt) {
        localStorage.removeItem(key);
        return defaultValue;
      }
      return item.value;
    } catch {
      return defaultValue;
    }
  },
};

storageWithExpiry.set("token", "abc123", 3600000); // 1 hour
storageWithExpiry.get("token");
```

---

## 16. Cookies

### Get cookie

```js
const getCookie = (name) => {
  const match = document.cookie.match(new RegExp(`(?:^|; )${name}=([^;]*)`));
  return match ? decodeURIComponent(match[1]) : null;
};

getCookie("session");
```

### Set cookie

```js
const setCookie = (name, value, days = 7, path = "/") => {
  const expires = new Date(Date.now() + days * 864e5).toUTCString();
  document.cookie = `${encodeURIComponent(name)}=${encodeURIComponent(value)}; expires=${expires}; path=${path}`;
};

setCookie("theme", "dark", 30);
```

### Delete cookie

```js
const deleteCookie = (name, path = "/") => {
  document.cookie = `${encodeURIComponent(name)}=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=${path}`;
};

deleteCookie("session");
```

---

## 17. Regular Expressions

### Email validation

```js
const isValidEmail = (email) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);

isValidEmail("user@example.com"); // true
```

### URL validation

```js
const isValidUrl = (url) => {
  try {
    new URL(url);
    return true;
  } catch {
    return false;
  }
};
```

### Password strength

```js
const passwordStrength = (password) => {
  let score = 0;
  if (password.length >= 8) score++;
  if (/[a-z]/.test(password) && /[A-Z]/.test(password)) score++;
  if (/\d/.test(password)) score++;
  if (/[^a-zA-Z0-9]/.test(password)) score++;
  return score; // 0-4
};
```

### Extract URLs from text

```js
const extractUrls = (text) => text.match(/https?:\/\/[^\s]+/g) || [];

extractUrls("Visit https://example.com and http://test.com");
// ['https://example.com', 'http://test.com']
```

### Validate phone number (basic)

```js
const isValidPhone = (phone) => /^\+?[\d\s-()]{7,15}$/.test(phone);
```

### Match hex color

```js
const isValidHexColor = (color) =>
  /^#([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$/.test(color);
```

### Trim whitespace

```js
const trim = (str) => str.replace(/^\s+|\s+$/g, "");

trim("  hello  "); // 'hello'
```

---

## 18. Validation Utilities

### Required fields

```js
const validateRequired = (obj, fields) => {
  const missing = fields.filter(
    (f) =>
      !(f in obj) || obj[f] === undefined || obj[f] === null || obj[f] === "",
  );
  if (missing.length > 0) {
    throw new Error(`Missing required fields: ${missing.join(", ")}`);
  }
  return true;
};

validateRequired({ name: "Alice" }, ["name", "email"]);
// Error: Missing required fields: email
```

### Min / max length

```js
const validateLength = (str, min, max) => {
  if (str.length < min) throw new Error(`Minimum ${min} characters required`);
  if (str.length > max) throw new Error(`Maximum ${max} characters allowed`);
};
```

### Validate number range

```js
const validateRange = (num, min, max) => {
  if (typeof num !== "number") throw new Error("Value must be a number");
  if (num < min || num > max)
    throw new Error(`Value must be between ${min} and ${max}`);
};
```

---

## 19. DOM Manipulation

### Create element with attributes

```js
const createElement = (tag, attrs = {}, children = []) => {
  const el = document.createElement(tag);
  for (const [key, value] of Object.entries(attrs)) {
    if (key.startsWith("on")) {
      el.addEventListener(key.slice(2).toLowerCase(), value);
    } else if (key === "className") {
      el.className = value;
    } else {
      el.setAttribute(key, value);
    }
  }
  for (const child of children) {
    el.append(
      typeof child === "string" ? document.createTextNode(child) : child,
    );
  }
  return el;
};

const btn = createElement(
  "button",
  {
    className: "btn",
    onClick: () => alert("Clicked"),
  },
  ["Click me"],
);
```

### Insert after

```js
const insertAfter = (newNode, referenceNode) => {
  referenceNode.parentNode.insertBefore(newNode, referenceNode.nextSibling);
};
```

### Remove element

```js
const remove = (el) => el.parentNode && el.parentNode.removeChild(el);
```

### Get all siblings

```js
const siblings = (el) =>
  [...el.parentNode.childNodes].filter(
    (child) => child !== el && child.nodeType === 1,
  );
```

### Scroll to top

```js
const scrollToTop = (behavior = "smooth") =>
  window.scrollTo({ top: 0, behavior });
```

### Scroll to element

```js
const scrollToEl = (el, behavior = "smooth") =>
  el.scrollIntoView({ behavior, block: "start" });
```

### Toggle class

```js
const toggleClass = (el, className) => el.classList.toggle(className);
const addClass = (el, className) => el.classList.add(className);
const removeClass = (el, className) => el.classList.remove(className);
const hasClass = (el, className) => el.classList.contains(className);
```

---

## 20. URL & Query String

### Get query params

```js
const getParams = (url = window.location.href) => {
  const { searchParams } = new URL(url);
  return Object.fromEntries(searchParams.entries());
};

getParams("https://example.com?page=1&q=test");
// { page: '1', q: 'test' }
```

### Update query param

```js
const setParam = (key, value, url = window.location.href) => {
  const u = new URL(url);
  u.searchParams.set(key, value);
  return u.toString();
};

setParam("page", "2");
```

### Remove query param

```js
const removeParam = (key, url = window.location.href) => {
  const u = new URL(url);
  u.searchParams.delete(key);
  return u.toString();
};
```

### Get current route path

```js
const currentPath = () => window.location.pathname;
const currentHash = () => window.location.hash;
const currentOrigin = () => window.location.origin;
```

### Redirect

```js
const redirect = (url, replace = false) => {
  if (replace) window.location.replace(url);
  else window.location.href = url;
};
```

---

## 21. Design Patterns

### Observer (Pub/Sub)

```js
class EventBus {
  constructor() {
    this.listeners = new Map();
  }

  on(event, fn) {
    if (!this.listeners.has(event)) this.listeners.set(event, new Set());
    this.listeners.get(event).add(fn);
    return () => this.off(event, fn);
  }

  off(event, fn) {
    this.listeners.get(event)?.delete(fn);
  }

  emit(event, ...args) {
    this.listeners.get(event)?.forEach((fn) => fn(...args));
  }

  once(event, fn) {
    const wrapper = (...args) => {
      fn(...args);
      this.off(event, wrapper);
    };
    this.on(event, wrapper);
  }
}

const bus = new EventBus();
const unsub = bus.on("user:login", (user) => console.log(user));
bus.emit("user:login", { id: 1 });
unsub();
```

### Singleton

```js
const singleton = (fn) => {
  let instance;
  return (...args) => {
    if (!instance) instance = fn(...args);
    return instance;
  };
};

const createDb = singleton(() => ({ connection: "connected" }));
const db1 = createDb();
const db2 = createDb();
db1 === db2; // true
```

### Factory

```js
class ServiceFactory {
  static registry = new Map();

  static register(name, cls) {
    this.registry.set(name, cls);
  }

  static create(name, ...args) {
    const Cls = this.registry.get(name);
    if (!Cls) throw new Error(`Service ${name} not found`);
    return new Cls(...args);
  }
}

class EmailService {
  send(msg) {
    console.log("Email:", msg);
  }
}

ServiceFactory.register("email", EmailService);
const svc = ServiceFactory.create("email");
svc.send("Hello");
```

### Command pattern

```js
class Command {
  constructor(execute, undo) {
    this.executeFn = execute;
    this.undoFn = undo;
  }

  execute() {
    this.executeFn();
  }
  undo() {
    this.undoFn?.();
  }
}

class CommandHistory {
  constructor() {
    this.history = [];
  }

  execute(command) {
    command.execute();
    this.history.push(command);
  }

  undo() {
    const command = this.history.pop();
    if (command) command.undo();
  }
}
```

### State machine

```js
class StateMachine {
  constructor(initial, transitions) {
    this.state = initial;
    this.transitions = transitions; // { from: { event: to } }
    this.handlers = new Map();
  }

  on(event, fn) {
    if (!this.handlers.has(event)) this.handlers.set(event, []);
    this.handlers.get(event).push(fn);
  }

  transition(event) {
    const currentTransitions = this.transitions[this.state];
    const nextState = currentTransitions?.[event];
    if (!nextState)
      throw new Error(`Invalid transition: ${this.state} -> ${event}`);
    this.state = nextState;
    this.handlers.get(event)?.forEach((fn) => fn(this.state));
  }
}

const machine = new StateMachine("idle", {
  idle: { START: "running" },
  running: { STOP: "idle", PAUSE: "paused" },
  paused: { RESUME: "running", STOP: "idle" },
});

machine.on("START", () => console.log("Started"));
machine.transition("START"); // 'Started', state = 'running'
```

---

## 22. Data Structures

### Stack (LIFO)

```js
class Stack {
  #items = [];

  push(item) {
    this.#items.push(item);
  }
  pop() {
    return this.#items.pop();
  }
  peek() {
    return this.#items[this.#items.length - 1];
  }
  get size() {
    return this.#items.length;
  }
  get isEmpty() {
    return this.#items.length === 0;
  }
  clear() {
    this.#items = [];
  }
}

const stack = new Stack();
stack.push(1);
stack.push(2);
stack.pop(); // 2
```

### Queue (FIFO)

```js
class Queue {
  #items = [];

  enqueue(item) {
    this.#items.push(item);
  }
  dequeue() {
    return this.#items.shift();
  }
  peek() {
    return this.#items[0];
  }
  get size() {
    return this.#items.length;
  }
  get isEmpty() {
    return this.#items.length === 0;
  }
}

const q = new Queue();
q.enqueue(1);
q.enqueue(2);
q.dequeue(); // 1
```

### Linked List

```js
class ListNode {
  constructor(value) {
    this.value = value;
    this.next = null;
  }
}

class LinkedList {
  constructor() {
    this.head = null;
    this.tail = null;
    this.length = 0;
  }

  append(value) {
    const node = new ListNode(value);
    if (!this.head) {
      this.head = node;
      this.tail = node;
    } else {
      this.tail.next = node;
      this.tail = node;
    }
    this.length++;
  }

  prepend(value) {
    const node = new ListNode(value);
    if (!this.head) {
      this.head = node;
      this.tail = node;
    } else {
      node.next = this.head;
      this.head = node;
    }
    this.length++;
  }

  delete(value) {
    if (!this.head) return false;
    if (this.head.value === value) {
      this.head = this.head.next;
      this.length--;
      return true;
    }
    let current = this.head;
    while (current.next) {
      if (current.next.value === value) {
        current.next = current.next.next;
        if (!current.next) this.tail = current;
        this.length--;
        return true;
      }
      current = current.next;
    }
    return false;
  }

  toArray() {
    const result = [];
    let current = this.head;
    while (current) {
      result.push(current.value);
      current = current.next;
    }
    return result;
  }
}
```

### Binary Heap (Min-Heap)

```js
class MinHeap {
  constructor() {
    this.heap = [];
  }

  insert(value) {
    this.heap.push(value);
    this._bubbleUp(this.heap.length - 1);
  }

  extractMin() {
    if (this.heap.length === 0) return undefined;
    [this.heap[0], this.heap[this.heap.length - 1]] = [
      this.heap[this.heap.length - 1],
      this.heap[0],
    ];
    const min = this.heap.pop();
    this._sinkDown(0);
    return min;
  }

  peek() {
    return this.heap[0];
  }

  get size() {
    return this.heap.length;
  }

  _bubbleUp(index) {
    while (index > 0) {
      const parent = Math.floor((index - 1) / 2);
      if (this.heap[parent] <= this.heap[index]) break;
      [this.heap[parent], this.heap[index]] = [
        this.heap[index],
        this.heap[parent],
      ];
      index = parent;
    }
  }

  _sinkDown(index) {
    while (true) {
      let smallest = index;
      const left = 2 * index + 1;
      const right = 2 * index + 2;
      if (left < this.heap.length && this.heap[left] < this.heap[smallest])
        smallest = left;
      if (right < this.heap.length && this.heap[right] < this.heap[smallest])
        smallest = right;
      if (smallest === index) break;
      [this.heap[index], this.heap[smallest]] = [
        this.heap[smallest],
        this.heap[index],
      ];
      index = smallest;
    }
  }
}
```

### Trie (Prefix Tree)

```js
class TrieNode {
  constructor() {
    this.children = new Map();
    this.isEnd = false;
  }
}

class Trie {
  constructor() {
    this.root = new TrieNode();
  }

  insert(word) {
    let node = this.root;
    for (const ch of word) {
      if (!node.children.has(ch)) node.children.set(ch, new TrieNode());
      node = node.children.get(ch);
    }
    node.isEnd = true;
  }

  search(word) {
    let node = this.root;
    for (const ch of word) {
      if (!node.children.has(ch)) return false;
      node = node.children.get(ch);
    }
    return node.isEnd;
  }

  startsWith(prefix) {
    let node = this.root;
    for (const ch of prefix) {
      if (!node.children.has(ch)) return false;
      node = node.children.get(ch);
    }
    return true;
  }
}
```

### Graph (Adjacency List)

```js
class Graph {
  constructor() {
    this.adjacencyList = new Map();
  }

  addVertex(v) {
    if (!this.adjacencyList.has(v)) this.adjacencyList.set(v, []);
  }

  addEdge(v1, v2, directed = false) {
    this.addVertex(v1);
    this.addVertex(v2);
    this.adjacencyList.get(v1).push(v2);
    if (!directed) this.adjacencyList.get(v2).push(v1);
  }

  bfs(start) {
    const visited = new Set();
    const queue = [start];
    const result = [];
    visited.add(start);
    while (queue.length > 0) {
      const vertex = queue.shift();
      result.push(vertex);
      for (const neighbor of this.adjacencyList.get(vertex) || []) {
        if (!visited.has(neighbor)) {
          visited.add(neighbor);
          queue.push(neighbor);
        }
      }
    }
    return result;
  }

  dfs(start) {
    const visited = new Set();
    const result = [];
    const dfsRecursive = (vertex) => {
      visited.add(vertex);
      result.push(vertex);
      for (const neighbor of this.adjacencyList.get(vertex) || []) {
        if (!visited.has(neighbor)) dfsRecursive(neighbor);
      }
    };
    dfsRecursive(start);
    return result;
  }
}

const g = new Graph();
g.addEdge("A", "B");
g.addEdge("A", "C");
g.addEdge("B", "D");
console.log(g.bfs("A")); // ['A', 'B', 'C', 'D']
```

---

## 23. Error Handling

### Custom error class

```js
class AppError extends Error {
  constructor(message, statusCode = 500, code = "INTERNAL_ERROR") {
    super(message);
    this.name = "AppError";
    this.statusCode = statusCode;
    this.code = code;
    Error.captureStackTrace(this, this.constructor);
  }

  toJSON() {
    return {
      error: {
        code: this.code,
        message: this.message,
        statusCode: this.statusCode,
      },
    };
  }
}

class NotFoundError extends AppError {
  constructor(resource = "Resource") {
    super(`${resource} not found`, 404, "NOT_FOUND");
    this.name = "NotFoundError";
  }
}

throw new NotFoundError("User");
```

### Result type (Either)

```js
class Result {
  static ok(value) {
    return new Result(true, value, null);
  }

  static fail(error) {
    return new Result(false, null, error);
  }

  constructor(isOk, value, error) {
    this.isOk = isOk;
    this.value = value;
    this.error = error;
  }

  get isFail() {
    return !this.isOk;
  }

  unwrap() {
    if (this.isFail) throw this.error;
    return this.value;
  }

  unwrapOr(defaultValue) {
    return this.isOk ? this.value : defaultValue;
  }

  map(fn) {
    return this.isOk ? Result.ok(fn(this.value)) : this;
  }

  chain(fn) {
    return this.isOk ? fn(this.value) : this;
  }

  match({ ok, fail }) {
    return this.isOk ? ok(this.value) : fail(this.error);
  }
}

function divide(a, b) {
  if (b === 0) return Result.fail(new Error("Division by zero"));
  return Result.ok(a / b);
}

const r = divide(10, 2);
r.match({
  ok: (val) => console.log(val),
  fail: (err) => console.error(err.message),
});
```

### Try-catch wrapper

```js
const tryCatch =
  (fn, fallback) =>
  async (...args) => {
    try {
      return await fn(...args);
    } catch (error) {
      return typeof fallback === "function" ? fallback(error) : fallback;
    }
  };

const safeFetch = tryCatch(
  async (url) => {
    const res = await fetch(url);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return res.json();
  },
  { data: null, error: "Request failed" },
);

const data = await safeFetch("/api/data");
```

### Global error handler

```js
const setupGlobalErrorHandler = () => {
  window.addEventListener("unhandledrejection", (event) => {
    console.error("Unhandled Promise rejection:", event.reason);
    event.preventDefault();
  });

  window.addEventListener("error", (event) => {
    console.error("Uncaught error:", event.error || event.message);
    event.preventDefault();
  });
};

setupGlobalErrorHandler();
```

---

## 24. Logging & Debugging

### Simple logger

```js
const logger = {
  debug: (...args) => console.debug("[DEBUG]", ...args),
  info: (...args) => console.info("[INFO]", ...args),
  warn: (...args) => console.warn("[WARN]", ...args),
  error: (...args) => console.error("[ERROR]", ...args),
  group: (label) => console.group(label),
  groupEnd: () => console.groupEnd(),
};

logger.info("App started");
```

### Performance measurement

```js
const measure = (label, fn) => {
  console.time(label);
  const result = fn();
  console.timeEnd(label);
  return result;
};

const asyncMeasure = async (label, fn) => {
  console.time(label);
  const result = await fn();
  console.timeEnd(label);
  return result;
};

measure("sort", () => largeArray.sort());
```

### Trace object changes

```js
const trace = (obj, label = "obj") =>
  new Proxy(obj, {
    get(target, prop) {
      console.log(`  ${label}.${String(prop)} (get)`);
      return target[prop];
    },
    set(target, prop, value) {
      console.log(`  ${label}.${String(prop)} = ${JSON.stringify(value)}`);
      target[prop] = value;
      return true;
    },
  });

const user = trace({ name: "Alice" }, "user");
user.name; // '  user.name (get)'
user.name = "Bob"; // '  user.name = "Bob"'
```

---

## 25. Polyfills & Compatibility

### Array.flat polyfill

```js
if (!Array.prototype.flat) {
  Object.defineProperty(Array.prototype, "flat", {
    value(depth = 1) {
      return this.reduce(
        (acc, val) =>
          acc.concat(
            Array.isArray(val) && depth > 1 ? val.flat(depth - 1) : val,
          ),
        [],
      );
    },
  });
}
```

### Array.flatMap polyfill

```js
if (!Array.prototype.flatMap) {
  Object.defineProperty(Array.prototype, "flatMap", {
    value(fn) {
      return this.reduce((acc, val, i, arr) => acc.concat(fn(val, i, arr)), []);
    },
  });
}
```

### Object.fromEntries polyfill

```js
if (!Object.fromEntries) {
  Object.fromEntries = (entries) =>
    [...entries].reduce((obj, [key, value]) => {
      obj[key] = value;
      return obj;
    }, {});
}
```

### String.replaceAll polyfill

```js
if (!String.prototype.replaceAll) {
  Object.defineProperty(String.prototype, "replaceAll", {
    value(search, replacement) {
      if (search instanceof RegExp && !search.flags.includes("g")) {
        throw new TypeError("replaceAll must have global flag");
      }
      const regex = search instanceof RegExp ? search : new RegExp(search, "g");
      return this.replace(regex, replacement);
    },
  });
}
```

### structuredClone polyfill

```js
if (!globalThis.structuredClone) {
  globalThis.structuredClone = (obj) => JSON.parse(JSON.stringify(obj));
}
```

### requestIdleCallback polyfill

```js
if (!window.requestIdleCallback) {
  window.requestIdleCallback = (fn) => {
    const start = Date.now();
    return setTimeout(() => {
      fn({
        didTimeout: false,
        timeRemaining: () => Math.max(0, 50 - (Date.now() - start)),
      });
    }, 1);
  };
  window.cancelIdleCallback = (id) => clearTimeout(id);
}
```
