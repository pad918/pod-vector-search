import React from "react";
import logo from "./logo.svg";
import "./App.css";
import PasswordForm  from "./components/PasswordForm.js";
import UploadPage  from "./components/UploadPage.js";
import HomePage  from "./components/HomePage.js";
import { Routes, Route } from 'react-router-dom';

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

  return (
    <>
      <Routes>
        <Route path="/" element={<HomePage auth={auth} dispatchAuth={dispatchAuth}/>} />
        <Route path="/upload" element={<UploadPage auth={auth} />} />
      </Routes>
    </>
    
    
  );
}

export default App;

/*
    <div>
      <h1>React App</h1>
      <h2>Authenticated as user {auth.user_id}</h2>
    </div>
*/