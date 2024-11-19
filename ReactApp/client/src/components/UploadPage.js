import React,  { useEffect, useState } from "react";
import { useNavigate } from 'react-router-dom'

export default function UploadPage({auth}) {
    
    // This does not fully hide /upload to users,
    // it simply makes it unaccessable if not 
    // singed in. A hacker can circumvent this
    // but there is nothing to hide here

    // Uploads requests are authenticated by the 
    // server and a hacker and can not circumvent 
    // it easely.
    const navigate = useNavigate();
    useEffect(() => {
        if(!auth.signed_in) {
            console.log("not signed in, redirecting...");
            navigate("/");
        }
    }, []);

    const [currJobs, setCurrJobs] = useState([
        "Video 1",
        "Video 2",
        "Video 3",
        "Video 4"
    ]);
    
    const [jobUrl, setJobUrl] = React.useState("");
    
    const uploadJobRequest = (e) => {
        e.preventDefault();
        setCurrJobs([...currJobs, jobUrl]);
        console.log(jobUrl + " ADDED");
        fetch(`/api/video/index_video?url=${jobUrl}`)
            .then(res => res.json())
            .then(data => console.log(data))
            .catch(err => console.log(err));
        
    }

    return (
        <div>
            <h1>Add upload jobs, Username: {auth.user_id}</h1>
            <form onSubmit={(e) => uploadJobRequest(e)}>
                <input type="url" onChange={(e) => setJobUrl(e.target.value)}/>
                <button type="submit">Submit</button>
            </form>
            
            <div>
                <h2>Current Jobs</h2>
                <ul>
                    {currJobs.map((job) => <li>{job}</li>)}
                </ul>
            </div>
            
        </div>
    );
}