//Almost Done!!!

var casper = require('casper').create();
var fs = require('fs');
//var url = 'http://www.springer.com/psychology/journal/10615?print_view=true&detailsPage=pltci_1691621';
var burl = 'http://www.springer.com/';
var purl;
var furl;

casper.start();

casper.then(function () {
    stream = fs.open('url.csv', 'r');
    line = stream.readLine();
    while(line) {
        var id = line.split(',')[0]
        var url = line.split(',')[1]
        line = stream.readLine();

        if (url.indexOf('springer') > -1) {
            function write(id,url) {

                casper.thenOpen(url, function () {
                    var html = this.getHTML()
                    if (html.indexOf('Manuscript Guidelines (pdf,') > -1) {
                        var si = html.indexOf('Manuscript Guidelines (pdf,') - 500
                        var ei = html.indexOf('Manuscript Guidelines (pdf,')
                        purl = html.slice(si, ei);
                        furl = purl.slice(purl.indexOf('http://www'), purl.indexOf('" wicketpath='));
                        //this.echo(furl);
                        this.download(furl, './PDF/' + id + '.pdf');
                        console.log("download the file successfully")

                    }
                    else if (html.indexOf('Instructions for authors (pdf,') > -1) {
                        var si = html.indexOf('Instructions for authors (pdf,') - 500
                        var ei = html.indexOf('Instructions for authors (pdf,')
                        purl = html.slice(si, ei);
                        furl = purl.slice(purl.indexOf('http://www'), purl.indexOf('" wicketpath='));
                        //this.echo(furl);
                        this.download(furl, './PDF/' + id + '.pdf');
                        console.log("download the file successfully")

                    }
                    else if (html.indexOf('Instructions for Authors</span></a>') > -1) {
                        var si = html.indexOf('Instructions for Authors</span></a>') - 1000
                        var ei = html.indexOf('Instructions for Authors</span></a>')
                        purl = html.slice(si, ei);
                        furl = burl + purl.slice(purl.indexOf('?wicket:interface'), purl.indexOf("',function()"));
                        casper.thenOpen(furl, function () {
                            fs.write('./XML/' + id + '.txt', this.getHTML(), 'w');
                            console.log("wrote the " + id + " file successfully")
                        })
                    }
                });
            }
            write(id,url)
        }
    }
})

casper.run();