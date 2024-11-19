// server/index.js


const youtubedl = require('youtube-dl-exec')

const express = require("express");

const PORT = process.env.PORT || 3001;

const app = express();

const VideoDBAddress = "http://localhost:3002";
const AuthAPIAddress = "http://localhost:3003";

app.get("/api", (req, res) => {
  res.send("ok");
});

// Add routes to video DB
app.get("/api/video/caption_search", (req, res) => {
  const query = req.query.query;
  const top = req.query.top;
  fetch(`${VideoDBAddress}/search?query=${query}&top=${top}`)
    .then((response) => response.json())
    .then((data) => res.send(data))
    .catch((err) => res.send("Could search for captions", 500));

})

app.get("/api/video/index_video", (req, res) => {
  const url = req.query.url;
  fetch(`${VideoDBAddress}/add_video?url=${url}`)
    .then((response) => response.json())
    .then((data) => res.send(data))
    .catch((err) => res.send("Could index video", 500));
})


// Add routes to auth API
app.get("/api/auth/login", (req, res) => {
  const username = req.query.user;
  const password = req.query.password;
  fetch(`${AuthAPIAddress}/login?user=${username}&password=${password}`)
    .then((response) => response.json())
    .then((data) => res.send(data))
    .catch((err) => res.send("Authentication error", 500));
})

app.get("/api/auth/register", (req, res) => {
  const username = req.query.user;
  const password = req.query.password;
  fetch(`${AuthAPIAddress}/register?user=${username}&password=${password}`)
    .then((response) => response.json())
    .then((data) => res.send(data))
    .catch((err) => res.send("Authentication error", 500));
})

app.listen(PORT, () => {
  console.log(`Server listening on ${PORT}`);
});
