const express = require("express");
const Promise = require("promise");
const https = require('https');
const app = express();
const JSONStream = require("JSONStream");
const fileSystem = require( "fs" );

function sleep(t) {
    return new Promise(resolve => setTimeout(resolve, t));
};

function get_html(url, ticker, t) {
  return new Promise(async (res, rej) => {

    await sleep(t);
    https.get(url + ticker, resp => {
      let html = ''

      resp.on("data", page => {
          html += page;
        });

      resp.on("end", () => {

        const obj = {};
        obj[ticker] = html.toString();
        transformStream.write(obj);

        console.log(t + " - " + ticker + ": Done")
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
 t = 0;
 global.transformStream = JSONStream.stringify();
 const outputStream = fileSystem.createWriteStream("html.json");
 transformStream.pipe( outputStream );
 outputStream.on(
   "finish",
   function handleFinish() {
     console.log("Successfully saved all html files!");
   }
 );
 for(let ticker of ticker_list){
   promise = get_html("https://www.fundsexplorer.com.br/funds/", ticker, 200*t);
   promises.push(promise);
   t++;
 };
 Promise.all(promises).then(resp => {
   console.log("All promises resolved!")
   transformStream.end();
   res.send("Successfully queried all html files!")});
});
