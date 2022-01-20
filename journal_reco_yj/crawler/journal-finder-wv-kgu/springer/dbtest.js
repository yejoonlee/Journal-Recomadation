const mysql = require('async-mysql')
const dbconfig   = require('./config/database.js')
const fs = require('fs')

let path = './url.txt'
let main;

main = async() => {
    let connection, rows
    connection = await mysql.connect(dbconfig)

    rows = await connection.query("SELECT * from a_journal_crawling_log")

    let i=1
    fs.open(path, 'w', function(err, fd) {
        if (err) {
            throw 'could not open file: ' + err;
        }
        for(let row of rows) {
            let buffer = new Buffer(row.a_journal_id + " , " + row.step1_url + "\n");
            if (buffer.indexOf('null') == -1 ) {
                fs.write(fd, buffer, 0, buffer.length, null, function (err) {
                    if (err) throw 'error writing file: ' + err;
                    fs.close(fd);
                });
                i++
                if (i==10){
                    break
                }
            }
        }
        console.log('wrote the file successfully');
    });

}

main()