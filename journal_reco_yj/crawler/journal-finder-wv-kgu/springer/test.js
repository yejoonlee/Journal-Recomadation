const mysql = require('async-mysql')
const dbconfig   = require('./config/database.js')
const fs = require('fs')
const request = require("request");

let main;

main = async() => {
    let connection, rows
    connection = await mysql.connect(dbconfig)

    rows = await connection.query("SELECT * from a_journal_crawling_log")

    let i= await 1
    await fs.open(await "./url.csv", 'w', async function (err, fd) {
        if (err) {
            throw 'could not open file: ' + err;
        }
        for (let row of await rows) {
            var url = await row.step1_url
            if (url !== null) {
                request(url, async function (err, response, body) {
                    if (err) throw err;
                    var html = await body
                    if (html.indexOf('Journal homepage') !== -1) {
                        var si = await html.indexOf('Journal homepage') - 100
                        var ei = await html.indexOf('urnal homepage')
                        var purl = await html.slice(si, ei);
                        if (purl.indexOf('https') == -1) {
                            var furl = await purl.slice(await purl.indexOf('http://'), await purl.indexOf('">Jo'));
                            let buffer = await new Buffer(await row.a_journal_id + "," + await furl + "\n")
                            fs.write(await fd, await buffer, function (err) {
                                //if (err) throw 'error writing file: ' + err;
                                fs.close(fd);
                            });
                            //console.log(buffer)
                        }
                        else {
                            var furl = await purl.slice(await purl.indexOf('https://'), await purl.indexOf('">Jo'));
                            let buffer = await new Buffer(await row.a_journal_id + "," + await furl + "\n")
                            fs.write(await fd, await buffer, function (err) {
                                if (err) throw 'error writing file: ' + err;
                                fs.close(fd);
                            });
                            //console.log(buffer)
                        }
                    }
                });
            }
            i++
            if (i > 50) {
                break
            }
        }
        //console.log(txt)
        // fs.write(fd, buffer, 0, buffer.length, null, function (err) {
        //     if (err) throw 'error writing file: ' + err;
        //     fs.close(fd);
        // });
    })
    console.log('wrote the file successfully');
}

main()