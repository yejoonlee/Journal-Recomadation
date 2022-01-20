//DB wiki url을 저널 url로 변환

const mysql = require('async-mysql')
const dbconfig = require('./config/database.js')
const fs = require('fs')
const axios = require('axios')
let main;

main = async () => {
    let connection, rows
    connection = await mysql.connect(dbconfig)

    rows = await connection.query("SELECT * from a_journal_crawling_log WHERE step1_url IS NOT NULL LIMIT 0, 100")

    fs.open("./url_0_to_100.csv", 'w', async function (err, fd) {
        if (err) {
            throw 'could not open file: ' + err;
        }
        for (let row of  rows) {
            var url = row.step1_url
            try {
                console.log(url)
                let response = await axios.get(url)
                let html = response.data

                if (html.indexOf('Journal homepage') !== -1) {
                    var si = html.indexOf('Journal homepage') - 250
                    var ei = html.indexOf('urnal homepage')
                    var purl = html.slice(si, ei);
                    if (purl.indexOf('https') == -1) {
                        var furl = purl.slice(purl.indexOf('http://'), purl.indexOf('">Jo'));
                        let buffer = new Buffer(row.a_journal_id + "," + furl + "\n")
                        fs.write(fd, buffer, function (err) {
                            if (err) throw 'error writing file: ' + err;
                        });
                    }
                    // else if (purl.indexOf('">Jo') == -1){
                    //     var furl = purl.slice(purl.indexOf('http://'), purl.indexOf('"><sup'));
                    //     let buffer = new Buffer(row.a_journal_id + "," + furl + "\n")
                    //     fs.write(fd, buffer, function (err) {
                    //         if (err) throw 'error writing file: ' + err;
                    //     });
                    // }
                    else {
                        var furl = purl.slice(purl.indexOf('https://'), purl.indexOf('">Jo'));
                        let buffer = new Buffer(row.a_journal_id + "," + furl + "\n")
                        fs.write(fd, buffer, function (err) {
                            if (err) throw 'error writing file: ' + err;
                        });
                    }
                }
            } catch (error) {
                console.log(error)
            }

        }
        fs.close(fd);
        console.log('wrote the file successfully');
    })
}

main()