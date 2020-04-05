const express = require("express");
const Promise = require("promise");
const https = require('follow-redirects').https;
const app = express();
const JSONStream = require("JSONStream");
const fileSystem = require( "fs" );

function sleep(t) {
    return new Promise(resolve => setTimeout(resolve, t));
};

function get_html(url, ticker, html_id, t) {
  return new Promise(async (res, rej) => {

    await sleep(t);
    https.get(url + ticker, (resp) => {
      let html = ''

      resp.on("data", page => {
          html += page;
        });

      resp.on("end", () => {

        const obj = [ticker, html.toString()];

        if(html_id == 1){
          transformStream1.write(obj);
        }
        else{
          transformStream2.write(obj);
        };

        console.log(t + " - " + ticker + " " + html_id + ": Done")
        res()
      });

      resp.on('error', function(e) {
        rej("Error " + ticker + ": " + e.message);
      });
    });

  });
};

app.listen(3000, () => {
 console.log("Server running on port 3000");
});

app.get("/get-fii-info", (req, res) => {
 const ticker_list = req.query.ticker_list
 html_list = []
 var promises = []
 var t = 0;

 global.transformStream1 = JSONStream.stringify();
 const outputStream1 = fileSystem.createWriteStream("html1.json");
 transformStream1.pipe( outputStream1 );

 global.transformStream2 = JSONStream.stringify();
 const outputStream2 = fileSystem.createWriteStream("html2.json");
 transformStream2.pipe( outputStream2 );

 outputStream1.on(
   "finish",
   function handleFinish() {
     console.log("Successfully saved all html1 files!");
   }
 );

 outputStream2.on(
   "finish",
   function handleFinish() {
     console.log("Successfully saved all html2 files!");
   }
 );

 for(let ticker of ticker_list){
   promise = get_html("https://www.fundsexplorer.com.br/funds/", ticker, 1, 200*t);
   promises.push(promise);
   t++;

   promise = get_html("https://fiis.com.br/", ticker, 2, 200*t);
   promises.push(promise);
   t++;
 };

 Promise.all(promises).then(resp => {
   console.log("All promises resolved!")
   transformStream1.end();
   transformStream2.end();
   res.send("Successfully queried all html files!")});
});
