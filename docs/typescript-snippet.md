# TypeScript Snippets

## Table of Contents
1. [Basic Types & Interfaces](#1-basic-types--interfaces)
2. [Utility Types](#2-utility-types)
3. [Generics](#3-generics)
4. [Type Guards & Narrowing](#4-type-guards--narrowing)
5. [Mapped Types](#5-mapped-types)
6. [Conditional Types](#6-conditional-types)
7. [Template Literal Types](#7-template-literal-types)
8. [Discriminated Unions](#8-discriminated-unions)
9. [Enums & Const Enums](#9-enums--const-enums)
10. [Functions & Overloads](#10-functions--overloads)
11. [Classes & Mixins](#11-classes--mixins)
12. [Decorators](#12-decorators)
13. [Branded Types](#13-branded-types)
14. [Assertion Functions](#14-assertion-functions)
15. [The satisfies Operator](#15-the-satisfies-operator)
16. [Satisfies + as const](#16-satisfies--as-const)
17. [Nominal Typing Patterns](#17-nominal-typing-patterns)
18. [Builder Pattern](#18-builder-pattern)
19. [Result / Either Type](#19-result--either-type)
20. [Option / Maybe Type](#20-option--maybe-type)
21. [Async Patterns](#21-async-patterns)
22. [API Client Patterns](#22-api-client-patterns)
23. [Event Emitter](#23-event-emitter)
24. [Dependency Injection](#24-dependency-injection)
25. [Configuration & Environment](#25-configuration--environment)

---

## 1. Basic Types & Interfaces

### Primitives & basic types
```ts
// Primitives
let name: string = 'Alice';
let age: number = 30;
let isActive: boolean = true;
let id: symbol = Symbol('id');
let big: bigint = 100n;

// Nullish
let nullable: string | null = null;
let undef: number | undefined = undefined;

// Any / unknown / never / void
let flexible: any = 'can be anything';
let safe: unknown = JSON.parse('{"a":1}');
function throwError(): never { throw new Error(); }
function log(msg: string): void { console.log(msg); }
```

### Interfaces vs Types
```ts
// Interface (extends, declaration merging)
interface User {
  id: string;
  name: string;
  email: string;
}

interface Admin extends User {
  role: 'admin';
  permissions: string[];
}

// Type alias (unions, intersections, primitives)
type Status = 'active' | 'inactive' | 'pending';
type Point = { x: number; y: number };
type NamedPoint = Point & { name: string };
type ID = string | number;
```

### Index signatures
```ts
interface Dictionary<T> {
  [key: string]: T;
}

const dict: Dictionary<number> = { a: 1, b: 2 };

// Specific + index
interface Config {
  mode: 'dev' | 'prod';
  [key: string]: unknown;
}
```

### Readonly & Optional
```ts
interface Todo {
  readonly id: string;
  title: string;
  description?: string;
  completed?: boolean;
}

const todo: Todo = { id: '1', title: 'Task' };
// todo.id = '2'; // Error
```

### Tuple types
```ts
type Pair<T, U> = [T, U];
type RGB = [number, number, number];
type NamedTuple = [name: string, age: number, active: boolean];

const pair: Pair<string, number> = ['hello', 42];
const color: RGB = [255, 0, 0];

// Variadic tuples
type Head<T extends unknown[]> = T extends [infer H, ...unknown[]] ? H : never;
type Tail<T extends unknown[]> = T extends [unknown, ...infer R] ? R : never;
```

### Array types
```ts
const nums1: number[] = [1, 2, 3];
const nums2: Array<number> = [1, 2, 3];
const readonlyNums: ReadonlyArray<number> = [1, 2, 3];

// Non-empty array
type NonEmptyArray<T> = [T, ...T[]];
const nonEmpty: NonEmptyArray<string> = ['a', 'b']; // OK
// const empty: NonEmptyArray<string> = []; // Error
```

---

## 2. Utility Types

### Built-in utility types
```ts
interface Person {
  name: string;
  age: number;
  email: string;
  address?: string;
}

// Partial - all optional
const update: Partial<Person> = { age: 31 };

// Required - all required
const full: Required<Person> = { name: 'A', age: 1, email: 'a@b.com', address: 'x' };

// Readonly - all readonly
const frozen: Readonly<Person> = { name: 'A', age: 1, email: 'a@b.com' };

// Pick - subset of keys
const nameAndAge: Pick<Person, 'name' | 'age'> = { name: 'A', age: 1 };

// Omit - remove keys
const withoutEmail: Omit<Person, 'email'> = { name: 'A', age: 1 };

// Record - key-value map
const roles: Record<string, string[]> = { admin: ['read', 'write'], user: ['read'] };

// Extract / Exclude (union filtering)
type Colors = 'red' | 'green' | 'blue';
type Warm = Extract<Colors, 'red' | 'yellow'>; // 'red'
type NotGreen = Exclude<Colors, 'green'>; // 'red' | 'blue'

// NonNullable - remove null/undefined
type Maybe = string | null | undefined;
type Definite = NonNullable<Maybe>; // string
```

### ReturnType / Parameters / ConstructorParameters
```ts
function createUser(name: string, age: number): Person {
  return { name, age, email: '' };
}

type CreateUserParams = Parameters<typeof createUser>;
type CreateUserReturn = ReturnType<typeof createUser>;

class MyClass {
  constructor(a: string, b: number) {}
}
type MyClassParams = ConstructorParameters<typeof MyClass>;
type MyClassInstance = InstanceType<typeof MyClass>;
```

### Awaited (unwraps promises)
```ts
type AsyncData = Promise<Promise<string>>;
type Data = Awaited<AsyncData>; // string

async function fetchUser(): Promise<{ id: string }> {
  return { id: '1' };
}
type UserData = Awaited<ReturnType<typeof fetchUser>>; // { id: string }
```

### ThisParameterType / OmitThisParameter
```ts
function onClick(this: HTMLElement, e: MouseEvent) {}

type ThisType_of_onClick = ThisParameterType<typeof onClick>; // HTMLElement
type WithoutThis = OmitThisParameter<typeof onClick>; // (e: MouseEvent) => void
```

### Uppercase / Lowercase / Capitalize / Uncapitalize
```ts
type Lower = 'hello';
type Upper = Uppercase<Lower>; // 'HELLO'
type Cap = Capitalize<Lower>; // 'Hello'
type Uncap = Uncapitalize<'Hello'>; // 'hello'
```

---

## 3. Generics

### Basic generic function
```ts
function identity<T>(value: T): T {
  return value;
}

const num = identity(42); // number
const str = identity('hello'); // string
```

### Generic constraints
```ts
interface HasLength {
  length: number;
}

function logLength<T extends HasLength>(value: T): T {
  console.log(value.length);
  return value;
}

logLength('hello'); // 5
logLength([1, 2, 3]); // 3
// logLength(42); // Error
```

### Generic interface
```ts
interface Repository<T, ID = string> {
  findById(id: ID): Promise<T | null>;
  findAll(): Promise<T[]>;
  create(data: Omit<T, 'id'>): Promise<T>;
  update(id: ID, data: Partial<T>): Promise<T>;
  delete(id: ID): Promise<void>;
}

class UserRepo implements Repository<{ id: string; name: string }> {
  async findById(id: string) { return null; }
  async findAll() { return []; }
  async create(data) { return { id: '1', ...data }; }
  async update(id, data) { return { id, name: '' }; }
  async delete(id) {}
}
```

### Generic class
```ts
class Stack<T> {
  private items: T[] = [];

  push(item: T): void {
    this.items.push(item);
  }

  pop(): T | undefined {
    return this.items.pop();
  }

  peek(): T | undefined {
    return this.items[this.items.length - 1];
  }

  get size(): number {
    return this.items.length;
  }

  *[Symbol.iterator](): Iterator<T> {
    for (const item of this.items) yield item;
  }
}

const stack = new Stack<number>();
stack.push(1);
stack.push(2);
stack.pop(); // 2
```

### Generic with keyof constraint
```ts
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}

const person: Person = { name: 'Alice', age: 30, email: 'a@b.com' };
getProperty(person, 'name'); // string
getProperty(person, 'age');  // number
// getProperty(person, 'invalid'); // Error
```

### Generic mapped parameter
```ts
function mapObject<T, R>(
  obj: { [K in keyof T]: T[K] },
  fn: <K extends keyof T>(value: T[K], key: K) => R
): { [K in keyof T]: R } {
  const result = {} as { [K in keyof T]: R };
  for (const key in obj) {
    result[key] = fn(obj[key], key);
  }
  return result;
}

const doubled = mapObject({ a: 1, b: 2 }, (v) => v * 2);
// { a: number, b: number }
```

### Generic type inference from arguments
```ts
function createPair<T, U>(first: T, second: U): [T, U] {
  return [first, second];
}

const pair = createPair('hello', 42); // [string, number]
```

### Const type parameters (TypeScript 5.0+)
```ts
function tuples<T extends readonly string[]>(...args: T): T {
  return args;
}

const result = tuples('a', 'b', 'c');
// type: readonly ["a", "b", "c"]
```

---

## 4. Type Guards & Narrowing

### typeof guard
```ts
function format(value: string | number): string {
  if (typeof value === 'string') {
    return value.toUpperCase();
  }
  return value.toFixed(2);
}
```

### instanceof guard
```ts
class ApiError extends Error {
  constructor(public statusCode: number, message: string) {
    super(message);
  }
}

function handleError(error: unknown) {
  if (error instanceof ApiError) {
    console.log(`API Error ${error.statusCode}: ${error.message}`);
  } else if (error instanceof Error) {
    console.log(error.message);
  }
}
```

### Custom type guard (value is)
```ts
interface Cat { meow(): void }
interface Dog { bark(): void }

function isCat(pet: Cat | Dog): pet is Cat {
  return 'meow' in pet;
}

function handlePet(pet: Cat | Dog) {
  if (isCat(pet)) {
    pet.meow(); // narrowed to Cat
  } else {
    pet.bark(); // narrowed to Dog
  }
}
```

### in operator narrowing
```ts
interface Square { kind: 'square'; size: number }
interface Circle { kind: 'circle'; radius: number }

function area(shape: Square | Circle): number {
  if ('size' in shape) {
    return shape.size ** 2;
  }
  return Math.PI * shape.radius ** 2;
}
```

### Discriminated union switch
```ts
type Shape =
  | { kind: 'circle'; radius: number }
  | { kind: 'square'; size: number }
  | { kind: 'triangle'; base: number; height: number };

function getArea(shape: Shape): number {
  switch (shape.kind) {
    case 'circle':
      return Math.PI * shape.radius ** 2;
    case 'square':
      return shape.size ** 2;
    case 'triangle':
      return (shape.base * shape.height) / 2;
    default:
      // Exhaustive check
      const _exhaustive: never = shape;
      throw new Error(`Unknown shape: ${_exhaustive}`);
  }
}
```

### Assertion function
```ts
function assert(condition: unknown, message?: string): asserts condition {
  if (!condition) throw new Error(message ?? 'Assertion failed');
}

function assertDefined<T>(value: T | null | undefined): asserts value is T {
  if (value === null || value === undefined) {
    throw new Error('Value is null or undefined');
  }
}

function process(data: unknown) {
  assert(typeof data === 'string', 'Expected string');
  data.toUpperCase(); // narrowed to string
}

const maybe: string | null = getValue();
assertDefined(maybe);
maybe.toUpperCase(); // narrowed to string
```

### Type predicate array filter
```ts
function isDefined<T>(value: T | null | undefined): value is T {
  return value !== null && value !== undefined;
}

const items: (string | null)[] = ['a', null, 'b', undefined, 'c'];
const defined: string[] = items.filter(isDefined);
// type: string[], not (string | null)[]
```

---

## 5. Mapped Types

### Basic mapped type
```ts
type Nullable<T> = { [K in keyof T]: T[K] | null };
type Optional<T> = { [K in keyof T]?: T[K] };
type ReadOnly<T> = { readonly [K in keyof T]: T[K] };

const nullable: Nullable<Person> = { name: null, age: 30, email: 'a@b.com' };
```

### With key remapping (TS 4.1+)
```ts
type Getters<T> = {
  [K in keyof T as `get${Capitalize<K & string>}`]: () => T[K];
};

type PersonGetters = Getters<{ name: string; age: number }>;
// { getName: () => string; getAge: () => number }
```

### Filter keys by value type
```ts
type ExtractKeysByValue<T, V> = {
  [K in keyof T]: T[K] extends V ? K : never
}[keyof T];

type StringKeys<T> = ExtractKeysByValue<T, string>;
type NumberKeys<T> = ExtractKeysByValue<T, number>;

interface Example {
  name: string;
  age: number;
  email: string;
  id: number;
}

type StrKeys = StringKeys<Example>; // "name" | "email"
type NumKeys = NumberKeys<Example>; // "age" | "id"
```

### PickByValue + OmitByValue
```ts
type PickByValue<T, V> = {
  [K in keyof T as T[K] extends V ? K : never]: T[K];
};

type OmitByValue<T, V> = {
  [K in keyof T as T[K] extends V ? never : K]: T[K];
};

type StringsOnly = PickByValue<Example, string>;
// { name: string; email: string }
```

### Deep readonly
```ts
type DeepReadonly<T> = {
  readonly [K in keyof T]: T[K] extends Record<string, unknown> | Array<unknown>
    ? DeepReadonly<T[K]>
    : T[K];
};

interface Config {
  db: { host: string; port: number };
  features: string[];
}
type ReadonlyConfig = DeepReadonly<Config>;
```

### Mapped type with union
```ts
type EventHandlers<T extends string> = {
  [K in T as `on${Capitalize<K>}`]: (payload: { type: K }) => void;
};

type ClickEvents = 'click' | 'doubleclick' | 'contextmenu';
type ClickHandlers = EventHandlers<ClickEvents>;
// { onClick: (p: { type: 'click' }) => void; ... }
```

---

## 6. Conditional Types

### Basic conditional
```ts
type IsString<T> = T extends string ? 'yes' : 'no';
type A = IsString<'hello'>; // 'yes'
type B = IsString<42>;       // 'no'
```

### Distributive conditional types
```ts
type ToArray<T> = T extends unknown ? T[] : never;
type Result = ToArray<string | number>;
// string[] | number[] (distributes)

type ToArrayNonDist<T> = [T] extends [unknown] ? T[] : never;
type Result2 = ToArrayNonDist<string | number>;
// (string | number)[] (does not distribute)
```

### Infer keyword
```ts
// Extract return type
type MyReturnType<T> = T extends (...args: unknown[]) => infer R ? R : never;

// Extract promise value
type Unwrap<T> = T extends Promise<infer U> ? U : T;
type A = Unwrap<Promise<string>>; // string
type B = Unwrap<number>; // number

// Extract array element
type ElementType<T> = T extends (infer U)[] ? U : never;
type NumElem = ElementType<number[]>; // number

// Extract first parameter
type FirstParam<T> = T extends (first: infer F, ...rest: unknown[]) => unknown ? F : never;
```

### Recursive conditional types
```ts
type DeepPartial<T> = T extends object
  ? { [K in keyof T]?: DeepPartial<T[K]> }
  : T;

type DeepRequired<T> = T extends object
  ? { [K in keyof T]-?: DeepRequired<T[K]> }
  : T;

interface Nested {
  a: { b: { c: string; d?: number } };
  e?: string;
}
type PartialNested = DeepPartial<Nested>;
type RequiredNested = DeepRequired<Nested>;
```

### Flatten type
```ts
type Flatten<T> = T extends Array<infer U> ? Flatten<U> : T;

type Flat = Flatten<[[[1]], [[2]], 3]>;
// 1 | 2 | 3
```

### Union to intersection
```ts
type UnionToIntersection<U> =
  (U extends unknown ? (k: U) => void : never) extends (k: infer I) => void
    ? I
    : never;

type Union = { a: string } | { b: number };
type Intersection = UnionToIntersection<Union>; // { a: string } & { b: number }
```

---

## 7. Template Literal Types

### Basic template literal
```ts
type EventName = `on${Capitalize<string>}`;
type Event = `user:${string}`;
type Route = `/${string}`;

const route: Route = '/api/users'; // OK
// const bad: Route = 'api/users'; // Error (no leading /)
```

### Union in template literals
```ts
type Method = 'GET' | 'POST' | 'PUT' | 'DELETE';
type Path = `/api/${string}`;
type APIEndpoint = `${Method} ${Path}`;

const endpoint: APIEndpoint = 'GET /api/users'; // OK
```

### Template literal with infer
```ts
type ExtractId<T extends string> =
  T extends `/api/${infer Resource}/${infer Id}`
    ? { resource: Resource; id: Id }
    : never;

type UserId = ExtractId<'/api/users/123'>;
// { resource: "users"; id: "123" }
```

### String manipulation with template literals
```ts
type ToCamel<S extends string> =
  S extends `${infer A}_${infer B}`
    ? `${A}${Capitalize<ToCamel<B>>}`
    : S;

type SnakeCase = 'user_name' | 'first_name' | 'last_name';
type CamelCase = ToCamel<SnakeCase>;
// 'userName' | 'firstName' | 'lastName'
```

### CSS type safe properties (example)
```ts
type CSSUnit = 'px' | 'rem' | 'em' | '%' | 'vh' | 'vw';

type CSSLength = `${number}${CSSUnit}`;

const width: CSSLength = '100px'; // OK
const height: CSSLength = '50%';  // OK
// const bad: CSSLength = '10';   // Error

type CSSProperty = `margin${Capitalize<'top' | 'bottom' | 'left' | 'right'>}`;
// 'marginTop' | 'marginBottom' | 'marginLeft' | 'marginRight'
```

### Enum-like const objects with template literals
```ts
const Colors = {
  Primary: '#007bff',
  Secondary: '#6c757d',
  Success: '#28a745',
} as const;

type ColorName = keyof typeof Colors;
type ColorValue = (typeof Colors)[ColorName];
type ColorVar = `--color-${ToCamel<ColorName & string>}`;
// '--color-primary' | '--color-secondary' | '--color-success'
```

---

## 8. Discriminated Unions

### Classic discriminated union
```ts
type ApiResponse<T> =
  | { status: 'success'; data: T }
  | { status: 'error'; error: string; code: number }
  | { status: 'loading' };

function handleResponse<T>(response: ApiResponse<T>) {
  switch (response.status) {
    case 'success':
      return response.data;
    case 'error':
      console.error(`${response.code}: ${response.error}`);
      return null;
    case 'loading':
      return null;
  }
}
```

### Async state machine
```ts
type AsyncState<T, E = Error> =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: T }
  | { status: 'error'; error: E };

class AsyncManager<T, E = Error> {
  private state: AsyncState<T, E> = { status: 'idle' };

  get data() {
    return this.state.status === 'success' ? this.state.data : null;
  }

  get isLoading() {
    return this.state.status === 'loading';
  }

  get error() {
    return this.state.status === 'error' ? this.state.error : null;
  }

  setLoading() { this.state = { status: 'loading' }; }
  setSuccess(data: T) { this.state = { status: 'success', data }; }
  setError(error: E) { this.state = { status: 'error', error }; }
}
```

### Form field state
```ts
type FieldState<T> =
  | { status: 'pristine'; value: T }
  | { status: 'dirty'; value: T }
  | { status: 'touched'; value: T }
  | { status: 'validating'; value: T }
  | { status: 'valid'; value: T }
  | { status: 'invalid'; value: T; error: string };

class FormField<T> {
  private state: FieldState<T>;

  constructor(initial: T) {
    this.state = { status: 'pristine', value: initial };
  }

  get value() { return this.state.value; }
  get isValid() { return this.state.status === 'valid'; }
  get error() { return this.state.status === 'invalid' ? this.state.error : null; }
}
```

### UI Component variants
```ts
type ButtonProps =
  | { variant: 'primary'; size?: 'sm' | 'md' | 'lg' }
  | { variant: 'secondary'; size?: 'sm' | 'md' | 'lg' }
  | { variant: 'ghost'; iconOnly?: boolean }
  | { variant: 'danger'; confirmText?: string };

function Button(props: ButtonProps) {
  switch (props.variant) {
    case 'primary':
    case 'secondary':
      return `<button class="${props.variant} ${props.size ?? 'md'}">`;
    case 'ghost':
      return `<button class="ghost">${props.iconOnly ? 'icon' : ''}`;
    case 'danger':
      return `<button class="danger" data-confirm="${props.confirmText ?? ''}">`;
  }
}
```

### Exhaustive switch helper
```ts
function assertNever(value: never): never {
  throw new Error(`Unexpected value: ${value}`);
}

type Shape =
  | { kind: 'circle'; radius: number }
  | { kind: 'square'; side: number }
  | { kind: 'triangle'; base: number; height: number };

function getArea(shape: Shape): number {
  switch (shape.kind) {
    case 'circle': return Math.PI * shape.radius ** 2;
    case 'square': return shape.side ** 2;
    case 'triangle': return (shape.base * shape.height) / 2;
    default: return assertNever(shape);
  }
}
```

---

## 9. Enums & Const Enums

### Numeric enum
```ts
enum Direction {
  Up = 1,
  Down,
  Left,
  Right,
}

// Usage
const dir: Direction = Direction.Up;
const name = Direction[1]; // 'Up' (reverse mapping)
```

### String enum
```ts
enum HttpStatus {
  OK = '200',
  Created = '201',
  BadRequest = '400',
  Unauthorized = '401',
  NotFound = '404',
  InternalServerError = '500',
}

function isSuccess(status: HttpStatus): boolean {
  return status === HttpStatus.OK || status === HttpStatus.Created;
}
```

### Const enum (zero runtime cost)
```ts
const enum Color {
  Red = '#FF0000',
  Green = '#00FF00',
  Blue = '#0000FF',
}

const bg = Color.Blue; // inlined as '#0000FF' at compile time
```

### Enum as union type
```ts
enum Status {
  Active = 'active',
  Inactive = 'inactive',
  Pending = 'pending',
}

type StatusUnion = `${Status}`; // 'active' | 'inactive' | 'pending'

function handleStatus(s: Status) {
  switch (s) {
    case Status.Active: break;
    case Status.Inactive: break;
    case Status.Pending: break;
  }
}
```

### Const object as enum alternative
```ts
const Permission = {
  Read: 'read',
  Write: 'write',
  Execute: 'execute',
  Admin: 'admin',
} as const;

type Permission = (typeof Permission)[keyof typeof Permission];
// 'read' | 'write' | 'execute' | 'admin'

function checkPermission(p: Permission) {
  if (p === Permission.Admin) return true;
  return false;
}
```

---

## 10. Functions & Overloads

### Function overloads
```ts
function parse(input: string): JSON;
function parse(input: string[]): JSON[];
function parse(input: string | string[]): JSON | JSON[] {
  if (Array.isArray(input)) {
    return input.map((item) => JSON.parse(item));
  }
  return JSON.parse(input);
}

const obj = parse('{"a":1}'); // JSON
const arr = parse(['{"a":1}', '{"b":2}']); // JSON[]
```

### Overloads with different return types
```ts
function find<T extends { id: string }>(items: T[], id: string): T | undefined;
function find<T extends { id: string }>(items: T[], ids: string[]): T[];
function find<T extends { id: string }>(
  items: T[],
  idOrIds: string | string[]
): T | T[] | undefined {
  if (Array.isArray(idOrIds)) {
    return items.filter((item) => idOrIds.includes(item.id));
  }
  return items.find((item) => item.id === idOrIds);
}
```

### Generic rest parameters
```ts
function tuple<T extends unknown[]>(...args: T): T {
  return args;
}

const result = tuple(1, 'hello', true); // [number, string, boolean]
```

### Typed variadic function
```ts
function merge<T extends Record<string, unknown>[]>(
  ...objects: T
): T extends [infer F, ...infer R]
  ? F & (R extends Record<string, unknown>[] ? MergeAll<R> : {})
  : {} {
  return Object.assign({}, ...objects);
}

type MergeAll<T extends Record<string, unknown>[]> =
  T extends [infer F, ...infer R]
    ? F & (R extends Record<string, unknown>[] ? MergeAll<R> : {})
    : {};

const merged = merge({ a: 1 }, { b: 2 }, { c: 3 });
// { a: number } & { b: number } & { c: number }
```

### Function with this parameter
```ts
interface HTMLElement {
  addClickListener(this: HTMLElement, handler: (this: HTMLElement, e: MouseEvent) => void): void;
}

function logger(this: { name: string }, message: string) {
  console.log(`[${this.name}] ${message}`);
}

const ctx = { name: 'App' };
const bound = logger.bind(ctx);
bound('started'); // '[App] started'
```

### Async function with generics
```ts
async function fetchJSON<T>(url: string, options?: RequestInit): Promise<T> {
  const response = await fetch(url, options);
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
  }
  return response.json() as Promise<T>;
}

interface User {
  id: string;
  name: string;
}

const user = await fetchJSON<User>('/api/users/1');
```

---

## 11. Classes & Mixins

### Abstract class
```ts
abstract class Database {
  abstract connect(): Promise<void>;
  abstract query<T>(sql: string): Promise<T[]>;
  abstract close(): Promise<void>;

  async transaction<T>(fn: () => Promise<T>): Promise<T> {
    await this.query('BEGIN');
    try {
      const result = await fn();
      await this.query('COMMIT');
      return result;
    } catch (error) {
      await this.query('ROLLBACK');
      throw error;
    }
  }
}

class PostgresDB extends Database {
  async connect() { /* connect */ }
  async query<T>(sql: string): Promise<T[]> { return []; }
  async close() { /* close */ }
}
```

### Parameter properties
```ts
class UserService {
  constructor(
    private readonly db: Database,
    private readonly logger: Logger,
    public readonly name: string = 'UserService'
  ) {}

  async getUser(id: string) {
    this.logger.info(`Fetching user ${id}`);
    return this.db.query(`SELECT * FROM users WHERE id = $1`, [id]);
  }
}
```

### Getter / Setter
```ts
class Temperature {
  private _celsius = 0;

  get celsius(): number {
    return this._celsius;
  }

  set celsius(value: number) {
    if (value < -273.15) throw new Error('Below absolute zero');
    this._celsius = value;
  }

  get fahrenheit(): number {
    return (this._celsius * 9) / 5 + 32;
  }

  set fahrenheit(value: number) {
    this._celsius = ((value - 32) * 5) / 9;
  }
}
```

### Static members & blocks
```ts
class Config {
  private static cache = new Map<string, string>();

  static {
    // Static initialization block (ES2022+)
    this.cache.set('mode', 'production');
    this.cache.set('version', '1.0.0');
  }

  static get(key: string): string | undefined {
    return this.cache.get(key);
  }

  static set(key: string, value: string): void {
    this.cache.set(key, value);
  }
}

Config.get('mode'); // 'production'
```

### Mixin pattern
```ts
type Constructor<T = object> = abstract new (...args: unknown[]) => T;

function Timestampable<TBase extends Constructor>(Base: TBase) {
  abstract class TimestampableClass extends Base {
    createdAt = new Date();
    updatedAt = new Date();

    touch(): void {
      this.updatedAt = new Date();
    }
  }
  return TimestampableClass;
}

function SoftDeletable<TBase extends Constructor>(Base: TBase) {
  class SoftDeletableClass extends Base {
    deletedAt: Date | null = null;

    softDelete(): void {
      this.deletedAt = new Date();
    }

    restore(): void {
      this.deletedAt = null;
    }

    get isDeleted(): boolean {
      return this.deletedAt !== null;
    }
  }
  return SoftDeletableClass;
}

class BaseEntity {
  constructor(public id: string) {}
}

class User extends Timestampable(SoftDeletable(BaseEntity)) {
  constructor(id: string, public name: string) {
    super(id);
  }
}

const user = new User('1', 'Alice');
user.touch();
user.softDelete();
console.log(user.isDeleted); // true
```

### Class validator pattern
```ts
class Validator<T> {
  private rules: Map<keyof T, ((value: unknown) => string | null)[]> = new Map();

  rule<K extends keyof T>(field: K, validator: (value: T[K]) => string | null): this {
    if (!this.rules.has(field)) this.rules.set(field, []);
    this.rules.get(field)!.push(validator as (value: unknown) => string | null);
    return this;
  }

  validate(data: T): { valid: boolean; errors: Partial<Record<keyof T, string[]>> } {
    const errors: Partial<Record<keyof T, string[]>> = {};
    for (const [field, validators] of this.rules) {
      const fieldErrors = validators
        .map((v) => v(data[field]))
        .filter((e): e is string => e !== null);
      if (fieldErrors.length > 0) errors[field] = fieldErrors;
    }
    return { valid: Object.keys(errors).length === 0, errors };
  }
}

interface UserInput {
  name: string;
  email: string;
}

const validator = new Validator<UserInput>()
  .rule('name', (v) => (v.length < 2 ? 'Too short' : null))
  .rule('email', (v) => (/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v) ? null : 'Invalid email'));

const result = validator.validate({ name: 'A', email: 'bad' });
```

---

## 12. Decorators

### Class decorator
```ts
function sealed(constructor: Function) {
  Object.seal(constructor);
  Object.seal(constructor.prototype);
}

@sealed
class ApiService {
  constructor(public baseUrl: string) {}
}
```

### Method decorator
```ts
function log(
  target: unknown,
  propertyKey: string,
  descriptor: PropertyDescriptor
): PropertyDescriptor {
  const original = descriptor.value;
  descriptor.value = function (...args: unknown[]) {
    console.log(`Calling ${propertyKey} with:`, args);
    const result = original.apply(this, args);
    console.log(`${propertyKey} returned:`, result);
    return result;
  };
  return descriptor;
}

class Calculator {
  @log
  add(a: number, b: number): number {
    return a + b;
  }
}
```

### Auto-bind decorator
```ts
function bound(
  _target: unknown,
  _propertyKey: string,
  descriptor: PropertyDescriptor
): PropertyDescriptor {
  return {
    get() {
      const bound = descriptor.value.bind(this);
      Object.defineProperty(this, _propertyKey, { value: bound });
      return bound;
    },
  };
}

class Button {
  @bound
  handleClick(e: MouseEvent) {
    console.log(this); // always the Button instance
  }
}
```

### Decorator factory (with parameters)
```ts
function throttle(delay: number) {
  return function (
    _target: unknown,
    _propertyKey: string,
    descriptor: PropertyDescriptor
  ): PropertyDescriptor {
    const original = descriptor.value;
    let lastCall = 0;

    descriptor.value = function (...args: unknown[]) {
      const now = Date.now();
      if (now - lastCall >= delay) {
        lastCall = now;
        return original.apply(this, args);
      }
    };
    return descriptor;
  };
}

class SearchService {
  @throttle(300)
  search(query: string) {
    console.log('Searching:', query);
  }
}
```

### Property decorator
```ts
function format(formatFn: (value: unknown) => string) {
  return function (target: unknown, propertyKey: string) {
    let value: unknown;

    Object.defineProperty(target, propertyKey, {
      get() { return value; },
      set(newVal: unknown) {
        value = formatFn(newVal);
      },
    });
  };
}

class Product {
  @format((v) => `$${(v as number).toFixed(2)}`)
  price!: string;
}

const p = new Product();
p.price = 19.99;
console.log(p.price); // '$19.99'
```

---

## 13. Branded Types

### String brand
```ts
type Brand<T, B> = T & { __brand: B };

type UserId = Brand<string, 'UserId'>;
type Email = Brand<string, 'Email'>;

function createUserId(id: string): UserId {
  return id as UserId;
}

function getUser(id: UserId): void {
  console.log(id);
}

const id = createUserId('abc123');
getUser(id);
// getUser('raw-string'); // Error - not branded
```

### Numeric brand
```ts
type Seconds = Brand<number, 'Seconds'>;
type Milliseconds = Brand<number, 'Milliseconds'>;

function toMs(seconds: Seconds): Milliseconds {
  return (seconds * 1000) as Milliseconds;
}

const timeout: Seconds = 5 as Seconds;
const ms: Milliseconds = toMs(timeout);
```

### Brand with class
```ts
class UserId {
  private readonly __brand!: 'UserId';
  constructor(public readonly value: string) {}
}

class ProductId {
  private readonly __brand!: 'ProductId';
  constructor(public readonly value: string) {}
}

function findUser(id: UserId) { /* ... */ }

const userId = new UserId('u1');
findUser(userId);
// findUser(new ProductId('p1')); // Error - different brand
```

### Branded type guard
```ts
function isBranded<T extends Brand<string, string>>(value: string, brand: string): value is T {
  return true; // runtime validation logic here
}

const rawId = 'user-123';
if (isBranded<UserId>(rawId, 'UserId')) {
  getUser(rawId);
}
```

---

## 14. Assertion Functions

### Basic assertions
```ts
function assertDefined<T>(value: T | null | undefined, name?: string): asserts value is T {
  if (value === null || value === undefined) {
    throw new Error(`${name ?? 'Value'} is null or undefined`);
  }
}

function assert(condition: unknown, message?: string): asserts condition {
  if (!condition) throw new Error(message ?? 'Assertion failed');
}
```

### Type narrowing with assert
```ts
function assertString(value: unknown): asserts value is string {
  if (typeof value !== 'string') throw new Error('Expected string');
}

function assertNumber(value: unknown): asserts value is number {
  if (typeof value !== 'number') throw new Error('Expected number');
}

function process(input: unknown) {
  assertString(input);
  input.toUpperCase(); // narrowed to string
}
```

### Assertion in API response
```ts
interface ApiSuccess<T> {
  ok: true;
  data: T;
}
interface ApiError {
  ok: false;
  error: string;
}
type ApiResult<T> = ApiSuccess<T> | ApiError;

function assertOk<T>(result: ApiResult<T>): asserts result is ApiSuccess<T> {
  if (!result.ok) throw new Error(result.error);
}

const res: ApiResult<{ id: string }> = await fetchJSON('/api/user');
assertOk(res);
res.data.id; // narrowed safely
```

### Assert with custom predicate
```ts
function isString(value: unknown): value is string {
  return typeof value === 'string';
}

function assertIsString(value: unknown): asserts value is string {
  if (!isString(value)) throw new Error('Not a string');
}
```

---

## 15. The satisfies Operator

### Basic satisfies
```ts
const palette = {
  red: [255, 0, 0],
  green: '#00ff00',
  blue: [0, 0, 255],
} satisfies Record<string, string | number[]>;

// palette.green // string (narrowed, not string | number[])
// palette.red   // number[] (narrowed)
```

### satisfies with strict typing
```ts
type Color = [number, number, number] | string;

const colors = {
  primary: [0, 123, 255],
  secondary: '#6c757d',
} satisfies Record<string, Color>;

// colors.primary[0] // number (narrowed from tuple)
```

### satisfies as const
```ts
const config = {
  api: 'https://api.example.com',
  timeout: 5000,
  retries: 3,
} as const satisfies Record<string, string | number>;

type Config = typeof config;
// type: { readonly api: string; readonly timeout: number; readonly retries: number }
```

### satisfies with enums
```ts
const Permission = {
  Read: 'read',
  Write: 'write',
  Execute: 'execute',
} as const satisfies Record<string, string>;

type Permission = (typeof Permission)[keyof typeof Permission];
// 'read' | 'write' | 'execute'
```

---

## 16. satisfies + as const

### Type-safe const object
```ts
const HttpStatus = {
  OK: 200,
  Created: 201,
  BadRequest: 400,
  NotFound: 404,
  InternalServerError: 500,
} as const satisfies Record<string, number>;

type HttpStatus = (typeof HttpStatus)[keyof typeof HttpStatus];
// 200 | 201 | 400 | 404 | 500
```

### Event map with satisfies
```ts
const events = {
  click: { x: 0, y: 0 },
  keydown: { key: 'Enter' },
  focus: { target: 'input' },
} as const satisfies Record<string, Record<string, unknown>>;

type EventMap = typeof events;
type EventName = keyof EventMap;
type EventPayload<N extends EventName> = EventMap[N];
```

### Route definition
```ts
const routes = {
  home: '/',
  users: '/users',
  userDetail: '/users/[id]',
  settings: '/settings',
} as const satisfies Record<string, `/${string}`>;

type Route = (typeof routes)[keyof typeof routes];
// '/' | '/users' | '/users/[id]' | '/settings'
```

---

## 17. Nominal Typing Patterns

### Unique symbol brand
```ts
declare const _brand: unique symbol;

type Branded<T, B extends string> = T & { [_brand]: B };

type UserId = Branded<string, 'UserId'>;
type OrderId = Branded<string, 'OrderId'>;

function userId(id: string): UserId {
  return id as UserId;
}

function orderId(id: string): OrderId {
  return id as OrderId;
}
```

### Flavoring (lighter brand)
```ts
type Flavor<T, F extends string> = T & { __flavor?: F };

type Kilometers = Flavor<number, 'km'>;
type Miles = Flavor<number, 'mi'>;

function toKm(miles: Miles): Kilometers {
  return (miles * 1.609) as Kilometers;
}

const dist: Kilometers = 100 as Kilometers;
// const bad: Miles = dist; // Error
```

### Opaque type using class
```ts
class Opaque<Tag extends string> {
  private readonly __tag!: Tag;
}

type OpaqueType<T, Tag extends string> = T & Opaque<Tag>;

function createOpaque<T, Tag extends string>(value: T): OpaqueType<T, Tag> {
  return value as OpaqueType<T, Tag>;
}

type Email = OpaqueType<string, 'Email'>;
type Password = OpaqueType<string, 'Password'>;

function login(email: Email, password: Password) {}

const e = createOpaque<string, 'Email'>('user@example.com');
const p = createOpaque<string, 'Password'>('secret123');
login(e, p);
```

---

## 18. Builder Pattern

### Simple builder
```ts
class QueryBuilder {
  private table: string = '';
  private conditions: string[] = [];
  private orderField: string = '';
  private orderDir: 'ASC' | 'DESC' = 'ASC';
  private limitCount: number = 0;

  from(table: string): this {
    this.table = table;
    return this;
  }

  where(condition: string): this {
    this.conditions.push(condition);
    return this;
  }

  orderBy(field: string, dir: 'ASC' | 'DESC' = 'ASC'): this {
    this.orderField = field;
    this.orderDir = dir;
    return this;
  }

  limit(n: number): this {
    this.limitCount = n;
    return this;
  }

  build(): string {
    let sql = `SELECT * FROM ${this.table}`;
    if (this.conditions.length > 0) {
      sql += ` WHERE ${this.conditions.join(' AND ')}`;
    }
    if (this.orderField) {
      sql += ` ORDER BY ${this.orderField} ${this.orderDir}`;
    }
    if (this.limitCount > 0) {
      sql += ` LIMIT ${this.limitCount}`;
    }
    return sql;
  }
}

const sql = new QueryBuilder()
  .from('users')
  .where('age > 18')
  .where('active = true')
  .orderBy('name', 'ASC')
  .limit(10)
  .build();
```

### Generic builder with type safety
```ts
class Builder<T extends Record<string, unknown>> {
  private data: Partial<T> = {};

  set<K extends keyof T>(key: K, value: T[K]): this {
    this.data[key] = value;
    return this;
  }

  build(): T {
    return this.data as T;
  }
}

interface User {
  id: string;
  name: string;
  email: string;
  age: number;
}

const user = new Builder<User>()
  .set('id', '1')
  .set('name', 'Alice')
  .set('email', 'alice@example.com')
  .set('age', 30)
  .build();
```

### URL Builder
```ts
class URLBuilder {
  private base: string;
  private pathSegments: string[] = [];
  private queryParams: Record<string, string> = {};
  private hashValue: string = '';

  constructor(base: string) {
    this.base = base.replace(/\/+$/, '');
  }

  path(...segments: string[]): this {
    this.pathSegments.push(...segments.map((s) => encodeURIComponent(s)));
    return this;
  }

  param(key: string, value: string): this {
    this.queryParams[key] = value;
    return this;
  }

  params(params: Record<string, string>): this {
    Object.assign(this.queryParams, params);
    return this;
  }

  hash(h: string): this {
    this.hashValue = h;
    return this;
  }

  build(): string {
    let url = this.base;
    if (this.pathSegments.length > 0) {
      url += '/' + this.pathSegments.join('/');
    }
    const qs = new URLSearchParams(this.queryParams).toString();
    if (qs) url += '?' + qs;
    if (this.hashValue) url += '#' + this.hashValue;
    return url;
  }
}

const url = new URLBuilder('https://api.example.com')
  .path('v1', 'users')
  .param('page', '1')
  .param('sort', 'name')
  .hash('section')
  .build();
// 'https://api.example.com/v1/users?page=1&sort=name#section'
```

---

## 19. Result / Either Type

### Generic Result type
```ts
type Result<T, E = Error> =
  | { ok: true; value: T }
  | { ok: false; error: E };

function success<T>(value: T): Result<T, never> {
  return { ok: true, value };
}

function failure<E>(error: E): Result<never, E> {
  return { ok: false, error };
}

function safeParse<T>(json: string): Result<T, SyntaxError> {
  try {
    return success(JSON.parse(json) as T);
  } catch (e) {
    return failure(e instanceof SyntaxError ? e : new SyntaxError('Parse failed'));
  }
}

const parsed = safeParse<{ a: number }>('{"a":1}');
if (parsed.ok) {
  console.log(parsed.value.a); // narrowed
} else {
  console.error(parsed.error.message);
}
```

### Result class with methods
```ts
class Result<T, E = Error> {
  private constructor(
    private readonly _value?: T,
    private readonly _error?: E
  ) {}

  static ok<T, E = never>(value: T): Result<T, E> {
    return new Result<T, E>(value, undefined);
  }

  static fail<T = never, E = Error>(error: E): Result<T, E> {
    return new Result<T, E>(undefined, error);
  }

  get isOk(): boolean {
    return this._error === undefined;
  }

  get isErr(): boolean {
    return this._error !== undefined;
  }

  unwrap(): T {
    if (this._error) throw this._error;
    return this._value!;
  }

  unwrapOr(defaultValue: T): T {
    return this.isOk ? this._value! : defaultValue;
  }

  map<U>(fn: (value: T) => U): Result<U, E> {
    return this.isOk ? Result.ok(fn(this._value!)) : this as unknown as Result<U, E>;
  }

  mapErr<F>(fn: (error: E) => F): Result<T, F> {
    return this.isOk ? this as unknown as Result<T, F> : Result.fail(fn(this._error!));
  }

  chain<U>(fn: (value: T) => Result<U, E>): Result<U, E> {
    return this.isOk ? fn(this._value!) : this as unknown as Result<U, E>;
  }

  match<U>(handlers: { ok: (value: T) => U; err: (error: E) => U }): U {
    return this.isOk ? handlers.ok(this._value!) : handlers.err(this._error!);
  }
}

// Usage
const r = Result.ok(42);
const doubled = r.map((n) => n * 2).unwrapOr(0); // 84

const f = Result.fail<number>(new Error('failed'));
f.match({
  ok: (n) => console.log(n),
  err: (e) => console.error(e.message),
});
```

### Async result helpers
```ts
async function tryCatch<T>(fn: () => Promise<T>): Promise<Result<T, Error>> {
  try {
    return Result.ok(await fn());
  } catch (e) {
    return Result.fail(e instanceof Error ? e : new Error(String(e)));
  }
}

const result = await tryCatch(() => fetchJSON<User>('/api/user'));
result.match({
  ok: (user) => console.log(user.name),
  err: (e) => console.error(e.message),
});
```

---

## 20. Option / Maybe Type

### Option type
```ts
type Option<T> = Some<T> | None;

interface Some<T> {
  tag: 'some';
  value: T;
}

interface None {
  tag: 'none';
}

function some<T>(value: T): Option<T> {
  return { tag: 'some', value };
}

const none: Option<never> = { tag: 'none' };

function isSome<T>(option: Option<T>): option is Some<T> {
  return option.tag === 'some';
}

function isNone<T>(option: Option<T>): option is None {
  return option.tag === 'none';
}
```

### Option class
```ts
class Option<T> {
  private constructor(private readonly value?: T) {}

  static some<T>(value: T): Option<T> {
    return new Option(value);
  }

  static none<T = never>(): Option<T> {
    return new Option<T>();
  }

  static from<T>(value: T | null | undefined): Option<T> {
    return value != null ? Option.some(value) : Option.none();
  }

  get isSome(): boolean {
    return this.value !== undefined;
  }

  get isNone(): boolean {
    return this.value === undefined;
  }

  unwrap(): T {
    if (this.value === undefined) throw new Error('Called unwrap on None');
    return this.value;
  }

  unwrapOr(defaultValue: T): T {
    return this.value ?? defaultValue;
  }

  map<U>(fn: (value: T) => U): Option<U> {
    return this.value !== undefined ? Option.some(fn(this.value)) : Option.none();
  }

  chain<U>(fn: (value: T) => Option<U>): Option<U> {
    return this.value !== undefined ? fn(this.value) : Option.none();
  }

  match<U>(handlers: { some: (value: T) => U; none: () => U }): U {
    return this.value !== undefined ? handlers.some(this.value) : handlers.none();
  }
}

const maybe = Option.from(getUserInput());
const doubled = maybe.map((v) => v * 2).unwrapOr(0);
```

### Option with pipe
```ts
function pipe2<A, B>(a: Option<A>, fn: (a: A) => Option<B>): Option<B> {
  return a.chain(fn);
}

function safeDivide(a: number, b: number): Option<number> {
  return b === 0 ? Option.none() : Option.some(a / b);
}

const result = pipe2(
  Option.some(10),
  (n) => safeDivide(n, 2)
).unwrapOr(0); // 5
```

---

## 21. Async Patterns

### AsyncQueue
```ts
class AsyncQueue<T> {
  private items: T[] = [];
  private resolvers: ((value: T) => void)[] = [];

  push(item: T): void {
    if (this.resolvers.length > 0) {
      const resolve = this.resolvers.shift()!;
      resolve(item);
    } else {
      this.items.push(item);
    }
  }

  async pop(): Promise<T> {
    if (this.items.length > 0) {
      return this.items.shift()!;
    }
    return new Promise((resolve) => {
      this.resolvers.push(resolve);
    });
  }

  get size(): number {
    return this.items.length;
  }

  get pending(): number {
    return this.resolvers.length;
  }
}

const queue = new AsyncQueue<string>();
queue.push('hello');
const item = await queue.pop(); // 'hello'
```

### Async Lazy
```ts
class AsyncLazy<T> {
  private promise: Promise<T> | null = null;

  constructor(private readonly factory: () => Promise<T>) {}

  get value(): Promise<T> {
    if (!this.promise) {
      this.promise = this.factory();
    }
    return this.promise;
  }

  get isStarted(): boolean {
    return this.promise !== null;
  }

  async reset(): Promise<void> {
    this.promise = null;
  }
}

const lazy = new AsyncLazy(async () => {
  const res = await fetch('/api/data');
  return res.json();
});

// First call triggers fetch
const data1 = await lazy.value;
// Second call uses cached promise
const data2 = await lazy.value;
```

### ConcurrentExecutor
```ts
class ConcurrentExecutor {
  private running = 0;
  private queue: (() => Promise<unknown>)[] = [];

  constructor(private readonly concurrency: number) {}

  async run<T>(fn: () => Promise<T>): Promise<T> {
    return new Promise((resolve, reject) => {
      const task = async () => {
        try {
          const result = await fn();
          resolve(result);
        } catch (error) {
          reject(error);
        } finally {
          this.running--;
          this.dequeue();
        }
      };

      this.queue.push(task);
      this.dequeue();
    });
  }

  private dequeue(): void {
    while (this.running < this.concurrency && this.queue.length > 0) {
      const task = this.queue.shift()!;
      this.running++;
      task();
    }
  }

  get pending(): number {
    return this.queue.length;
  }

  get active(): number {
    return this.running;
  }
}

const executor = new ConcurrentExecutor(3);
const results = await Promise.all([
  executor.run(() => fetch('/api/a')),
  executor.run(() => fetch('/api/b')),
  executor.run(() => fetch('/api/c')),
  executor.run(() => fetch('/api/d')), // queued
]);
```

### Mutex
```ts
class Mutex {
  private locked = false;
  private queue: (() => void)[] = [];

  async acquire(): Promise<() => void> {
    if (!this.locked) {
      this.locked = true;
      return this.release.bind(this);
    }

    return new Promise<() => void>((resolve) => {
      this.queue.push(() => {
        this.locked = true;
        resolve(this.release.bind(this));
      });
    });
  }

  private release(): void {
    if (this.queue.length > 0) {
      const next = this.queue.shift()!;
      next();
    } else {
      this.locked = false;
    }
  }

  async withLock<T>(fn: () => Promise<T>): Promise<T> {
    const release = await this.acquire();
    try {
      return await fn();
    } finally {
      release();
    }
  }
}

const mutex = new Mutex();
async function updateCounter() {
  await mutex.withLock(async () => {
    // critical section
    await db.increment('counter');
  });
}
```

### Semaphore
```ts
class Semaphore {
  private current: number;

  constructor(private readonly max: number) {
    this.current = max;
  }

  async acquire(): Promise<() => void> {
    if (this.current > 0) {
      this.current--;
      return this.release.bind(this);
    }

    return new Promise<() => void>((resolve) => {
      const tryAcquire = () => {
        if (this.current > 0) {
          this.current--;
          resolve(this.release.bind(this));
        } else {
          setTimeout(tryAcquire, 0);
        }
      };
      setTimeout(tryAcquire, 0);
    });
  }

  private release(): void {
    this.current++;
  }

  async withLock<T>(fn: () => Promise<T>): Promise<T> {
    const release = await this.acquire();
    try {
      return await fn();
    } finally {
      release();
    }
  }
}
```

---

## 22. API Client Patterns

### Typed fetch wrapper
```ts
interface ApiClientConfig {
  baseUrl: string;
  headers?: Record<string, string>;
  timeout?: number;
}

class ApiClient {
  private readonly baseUrl: string;
  private readonly defaultHeaders: Record<string, string>;
  private readonly timeout: number;

  constructor(config: ApiClientConfig) {
    this.baseUrl = config.baseUrl.replace(/\/+$/, '');
    this.defaultHeaders = { 'Content-Type': 'application/json', ...config.headers };
    this.timeout = config.timeout ?? 10000;
  }

  private async request<T>(
    method: string,
    path: string,
    options: { body?: unknown; params?: Record<string, string>; headers?: Record<string, string> } = {}
  ): Promise<T> {
    const url = new URL(`${this.baseUrl}${path}`);
    if (options.params) {
      Object.entries(options.params).forEach(([k, v]) => url.searchParams.set(k, v));
    }

    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), this.timeout);

    try {
      const response = await fetch(url.toString(), {
        method,
        headers: { ...this.defaultHeaders, ...options.headers },
        body: options.body ? JSON.stringify(options.body) : undefined,
        signal: controller.signal,
      });

      if (!response.ok) {
        throw new ApiError(response.status, await response.text());
      }

      return response.json() as Promise<T>;
    } finally {
      clearTimeout(timer);
    }
  }

  get<T>(path: string, params?: Record<string, string>): Promise<T> {
    return this.request<T>('GET', path, { params });
  }

  post<T>(path: string, body?: unknown): Promise<T> {
    return this.request<T>('POST', path, { body });
  }

  put<T>(path: string, body?: unknown): Promise<T> {
    return this.request<T>('PUT', path, { body });
  }

  patch<T>(path: string, body?: unknown): Promise<T> {
    return this.request<T>('PATCH', path, { body });
  }

  delete<T>(path: string): Promise<T> {
    return this.request<T>('DELETE', path);
  }
}

class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message);
    this.name = 'ApiError';
  }
}
```

### Typed API endpoints
```ts
interface UserAPI {
  list(params: { page: number; limit: number }): Promise<{ users: User[]; total: number }>;
  get(id: string): Promise<User>;
  create(data: Omit<User, 'id'>): Promise<User>;
  update(id: string, data: Partial<User>): Promise<User>;
  delete(id: string): Promise<void>;
}

function createUserAPI(client: ApiClient): UserAPI {
  return {
    list: (params) => client.get('/users', { page: String(params.page), limit: String(params.limit) }),
    get: (id) => client.get(`/users/${id}`),
    create: (data) => client.post('/users', data),
    update: (id, data) => client.patch(`/users/${id}`, data),
    delete: (id) => client.delete(`/users/${id}`),
  };
}

const api = createUserAPI(new ApiClient({ baseUrl: 'https://api.example.com' }));
const users = await api.list({ page: 1, limit: 20 });
```

### WebSocket typed wrapper
```ts
type MessageHandler<T> = (data: T) => void;

class TypedWebSocket<T extends Record<string, unknown>> {
  private ws: WebSocket;
  private handlers = new Map<keyof T, Set<MessageHandler<unknown>>>();

  constructor(url: string) {
    this.ws = new WebSocket(url);
    this.ws.onmessage = (event) => {
      const message = JSON.parse(event.data) as { type: keyof T; payload: unknown };
      this.handlers.get(message.type)?.forEach((handler) => handler(message.payload));
    };
  }

  on<K extends keyof T>(type: K, handler: MessageHandler<T[K]>): () => void {
    if (!this.handlers.has(type)) this.handlers.set(type, new Set());
    this.handlers.get(type)!.add(handler as MessageHandler<unknown>);
    return () => this.handlers.get(type)?.delete(handler as MessageHandler<unknown>);
  }

  send<K extends keyof T>(type: K, payload: T[K]): void {
    this.ws.send(JSON.stringify({ type, payload }));
  }

  close(): void {
    this.ws.close();
  }
}

interface WSEvents {
  message: { text: string; userId: string };
  typing: { userId: string };
  status: { userId: string; online: boolean };
}

const ws = new TypedWebSocket<WSEvents>('wss://chat.example.com');
ws.on('message', (data) => console.log(data.text));
ws.send('message', { text: 'Hello', userId: 'u1' });
```

---

## 23. Event Emitter

### Typed EventEmitter
```ts
type EventMap = Record<string, unknown[]>;

class TypedEventEmitter<T extends EventMap> {
  private listeners: { [K in keyof T]?: Set<(...args: T[K]) => void> } = {};

  on<K extends keyof T>(event: K, listener: (...args: T[K]) => void): () => void {
    if (!this.listeners[event]) this.listeners[event] = new Set();
    this.listeners[event]!.add(listener);
    return () => this.off(event, listener);
  }

  off<K extends keyof T>(event: K, listener: (...args: T[K]) => void): void {
    this.listeners[event]?.delete(listener);
  }

  emit<K extends keyof T>(event: K, ...args: T[K]): void {
    this.listeners[event]?.forEach((listener) => listener(...args));
  }

  once<K extends keyof T>(event: K, listener: (...args: T[K]) => void): void {
    const wrapper = (...args: T[K]) => {
      listener(...args);
      this.off(event, wrapper);
    };
    this.on(event, wrapper);
  }

  removeAllListeners<K extends keyof T>(event?: K): void {
    if (event) {
      delete this.listeners[event];
    } else {
      this.listeners = {};
    }
  }
}

// Usage
interface AppEvents {
  userLogin: [user: { id: string; name: string }];
  userLogout: [userId: string];
  error: [error: Error, context?: string];
}

const emitter = new TypedEventEmitter<AppEvents>();
const unsub = emitter.on('userLogin', (user) => {
  console.log(`${user.name} logged in`);
});
emitter.emit('userLogin', { id: '1', name: 'Alice' });
unsub();
```

### EventEmitter with generics
```ts
class EventBus<Events extends Record<string, (...args: unknown[]) => void>> {
  private handlers = new Map<keyof Events, Set<Events[keyof Events]>>();

  on<K extends keyof Events>(event: K, handler: Events[K]): () => void {
    if (!this.handlers.has(event)) this.handlers.set(event, new Set());
    this.handlers.get(event)!.add(handler);
    return () => this.handlers.get(event)?.delete(handler);
  }

  once<K extends keyof Events>(event: K, handler: Events[K]): void {
    const wrapper = ((...args: Parameters<Events[K]>) => {
      handler(...args);
      this.handlers.get(event)?.delete(wrapper as Events[K]);
    }) as Events[K];
    this.on(event, wrapper);
  }

  emit<K extends keyof Events>(event: K, ...args: Parameters<Events[K]>): void {
    this.handlers.get(event)?.forEach((handler) => handler(...args));
  }

  off<K extends keyof Events>(event: K, handler: Events[K]): void {
    this.handlers.get(event)?.delete(handler);
  }

  clear(event?: keyof Events): void {
    if (event) this.handlers.delete(event);
    else this.handlers.clear();
  }
}

type MyEvents = {
  dataLoaded: (data: { id: string }) => void;
  progress: (pct: number) => void;
  error: (message: string, code: number) => void;
};

const bus = new EventBus<MyEvents>();
bus.on('progress', (pct) => console.log(`${pct}%`));
bus.emit('progress', 50);
```

---

## 24. Dependency Injection

### Simple DI container
```ts
type Token<T> = string & { __type?: T };

function createToken<T>(name: string): Token<T> {
  return name as Token<T>;
}

class Container {
  private services = new Map<string, unknown>();

  register<T>(token: Token<T>, factory: () => T): void {
    this.services.set(token, factory);
  }

  registerSingleton<T>(token: Token<T>, factory: () => T): void {
    let instance: T | null = null;
    this.services.set(token, () => {
      if (!instance) instance = factory();
      return instance;
    });
  }

  resolve<T>(token: Token<T>): T {
    const factory = this.services.get(token);
    if (!factory) throw new Error(`Service not found: ${token}`);
    return (factory as () => T)();
  }
}

// Define tokens
const DB_TOKEN = createToken<Database>('db');
const LOGGER_TOKEN = createToken<Logger>('logger');
const USER_SERVICE_TOKEN = createToken<UserService>('userService');

// Setup container
const container = new Container();
container.registerSingleton(DB_TOKEN, () => new PostgresDB());
container.registerSingleton(LOGGER_TOKEN, () => new ConsoleLogger());
container.register(USER_SERVICE_TOKEN, () => new UserService(
  container.resolve(DB_TOKEN),
  container.resolve(LOGGER_TOKEN)
));
```

### Class-based DI with decorators
```ts
const INJECT_METADATA_KEY = Symbol('inject');

function inject(token: string) {
  return function (target: unknown, propertyKey: string, parameterIndex: number) {
    const existing = Reflect.getOwnMetadata(INJECT_METADATA_KEY, target) ?? [];
    existing[parameterIndex] = token;
    Reflect.defineMetadata(INJECT_METADATA_KEY, existing, target);
  };
}

class DIContainer {
  private instances = new Map<string, unknown>();
  private factories = new Map<string, () => unknown>();

  register<T>(token: string, factory: () => T): void {
    this.factories.set(token, factory);
  }

  resolve<T>(token: string): T {
    if (this.instances.has(token)) return this.instances.get(token) as T;

    const factory = this.factories.get(token);
    if (!factory) throw new Error(`No factory registered for ${token}`);

    const instance = factory();
    this.instances.set(token, instance);
    return instance as T;
  }

  create<T>(ctor: new (...args: unknown[]) => T): T {
    const paramTokens: string[] = Reflect.getOwnMetadata(INJECT_METADATA_KEY, ctor) ?? [];
    const params = paramTokens.map((t) => this.resolve(t));
    return new ctor(...params);
  }
}

// Usage
class Logger {
  log(msg: string) { console.log(msg); }
}

class UserService {
  constructor(@inject('logger') private logger: Logger) {}

  getUser(id: string) {
    this.logger.log(`Fetching user ${id}`);
    return { id, name: 'Alice' };
  }
}

const di = new DIContainer();
di.register('logger', () => new Logger());
di.register('userService', () => di.create(UserService));

const svc = di.resolve<UserService>('userService');
svc.getUser('1');
```

### Provider pattern
```ts
interface Provider<T> {
  (): T;
}

function singleton<T>(provider: Provider<T>): Provider<T> {
  let instance: T;
  let initialized = false;
  return () => {
    if (!initialized) {
      instance = provider();
      initialized = true;
    }
    return instance;
  };
}

function factory<T>(provider: Provider<T>): Provider<T> {
  return provider;
}

const dbProvider = singleton(() => new PostgresDB());
const loggerProvider = singleton(() => new ConsoleLogger());
const userServiceProvider = factory(() => new UserService(dbProvider(), loggerProvider()));

// Usage
const userService = userServiceProvider();
```

---

## 25. Configuration & Environment

### Typed environment variables
```ts
interface EnvConfig {
  NODE_ENV: 'development' | 'production' | 'test';
  PORT: number;
  DATABASE_URL: string;
  JWT_SECRET: string;
  API_KEY: string;
  CORS_ORIGINS: string[];
  LOG_LEVEL: 'debug' | 'info' | 'warn' | 'error';
  REDIS_URL?: string;
}

function loadConfig(): EnvConfig {
  const env = process.env;

  return {
    NODE_ENV: parseEnum(env.NODE_ENV, ['development', 'production', 'test']),
    PORT: parseNumber(env.PORT, 3000),
    DATABASE_URL: parseString(env.DATABASE_URL),
    JWT_SECRET: parseString(env.JWT_SECRET),
    API_KEY: parseString(env.API_KEY),
    CORS_ORIGINS: parseArray(env.CORS_ORIGINS, ','),
    LOG_LEVEL: parseEnum(env.LOG_LEVEL, ['debug', 'info', 'warn', 'error'], 'info'),
    REDIS_URL: env.REDIS_URL,
  };
}

function parseString(value: string | undefined, fallback?: string): string {
  if (value === undefined && fallback === undefined) throw new Error('Required env var missing');
  return value ?? fallback!;
}

function parseNumber(value: string | undefined, fallback?: number): number {
  if (value === undefined && fallback === undefined) throw new Error('Required env var missing');
  const n = Number(value ?? fallback);
  if (isNaN(n)) throw new Error(`Invalid number: ${value}`);
  return n;
}

function parseEnum<T extends string>(value: string | undefined, valid: readonly T[], fallback?: T): T {
  if (value === undefined && fallback === undefined) throw new Error('Required env var missing');
  const v = (value ?? fallback) as T;
  if (!valid.includes(v)) throw new Error(`Invalid value: ${v}. Expected: ${valid.join(' | ')}`);
  return v;
}

function parseArray(value: string | undefined, separator: string): string[] {
  if (!value) return [];
  return value.split(separator).map((s) => s.trim()).filter(Boolean);
}

export const config = loadConfig();
```

### Config with Zod validation
```ts
import { z } from 'zod';

const envSchema = z.object({
  NODE_ENV: z.enum(['development', 'production', 'test']),
  PORT: z.coerce.number().default(3000),
  DATABASE_URL: z.string().url(),
  JWT_SECRET: z.string().min(32),
  API_KEY: z.string(),
  CORS_ORIGINS: z.string().transform((s) => s.split(',')),
  LOG_LEVEL: z.enum(['debug', 'info', 'warn', 'error']).default('info'),
  REDIS_URL: z.string().url().optional(),
});

type EnvConfig = z.infer<typeof envSchema>;

function loadConfig(): EnvConfig {
  const parsed = envSchema.safeParse(process.env);
  if (!parsed.success) {
    console.error('Invalid configuration:', parsed.error.flatten().fieldErrors);
    process.exit(1);
  }
  return parsed.data;
}

export const config = loadConfig();
```

### Feature flags
```ts
type FeatureFlag = {
  [K in string]: boolean | number | string;
};

const featureFlags = {
  newDashboard: true,
  darkMode: false,
  maxUploadSizeMB: 100,
  apiVersion: 'v2',
} as const satisfies FeatureFlag;

type FeatureFlags = typeof featureFlags;

class FeatureFlagService {
  private flags: Map<string, boolean | number | string>;

  constructor(flags: Record<string, boolean | number | string>) {
    this.flags = new Map(Object.entries(flags));
  }

  isEnabled(flag: keyof FeatureFlags): boolean {
    return this.flags.get(flag) === true;
  }

  getValue<T extends boolean | number | string>(flag: keyof FeatureFlags): T {
    return this.flags.get(flag) as T;
  }

  updateFlag(flag: keyof FeatureFlags, value: boolean | number | string): void {
    this.flags.set(flag, value);
  }

  loadFrom(overrides: Partial<FeatureFlags>): void {
    Object.entries(overrides).forEach(([k, v]) => this.flags.set(k, v));
  }
}

const features = new FeatureFlagService(featureFlags);
if (features.isEnabled('newDashboard')) {
  renderNewDashboard();
}
```
