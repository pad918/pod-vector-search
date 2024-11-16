import React from "react";
import logo from "./logo.svg";
import "./App.css";
import PasswordForm  from "./components/PasswordForm.js";

const authReducer = (state, action) => {
  switch (action.type) {
    case "LOGIN_SUCCESS":
      return {
        ...state,
        signed_in: true,
        auth_token: action.payload.auth_token,
        user_id: action.payload.user_id
      };
    case "LOGOUT_SUCCESS":
      return {
        ...state, 
        signed_in: false,
        auth_token: "",
        user_id: ""
      };
    default:
      return state;
  }
}

function App() {
  
  const [auth, dispatchAuth] = React.useReducer(authReducer, {signed_in: false, auth_token: "", user_id: ""});
  
  // If not signed in, only show login page
  if(!auth.signed_in) {
    return (<PasswordForm auth={auth} dispatchAuth={dispatchAuth}/>);
  }

  // If signed in, list all files owned by user?
  return (
    <div>
      <h1>React App</h1>
      <h2>Authenticated as user {auth.user_id}</h2>
    </div>
    
  );
}

export default App;