import React from "react";

export default function PasswordForm({auth, dispatchAuth}) {
    const [username, setUsername] = React.useState("");
    const [password, setPassword] = React.useState("");
    const trySignIn = (e) => {
        e.preventDefault();
        fetch(`/login?user=${username}&password=${password}`)
            .then(res => {
                console.log(res);
                if(!res.ok) throw res;
                return res.json();
            })
            .then(data => dispatchAuth({type: "LOGIN_SUCCESS", payload: {user_id: data.user, auth_token: data.token}}))
            .catch(err => console.log(err));
            
    }

    return (
        <form onSubmit={(e) => trySignIn(e)}>
            <h2>Enter username and password to sign in</h2>
            <input type="text" placeholder="Username" onChange={(e) => setUsername(e.target.value)} />
            <input type="password" placeholder="Password" onChange={(e)=>setPassword(e.target.value)}/>
            <button type="submit" disabled={!username}>Sign in</button>
        </form>
    );

}