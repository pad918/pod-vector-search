import React from "react";
import PasswordForm  from "./PasswordForm.js";
import { NavLink } from "react-router-dom";

export default function HomePage({auth, dispatchAuth}) {
    
    if(!auth.signed_in) return <PasswordForm auth={auth} dispatchAuth={dispatchAuth}/>;
    return (
        <div>
                <NavLink to="/upload">Upload / add index</NavLink>
                <NavLink to="/search">Search</NavLink>
        </div>
    );
}