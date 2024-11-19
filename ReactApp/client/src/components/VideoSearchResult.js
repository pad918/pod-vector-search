import React from "react";

export default function VideoSearchResult({url, timestamp}) {
    const timestampToSeconds = (timestamp) => {
        const [hours, minutes, seconds] = timestamp.split(":");
        return parseInt(parseFloat(hours)*3600 + parseFloat(minutes)*60 + parseFloat(seconds))
    }

    const convertToEmbeddPath = (url) => {
        return url.replace("watch?v=", "embed/");
    }

    const embedd_url = convertToEmbeddPath(url);

    const seconds = timestampToSeconds(timestamp);

    return (
        <div>
            <h2>Video: {url} @ {timestamp}</h2>
            <iframe className="youtube-iframe" src={`${embedd_url}?start=${seconds}`}>
            </iframe> 
        </div>
    );
}