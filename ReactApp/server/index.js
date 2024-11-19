// server/index.js


const youtubedl = require('youtube-dl-exec')

const indexer =  require("./Indexer.js");

const express = require("express");

const PORT = process.env.PORT || 3001;

const app = express();

app.get("/api", (req, res) => {
  console.log("api called, testing youtube-dl");
  indexer.getSubs(''+ 'jkskjsks') //https://www.youtube.com/watch?v=AOw7F2iF3Ao
    .then((subs) => console.log(subs))
    .catch((err) => console.log(err));
});
  
app.listen(PORT, () => {
  console.log(`Server listening on ${PORT}`);
});
