import React from "react";
import PasswordForm  from "./PasswordForm.js";
import { NavLink } from "react-router-dom";

export default function HomePage({auth, dispatchAuth}) {
    
    return (
        <div>
            {
            auth.signed_in ? 
                <NavLink to="/upload">Upload / add index</NavLink>
                : 
                <PasswordForm auth={auth} dispatchAuth={dispatchAuth}/>
            }
        </div>
    );
}