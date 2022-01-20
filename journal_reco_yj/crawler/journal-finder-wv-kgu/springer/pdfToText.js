var pdfText = require('pdf-text')
const fs = require('fs')
let txt = new Buffer('')
let id = 0

for (id; id < 10; id++) {
    var file = './PDF/'+ id +'.txt'
    fs.open(file, 'w', function (err, fd) {
        if (err){
            console.log("No file")
        }

        var pathToPdf = "./PDF/" + id + ".pdf"
        var buffer = fs.readFileSync(pathToPdf);
        if (err) throw err;

        pdfText(buffer, function (err, chunks) {
            txt = chunks.join("") + "\n"
            // console.log(txt)
            fs.write(fd, txt, function (err) {
                if (err) throw 'error writing file: ' + err
                console.log("wrote the pdf successfully")
            })
        })
        fs.close(fd)
    })
}