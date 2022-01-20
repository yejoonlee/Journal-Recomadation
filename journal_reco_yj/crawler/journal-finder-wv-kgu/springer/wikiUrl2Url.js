//안쓸듯
var casper = require('casper').create();
var url = 'https://en.wikipedia.org/wiki/Academic_Emergency_Medicine';
var jurl

casper.start(url, function () {
    var html = this.getHTML()
    var si = html.indexOf('Journal homepage') - 100
    var ei = html.indexOf('Journal homepage')
    var purl = html.slice(si, ei);
    jurl = purl.slice(purl.indexOf('http://www'), purl.indexOf('">'));
    this.echo(jurl);
})

casper.run()