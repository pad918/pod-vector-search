const Queue = require('bull');

const youtubedl = require('youtube-dl-exec')
class Indexer{
    constructor(){
        console.log("Created Indexer")
        this.jobQueue = new Queue('jobQueue');
    }

    get jobQueue(){
        return this.jobQueue;
    }

    get previousJobs(){
        return this.previousJobs;
    }

    addJob(url){
        this.jobQueue.push(new Job(url));
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