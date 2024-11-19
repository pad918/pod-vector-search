import React from "react";
import VideoSearchResult from "./VideoSearchResult.js";

import { NavLink } from "react-router-dom";

export default function SearchPage({auth}) {
    
    const [query, setQuery] = React.useState("");
    const [results, setResults] = React.useState([]);
    const searchCaptions = (e) => {
        e.preventDefault();
        fetch(`/api/video/caption_search?query=${query}&top=5`)
            .then(res => res.json())
            .then(data => {
                console.log(data[1]);
                return setResults(data);
            }
            )
            .catch(err => console.log(err));
    }

    return (
        <div className="root">
            <div className="navbar">
                <ul className="navbar-item">
                    <li>
                        <NavLink to="/" className="navlink">Home</NavLink>
                        <NavLink to="/upload" className="navlink">Upload / add index</NavLink>
                    </li>
                </ul>
            </div>
            <h1 className="title">Search Page</h1>
            <div className="content">
                <form onSubmit={(e) => searchCaptions(e)}>
                    <input type="text" placeholder="Search for captions" onChange={(e) => setQuery(e.target.value)} />
                    <button type="submit" disabled={!query}>Search</button>
                </form>
                <hr />
                {results.map((result, index) => (
                    <VideoSearchResult url={result[1]} timestamp={result[3]} caption={result[2]} key={index} />
                ))}
            </div>
        </div>
    );
}