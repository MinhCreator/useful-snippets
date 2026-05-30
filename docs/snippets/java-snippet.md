# Java Snippets

## Table of Contents
1. [Basic Syntax](#1-basic-syntax)
2. [Strings](#2-strings)
3. [Collections & Streams](#3-collections--streams)
4. [Date & Time (java.time)](#4-date--time-javatime)
5. [File I/O](#5-file-io)
6. [Exception Handling](#6-exception-handling)
7. [Generics](#7-generics)
8. [Enums](#8-enums)
9. [Annotations](#9-annotations)
10. [OOP — Classes & Inheritance](#10-oop--classes--inheritance)
11. [OOP — Interfaces & Abstract Classes](#11-oop--interfaces--abstract-classes)
12. [OOP — Polymorphism](#12-oop--polymorphism)
13. [OOP — Composition](#13-oop--composition)
14. [OOP — Builder Pattern](#14-oop--builder-pattern)
15. [OOP — Factory Pattern](#15-oop--factory-pattern)
16. [OOP — Singleton](#16-oop--singleton)
17. [OOP — Strategy Pattern](#17-oop--strategy-pattern)
18. [OOP — Observer Pattern](#18-oop--observer-pattern)
19. [OOP — Decorator Pattern](#19-oop--decorator-pattern)
20. [Functional Programming (Streams & Lambdas)](#20-functional-programming-streams--lambdas)
21. [Optional](#21-optional)
22. [Concurrency & Threading](#22-concurrency--threading)
23. [Records (Java 16+)](#23-records-java-16)
24. [Sealed Classes (Java 17+)](#24-sealed-classes-java-17)
25. [Pattern Matching (Java 17+/21+)](#25-pattern-matching-java-1721)

---

## 1. Basic Syntax

### Hello World
```java
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}
```

### Variables & Data Types
```java
// Primitives
int count = 42;
long big = 1_000_000_000L;
double price = 19.99;
float tax = 0.08f;
boolean active = true;
char grade = 'A';
byte b = 127;
short s = 32000;

// Reference types
String name = "Alice";
Integer wrapper = 42;       // autoboxing
Double pi = 3.14159;

// var (local variable type inference, Java 10+)
var list = new ArrayList<String>();
var number = 42;            // inferred as int
```

### Input / Output
```java
import java.util.Scanner;

public class InputExample {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Enter name: ");
        String name = scanner.nextLine();

        System.out.print("Enter age: ");
        int age = scanner.nextInt();

        System.out.printf("Hello %s, you are %d years old.%n", name, age);
        scanner.close();
    }
}
```

### Arrays
```java
// Declaration and initialization
int[] numbers = new int[5];
int[] values = {1, 2, 3, 4, 5};
String[] names = {"Alice", "Bob", "Charlie"};

// Enhanced for-loop
for (int n : numbers) {
    System.out.println(n);
}

// Multidimensional
int[][] matrix = {
    {1, 2, 3},
    {4, 5, 6},
    {7, 8, 9}
};

// Copy
int[] copy = Arrays.copyOf(values, values.length);
int[] partial = Arrays.copyOfRange(values, 1, 3);
```

### Control Flow
```java
// If-else
if (score >= 90) {
    grade = "A";
} else if (score >= 80) {
    grade = "B";
} else {
    grade = "F";
}

// Switch (Java 14+)
String result = switch (day) {
    case "MONDAY", "FRIDAY" -> "Work day";
    case "SATURDAY", "SUNDAY" -> "Weekend";
    default -> "Midweek";
};

// Switch with blocks
int numLetters = switch (day) {
    case "MONDAY", "FRIDAY", "SUNDAY" -> 6;
    case "TUESDAY" -> 7;
    default -> {
        System.out.println("Unknown: " + day);
        yield 0;
    }
};

// Ternary
String status = (age >= 18) ? "Adult" : "Minor";
```

### Loops
```java
// For
for (int i = 0; i < 10; i++) {
    System.out.println(i);
}

// Enhanced for
for (String name : names) {
    System.out.println(name);
}

// While
while (scanner.hasNext()) {
    process(scanner.next());
}

// Do-while
do {
    input = read();
} while (input != null);

// For-each with Iterator
import java.util.Iterator;
Iterator<String> it = list.iterator();
while (it.hasNext()) {
    String item = it.next();
}
```

---

## 2. Strings

### Basic String Operations
```java
String s = "Hello World";

// Length
int len = s.length();               // 11

// Character access
char ch = s.charAt(0);              // 'H'

// Substring
String sub = s.substring(0, 5);     // "Hello"
String rest = s.substring(6);       // "World"

// Search
int idx1 = s.indexOf("World");      // 6
int idx2 = s.indexOf('o');          // 4
int idx3 = s.lastIndexOf('o');      // 7
boolean has = s.contains("World");  // true

// Comparison
boolean eq = s.equals("Hello World");       // true
boolean eqIgnore = s.equalsIgnoreCase("hello world");

// startsWith / endsWith
boolean starts = s.startsWith("Hello");      // true

// Replace
String replaced = s.replace('o', '0');       // "Hell0 W0rld"
String replacedAll = s.replaceAll("\\s+", "-");  // "Hello-World"

// Split
String[] parts = s.split(" ");              // ["Hello", "World"]

// Join
String joined = String.join(", ", "a", "b", "c"); // "a, b, c"
String joinedList = String.join(", ", list);

// Case conversion
String upper = s.toUpperCase();              // "HELLO WORLD"
String lower = s.toLowerCase();              // "hello world"

// Trim / strip (Java 11+)
String trimmed = "  text  ".strip();         // "text"
String stripLeading = "  text  ".stripLeading();
String stripTrailing = "  text  ".stripTrailing();

// isBlank (Java 11+)
boolean blank = "   ".isBlank();             // true

// Repeat (Java 11+)
String repeated = "ha".repeat(3);            // "hahaha"

// Transform (Java 12+)
String transformed = "42".transform(Integer::parseInt);
```

### StringBuilder
```java
StringBuilder sb = new StringBuilder();

sb.append("Hello");
sb.append(" ");
sb.append("World");
sb.insert(5, ",");
sb.delete(5, 6);
sb.reverse();

String result = sb.toString();

// Efficient concatenation in loops
StringBuilder builder = new StringBuilder();
for (int i = 0; i < 100; i++) {
    builder.append(i).append(", ");
}
String csv = builder.toString();
```

### String Formatting
```java
// String.format
String msg = String.format("Hello %s, you have %d new messages", name, count);

// printf
System.out.printf("Price: $%.2f%n", 19.995);  // "Price: $20.00"

// Text blocks (Java 13+)
String json = """
    {
        "name": "%s",
        "age": %d
    }
    """.formatted(name, age);

String html = """
    <html>
        <body>
            <h1>Hello</h1>
        </body>
    </html>
    """;
```

### Regex
```java
import java.util.regex.Pattern;
import java.util.regex.Matcher;

Pattern pattern = Pattern.compile("\\b(\\w+)\\b");
Matcher matcher = pattern.matcher("Hello World");

while (matcher.find()) {
    System.out.println(matcher.group());       // Hello, World
    System.out.println(matcher.group(1));      // Hello, World
}

// Matching
boolean matches = Pattern.matches("\\d+", "12345");  // true

// Split with regex
String[] parts = "a,b;c".split("[;,]");              // ["a", "b", "c"]

// Replace with regex
String cleaned = "a1b2c3".replaceAll("\\d", "");     // "abc"
```

---

## 3. Collections & Streams

### List
```java
import java.util.*;

// Creation
List<String> list = new ArrayList<>();                 // mutable
List<String> immutable = List.of("a", "b", "c");       // Java 9+
List<String> copy = List.copyOf(source);               // Java 10+

// Operations
list.add("item");
list.addAll(otherList);
list.remove("item");
list.remove(0);
list.get(0);
list.set(0, "newValue");
list.contains("item");
list.indexOf("item");
list.isEmpty();
list.size();

// Iteration
for (String s : list) { /* ... */ }
list.forEach(System.out::println);
list.stream().filter(s -> s.startsWith("a")).collect(Collectors.toList());

// Sorting
list.sort(Comparator.naturalOrder());
list.sort(Comparator.reverseOrder());
list.sort(Comparator.comparing(String::length));

// Sublist
List<String> sub = list.subList(0, 2);

// Remove if
list.removeIf(s -> s == null);
```

### Set
```java
Set<String> set = new HashSet<>();                         // unordered
Set<String> linked = new LinkedHashSet<>();                // insertion order
Set<String> tree = new TreeSet<>();                        // sorted

Set<String> immutable = Set.of("a", "b", "c");             // Java 9+

set.add("item");
set.remove("item");
set.contains("item");
set.addAll(otherCollection);

// Operations
Set<String> union = new HashSet<>(a);
union.addAll(b);

Set<String> intersection = new HashSet<>(a);
intersection.retainAll(b);

Set<String> difference = new HashSet<>(a);
difference.removeAll(b);
```

### Map
```java
Map<String, Integer> map = new HashMap<>();
Map<String, Integer> linkedMap = new LinkedHashMap<>();    // insertion order
Map<String, Integer> treeMap = new TreeMap<>();            // sorted by key

Map<String, Integer> immutable = Map.of("a", 1, "b", 2);  // Java 9+

// Operations
map.put("key", 42);
map.putIfAbsent("key", 0);
map.get("key");
map.getOrDefault("key", 0);
map.containsKey("key");
map.containsValue(42);
map.remove("key");
map.replace("key", 42, 43);

// Iteration
map.forEach((k, v) -> System.out.println(k + "=" + v));
for (Map.Entry<String, Integer> entry : map.entrySet()) {
    String key = entry.getKey();
    Integer val = entry.getValue();
}

// Compute
map.compute("key", (k, v) -> v == null ? 1 : v + 1);
map.computeIfAbsent("key", k -> computeExpensive(k));
map.computeIfPresent("key", (k, v) -> v + 1);
map.merge("key", 1, Integer::sum);

// Immutable copy
Map<String, Integer> snapshot = Map.copyOf(original);
```

### Queue & Deque
```java
Queue<String> queue = new LinkedList<>();                 // FIFO
queue.offer("item");                                      // add (returns false if full)
queue.poll();                                             // remove + null if empty
queue.peek();                                             // inspect + null if empty

Deque<String> stack = new ArrayDeque<>();                 // LIFO
stack.push("item");
stack.pop();                                              // remove + throw if empty
stack.peek();

// Deque as double-ended queue
Deque<String> deque = new ArrayDeque<>();
deque.addFirst("front");
deque.addLast("back");
deque.removeFirst();
deque.removeLast();

// Priority queue
Queue<Task> pq = new PriorityQueue<>(Comparator.comparingInt(Task::priority));
```

### Stream API
```java
List<String> result = items.stream()
    .filter(item -> item.isActive())
    .map(Item::getName)
    .sorted()
    .distinct()
    .limit(10)
    .skip(5)
    .collect(Collectors.toList());

// Map operations
List<Integer> lengths = items.stream()
    .map(String::length)
    .toList();                                          // Java 16+

// FlatMap
List<String> words = sentences.stream()
    .flatMap(s -> Arrays.stream(s.split("\\s+")))
    .collect(Collectors.toList());

// Reduction
int sum = numbers.stream().reduce(0, Integer::sum);
int sum2 = numbers.stream().mapToInt(Integer::intValue).sum();

// Grouping
Map<String, List<Person>> byCity = people.stream()
    .collect(Collectors.groupingBy(Person::city));

Map<String, Long> countByCity = people.stream()
    .collect(Collectors.groupingBy(Person::city, Collectors.counting()));

Map<String, Optional<Person>> oldestByCity = people.stream()
    .collect(Collectors.groupingBy(Person::city,
        Collectors.maxBy(Comparator.comparingInt(Person::age))));

// Partitioning
Map<Boolean, List<Person>> adults = people.stream()
    .collect(Collectors.partitioningBy(p -> p.age() >= 18));

// Joining
String csv = names.stream().collect(Collectors.joining(", "));

// Finding
Optional<String> first = list.stream().filter(s -> s.startsWith("a")).findFirst();
Optional<String> any = list.parallelStream().filter(s -> s.startsWith("a")).findAny();

// Matching
boolean allMatch = list.stream().allMatch(s -> s.length() > 0);
boolean anyMatch = list.stream().anyMatch(s -> s.contains("a"));
boolean noneMatch = list.stream().noneMatch(String::isEmpty);

// Statistics
IntSummaryStatistics stats = numbers.stream()
    .mapToInt(Integer::intValue)
    .summaryStatistics();
stats.getMin();
stats.getMax();
stats.getAverage();
stats.getSum();
stats.getCount();
```

### Collections Utilities
```java
import java.util.Collections;

List<String> syncList = Collections.synchronizedList(new ArrayList<>());
List<String> unmodifiable = Collections.unmodifiableList(list);
Map<String, String> syncMap = Collections.synchronizedMap(new HashMap<>());

// Min / Max
String min = Collections.min(list);
String max = Collections.max(list, Comparator.comparing(String::length));

// Frequency
int freq = Collections.frequency(list, "target");

// Reverse / Shuffle / Rotate
Collections.reverse(list);
Collections.shuffle(list);
Collections.rotate(list, 3);

// Fill
Collections.fill(list, "default");
```

---

## 4. Date & Time (java.time)

### LocalDate, LocalTime, LocalDateTime
```java
import java.time.*;
import java.time.format.DateTimeFormatter;
import java.time.temporal.ChronoUnit;

// Current date/time
LocalDate today = LocalDate.now();
LocalTime now = LocalTime.now();
LocalDateTime nowDT = LocalDateTime.now();

// Specific values
LocalDate date = LocalDate.of(2026, Month.MAY, 25);
LocalTime time = LocalTime.of(14, 30, 0);
LocalDateTime dt = LocalDateTime.of(2026, 5, 25, 14, 30);

// Parsing
LocalDate parsed = LocalDate.parse("2026-05-25");
LocalDateTime parsedDT = LocalDateTime.parse("2026-05-25T14:30:00");
LocalDate custom = LocalDate.parse("25/05/2026", DateTimeFormatter.ofPattern("dd/MM/yyyy"));

// Formatting
String formatted = today.format(DateTimeFormatter.ISO_LOCAL_DATE);
String customFmt = today.format(DateTimeFormatter.ofPattern("dd/MM/yyyy"));

// Manipulation
LocalDate tomorrow = today.plusDays(1);
LocalDate nextWeek = today.plusWeeks(1);
LocalDate nextMonth = today.plusMonths(1);
LocalDate lastYear = today.minusYears(1);
LocalDate firstOfMonth = today.withDayOfMonth(1);

// Difference
long daysBetween = ChronoUnit.DAYS.between(today, futureDate);
long monthsBetween = ChronoUnit.MONTHS.between(start, end);

// Compare
boolean isBefore = date1.isBefore(date2);
boolean isAfter = date1.isAfter(date2);
boolean isEqual = date1.isEqual(date2);
```

### ZonedDateTime / OffsetDateTime
```java
ZonedDateTime zdt = ZonedDateTime.now(ZoneId.of("Asia/Ho_Chi_Minh"));
ZonedDateTime utc = ZonedDateTime.now(ZoneOffset.UTC);

// Convert zone
ZonedDateTime ny = zdt.withZoneSameInstant(ZoneId.of("America/New_York"));

// Offset from UTC
OffsetDateTime odt = OffsetDateTime.now();
OffsetDateTime fixed = OffsetDateTime.of(2026, 5, 25, 14, 30, 0, 0, ZoneOffset.ofHours(7));
```

### Duration & Period
```java
Duration duration = Duration.ofHours(2);
Duration halfDay = Duration.ofMinutes(30);
long minutes = duration.toMinutes();

Period period = Period.ofMonths(6);
Period tenDays = Period.ofDays(10);
int months = period.getMonths();

// Between
Duration elapsed = Duration.between(startTime, endTime);
Period age = Period.between(birthDate, today);
```

### Instant
```java
Instant now = Instant.now();                            // UTC timestamp
Instant epoch = Instant.ofEpochSecond(1_700_000_000);
long epochMillis = now.toEpochMilli();

// Convert to LocalDateTime
LocalDateTime ldt = LocalDateTime.ofInstant(now, ZoneId.systemDefault());
```

---

## 5. File I/O

### Reading Files
```java
import java.nio.file.*;
import java.io.*;

// Read all lines (Java 8+)
List<String> lines = Files.readAllLines(Paths.get("file.txt"));

// Read entire file as string (Java 11+)
String content = Files.readString(Paths.get("file.txt"));

// Stream lines
try (Stream<String> stream = Files.lines(Paths.get("file.txt"))) {
    stream.filter(l -> !l.isEmpty()).forEach(System.out::println);
}

// BufferedReader
try (BufferedReader reader = Files.newBufferedReader(Paths.get("file.txt"))) {
    String line;
    while ((line = reader.readLine()) != null) {
        process(line);
    }
}

// Scanner
try (Scanner scanner = new Scanner(Paths.get("file.txt"))) {
    while (scanner.hasNextLine()) {
        String line = scanner.nextLine();
    }
}
```

### Writing Files
```java
// Write bytes
Files.write(Paths.get("output.txt"), content.getBytes());

// Write lines (Java 8+)
Files.write(Paths.get("output.txt"), lines);

// Write string (Java 11+)
Files.writeString(Paths.get("output.txt"), content);

// Append
Files.write(Paths.get("output.txt"), lines, StandardOpenOption.APPEND);

// BufferedWriter
try (BufferedWriter writer = Files.newBufferedWriter(Paths.get("output.txt"))) {
    writer.write("Hello");
    writer.newLine();
    writer.write("World");
}
```

### File & Path Operations
```java
Path path = Paths.get("dir", "subdir", "file.txt");

// Check
boolean exists = Files.exists(path);
boolean isDirectory = Files.isDirectory(path);
boolean isRegularFile = Files.isRegularFile(path);

// Attributes
long size = Files.size(path);
FileTime lastModified = Files.getLastModifiedTime(path);
PosixFilePermissions perms = Files.getPosixFilePermissions(path); // Unix

// Create / Delete
Files.createDirectories(path.getParent());
Files.createFile(path);
Files.delete(path);
Files.deleteIfExists(path);

// Copy / Move
Files.copy(source, target, StandardCopyOption.REPLACE_EXISTING);
Files.move(source, target, StandardCopyOption.ATOMIC_MOVE);

// List directory
try (Stream<Path> entries = Files.list(Paths.get("."))) {
    entries.forEach(System.out::println);
}

// Walk directory tree
try (Stream<Path> walk = Files.walk(Paths.get("src"))) {
    walk.filter(Files::isRegularFile).forEach(System.out::println);
}
```

### Object Serialization
```java
import java.io.*;

// Serializable class
record Person(String name, int age) implements Serializable {
    private static final long serialVersionUID = 1L;
}

// Serialize
try (ObjectOutputStream out = new ObjectOutputStream(
        new FileOutputStream("person.ser"))) {
    out.writeObject(new Person("Alice", 30));
}

// Deserialize
try (ObjectInputStream in = new ObjectInputStream(
        new FileInputStream("person.ser"))) {
    Person p = (Person) in.readObject();
}
```

---

## 6. Exception Handling

### Try-Catch-Finally
```java
try {
    riskyOperation();
} catch (IOException e) {
    System.err.println("IO error: " + e.getMessage());
} catch (IllegalArgumentException e) {
    log.warn("Invalid argument", e);
} finally {
    cleanup();
}
```

### Try-with-Resources (Java 7+)
```java
try (BufferedReader reader = Files.newBufferedReader(path);
     BufferedWriter writer = Files.newBufferedWriter(output)) {
    String line;
    while ((line = reader.readLine()) != null) {
        writer.write(line);
        writer.newLine();
    }
} catch (IOException e) {
    log.error("File error", e);
}
```

### Custom Exceptions
```java
// Checked exception
public class BusinessException extends Exception {
    private final String code;

    public BusinessException(String code, String message) {
        super(message);
        this.code = code;
    }

    public String getCode() {
        return code;
    }
}

// Unchecked exception
public class ValidationException extends RuntimeException {
    private final Map<String, String> errors;

    public ValidationException(Map<String, String> errors) {
        super("Validation failed");
        this.errors = errors;
    }

    public Map<String, String> getErrors() {
        return errors;
    }
}
```

### Multi-catch (Java 7+)
```java
try {
    parseAndWrite(input);
} catch (IOException | ParseException e) {
    log.error("Operation failed", e);
}
```

### Rethrowing (precise, Java 7+)
```java
public void process() throws IOException, SQLException {
    try {
        readFromDB();
    } catch (Exception e) {
        log.error("Error", e);
        throw e;  // compiler knows exact types
    }
}
```

### Try with multiple catches
```java
try {
    process();
} catch (IOException | IllegalArgumentException e) {
    // e is implicitly final
    throw new RuntimeException(e);
}
```

### Pattern matching for catch (Java 17+ preview / Java 21+)
```java
try {
    process();
} catch (Exception e) {
    switch (e) {
        case IOException ioe -> log.error("IO", ioe);
        case IllegalArgumentException iae -> log.warn("Bad arg", iae);
        default -> log.error("Unknown", e);
    }
}
```

---

## 7. Generics

### Generic Class
```java
public class Box<T> {
    private T value;

    public void set(T value) {
        this.value = value;
    }

    public T get() {
        return value;
    }

    public boolean isEmpty() {
        return value == null;
    }
}

Box<String> stringBox = new Box<>();
stringBox.set("Hello");
String val = stringBox.get();
```

### Generic Method
```java
public static <T> T getLast(List<T> list) {
    return list.get(list.size() - 1);
}

public static <T, R> List<R> map(List<T> list, Function<T, R> mapper) {
    return list.stream().map(mapper).collect(Collectors.toList());
}

// Usage
String last = getLast(List.of("a", "b", "c"));
```

### Bounded Type Parameters
```java
// Upper bound
public static <T extends Comparable<T>> T max(T a, T b) {
    return a.compareTo(b) > 0 ? a : b;
}

// Multiple bounds
public static <T extends Comparable<T> & Serializable> void process(T item) {
    // item must implement both interfaces
}
```

### Wildcards
```java
// Unbounded
public static void printList(List<?> list) {
    for (Object obj : list) System.out.println(obj);
}

// Upper bounded (producer extends)
public static double sumOfList(List<? extends Number> list) {
    return list.stream().mapToDouble(Number::doubleValue).sum();
}

// Lower bounded (consumer super)
public static void addNumbers(List<? super Integer> list) {
    for (int i = 1; i <= 10; i++) list.add(i);
}

// PECS (Producer extends, Consumer super)
public static <T> void copy(List<? extends T> src, List<? super T> dest) {
    dest.addAll(src);
}
```

### Type Erasure Workarounds
```java
// Generic array creation (compile error)
// T[] array = new T[10]; // Error

// Workaround
@SuppressWarnings("unchecked")
public static <T> T[] toArray(List<T> list, IntFunction<T[]> generator) {
    return list.toArray(generator.apply(0));
}

// Class token
public static <T> T fromJson(String json, Class<T> clazz) {
    return objectMapper.readValue(json, clazz);
}

// Usage
User user = fromJson("{\"name\":\"Alice\"}", User.class);
```

---

## 8. Enums

### Basic Enum
```java
public enum Status {
    ACTIVE,
    INACTIVE,
    PENDING,
    DELETED
}

Status s = Status.ACTIVE;
String name = s.name();             // "ACTIVE"
int ordinal = s.ordinal();          // 0
Status fromName = Status.valueOf("ACTIVE");
Status[] all = Status.values();
```

### Enum with Fields & Methods
```java
public enum HttpStatus {
    OK(200, "OK"),
    CREATED(201, "Created"),
    BAD_REQUEST(400, "Bad Request"),
    NOT_FOUND(404, "Not Found"),
    INTERNAL_SERVER_ERROR(500, "Internal Server Error");

    private final int code;
    private final String reasonPhrase;

    HttpStatus(int code, String reasonPhrase) {
        this.code = code;
        this.reasonPhrase = reasonPhrase;
    }

    public int getCode() { return code; }
    public String getReasonPhrase() { return reasonPhrase; }

    public boolean isSuccess() {
        return code >= 200 && code < 300;
    }

    public static HttpStatus fromCode(int code) {
        return Arrays.stream(values())
            .filter(s -> s.code == code)
            .findFirst()
            .orElseThrow(() -> new IllegalArgumentException("Unknown code: " + code));
    }
}

HttpStatus status = HttpStatus.NOT_FOUND;
System.out.println(status.getCode());         // 404
System.out.println(status.isSuccess());       // false
```

### Enum with Abstract Method
```java
public enum Operation {
    ADD {
        @Override public double apply(double a, double b) { return a + b; }
    },
    SUBTRACT {
        @Override public double apply(double a, double b) { return a - b; }
    },
    MULTIPLY {
        @Override public double apply(double a, double b) { return a * b; }
    },
    DIVIDE {
        @Override public double apply(double a, double b) {
            if (b == 0) throw new ArithmeticException("Divide by zero");
            return a / b;
        }
    };

    public abstract double apply(double a, double b);
}

double result = Operation.ADD.apply(10, 5); // 15.0
```

### Enum Implementing Interface
```java
public interface ErrorCode {
    int getCode();
    String getMessage();
}

public enum AppError implements ErrorCode {
    NOT_FOUND(1001, "Resource not found"),
    VALIDATION(1002, "Validation failed"),
    UNAUTHORIZED(1003, "Unauthorized access");

    private final int code;
    private final String message;

    AppError(int code, String message) {
        this.code = code;
        this.message = message;
    }

    @Override public int getCode() { return code; }
    @Override public String getMessage() { return message; }
}
```

---

## 9. Annotations

### Defining Custom Annotations
```java
import java.lang.annotation.*;

@Retention(RetentionPolicy.RUNTIME)       // available at runtime via reflection
@Target({ElementType.FIELD, ElementType.METHOD, ElementType.TYPE})
public @interface Validate {
    boolean required() default false;
    int minLength() default 0;
    int maxLength() default Integer.MAX_VALUE;
    String pattern() default "";
}
```

### Using Custom Annotations
```java
@Validate(required = true)
private String name;

@Validate(minLength = 6)
private String password;
```

### Processing Annotations
```java
public class ValidatorProcessor {
    public static List<String> validate(Object obj) throws IllegalAccessException {
        List<String> errors = new ArrayList<>();

        for (Field field : obj.getClass().getDeclaredFields()) {
            Validate annotation = field.getAnnotation(Validate.class);
            if (annotation == null) continue;

            field.setAccessible(true);
            Object value = field.get(obj);

            if (annotation.required() && (value == null || value.toString().isEmpty())) {
                errors.add(field.getName() + " is required");
            }

            if (value != null) {
                String str = value.toString();
                if (str.length() < annotation.minLength()) {
                    errors.add(field.getName() + " min length is " + annotation.minLength());
                }
                if (str.length() > annotation.maxLength()) {
                    errors.add(field.getName() + " max length is " + annotation.maxLength());
                }
                if (!annotation.pattern().isEmpty() && !str.matches(annotation.pattern())) {
                    errors.add(field.getName() + " does not match pattern");
                }
            }
        }
        return errors;
    }
}
```

### Built-in Annotations
```java
@Deprecated(since = "2.0", forRemoval = true)
public void oldMethod() {}

@SuppressWarnings("unchecked")
List<String> list = (List<String>) rawList;

@Override
public String toString() { return "MyObject"; }

@SafeVarargs
public static <T> List<T> asList(T... args) {
    return Arrays.asList(args);
}

// FunctionalInterface
@FunctionalInterface
interface Calculator {
    int calculate(int a, int b);
}
```

---

## 10. OOP — Classes & Inheritance

### Basic Class
```java
public class Animal {
    protected String name;
    protected int age;

    // Constructor
    public Animal(String name, int age) {
        this.name = name;
        this.age = age;
    }

    // Methods
    public void speak() {
        System.out.println(name + " makes a sound");
    }

    public String getName() {
        return name;
    }

    // Static method
    public static Animal createUnknown() {
        return new Animal("Unknown", 0);
    }
}
```

### Inheritance
```java
public class Dog extends Animal {
    private String breed;

    public Dog(String name, int age, String breed) {
        super(name, age);   // parent constructor
        this.breed = breed;
    }

    @Override
    public void speak() {
        System.out.println(name + " barks");
    }

    // Additional method
    public void fetch() {
        System.out.println(name + " fetches the ball");
    }
}

// Usage
Animal animal = new Dog("Rex", 3, "Labrador");
animal.speak();          // "Rex barks" (polymorphism)
// animal.fetch();       // Compile error (Animal type doesn't have fetch)
```

### Constructor Chaining
```java
public class Employee {
    private String name;
    private String department;
    private double salary;

    public Employee(String name) {
        this(name, "General", 0);
    }

    public Employee(String name, String department) {
        this(name, department, 30000);
    }

    public Employee(String name, String department, double salary) {
        this.name = name;
        this.department = department;
        this.salary = salary;
    }
}
```

### this vs super
```java
public class Parent {
    protected int value;

    public Parent(int value) {
        this.value = value;
    }

    public void display() {
        System.out.println("Parent: " + value);
    }
}

public class Child extends Parent {
    private int value;

    public Child(int parentVal, int childVal) {
        super(parentVal);          // call parent constructor
        this.value = childVal;     // child's own field
    }

    @Override
    public void display() {
        super.display();           // call parent method
        System.out.println("Child: " + this.value);
    }
}
```

### instanceof & Pattern Matching (Java 16+)
```java
public void process(Animal animal) {
    // Traditional
    if (animal instanceof Dog) {
        Dog dog = (Dog) animal;
        dog.fetch();
    }

    // Pattern matching (Java 16+)
    if (animal instanceof Dog dog) {
        dog.fetch();
    }

    // With conditions
    if (animal instanceof Dog dog && dog.getName().length() > 3) {
        dog.fetch();
    }
}
```

---

## 11. OOP — Interfaces & Abstract Classes

### Interface
```java
public interface Drawable {
    // Abstract method (implicitly public abstract)
    void draw();

    // Default method (Java 8+)
    default void print() {
        System.out.println("Drawing: " + getClass().getSimpleName());
    }

    // Static method (Java 8+)
    static Drawable createCircle(double radius) {
        return new Circle(radius);
    }

    // Private method (Java 9+)
    private void log(String msg) {
        System.out.println("[Drawable] " + msg);
    }
}
```

### Interface Implementation
```java
public class Circle implements Drawable, Resizable {
    private double radius;

    public Circle(double radius) {
        this.radius = radius;
    }

    @Override
    public void draw() {
        System.out.println("Drawing circle with radius " + radius);
    }

    @Override
    public void resize(double factor) {
        radius *= factor;
    }
}
```

### Functional Interface (SAM)
```java
@FunctionalInterface
public interface Transformer<T, R> {
    R transform(T input);
}

// Usage (lambda)
Transformer<String, Integer> length = s -> s.length();
Transformer<String, String> upper = String::toUpperCase;

// Method reference
Transformer<String, Integer> ref = String::length;
```

### Abstract Class
```java
public abstract class Database {
    protected String connectionString;

    public Database(String connectionString) {
        this.connectionString = connectionString;
    }

    // Abstract methods
    public abstract void connect();
    public abstract void disconnect();

    // Concrete method
    public void executeQuery(String sql) {
        connect();
        System.out.println("Executing: " + sql);
        disconnect();
    }

    // Template method pattern
    public final <T> T transaction(Supplier<T> operation) {
        connect();
        try {
            beginTransaction();
            T result = operation.get();
            commit();
            return result;
        } catch (Exception e) {
            rollback();
            throw e;
        } finally {
            disconnect();
        }
    }

    protected abstract void beginTransaction();
    protected abstract void commit();
    protected abstract void rollback();
}
```

### Interface vs Abstract Class Comparison
```java
// Interface — contract, multiple inheritance of type
public interface Flyable {
    void fly();
    default void takeOff() { System.out.println("Taking off"); }
}

// Abstract class — common state + partial implementation
public abstract class Vehicle {
    protected String licensePlate;

    public Vehicle(String licensePlate) {
        this.licensePlate = licensePlate;
    }

    public abstract void start();
    public void stop() { System.out.println("Stopped"); }
}

// Concrete class can extend ONE abstract + implement MANY interfaces
public class FlyingCar extends Vehicle implements Flyable {
    public FlyingCar(String licensePlate) {
        super(licensePlate);
    }

    @Override
    public void start() { System.out.println("Engine started"); }

    @Override
    public void fly() { System.out.println("Flying"); }
}
```

---

## 12. OOP — Polymorphism

### Runtime Polymorphism (Method Overriding)
```java
public abstract class Payment {
    public abstract void pay(double amount);
}

public class CreditCardPayment extends Payment {
    @Override
    public void pay(double amount) {
        System.out.printf("Paid $%.2f with Credit Card%n", amount);
    }
}

public class PayPalPayment extends Payment {
    @Override
    public void pay(double amount) {
        System.out.printf("Paid $%.2f with PayPal%n", amount);
    }
}

// Polymorphic usage
List<Payment> payments = List.of(
    new CreditCardPayment(),
    new PayPalPayment()
);

for (Payment p : payments) {
    p.pay(100.0);  // each invokes its own implementation
}
```

### Compile-time Polymorphism (Overloading)
```java
public class Calculator {
    public int add(int a, int b) {
        return a + b;
    }

    public int add(int a, int b, int c) {
        return a + b + c;
    }

    public double add(double a, double b) {
        return a + b;
    }

    public String add(String a, String b) {
        return a + b;
    }
}
```

### Covariant Return Types
```java
public class Base {
    public Base clone() {
        return new Base();
    }
}

public class Derived extends Base {
    @Override
    public Derived clone() {   // covariant return type
        return new Derived();
    }
}
```

### Polymorphic Collections
```java
List<Shape> shapes = new ArrayList<>();
shapes.add(new Circle(5));
shapes.add(new Rectangle(3, 4));
shapes.add(new Triangle(6, 8));

// Process all shapes polymorphically
double totalArea = shapes.stream()
    .mapToDouble(Shape::area)
    .sum();
```

---

## 13. OOP — Composition

### Composition over Inheritance
```java
// Instead of: Engine -> Car (inheritance)
// Use: Car has-an Engine (composition)

public class Engine {
    private String type;
    private int horsepower;

    public Engine(String type, int horsepower) {
        this.type = type;
        this.horsepower = horsepower;
    }

    public void start() { System.out.println(type + " engine started"); }
    public int getHorsepower() { return horsepower; }
}

public class Car {
    private final Engine engine;      // composition
    private final List<Wheel> wheels; // composition
    private String color;

    public Car(Engine engine, List<Wheel> wheels, String color) {
        this.engine = engine;
        this.wheels = wheels;
        this.color = color;
    }

    public void start() {
        engine.start();               // delegation
        System.out.println("Car is ready");
    }

    public void drive() {
        if (wheels.stream().allMatch(Wheel::isInflated)) {
            System.out.println("Driving...");
        }
    }
}
```

### Builder with Composition
```java
public class Computer {
    private final CPU cpu;
    private final RAM ram;
    private final Storage storage;
    private final GPU gpu;           // optional

    private Computer(Builder builder) {
        this.cpu = builder.cpu;
        this.ram = builder.ram;
        this.storage = builder.storage;
        this.gpu = builder.gpu;
    }

    // Getters...

    public static class Builder {
        private CPU cpu;
        private RAM ram;
        private Storage storage;
        private GPU gpu;

        public Builder cpu(CPU cpu) { this.cpu = cpu; return this; }
        public Builder ram(RAM ram) { this.ram = ram; return this; }
        public Builder storage(Storage storage) { this.storage = storage; return this; }
        public Builder gpu(GPU gpu) { this.gpu = gpu; return this; }

        public Computer build() {
            if (cpu == null || ram == null || storage == null) {
                throw new IllegalStateException("CPU, RAM, Storage required");
            }
            return new Computer(this);
        }
    }
}
```

---

## 14. OOP — Builder Pattern

### Classic Builder
```java
public class UserProfile {
    private final String firstName;   // required
    private final String lastName;    // required
    private final int age;            // optional
    private final String phone;       // optional
    private final String address;     // optional

    private UserProfile(Builder builder) {
        this.firstName = builder.firstName;
        this.lastName = builder.lastName;
        this.age = builder.age;
        this.phone = builder.phone;
        this.address = builder.address;
    }

    // Getters...

    public static class Builder {
        private final String firstName;   // required
        private final String lastName;    // required
        private int age = 0;
        private String phone = "";
        private String address = "";

        public Builder(String firstName, String lastName) {
            this.firstName = firstName;
            this.lastName = lastName;
        }

        public Builder age(int age) { this.age = age; return this; }
        public Builder phone(String phone) { this.phone = phone; return this; }
        public Builder address(String address) { this.address = address; return this; }

        public UserProfile build() {
            return new UserProfile(this);
        }
    }
}

// Usage
UserProfile user = new UserProfile.Builder("John", "Doe")
    .age(30)
    .phone("123-456-7890")
    .address("123 Main St")
    .build();
```

### Generic Builder
```java
public class GenericBuilder<T> {
    private final Supplier<T> constructor;
    private final List<Consumer<T>> setters = new ArrayList<>();

    public GenericBuilder(Supplier<T> constructor) {
        this.constructor = constructor;
    }

    public GenericBuilder<T> with(Consumer<T> setter) {
        setters.add(setter);
        return this;
    }

    public T build() {
        T instance = constructor.get();
        setters.forEach(setter -> setter.accept(instance));
        return instance;
    }
}

// Usage
Person p = new GenericBuilder<>(Person::new)
    .with(person -> person.setName("Alice"))
    .with(person -> person.setAge(30))
    .build();
```

### Fluent Interface (Self-referential)
```java
public class Query {
    private String select;
    private String from;
    private String where;
    private String orderBy;
    private int limit;

    public Query select(String select) { this.select = select; return this; }
    public Query from(String from) { this.from = from; return this; }
    public Query where(String where) { this.where = where; return this; }
    public Query orderBy(String orderBy) { this.orderBy = orderBy; return this; }
    public Query limit(int limit) { this.limit = limit; return this; }

    public String build() {
        StringBuilder sql = new StringBuilder("SELECT ");
        sql.append(select).append(" FROM ").append(from);
        if (where != null) sql.append(" WHERE ").append(where);
        if (orderBy != null) sql.append(" ORDER BY ").append(orderBy);
        if (limit > 0) sql.append(" LIMIT ").append(limit);
        return sql.toString();
    }
}

String sql = new Query()
    .select("*")
    .from("users")
    .where("age > 18")
    .orderBy("name")
    .limit(10)
    .build();
```

---

## 15. OOP — Factory Pattern

### Simple Factory
```java
public class PaymentFactory {
    public static Payment create(String type) {
        return switch (type.toLowerCase()) {
            case "creditcard" -> new CreditCardPayment();
            case "paypal" -> new PayPalPayment();
            case "banktransfer" -> new BankTransferPayment();
            default -> throw new IllegalArgumentException("Unknown payment: " + type);
        };
    }
}

Payment payment = PaymentFactory.create("paypal");
payment.pay(100.0);
```

### Factory Method Pattern
```java
public abstract class DocumentGenerator {
    // Factory method
    protected abstract Document createDocument();

    public Document generate(String content) {
        Document doc = createDocument();
        doc.setContent(content);
        doc.validate();
        return doc;
    }
}

public class PdfGenerator extends DocumentGenerator {
    @Override
    protected Document createDocument() {
        return new PdfDocument();
    }
}

public class HtmlGenerator extends DocumentGenerator {
    @Override
    protected Document createDocument() {
        return new HtmlDocument();
    }
}

// Usage
DocumentGenerator generator = new PdfGenerator();
Document doc = generator.generate("Hello");
```

### Abstract Factory
```java
public interface UIFactory {
    Button createButton();
    Checkbox createCheckbox();
    TextField createTextField();
}

public class DarkThemeFactory implements UIFactory {
    @Override public Button createButton() { return new DarkButton(); }
    @Override public Checkbox createCheckbox() { return new DarkCheckbox(); }
    @Override public TextField createTextField() { return new DarkTextField(); }
}

public class LightThemeFactory implements UIFactory {
    @Override public Button createButton() { return new LightButton(); }
    @Override public Checkbox createCheckbox() { return new LightCheckbox(); }
    @Override public TextField createTextField() { return new LightTextField(); }
}

// Usage
UIFactory factory = new DarkThemeFactory();
Button button = factory.createButton();
button.render();
```

### Static Factory Method
```java
public class User {
    private final String email;
    private final String displayName;

    private User(String email, String displayName) {
        this.email = email;
        this.displayName = displayName;
    }

    // Static factory methods
    public static User withEmail(String email) {
        return new User(email, email.split("@")[0]);
    }

    public static User fromOAuth(String provider, String token) {
        // Fetch from OAuth provider
        return new User(fetchEmail(provider, token), "OAuth User");
    }

    public static User anonymous() {
        return new User("anonymous@example.com", "Anonymous");
    }
}

User user = User.withEmail("alice@example.com");
```

---

## 16. OOP — Singleton

### Eager Singleton
```java
public class EagerSingleton {
    private static final EagerSingleton INSTANCE = new EagerSingleton();

    private EagerSingleton() {}

    public static EagerSingleton getInstance() {
        return INSTANCE;
    }
}
```

### Lazy Singleton (Thread-safe)
```java
public class LazySingleton {
    private static volatile LazySingleton instance;

    private LazySingleton() {}

    public static LazySingleton getInstance() {
        if (instance == null) {
            synchronized (LazySingleton.class) {
                if (instance == null) {
                    instance = new LazySingleton();
                }
            }
        }
        return instance;
    }
}
```

### Bill Pugh Singleton (Initialization-on-demand)
```java
public class BillPughSingleton {
    private BillPughSingleton() {}

    private static class SingletonHolder {
        private static final BillPughSingleton INSTANCE = new BillPughSingleton();
    }

    public static BillPughSingleton getInstance() {
        return SingletonHolder.INSTANCE;
    }
}
```

### Enum Singleton (best for serialization)
```java
public enum EnumSingleton {
    INSTANCE;

    private final Database database = new Database();

    public Database getDatabase() {
        return database;
    }

    public void doSomething() {
        System.out.println("Singleton action");
    }
}

// Usage
EnumSingleton.INSTANCE.doSomething();
Database db = EnumSingleton.INSTANCE.getDatabase();
```

---

## 17. OOP — Strategy Pattern

### Traditional Strategy
```java
public interface CompressionStrategy {
    byte[] compress(byte[] data);
    byte[] decompress(byte[] data);
}

public class ZipCompression implements CompressionStrategy {
    @Override
    public byte[] compress(byte[] data) {
        System.out.println("Compressing with ZIP");
        return data; // actual zip logic
    }

    @Override
    public byte[] decompress(byte[] data) {
        System.out.println("Decompressing with ZIP");
        return data;
    }
}

public class GzipCompression implements CompressionStrategy {
    @Override
    public byte[] compress(byte[] data) {
        System.out.println("Compressing with GZIP");
        return data;
    }

    @Override
    public byte[] decompress(byte[] data) {
        System.out.println("Decompressing with GZIP");
        return data;
    }
}

// Context
public class FileProcessor {
    private CompressionStrategy strategy;

    public FileProcessor(CompressionStrategy strategy) {
        this.strategy = strategy;
    }

    public void setStrategy(CompressionStrategy strategy) {
        this.strategy = strategy;
    }

    public byte[] save(byte[] data) {
        return strategy.compress(data);
    }

    public byte[] load(byte[] compressed) {
        return strategy.decompress(compressed);
    }
}

// Usage
FileProcessor processor = new FileProcessor(new ZipCompression());
processor.save(data);
processor.setStrategy(new GzipCompression());
processor.save(data);
```

### Strategy with Lambdas (Java 8+)
```java
public class ComparatorExample {
    public static void main(String[] args) {
        List<String> names = Arrays.asList("Charlie", "Alice", "Bob");

        // Strategy as lambda
        names.sort(String::compareTo);                        // natural order
        names.sort((a, b) -> b.compareTo(a));                 // reverse order
        names.sort(Comparator.comparingInt(String::length));  // by length

        // Strategy as method reference
        names.sort(String::compareToIgnoreCase);
    }
}
```

### Enum Strategy
```java
public enum TaxStrategy {
    VAT_20 {
        @Override public double calculate(double price) { return price * 0.20; }
    },
    VAT_10 {
        @Override public double calculate(double price) { return price * 0.10; }
    },
    NO_TAX {
        @Override public double calculate(double price) { return 0; }
    };

    public abstract double calculate(double price);
}

double tax = TaxStrategy.VAT_20.calculate(100.0);
```

---

## 18. OOP — Observer Pattern

### Observer with PropertyChangeSupport (java.beans)
```java
import java.beans.PropertyChangeListener;
import java.beans.PropertyChangeSupport;

public class ObservableModel {
    private final PropertyChangeSupport support = new PropertyChangeSupport(this);
    private String name;

    public void addListener(PropertyChangeListener listener) {
        support.addPropertyChangeListener(listener);
    }

    public void removeListener(PropertyChangeListener listener) {
        support.removePropertyChangeListener(listener);
    }

    public void setName(String newName) {
        String oldName = this.name;
        this.name = newName;
        support.firePropertyChange("name", oldName, newName);
    }
}

// Observer
public class ConsoleView implements PropertyChangeListener {
    @Override
    public void propertyChange(PropertyChangeEvent evt) {
        System.out.println(evt.getPropertyName() + ": " +
            evt.getOldValue() + " -> " + evt.getNewValue());
    }
}

// Usage
ObservableModel model = new ObservableModel();
model.addListener(new ConsoleView());
model.setName("Alice");  // prints: name: null -> Alice
```

### Custom Observer Pattern
```java
import java.util.concurrent.CopyOnWriteArrayList;

// Event generic
public interface Observer<T> {
    void onChange(T data);
}

public class Observable<T> {
    private final List<Observer<T>> observers = new CopyOnWriteArrayList<>();
    private T value;

    public Observable(T initialValue) {
        this.value = initialValue;
    }

    public void subscribe(Observer<T> observer) {
        observers.add(observer);
    }

    public void unsubscribe(Observer<T> observer) {
        observers.remove(observer);
    }

    public void set(T newValue) {
        T oldValue = this.value;
        this.value = newValue;
        if (oldValue != newValue) {
            observers.forEach(o -> o.onChange(newValue));
        }
    }

    public T get() {
        return value;
    }
}

// Usage
Observable<String> nameObservable = new Observable<>("Initial");

nameObservable.subscribe(newValue ->
    System.out.println("Name changed to: " + newValue));

nameObservable.set("Alice");   // prints: Name changed to: Alice
nameObservable.set("Bob");     // prints: Name changed to: Bob
```

### Event Bus Pattern
```java
public class EventBus {
    private static final Map<Class<?>, List<Consumer<?>>> handlers = new ConcurrentHashMap<>();

    public static <T> void register(Class<T> eventType, Consumer<T> handler) {
        handlers.computeIfAbsent(eventType, k -> new CopyOnWriteArrayList<>())
                .add(handler);
    }

    @SuppressWarnings("unchecked")
    public static <T> void post(T event) {
        List<Consumer<?>> consumers = handlers.get(event.getClass());
        if (consumers != null) {
            consumers.forEach(c -> ((Consumer<T>) c).accept(event));
        }
    }
}

// Event classes
public record UserLoggedIn(String userId, String name) {}
public record UserLoggedOut(String userId) {}
public record ErrorEvent(String message, Throwable cause) {}

// Usage
EventBus.register(UserLoggedIn.class, event ->
    System.out.println("Welcome " + event.name()));

EventBus.register(ErrorEvent.class, event ->
    System.err.println("Error: " + event.message()));

EventBus.post(new UserLoggedIn("u1", "Alice"));
```

---

## 19. OOP — Decorator Pattern

### Classic Decorator
```java
// Component interface
public interface Coffee {
    String getDescription();
    double getCost();
}

// Concrete component
public class SimpleCoffee implements Coffee {
    @Override
    public String getDescription() {
        return "Simple coffee";
    }

    @Override
    public double getCost() {
        return 2.0;
    }
}

// Abstract decorator
public abstract class CoffeeDecorator implements Coffee {
    protected final Coffee wrapped;

    public CoffeeDecorator(Coffee wrapped) {
        this.wrapped = wrapped;
    }

    @Override
    public String getDescription() {
        return wrapped.getDescription();
    }

    @Override
    public double getCost() {
        return wrapped.getCost();
    }
}

// Concrete decorators
public class MilkDecorator extends CoffeeDecorator {
    public MilkDecorator(Coffee wrapped) {
        super(wrapped);
    }

    @Override
    public String getDescription() {
        return wrapped.getDescription() + ", Milk";
    }

    @Override
    public double getCost() {
        return wrapped.getCost() + 0.5;
    }
}

public class SugarDecorator extends CoffeeDecorator {
    public SugarDecorator(Coffee wrapped) {
        super(wrapped);
    }

    @Override
    public String getDescription() {
        return wrapped.getDescription() + ", Sugar";
    }

    @Override
    public double getCost() {
        return wrapped.getCost() + 0.25;
    }
}

public class WhippedCreamDecorator extends CoffeeDecorator {
    public WhippedCreamDecorator(Coffee wrapped) {
        super(wrapped);
    }

    @Override
    public String getDescription() {
        return wrapped.getDescription() + ", Whipped Cream";
    }

    @Override
    public double getCost() {
        return wrapped.getCost() + 0.75;
    }
}

// Usage
Coffee coffee = new SimpleCoffee();
coffee = new MilkDecorator(coffee);
coffee = new SugarDecorator(coffee);
coffee = new WhippedCreamDecorator(coffee);

System.out.println(coffee.getDescription()); // "Simple coffee, Milk, Sugar, Whipped Cream"
System.out.println(coffee.getCost());         // 3.5
```

### Functional Decorator (Java 8+)
```java
public interface FunctionDecorator {
    static <T, R> Function<T, R> decorate(
            Function<T, R> fn,
            Consumer<T> before,
            Consumer<R> after) {
        return input -> {
            before.accept(input);
            R result = fn.apply(input);
            after.accept(result);
            return result;
        };
    }
}

// Usage
Function<String, String> toUpper = String::toUpperCase;
Function<String, String> logged = FunctionDecorator.decorate(
    toUpper,
    input -> System.out.println("Input: " + input),
    result -> System.out.println("Result: " + result)
);
logged.apply("hello");
```

---

## 20. Functional Programming (Streams & Lambdas)

### Lambda Expressions
```java
// No parameters
Runnable runner = () -> System.out.println("Running");

// Single parameter
Consumer<String> printer = s -> System.out.println(s);
Consumer<String> printerMR = System.out::println;  // method reference

// Multiple parameters
Comparator<String> byLength = (a, b) -> Integer.compare(a.length(), b.length());

// Block body
Function<String, String> process = s -> {
    String trimmed = s.trim();
    return trimmed.toUpperCase();
};

// Effectively final
String prefix = "User: ";
Function<String, String> addPrefix = name -> prefix + name; // prefix is effectively final
```

### Common Functional Interfaces
```java
// java.util.function package

// Predicate<T> — boolean test
Predicate<String> isEmpty = String::isEmpty;
Predicate<Integer> isPositive = n -> n > 0;

// Function<T, R> — transform
Function<String, Integer> toLength = String::length;
Function<Integer, String> toString = Object::toString;

// Consumer<T> — consume (void)
Consumer<String> log = System.out::println;
Consumer<List<String>> addHello = list -> list.add("Hello");

// Supplier<T> — produce
Supplier<Double> random = Math::random;
Supplier<LocalDate> today = LocalDate::now;

// UnaryOperator<T> — T -> T
UnaryOperator<String> upperCase = String::toUpperCase;

// BinaryOperator<T> — (T, T) -> T
BinaryOperator<Integer> sum = Integer::sum;

// BiFunction<T, U, R>
BiFunction<String, String, String> concat = (a, b) -> a + b;

// BiConsumer<T, U>
BiConsumer<String, Integer> printEntry = (k, v) -> System.out.println(k + "=" + v);
```

### Method & Constructor References
```java
// Static method reference
Function<String, Integer> parseInt = Integer::parseInt;
Supplier<Double> random = Math::random;

// Instance method reference on a specific object
String prefix = "Hello ";
Function<String, String> addHello = prefix::concat;

// Instance method reference on arbitrary object
Function<String, String> toUpper = String::toUpperCase;
BiPredicate<String, String> equals = String::equals;

// Constructor reference
Supplier<List<String>> listCreator = ArrayList::new;
Function<String, StringBuilder> sbCreator = StringBuilder::new;
```

### Optional with Lambdas
```java
Optional<String> opt = Optional.of("hello");

opt.ifPresent(System.out::println);
opt.filter(s -> s.length() > 3).map(String::toUpperCase).orElse("DEFAULT");
String result = opt.orElseThrow(() -> new NoSuchElementException());
```

### Collectors to Map
```java
// toMap
Map<String, Integer> nameToLength = names.stream()
    .collect(Collectors.toMap(
        Function.identity(),    // key mapper
        String::length,         // value mapper
        (a, b) -> a             // merge function for duplicates
    ));

// groupingBy
Map<String, List<Person>> byCity = people.stream()
    .collect(Collectors.groupingBy(Person::getCity));

// partitioningBy
Map<Boolean, List<Integer>> partitioned = numbers.stream()
    .collect(Collectors.partitioningBy(n -> n > 10));
```

---

## 21. Optional

### Creating Optional
```java
Optional<String> empty = Optional.empty();
Optional<String> ofNonNull = Optional.of("hello");       // throws NPE if null
Optional<String> nullable = Optional.ofNullable(value);  // safe for null
```

### Checking & Getting
```java
if (optional.isPresent()) {
    String value = optional.get();
}

// Java 11+
if (optional.isEmpty()) {
    // handle absent
}

// Preferred: ifPresent
optional.ifPresent(value -> process(value));

// Java 9+
optional.ifPresentOrElse(
    value -> process(value),
    () -> System.out.println("Value absent")
);
```

### Transforming
```java
Optional<Integer> length = optional.map(String::length);
Optional<String> upper = optional.flatMap(s -> Optional.of(s.toUpperCase()));
Optional<String> filtered = optional.filter(s -> s.length() > 3);
```

### Defaults & Throwing
```java
String result = optional.orElse("default");
String computed = optional.orElseGet(() -> computeExpensiveDefault());
String fromThrow = optional.orElseThrow(() -> new NoSuchElementException());

// Java 10+
String orElseThrow = optional.orElseThrow(); // throws NoSuchElementException
```

### Optional in Streams (Java 9+)
```java
// flatMap Optional to Stream
List<String> result = optionals.stream()
    .flatMap(Optional::stream)
    .collect(Collectors.toList());
```

### Optional Builders
```java
public class UserRepository {
    public Optional<User> findById(String id) {
        User user = db.query(id);
        return Optional.ofNullable(user);
    }
}

// Usage
User user = repository.findById("123")
    .orElseThrow(() -> new NotFoundException("User not found"));
```

---

## 22. Concurrency & Threading

### Thread Basics
```java
// Extend Thread
class Worker extends Thread {
    @Override
    public void run() {
        System.out.println("Working in " + Thread.currentThread().getName());
    }
}
new Worker().start();

// Implement Runnable
Runnable task = () -> {
    System.out.println("Task in " + Thread.currentThread().getName());
};
new Thread(task).start();
new Thread(task, "worker-1").start();
```

### ExecutorService
```java
import java.util.concurrent.*;

ExecutorService executor = Executors.newFixedThreadPool(4);
// Executors.newSingleThreadExecutor();
// Executors.newCachedThreadPool();
// Executors.newScheduledThreadPool(2);

// Submit Runnable
executor.submit(() -> System.out.println("Task"));

// Submit Callable (returns result)
Future<Integer> future = executor.submit(() -> {
    Thread.sleep(1000);
    return 42;
});

Integer result = future.get();               // blocking
Integer resultWithTimeout = future.get(2, TimeUnit.SECONDS);

// InvokeAll
List<Callable<String>> tasks = List.of(
    () -> "Task 1",
    () -> "Task 2"
);
List<Future<String>> results = executor.invokeAll(tasks);

// InvokeAny (returns first completed)
String first = executor.invokeAny(tasks);

// Scheduled executor
ScheduledExecutorService scheduler = Executors.newScheduledThreadPool(2);
scheduler.schedule(() -> System.out.println("Delayed"), 1, TimeUnit.SECONDS);
scheduler.scheduleAtFixedRate(() -> System.out.println("Periodic"), 0, 5, TimeUnit.SECONDS);

// Shutdown
executor.shutdown();                    // no new tasks, wait for running
executor.shutdownNow();                 // interrupt running tasks
executor.awaitTermination(5, TimeUnit.SECONDS);
```

### CompletableFuture
```java
import java.util.concurrent.CompletableFuture;

// Create
CompletableFuture<String> future = CompletableFuture.supplyAsync(() -> {
    sleep(1000);
    return "Hello";
}, executor);

// Chain
future
    .thenApply(String::toUpperCase)
    .thenAccept(System.out::println)
    .thenRun(() -> System.out.println("Done"))
    .exceptionally(ex -> {
        System.err.println("Error: " + ex.getMessage());
        return null;
    });

// Combine
CompletableFuture<String> f1 = CompletableFuture.supplyAsync(() -> "Hello");
CompletableFuture<String> f2 = CompletableFuture.supplyAsync(() -> "World");
CompletableFuture<String> combined = f1.thenCombine(f2, (a, b) -> a + " " + b);

// AllOf / AnyOf
CompletableFuture<Void> all = CompletableFuture.allOf(f1, f2, f3);
CompletableFuture<Object> any = CompletableFuture.anyOf(f1, f2, f3);

// ForkJoinPool common pool
CompletableFuture.supplyAsync(() -> compute());  // uses ForkJoinPool.commonPool()
```

### Synchronization
```java
// Synchronized method
public synchronized void increment() {
    count++;
}

// Synchronized block
public void addItem(Item item) {
    synchronized (this) {
        items.add(item);
        notifyAll();
    }
}

// Explicit Lock
import java.util.concurrent.locks.*;

private final Lock lock = new ReentrantLock();
private final Condition notEmpty = lock.newCondition();

public void put(T item) {
    lock.lock();
    try {
        queue.add(item);
        notEmpty.signal();
    } finally {
        lock.unlock();
    }
}

public T take() throws InterruptedException {
    lock.lockInterruptibly();
    try {
        while (queue.isEmpty()) {
            notEmpty.await();
        }
        return queue.poll();
    } finally {
        lock.unlock();
    }
}

// ReadWriteLock
private final ReadWriteLock rwLock = new ReentrantReadWriteLock();

public T read() {
    rwLock.readLock().lock();
    try { return data; }
    finally { rwLock.readLock().unlock(); }
}

public void write(T value) {
    rwLock.writeLock().lock();
    try { this.data = value; }
    finally { rwLock.writeLock().unlock(); }
}
```

### Concurrent Collections
```java
// Thread-safe collections
Map<String, String> concurrentMap = new ConcurrentHashMap<>();
List<String> copyOnWriteList = new CopyOnWriteArrayList<>();
Set<String> concurrentSet = ConcurrentHashMap.newKeySet();
Queue<String> concurrentQueue = new ConcurrentLinkedQueue<>();
Deque<String> concurrentDeque = new ConcurrentLinkedDeque<>();

// Blocking queues (for producer-consumer)
BlockingQueue<String> queue = new ArrayBlockingQueue<>(100);
BlockingDeque<String> deque = new LinkedBlockingDeque<>();
TransferQueue<String> transfer = new LinkedTransferQueue<>();
SynchronousQueue<String> sync = new SynchronousQueue<>();

// Producer
queue.put(item);      // blocks if full
queue.offer(item, 1, TimeUnit.SECONDS);  // timeout

// Consumer
String item = queue.take();           // blocks if empty
String item = queue.poll(1, TimeUnit.SECONDS);  // timeout
```

### Atomic Variables
```java
import java.util.concurrent.atomic.*;

AtomicInteger counter = new AtomicInteger(0);
counter.incrementAndGet();
counter.addAndGet(5);
counter.getAndSet(10);
counter.compareAndSet(10, 20);

AtomicLong longCounter = new AtomicLong();
AtomicBoolean flag = new AtomicBoolean(true);
AtomicReference<String> ref = new AtomicReference<>("initial");

// Update with function
counter.updateAndGet(x -> x + 1);
counter.accumulateAndGet(5, Integer::sum);
```

### ThreadLocal
```java
private static final ThreadLocal<SimpleDateFormat> dateFormat =
    ThreadLocal.withInitial(() -> new SimpleDateFormat("yyyy-MM-dd"));

// Usage (each thread gets its own copy)
String formatted = dateFormat.get().format(new Date());

// Clean up
dateFormat.remove();

// Context holder
public class RequestContext {
    private static final ThreadLocal<String> currentUser = new ThreadLocal<>();

    public static void setUser(String user) { currentUser.set(user); }
    public static String getUser() { return currentUser.get(); }
    public static void clear() { currentUser.remove(); }
}
```

### Phaser / CountDownLatch / CyclicBarrier / Semaphore
```java
// CountDownLatch (one-time)
CountDownLatch latch = new CountDownLatch(3);
// In threads: latch.countDown();
// In waiter:  latch.await();

// CyclicBarrier (reusable)
CyclicBarrier barrier = new CyclicBarrier(3, () ->
    System.out.println("All threads reached barrier"));
// In threads: barrier.await();

// Semaphore
Semaphore semaphore = new Semaphore(3); // 3 permits
semaphore.acquire();     // block until permit
semaphore.release();     // return permit

// Phaser (flexible barrier)
Phaser phaser = new Phaser(1); // register self
phaser.register();       // add party
phaser.arriveAndAwaitAdvance();  // synchronize
phaser.arriveAndDeregister();    // leave
```

---

## 23. Records (Java 16+)

### Basic Record
```java
public record Point(int x, int y) {}

// Usage
Point p = new Point(3, 4);
int x = p.x();                   // accessor (not getX())
int y = p.y();
String s = p.toString();         // "Point[x=3, y=4]"
boolean eq = p.equals(new Point(3, 4));  // true
int hash = p.hashCode();
```

### Record with Validation
```java
public record Person(String name, int age) {
    // Compact constructor
    public Person {
        if (name == null || name.isBlank()) {
            throw new IllegalArgumentException("Name cannot be blank");
        }
        if (age < 0 || age > 150) {
            throw new IllegalArgumentException("Invalid age: " + age);
        }
    }
}
```

### Record with Methods
```java
public record Rectangle(double width, double height) {
    public double area() {
        return width * height;
    }

    public double perimeter() {
        return 2 * (width + height);
    }

    public boolean isSquare() {
        return width == height;
    }

    // Static factory
    public static Rectangle square(double side) {
        return new Rectangle(side, side);
    }
}
```

### Record with Multiple Constructors
```java
public record Email(String address, String displayName) {
    public Email(String address) {
        this(address, address.split("@")[0]);
    }

    // Static factory
    public static Email of(String address) {
        return new Email(address);
    }
}
```

### Generic Record
```java
public record Pair<T, U>(T first, U second) {
    public static <T, U> Pair<T, U> of(T first, U second) {
        return new Pair<>(first, second);
    }

    public Pair<U, T> swap() {
        return new Pair<>(second, first);
    }
}

Pair<String, Integer> pair = Pair.of("age", 30);
String first = pair.first();       // "age"
```

### Record with Custom Serialization
```java
import java.io.Serializable;

public record Config(String host, int port) implements Serializable {
    private static final long serialVersionUID = 1L;

    public Config {
        port = port > 0 ? port : 8080;  // normalize in constructor
    }
}
```

### Local Records (Java 16+, inside method)
```java
public List<String> processTransactions(List<Transaction> transactions) {
    // Local record
    record Summary(String category, double total) {}

    return transactions.stream()
        .collect(Collectors.groupingBy(
            Transaction::getCategory,
            Collectors.summingDouble(Transaction::getAmount)
        ))
        .entrySet().stream()
        .map(e -> new Summary(e.getKey(), e.getValue()))
        .map(s -> s.category() + ": $" + s.total())
        .toList();
}
```

---

## 24. Sealed Classes (Java 17+)

### Basic Sealed Class
```java
public sealed class Shape
    permits Circle, Rectangle, Triangle {
}

final class Circle extends Shape {
    private final double radius;
    public Circle(double radius) { this.radius = radius; }
    public double area() { return Math.PI * radius * radius; }
}

final class Rectangle extends Shape {
    private final double width, height;
    public Rectangle(double w, double h) { this.width = w; this.height = h; }
    public double area() { return width * height; }
}

final class Triangle extends Shape {
    private final double base, height;
    public Triangle(double b, double h) { this.base = b; this.height = h; }
    public double area() { return 0.5 * base * height; }
}
```

### Sealed Interface
```java
public sealed interface Notification
    permits EmailNotification, SMSNotification, PushNotification {
    void send(String message);
}

record EmailNotification(String address) implements Notification {
    @Override public void send(String message) {
        System.out.println("Email to " + address + ": " + message);
    }
}

record SMSNotification(String phone) implements Notification {
    @Override public void send(String message) {
        System.out.println("SMS to " + phone + ": " + message);
    }
}

record PushNotification(String deviceToken) implements Notification {
    @Override public void send(String message) {
        System.out.println("Push to " + deviceToken + ": " + message);
    }
}
```

### Sealed Hierarchy with non-sealed permit
```java
public sealed abstract class Vehicle permits Car, Truck, Motorcycle {
    public abstract String getType();
}

sealed class Car extends Vehicle permits Sedan, SUV {
    @Override public String getType() { return "Car"; }
}

// Non-sealed (open for extension)
non-sealed class Truck extends Vehicle {
    @Override public String getType() { return "Truck"; }
}

final class Sedan extends Car {
    @Override public String getType() { return "Sedan"; }
}

final class SUV extends Car {
    @Override public String getType() { return "SUV"; }
}
```

### Exhaustive Switch with Sealed Classes
```java
public String describeShape(Shape shape) {
    return switch (shape) {
        case Circle c -> "Circle with radius " + c.radius();  // record accessor
        case Rectangle r -> "Rectangle " + r.width() + "x" + r.height();
        case Triangle t -> "Triangle base=" + t.base() + " height=" + t.height();
        // No default needed! Compiler knows it's exhaustive
    };
}
```

---

## 25. Pattern Matching (Java 17+/21+)

### Pattern Matching for instanceof (Java 16+)
```java
public void process(Shape shape) {
    if (shape instanceof Circle c) {
        System.out.println("Circle area: " + c.area());
    } else if (shape instanceof Rectangle r) {
        System.out.println("Rectangle area: " + r.area());
    }

    // With AND condition
    if (shape instanceof Circle c && c.radius() > 5) {
        System.out.println("Large circle");
    }
}
```

### Pattern Matching for switch (Java 17+ preview, Java 21+)
```java
public String classify(Shape shape) {
    return switch (shape) {
        case Circle c -> "Circle: r=" + c.radius();
        case Rectangle r -> "Rectangle: " + r.width() + "x" + r.height();
        case Triangle t -> {
            if (t.base() == t.height()) {
                yield "Right triangle";
            }
            yield "Triangle";
        }
        // null handling (Java 17+)
        case null -> "Unknown shape";
    };
}
```

### Guarded Patterns (Java 17+ preview)
```java
public String describe(Object obj) {
    return switch (obj) {
        case String s && s.length() > 5 -> "Long string: " + s;
        case String s && s.length() <= 5 -> "Short string: " + s;
        case Integer i && i > 0 -> "Positive: " + i;
        case Integer i -> "Non-positive: " + i;
        case null -> "null value";
        default -> "Unknown type: " + obj.getClass().getSimpleName();
    };
}
```

### Record Patterns (Java 21+)
```java
public record Point(int x, int y) {}
public record Line(Point start, Point end) {}

// Destructure records in switch
public void process(Object obj) {
    switch (obj) {
        case Point(int x, int y) ->
            System.out.println("Point: " + x + "," + y);
        case Line(Point(int x1, int y1), Point(int x2, int y2)) ->
            System.out.println("Line from (" + x1 + "," + y1 + ") to (" + x2 + "," + y2 + ")");
        case null -> System.out.println("null");
        default -> System.out.println("Other");
    }
}

// Record patterns in instanceof
if (obj instanceof Point(int x, int y)) {
    System.out.println("Point: " + x + ", " + y);
}

// Nested record pattern
if (obj instanceof Line(Point start, Point end)) {
    System.out.println("Line from " + start + " to " + end);
}
```

### Exhaustive Pattern Matching
```java
sealed interface Tree permits Leaf, Node {}
record Leaf(int value) implements Tree {}
record Node(Tree left, Tree right) implements Tree {}

public int sum(Tree tree) {
    return switch (tree) {
        case Leaf(int v) -> v;
        case Node(Tree left, Tree right) -> sum(left) + sum(right);
        // No default needed - exhaustive over sealed types
    };
}
```
