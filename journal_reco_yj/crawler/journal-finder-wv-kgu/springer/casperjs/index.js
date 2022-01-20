// npm install casperjs phantomjs -g
// npm install
// 실행: casper index.js

var casper = require('casper').create();

var url = 'http://www.springer.com/philosophy/ethics+and+moral+philosophy/journal/10551';

casper.start(url);
casper.then(function() {
    var elements = this.getElementsInfo('a.linkToOpenLayer')
    elements.forEach(function(element) {
        if(element.text.indexOf('Instructions for Authors') !== -1) {
            var onclick = element.attributes['onclick']
            var link = 'http://www.springer.com/' + onclick.slice(onclick.indexOf('?'), onclick.indexOf("',"));

            if(link) {
                casper.thenOpen(link, function() {
                    console.log(this.page.content)
                })
            }
        }
    })
});
casper.run();4