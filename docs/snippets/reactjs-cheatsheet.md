# CORE CONCEPTS

## Các element và JSX

Cú pháp căn bản cho một React element:

```jsx
// In a nutshell, JSX allows us to write HTML in our JS
// JSX can use any valid html tags (i.e. div/span, h1-h6, form/input, etc)
<div>Hello React</div>
```

Cú pháp JSX là expressions:

```jsx
// as an expression, JSX can be assigned to variables...
const greeting = <div>Hello React</div>;

const isNewToReact = true;

// ... or can be displayed conditionally
function sayGreeting() {
  if (isNewToReact) {
    // ... or returned from functions, etc.
    return greeting; // displays: Hello React
  } else {
    return <div>Hi again, React</div>;
  }
}
```

JSX cho phép nest expressions:

```jsx
const year = 2020;
// we can insert primitive JS values in curly braces: {}
const greeting = <div>Hello React in {year}</div>;
// trying to insert objects will result in an error
```

JSX cho phép nest các elements:

```jsx
// to write JSX on multiple lines, wrap in parentheses: ()
const greeting = (
  // div is the parent element
  <div>
    {/* h1 and p are child elements */}
    <h1>Hello!</h1>
    <p>Welcome to React</p>
  </div>
);
// 'parents' and 'children' are how we describe JSX elements in relation
// to one another, like we would talk about HTML elements
```

HTML và JSX có sự khác biệt một ít về cú pháp:

```jsx
// Empty div is not <div></div> (HTML), but <div/> (JSX)
<div/>

// A single tag element like input is not <input> (HTML), but <input/> (JSX)
<input name="email" />

// Attributes are written in camelcase for JSX (like JS variables)
<button className="submit-button">Submit</button> // not 'class' (HTML)
```

App React cơ bản nhất yêu cầu 3 thứ:

- `ReactDOM.render()` để render app
- Một JSX element (được gọi là root node)
- Một DOM element để mount app (thường là một div với một id của root trong index.html file)

```jsx
// imports needed if using NPM package; not if from CDN links
import React from "react";
import ReactDOM from "react-dom";

const greeting = <h1>Hello React</h1>;

// ReactDOM.render(root node, mounting point)
ReactDOM.render(greeting, document.getElementById("root"));
```

---

## Component và Prop của React

Cấu trúc cho một component React cơ bản:

```jsx
import React from "react";

// 1st component type: function component
function Header() {
  // function components must be capitalized unlike normal JS functions
  // note the capitalized name here: 'Header'
  return <h1>Hello React</h1>;
}

// function components with arrow functions are also valid
const Header = () => <h1>Hello React</h1>;

// 2nd component type: class component
// (classes are another type of function)
class Header extends React.Component {
  // class components have more boilerplate (with extends and render method)
  render() {
    return <h1>Hello React</h1>;
  }
}
```

Cách sử dụng components:

```jsx
// do we call these function components like normal functions?

// No, to execute them and display the JSX they return...
const Header = () => <h1>Hello React</h1>;

// ...we use them as 'custom' JSX elements
ReactDOM.render(<Header />, document.getElementById("root"));
// renders: <h1>Hello React</h1>
```

Component có thể sử dụng lại trong app:

```jsx
// for example, this Header component can be reused in any app page

// this component shown for the '/' route
function IndexPage() {
  return (
    <div>
      <Header />
      <Hero />
      <Footer />
    </div>
  );
}

// shown for the '/about' route
function AboutPage() {
  return (
    <div>
      <Header />
      <About />
      <Testimonials />
      <Footer />
    </div>
  );
}
```

Data có thể chuyển đến component với prop:

```jsx
// What if we want to pass data to our component from a parent?
// I.e. to pass a user's name to display in our Header?

const username = "John";

// we add custom 'attributes' called props
ReactDOM.render(
  <Header username={username} />,
  document.getElementById("root"),
);
// we called this prop 'username', but can use any valid JS identifier

// props is the object that every component receives as an argument
function Header(props) {
  // the props we make on the component (i.e. username)
  // become properties on the props object
  return <h1>Hello {props.username}</h1>;
}
```

Props không thể thay đổi được (mutated):

```jsx
// Components must ideally be 'pure' functions.
// That is, for every input, we be able to expect the same output

// we cannot do the following with props:
function Header(props) {
  // we cannot mutate the props object, we can only read from it
  props.username = "Doug";

  return <h1>Hello {props.username}</h1>;
}
// But what if we want to modify a prop value that comes in?
// That's where we would use state (see the useState section)
```

Chúng ta có thể dùng children prop khi muốn chuyển element/component như là props đến các component khác:

```jsx
// Can we accept React elements (or components) as props?
// Yes, through a special property on the props object called 'children'

function Layout(props) {
  return <div className="container">{props.children}</div>;
}

// The children prop is very useful for when you want the same
// component (such as a Layout component) to wrap all other components:
function IndexPage() {
  return (
    <Layout>
      <Header />
      <Hero />
      <Footer />
    </Layout>
  );
}

// different page, but uses same Layout component (thanks to children prop)
function AboutPage() {
  return (
    <Layout>
      <About />
      <Footer />
    </Layout>
  );
}
```

Hiển thị có điều kiện các components với ternaries và short-circuiting:

```jsx
// if-statements are fine to conditionally show , however...
// ...only ternaries (seen below) allow us to insert these conditionals
// in JSX, however
function Header() {
  const isAuthenticated = checkAuth();

  return (
    <nav>
      <Logo />
      {/* if isAuth is true, show AuthLinks. If false, Login  */}
      {isAuthenticated ? <AuthLinks /> : <Login />}
      {/* if isAuth is true, show Greeting. If false, nothing. */}
      {isAuthenticated && <Greeting />}
    </nav>
  );
}
```

Fragment là các components được dùng để hiển thị các loại component mà không cần thêm element vào DOM. Fragments phù hợp với conditional logic:

```jsx
// we can improve the logic in the previous example
// if isAuthenticated is true, how do we display both AuthLinks and Greeting?
function Header() {
  const isAuthenticated = checkAuth();

  return (
    <nav>
      <Logo />
      {/* we can render both components with a fragment */}
      {/* fragments are very concise: <> </> */}
      {isAuthenticated ? (
        <>
          <AuthLinks />
          <Greeting />
        </>
      ) : (
        <Login />
      )}
    </nav>
  );
}
```

---

## List và key

Dùng `.map()` để chuyển mảng list of data vào list of elements:

```jsx
const people = ["John", "Bob", "Fred"];
const peopleList = people.map((person) => <p>{person}</p>);
```

`.map()` cũng được dùng cho components như là elements:

```jsx
function App() {
  const people = ['John', 'Bob', 'Fred'];
  // can interpolate returned list of elements in {}
  return (
    <ul>
      {/* we're passing each array element as props */}
      {people.map(person => <Person name={person} />}
    </ul>
  );
}

function Person({ name }) {
  // gets 'name' prop using object destructuring
  return <p>this person's name is: {name}</p>;
}
```

Mỗi React element được lặp lại cần một `key` props. Keys là nhân tố cần thiết để React theo dõi từng element được lặp lại với map. Nếu không có Keys thì sẽ khó để update các element khi data thay đổi. Và Keys phải là các giá trị duy nhất để thể hiện rằng các elements này tách biệt với nhau.

```jsx
function App() {
  const people = ["John", "Bob", "Fred"];

  return (
    <ul>
      {/* keys need to be primitive values, ideally a generated id */}
      {people.map((person) => (
        <Person key={person} name={person} />
      ))}
    </ul>
  );
}

// If you don't have ids with your set of data or unique primitive values,
// you can use the second parameter of .map() to get each elements index
function App() {
  const people = ["John", "Bob", "Fred"];

  return (
    <ul>
      {/* use array element index for key */}
      {people.map((person, i) => (
        <Person key={i} name={person} />
      ))}
    </ul>
  );
}
```

---

## Events và Event Handlers

Events trong React và HTML có sự khác biệt nhỏ:

```jsx
// Note: most event handler functions start with 'handle'
function handleToggleTheme() {
  // code to toggle app theme
}

// in html, onclick is all lowercase
<button onclick="handleToggleTheme()">
  Submit
</button>

// in JSX, onClick is camelcase, like attributes / props
// we also pass a reference to the function with curly braces
<button onClick={handleToggleTheme}>
  Submit
</button>
```

Hai thứ quan trọng nhất trong React events là `onClick` và `onChange`:

- `onClick` xử lý click events trên JSX element (được gọi là buttons)
- `onChange` thì xử lý keyboard events (được gọi là inputs)

```jsx
function App() {
  function handleChange(event) {
    // when passing the function to an event handler, like onChange
    // we get access to data about the event (an object)
    const inputText = event.target.value;
    const inputName = event.target.name; // myInput
    // we get the text typed in and other data from event.target
  }

  function handleSubmit() {
    // on click doesn't usually need event data
  }

  return (
    <div>
      <input type="text" name="myInput" onChange={handleChange} />
      <button onClick={handleSubmit}>Submit</button>
    </div>
  );
}
```

---

# React Hooks

## State và useState

`useState` cho phép chúng ta khai báo local state trong Function Component:

```jsx
import React from "react";

// create state variable
// syntax: const [stateVariable] = React.useState(defaultValue);
function App() {
  const [language] = React.useState("javascript");
  // we use array destructuring to declare state variable

  return <div>I am learning {language}</div>;
}
```

Ghi chú: Bất kỳ hook trong phần này được lấy từ React package và có thể import riêng lẻ.

```jsx
import React, { useState } from "react";

function App() {
  const [language] = useState("javascript");

  return <div>I am learning {language}</div>;
}
```

`useState` cũng cho chúng ta chức năng 'setter' để update các state mà nó tạo:

```jsx
function App() {
  // the setter function is always the second destructured value
  const [language, setLanguage] = React.useState("python");
  // the convention for the setter name is 'setStateVariable'

  return (
    <div>
      {/*  why use an arrow function here instead onClick={setterFn()} ? */}
      <button onClick={() => setLanguage("javascript")}>
        Change language to JS
      </button>
      {/*  if not, setLanguage would be called immediately and not on click */}
      <p>I am now learning {language}</p>
    </div>
  );
}

// note that whenever the setter function is called, the state updates,
// and the App component re-renders to display the new state
```

`useState` có thể sử dụng một hoặc nhiều lần với single component:

```jsx
function App() {
  const [language, setLanguage] = React.useState("python");
  const [yearsExperience, setYearsExperience] = React.useState(0);

  return (
    <div>
      <button onClick={() => setLanguage("javascript")}>
        Change language to JS
      </button>
      <input
        type="number"
        value={yearsExperience}
        onChange={(event) => setYearsExperience(event.target.value)}
      />
      <p>I am now learning {language}</p>
      <p>I have {yearsExperience} years of experience</p>
    </div>
  );
}
```

`useState` chấp nhận các value primitive hay object để quản lý state:

```jsx
// we have the option to organize state using whatever is the
// most appropriate data type, according to the data we're tracking
function App() {
  const [developer, setDeveloper] = React.useState({
    language: "",
    yearsExperience: 0,
  });

  function handleChangeYearsExperience(event) {
    const years = event.target.value;
    // we must pass in the previous state object we had with the spread operator
    setDeveloper({ ...developer, yearsExperience: years });
  }

  return (
    <div>
      {/* no need to get prev state here; we are replacing the entire object */}
      <button
        onClick={() =>
          setDeveloper({
            language: "javascript",
            yearsExperience: 0,
          })
        }
      >
        Change language to JS
      </button>
      {/* we can also pass a reference to the function */}
      <input
        type="number"
        value={developer.yearsExperience}
        onChange={handleChangeYearsExperience}
      />
      <p>I am now learning {developer.language}</p>
      <p>I have {developer.yearsExperience} years of experience</p>
    </div>
  );
}
```

Nếu state mới phụ thuộc vào state trước đó, để đảm bảo update đã hoàn tất, chúng ta có thể dùng một function trong setter function đưa ra chính xác state trước đó.

```jsx
function App() {
  const [developer, setDeveloper] = React.useState({
    language: "",
    yearsExperience: 0,
    isEmployed: false,
  });

  function handleToggleEmployment(event) {
    // we get the previous state variable's value in the parameters
    // we can name 'prevState' however we like
    setDeveloper((prevState) => {
      return { ...prevState, isEmployed: !prevState.isEmployed };
      // it is essential to return the new state from this function
    });
  }

  return (
    <button onClick={handleToggleEmployment}>Toggle Employment Status</button>
  );
}
```

---

## Side effects và useEffect

`useEffect` cho phép thực hiện side effect bên trong các function component. Vậy các side effect là những gì?

- Sử dụng side effects khi chúng ta cần "đụng" đến thế giới bên ngoài. Ví dụ như fetching data từ API hay làm việc với DOM.
- Side effect là các hành động có thể thay đổi component state.

`useEffect` chấp nhận callback function (hay còn được gọi là 'effect' function), được chạy mặc định mỗi lần re-render. Nó chạy một lần khi component mount, cũng là thời điểm phù hợp để thực hiện side effect trong một lifecycle của component.

```jsx
// what does our code do? Picks a color from the colors array
// and makes it the background color
function App() {
  const [colorIndex, setColorIndex] = React.useState(0);
  const colors = ["blue", "green", "red", "orange"];

  // we are performing a 'side effect' since we are working with an API
  // we are working with the DOM, a browser API outside of React
  useEffect(() => {
    document.body.style.backgroundColor = colors[colorIndex];
  });
  // whenever state is updated, App re-renders and useEffect runs

  function handleChangeIndex() {
    const next = colorIndex + 1 === colors.length ? 0 : colorIndex + 1;
    setColorIndex(next);
  }

  return <button onClick={handleChangeIndex}>Change background color</button>;
}
```

Để tránh thực hiện callback sau mỗi lần render, chúng ta có thể tạo argument thứ 2 là một array (mảng) trống:

```jsx
function App() {
  ...
  // now our button doesn't work no matter how many times we click it...
  useEffect(() => {
    document.body.style.backgroundColor = colors[colorIndex];
  }, []);
  // the background color is only set once, upon mount

  // how do we not have the effect function run for every state update...
  // but still have it work whenever the button is clicked?

  return (
    <button onClick={handleChangeIndex}>
      Change background color
    </button>
  );
}
```

`useEffect` cho phép chúng ta thực hiện các effect với các mảng dependencies. Mảng dependencies là argument thứ hai, nếu có một trong những giá trị trong mảng thay đổi, thì effect function sẽ chạy lại.

```jsx
function App() {
  const [colorIndex, setColorIndex] = React.useState(0);
  const colors = ["blue", "green", "red", "orange"];

  // we add colorIndex to our dependencies array
  // when colorIndex changes, useEffect will execute the effect fn again
  useEffect(() => {
    document.body.style.backgroundColor = colors[colorIndex];
    // when we use useEffect, we must think about what state values
    // we want our side effect to sync with
  }, [colorIndex]);

  function handleChangeIndex() {
    const next = colorIndex + 1 === colors.length ? 0 : colorIndex + 1;
    setColorIndex(next);
  }

  return <button onClick={handleChangeIndex}>Change background color</button>;
}
```

`useEffect` cho phép chúng ta unsubscribe những effect nhất định bằng cách trả lại function vào lúc cuối:

```jsx
function MouseTracker() {
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });

  React.useEffect(() => {
    // .addEventListener() sets up an active listener...
    window.addEventListener("mousemove", (event) => {
      const { pageX, pageY } = event;
      setMousePosition({ x: pageX, y: pageY });
    });

    // ...so when we navigate away from this page, it needs to be
    // removed to stop listening. Otherwise, it will try to set
    // state in a component that doesn't exist (causing an error)

    // We unsubscribe any subscriptions / listeners w/ this 'cleanup function'
    return () => {
      window.removeEventListener("mousemove", (event) => {
        const { pageX, pageY } = event;
        setMousePosition({ x: pageX, y: pageY });
      });
    };
  }, []);

  return (
    <div>
      <h1>The current mouse position is:</h1>
      <p>
        X: {mousePosition.x}, Y: {mousePosition.y}
      </p>
    </div>
  );
}

// Note: we could extract the reused logic in the callbacks to
// their own function, but I believe this is more readable
```

Fetching data với useEffect:

Nên chú ý khi xử lý các promise với các cú pháp async/await ngắn gọn yêu cầu phải tạo thêm function riêng biệt (Vì effect callback function không thể async.)

```jsx
const endpoint = "https://api.github.com/users/codeartistryio";

// with promises:
function App() {
  const [user, setUser] = React.useState(null);

  React.useEffect(() => {
    // promises work in callback
    fetch(endpoint)
      .then((response) => response.json())
      .then((data) => setUser(data));
  }, []);
}

// with async / await syntax for promise:
function App() {
  const [user, setUser] = React.useState(null);
  // cannot make useEffect callback function async
  React.useEffect(() => {
    getUser();
  }, []);

  // instead, use async / await in separate function, then call
  // function back in useEffect
  async function getUser() {
    const response = await fetch("https://api.github.com/codeartistryio");
    const data = await response.json();
    setUser(data);
  }
}
```

---

## Performance và useCallback

`useCallback` là một hook được sử dụng để cải thiện performance của component.

Nếu có một component thường xuyên re-render, useCallback sẽ ngăn chặn tình trạng callback functions trong component được tạo lại mỗi lần component re-render (đồng nghĩa với việc function component re-run).

`useCallback` re-run chỉ khi một trong những dependencies thay đổi.

```jsx
// in Timer, we are calculating the date and putting it in state a lot
// this results in a re-render for every state update

// we had a function handleIncrementCount to increment the state 'count'...
function Timer() {
  const [time, setTime] = React.useState();
  const [count, setCount] = React.useState(0);

  // ... but unless we wrap it in useCallback, the function is
  // recreated for every single re-render (bad performance hit)
  // useCallback hook returns a callback that isn't recreated every time
  const inc = React.useCallback(
    function handleIncrementCount() {
      setCount((prevCount) => prevCount + 1);
    },
    // useCallback accepts a second arg of a dependencies array like useEffect
    // useCallback will only run if any dependency changes (here it's 'setCount')
    [setCount],
  );

  React.useEffect(() => {
    const timeout = setTimeout(() => {
      const currentTime = JSON.stringify(new Date(Date.now()));
      setTime(currentTime);
    }, 300);

    return () => {
      clearTimeout(timeout);
    };
  }, [time]);

  return (
    <div>
      <p>The current time is: {time}</p>
      <p>Count: {count}</p>
      <button onClick={inc}>+</button>
    </div>
  );
}
```

---

## Memorization và useMemo

`useMemo` khá tương tự với useCallback và để cải thiện hiệu năng. Thay vì dùng để callback, nó được dùng để lưu lại kết quả của hàm nào và những giá trị nào sẽ làm thay đổi kết quả đó.

```jsx
// useMemo is useful when we need a lot of computing resources
// to perform an operation, but don't want to repeat it on each re-render

function App() {
  // state to select a word in 'words' array below
  const [wordIndex, setWordIndex] = useState(0);
  // state for counter
  const [count, setCount] = useState(0);

  // words we'll use to calculate letter count
  const words = ["i", "am", "learning", "react"];
  const word = words[wordIndex];

  function getLetterCount(word) {
    // we mimic expensive calculation with a very long (unnecessary) loop
    let i = 0;
    while (i < 1000000) i++;
    return word.length;
  }

  // Memoize expensive function to return previous value if input was the same
  // only perform calculation if new word without a cached value
  const letterCount = React.useMemo(() => getLetterCount(word), [word]);

  // if calculation was done without useMemo, like so:

  // const letterCount = getLetterCount(word);

  // there would be a delay in updating the counter
  // we would have to wait for the expensive function to finish

  function handleChangeIndex() {
    // flip from one word in the array to the next
    const next = wordIndex + 1 === words.length ? 0 : wordIndex + 1;
    setWordIndex(next);
  }

  return (
    <div>
      <p>
        {word} has {letterCount} letters
      </p>
      <button onClick={handleChangeIndex}>Next word</button>
      <p>Counter: {count}</p>
      <button onClick={() => setCount(count + 1)}>+</button>
    </div>
  );
}
```

---

## Refs và useRef

Ref là attribute đặc biệt và luôn có sẵn trên tất cả React components. Chúng cho phép chúng ta tạo ra reference đến element/component có sẵn khi mount component.

`useRef` cho phép chúng ta sử dụng React Refs một cách dễ dàng. Chúng ta gọi useRef (ở top của component đó) và đính kèm giá trị trả về vào attribute ref của element đó để tham chiếu.

Khi đã tạo reference, chúng ta sử dụng property hiện có để chỉnh sửa (modify-mutate) các properties của element đó. Hoặc chúng ta có thể call bất kỳ methods nào trên element đó (như `.focus()` để focus một input).

```jsx
function App() {
  const [query, setQuery] = React.useState("react hooks");
  // we can pass useRef a default value
  // we don't need it here, so we pass in null to ref an empty object
  const searchInput = useRef(null);

  function handleClearSearch() {
    // current references the text input once App mounts
    searchInput.current.value = "";
    // useRef can store basically any value in its .current property
    searchInput.current.focus();
  }

  return (
    <form>
      <input
        type="text"
        onChange={(event) => setQuery(event.target.value)}
        ref={searchInput}
      />
      <button type="submit">Search</button>
      <button type="button" onClick={handleClearSearch}>
        Clear
      </button>
    </form>
  );
}
```

---

# Hooks nâng cao

## Context và useContext

Trong React, chúng ta nên tránh tạo ra các multiple props để chuyển data xuống 2 hay nhiều level từ một parent component:

```jsx
// Context helps us avoid creating multiple duplicate props
// This pattern is also called props drilling:
function App() {
  // we want to pass user data down to Header
  const [user] = React.useState({ name: "Fred" });

  return (
   {/* first 'user' prop */}
    <Main user={user} />
  );
}

const Main = ({ user }) => (
  <>
    {/* second 'user' prop */}
    <Header user={user} />
    <div>Main app content...</div>
  </>
);

const Header = ({ user }) => <header>Welcome, {user.name}!</header>;
```

Context khá hữu ích dùng để chuyển props xuống các tầng levels của child:

```jsx
// Here is the previous example rewritten with Context
// First we create context, where we can pass in default values
const UserContext = React.createContext();
// we call this 'UserContext' because that's what data we're passing down

function App() {
  // we want to pass user data down to Header
  const [user] = React.useState({ name: "Fred" });

  return (
    {/* we wrap the parent component with the provider property */}
    {/* we pass data down the computer tree w/ value prop */}
    <UserContext.Provider value={user}>
      <Main />
    </UserContext.Provider>
  );
}

const Main = () => (
  <>
    <Header />
    <div>Main app content...</div>
  </>
);

// we can remove the two 'user' props, we can just use consumer
// to consume the data where we need it
const Header = () => (
  {/* we use this pattern called render props to get access to the data*/}
  <UserContext.Consumer>
    {user => <header>Welcome, {user.name}!</header>}
  </UserContext.Consumer>
);
```

`useContext` hook có thể xóa render props pattern này, tuy nhiên, để có thể consume context trong bất kỳ function component nào:

```jsx
const Header = () => {
  // we pass in the entire context object to consume it
  const user = React.useContext(UserContext);
  // and we can remove the Consumer tags
  return <header>Welcome, {user.name}!</header>;
};
```

---

## Reducers và useReducer

Reducer là function khá đơn giản, được dùng để lấy state object trước đó và một action object và trả về một state object mới. Ví dụ:

```jsx
// let's say this reducer manages user state in our app:
function reducer(state, action) {
  // reducers often use a switch statement to update state
  // in one way or another based on the action's type property
  switch (action.type) {
    // if action.type has the string 'LOGIN' on it
    case "LOGIN":
      // we get data from the payload object on action
      return { username: action.payload.username, isAuth: true };
    case "SIGNOUT":
      return { username: "", isAuth: false };
    default:
      // if no case matches, return previous state
      return state;
  }
}
```

React `useReducer` hook là một cách hữu ích để quản lý state trong React bên cạnh useState, và nó có thể kết hợp với context dùng để quản lý state trong một ứng dụng mà có thể không cần sử dụng đến redux. Ngoài ra, sự kết hợp useReducer và useContext có thể là hệ thống quản lý state cho apps.

```jsx
const initialState = { username: "", isAuth: false };

function reducer(state, action) {
  switch (action.type) {
    case "LOGIN":
      return { username: action.payload.username, isAuth: true };
    case "SIGNOUT":
      // could also spread in initialState here
      return { username: "", isAuth: false };
    default:
      return state;
  }
}

function App() {
  // useReducer requires a reducer function to use and an initialState
  const [state, dispatch] = useReducer(reducer, initialState);
  // we get the current result of the reducer on 'state'

  // we use dispatch to 'dispatch' actions, to run our reducer
  // with the data it needs (the action object)
  function handleLogin() {
    dispatch({ type: "LOGIN", payload: { username: "Ted" } });
  }

  function handleSignout() {
    dispatch({ type: "SIGNOUT" });
  }

  return (
    <>
      Current user: {state.username}, isAuthenticated: {state.isAuth}
      <button onClick={handleLogin}>Login</button>
      <button onClick={handleSignout}>Signout</button>
    </>
  );
}
```

---

## Các hooks custom

Các hooks được tạo ra nhằm tái sử dụng behavior dễ dàng giữa các component. Chúng là pattern dễ hiểu hơn các loại khác của class components, như higher-order component hay render props. Chúng ta có thể tự tạo ra hook của riêng mình tùy thuộc vào nhu cầu từng dự án, bên cạnh những gì React đã có sẵn:

```jsx
// here's a custom hook that is used to fetch data from an API
function useAPI(endpoint) {
  const [value, setValue] = React.useState([]);

  React.useEffect(() => {
    getData();
  }, []);

  async function getData() {
    const response = await fetch(endpoint);
    const data = await response.json();
    setValue(data);
  };

  return value;
};

// this is a working example! try it yourself (i.e. in codesandbox.io)
function App() {
  const todos = useAPI("https://todos-dsequjaojf.now.sh/todos");

  return (
    <ul>
      {todos.map(todo => <li key={todo.id}>{todo.text}</li>}
    </ul>
  );
}
```

---

## Các quy tắc của hooks

Khi sử dụng React hooks thì có 2 nguyên tắc không nên vi phạm:

1. Hooks chỉ có thể được call trên top của components (chúng không thể ở trong conditionals, loops hay nested functions).
2. Hooks chỉ có thể sử dụng trong function components (chúng không thể dùng trong Javascript function bình thường hay class components).

```jsx
function checkAuth() {
  // Rule 2 Violated! Hooks cannot be used in normal functions, only components
  React.useEffect(() => {
    getUser();
  }, []);
}

function App() {
  // this is the only validly executed hook in this component
  const [user, setUser] = React.useState(null);

  // Rule 1 violated! Hooks cannot be used within conditionals (or loops)
  if (!user) {
    React.useEffect(() => {
      setUser({ isAuth: false });
      // if you want to conditionally execute an effect, use the
      // dependencies array for useEffect
    }, []);
  }

  checkAuth();

  // Rule 1 violated! Hooks cannot be used in nested functions
  return <div onClick={() => React.useMemo(() => doStuff(), [])}>Our app</div>;
}
```
