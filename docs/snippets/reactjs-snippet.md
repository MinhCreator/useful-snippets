# Useful ReactJS Snippets

> Compiled from popular VS Code React snippet extensions (ES7 React/Redux, React Snippets, Modern React Snippets, etc.)

---

## 1. Imports

| Prefix | Content |
|-------:|---------|
| `imr` | `import React from 'react'` |
| `imrd` | `import ReactDOM from 'react-dom'` |
| `imrc` | `import React, { Component } from 'react'` |
| `imrcp` | `import React, { Component } from 'react'` + `import PropTypes from 'prop-types'` |
| `imrpc` | `import React, { PureComponent } from 'react'` |
| `imrpcp` | `import React, { PureComponent } from 'react'` + `import PropTypes from 'prop-types'` |
| `imrm` | `import React, { memo } from 'react'` |
| `imrmp` | `import React, { memo } from 'react'` + `import PropTypes from 'prop-types'` |
| `imrs` | `import React, { useState } from 'react'` |
| `imrse` | `import React, { useState, useEffect } from 'react'` |
| `impt` | `import PropTypes from 'prop-types'` |
| `irbh` | `import React, { useState, useEffect, useContext, useRef, useCallback, useMemo } from 'react'` |
| `ibh` | `import { useState, useEffect, useContext } from 'react'` |
| `irt` | `import React from 'react'` (TypeScript) |
| `irts` | `import React, { useState } from 'react'` (TypeScript) |

### React Router Imports

| Prefix | Content |
|-------:|---------|
| `imrr` | `import { BrowserRouter as Router, Route, Link } from 'react-router-dom'` |
| `imbr` | `import { BrowserRouter as Router } from 'react-router-dom'` |
| `imbrc` | `import { Route, Switch, NavLink, Link } from 'react-router-dom'` |
| `imbrr` | `import { Route } from 'react-router-dom'` |
| `imbrs` | `import { Switch } from 'react-router-dom'` |
| `imbrl` | `import { Link } from 'react-router-dom'` |
| `imbrnl` | `import { NavLink } from 'react-router-dom'` |

---

## 2. Functional Components

| Prefix | Content |
|-------:|---------|
| `rfc` | React Functional Component |
| `rfce` | React Functional Component (exported) |
| `rfcp` | React Functional Component with PropTypes |
| `rafc` | React Arrow Function Component |
| `rafce` | React Arrow Function Component (exported) |
| `rafcp` | React Arrow Function Component with PropTypes |
| `rmc` | React.memo Functional Component |
| `rmcp` | React.memo Functional Component with PropTypes |
| `rsc` | React Styled Component (no hooks) |
| `rhc` | React Hooks Component (with useState + useEffect) |
| `rfcb` | React Functional Component + Boilerplate |
| `rc` | React functional component |
| `rcm` | React functional component with `memo` |

### TypeScript Functional Components

| Prefix | Content |
|-------:|---------|
| `rfc` (TS) | React.FC with typed props |
| `tsrc` | TypeScript React Component |
| `rtf` | function prop type |
| `rtb` | boolean prop type |
| `rts` | string prop type |
| `rtn` | number prop type |
| `rtch` | children prop type |
| `rtcn` | className prop type |

---

## 3. Class Components

| Prefix | Content |
|-------:|---------|
| `rcc` | React Class Component |
| `rccp` | React Class Component with PropTypes |
| `rce` | React Class Component (exported) |
| `rcep` | React Class Component (exported) with PropTypes |
| `rpc` | React PureComponent |
| `rpcp` | React PureComponent with PropTypes |
| `rpce` | React Class Export PureComponent |
| `rcpc` | React Class PureComponent |

### Class Lifecycle & State

| Prefix | Content |
|-------:|---------|
| `rconst` | `constructor(props)` with `this.state` |
| `rconc` | `constructor(props, context)` with `this.state` |
| `est` | `this.state = { }` |
| `sst` | `this.setState({ })` |
| `ssf` | `this.setState((state, props) => return { })` |
| `props` | `this.props.propName` |
| `state` | `this.state.stateName` |
| `bnd` | `this.methodName = this.methodName.bind(this)` |

---

## 4. Hooks

| Prefix | Content |
|-------:|---------|
| `rus` / `ush` / `st` | `const [state, setState] = useState(initialState)` |
| `rue` / `ueh` / `uf` | `useEffect(() => { }, [])` |
| `ruc` / `uch` | `useContext(MyContext)` |
| `rur` / `urd` / `urh` | `const [state, dispatch] = useReducer(reducer, initialState)` |
| `rurf` / `urefh` / `urf` | `const ref = useRef(initialValue)` |
| `rum` / `umh` / `um` | `const memoized = useMemo(() => compute(a, b), [a, b])` |
| `ruca` / `ucb` | `const callback = useCallback(() => { }, [])` |
| `rul` / `uleh` | `useLayoutEffect(() => { }, [])` |
| `rui` / `uih` | `useImperativeHandle(ref, () => { })` |
| `rudv` | `useDeferredValue(value)` |
| `rut` | `useTransition()` |
| `ruid` | `useId()` |
| `ruses` | `useSyncExternalStore(subscribe, getSnapshot)` |
| `rud` / `rdu` | `useDebugValue(value)` |
| `ruie` | `useInsertionEffect(() => { }, [])` |
| `hook` / `cuh` | Custom Hook generator |
| `cuht` | Custom Hook generator (TypeScript) |

### React 19 Hooks

| Prefix | Content |
|-------:|---------|
| `ruas` | `useActionState(action, initialState)` |
| `ruo` | `useOptimistic(state, updateFn)` |
| `ru` | `use(promiseOrContext)` |
| `rufs` | `useFormStatus()` |
| `rfrf` | `requestFormReset(form)` |

---

## 5. PropTypes

| Prefix | Content |
|-------:|---------|
| `pta` | `PropTypes.array` |
| `ptar` | `PropTypes.array.isRequired` |
| `ptb` | `PropTypes.bool` |
| `ptbr` | `PropTypes.bool.isRequired` |
| `ptf` | `PropTypes.func` |
| `ptfr` | `PropTypes.func.isRequired` |
| `ptn` | `PropTypes.number` |
| `ptnr` | `PropTypes.number.isRequired` |
| `pto` | `PropTypes.object` |
| `ptor` | `PropTypes.object.isRequired` |
| `pts` | `PropTypes.string` |
| `ptsr` | `PropTypes.string.isRequired` |
| `ptsm` | `PropTypes.symbol` |
| `ptsmr` | `PropTypes.symbol.isRequired` |
| `ptan` | `PropTypes.any` |
| `ptanr` | `PropTypes.any.isRequired` |
| `ptnd` | `PropTypes.node` |
| `ptndr` | `PropTypes.node.isRequired` |
| `ptel` | `PropTypes.element` |
| `ptelr` | `PropTypes.element.isRequired` |
| `pti` | `PropTypes.instanceOf(ClassName)` |
| `ptir` | `PropTypes.instanceOf(ClassName).isRequired` |
| `pte` | `PropTypes.oneOf(['News', 'Photos'])` |
| `pter` | `PropTypes.oneOf(['News', 'Photos']).isRequired` |
| `ptet` | `PropTypes.oneOfType([PropTypes.string, PropTypes.number])` |
| `ptetr` | `PropTypes.oneOfType([...]).isRequired` |
| `ptao` | `PropTypes.arrayOf(PropTypes.number)` |
| `ptaor` | `PropTypes.arrayOf(PropTypes.number).isRequired` |
| `ptoo` | `PropTypes.objectOf(PropTypes.number)` |
| `ptoor` | `PropTypes.objectOf(PropTypes.number).isRequired` |
| `ptsh` | `PropTypes.shape({ ... })` |
| `ptshr` | `PropTypes.shape({ ... }).isRequired` |
| `ptdf` | Start default PropTypes block |

---

## 6. Lifecycle Methods (Class Components)

| Prefix | Content |
|-------:|---------|
| `cdm` | `componentDidMount = () => { }` |
| `cwm` | `componentWillMount = () => { }` |
| `cwrp` | `componentWillReceiveProps = (nextProps) => { }` |
| `scu` | `shouldComponentUpdate = (nextProps, nextState) => { }` |
| `cwu` | `componentWillUpdate = (nextProps, nextState) => { }` |
| `cdu` / `cdup` | `componentDidUpdate = (prevProps, prevState) => { }` |
| `cwun` | `componentWillUnmount = () => { }` |
| `cdc` | `componentDidCatch = (error, info) => { }` |
| `gdsfp` / `rdsp` | `static getDerivedStateFromProps(nextProps, prevState)` |
| `gsbu` / `rsbu` | `getSnapshotBeforeUpdate = (prevProps, prevState) => { }` |
| `ren` | `render() { return ( ) }` |

---

## 7. Redux

| Prefix | Content |
|-------:|---------|
| `redux` | `import { connect } from 'react-redux'` |
| `rxaction` | Redux action template |
| `rxconst` | `export const CONSTANT = 'CONSTANT'` |
| `rxreducer` | Redux reducer template |
| `rxselect` | Redux selector template |
| `rxslice` | Redux slice template |
| `mstp` | `mapStateToProps` template |
| `mdtp` | `mapDispatchToProps` template |
| `rmap` | `mapStateToProps` + `mapDispatchToProps` template |
| `rconnect` | Redux `connect()` template |
| `useDispatch` | `const dispatch = useDispatch()` |
| `useSelector` | `const result = useSelector(state => state.value)` |
| `useStore` | `const store = useStore()` |

### Redux Class Components

| Prefix | Content |
|-------:|---------|
| `rcredux` | Class component connected to Redux |
| `rcreduxp` | Class component connected to Redux with PropTypes |
| `rfcredux` | Function component connected to Redux |
| `rfcreduxp` | Function component connected to Redux with PropTypes |

---

## 8. Context & Refs

| Prefix | Content |
|-------:|---------|
| `rcontext` / `ctx` | `const MyContext = React.createContext()` |
| `rcon` | `<MyContext.Consumer>{value => ()}</MyContext.Consumer>` |
| `cref` | `this.refNameRef = React.createRef()` |
| `fref` | `const ref = React.createRef()` |
| `rfr` / `forwardRef` | `React.forwardRef((props, ref) => { })` |

---

## 9. React Router

| Prefix | Content |
|-------:|---------|
| `rrs` | React Router setup |
| `rnrl` | `<NavLink to="/path">Link</NavLink>` |
| `rrt` | `<Route path="/path" component={Component} />` |
| `rrsw` | `<Switch>...</Switch>` |

---

## 10. React Portal & Suspense

| Prefix | Content |
|-------:|---------|
| `rcp` / `rpt` | `createPortal(children, domNode)` |
| `rlz` | `const LazyComp = React.lazy(() => import('./Comp'))` |
| `rls` | `<Suspense fallback={<Loading />}><LazyComp /></Suspense>` |

---

## 11. Error Boundaries

| Prefix | Content |
|-------:|---------|
| `recb` | Error Boundary boilerplate |
| `reb` | Error Boundary with fallback UI |

---

## 12. Higher-Order Components (HOC)

| Prefix | Content |
|-------:|---------|
| `rhoc` | React Higher-Order Component |
| `rhocc` | React Higher-Order Class Component |

---

## 13. Event Handlers

| Prefix | Content |
|-------:|---------|
| `hclk` | Click handler (`const handleClick = () => {}`) |
| `hclk_memo` | Click handler with `useCallback` |
| `hclk_event` | Click handler with event param |
| `hcg` | Change handler (`const handleChange = (e) => {}`) |
| `hcg_memo` | Change handler with `useCallback` |
| `hsubmit` / `rhse` | Form submit handler (`const handleSubmit = (e) => { e.preventDefault() }`) |

---

## 14. Styled Components

| Prefix | Content |
|-------:|---------|
| `imrsc` | `import React from 'react'` + `import styled from 'styled-components'` |
| `sc` | Styled component template |
| `thp` | Theme Provider wrapper |

---

## 15. Testing

| Prefix | Content |
|-------:|---------|
| `rtl` | React Testing Library test template |
| `sbst` | Storybook story template |

---

## 16. API / Data Fetching

| Prefix | Content |
|-------:|---------|
| `api` | Axios configuration file |
| `svc` | Axios API Service |
| `svc_auth` | Authentication Service Class |
| `svc_mgmt` | Dynamic Management Service Class |
| `api_get` | API GET with state management |
| `api_post` | API POST with state management |
| `api_put` | API PUT with state management |
| `api_delete` | API DELETE with state management |
| `apif` | Fetch API template |
| `rqh` | React Query hook template |
| `gql` | GraphQL query template |

---

## 17. Other Utilities

| Prefix | Content |
|-------:|---------|
| `rmap` | `.map()` in JSX markup |
| `cna` | `classnames()` as array |
| `danger` | `dangerouslySetInnerHTML={{ __html: }}` |
| `rimpa` | Absolute import (`import X from '@/X'`) |
| `rimpr` | Relative import (`import X from './X'`) |
| `st_data` | `const [data, setData] = useState(null)` |
| `st_loading` | `const [loading, setLoading] = useState(false)` |
| `st_error` | `const [error, setError] = useState(null)` |
| `rch` | Start custom hook |
| `ir` | Import React (bare) |
| `ird` | Import ReactDOM |
| `ipc` | Import React + PureComponent |
| `ipt` | Import PropTypes |

---

## 18. React Native

| Prefix | Content |
|-------:|---------|
| `rnc` | React Native Class Component |
| `rnf` | React Native Functional Component |
| `rnfs` | React Native Functional Component with StyleSheet |
| `rnfe` | React Native Functional Component (exported) |
| `rnfes` | React Native Functional Component exported with StyleSheet |
| `rncs` | React Native Component with StyleSheet |
| `rnce` | React Native Class Component (exported) |

---

*Prefixes may vary slightly across different snippet extensions. The most popular extension is **ES7 React/Redux/GraphQL/React-Native snippets** (by dsznajder / rodrigovallades).*
