const Queue = require('bull');

const youtubedl = require('youtube-dl-exec')

/*
Plan:
    Eftersom javascript är singlethreaded är det helt värdelöst
    som backend. Node kommer därför endast användas som kliser
    för att slippa cors? 
    Kommer ha två python api:er en för vektordatabas, en för auth
    Och alla requests kommer gå från frontend till nodejs, som 
    skickar vidare till python api:erna (NODE SUGER!)

*/


class Indexer{
    constructor(){
        console.log("Created Indexer")
        this.jobQueue = new Queue('jobQueue');
        this.jobQueue.process(function(job, done) {
            console.log("Processing job", job);
            console.log("Processing done")
            done();
          });
        this.jobQueue.on('completed', function(job, result) {
            console.log(`Job ${job} completed with result ${result}`);
        });
    }

    addJob(url){
        this.jobQueue.add(new Job(url));
    }
    
}

class Job{
    constructor(url){
        this.url = url;
        this.status = "INDEXING";
    }

    process(){
        var subs = null;
        this.getSubs(this.url)
            .then((subs) => {
                this.subs = subs;
                this.status = "COMPLETED";
            })
            .catch((err) => {
                this.status = "FAILED";
                console.log(err);
            });
        
    }

    async getSubs(url) {
        const resp = youtubedl(url, {
            dumpJson: true,
            allSubs: true,
            subLang: 'en',
            skipDownload: true,
            addHeader: ['referer:youtube.com', 'user-agent:googlebot']
          }).then((resp) => {
            let subs = resp.subtitles;
            if(!subs.hasOwnProperty('en')) throw("No subtitles found");
            return subs;
          }).catch((err) => {
            throw "Could not get subtitles";
          });
        return resp;
    }
}

module.exports = new Indexer();